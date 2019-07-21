import cv2
import numpy as np
import os


def get_images(number_of_screenshots, vidcap, border=True, border_size=2, resize_to_width=None, resize_to_height=None,
               timestamps=True, border_color=(192, 191, 187)):

    # Seeks end of video
    vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)

    # Gets total number of frames in video
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Gets FPS of video
    video_fps = vidcap.get(cv2.CAP_PROP_FPS)

    # Sets what the iterator will be
    itr = int(total_frames/number_of_screenshots)

    counter = 1

    vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

    # Iterates through video collecting frames
    images = []
    while counter < total_frames:
        frame_number = int(counter)
        success, image = vidcap.read()
        if border:
            image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT,
                                       value=border_color)
        if resize_to_height is not None and resize_to_width is not None:
            image = cv2.resize(image, (resize_to_width, resize_to_height))
        if timestamps:
            font = cv2.FONT_HERSHEY_SIMPLEX
            top_right = (5, int(resize_to_height/2) - 5)
            font_scale = 0.5
            font_color = (255, 255, 255)
            line_type = 8
            cv2.putText(image, format_time(frame_number, video_fps),
                        (top_right[0], 4 + top_right[1] * 2), fontFace=font, fontScale=font_scale, color=font_color,
                        lineType=line_type)
        images.append(image)
        counter += itr
        vidcap.set(1, counter)

        # Temp Fix for Going Over
        if len(images) == number_of_screenshots:
            break

    return images


def create_preview(columns, rows, video_file_name, target_width=1920, border_size=0, spacing=0,
                   border_color=(192, 191, 187), background_color=(49, 45, 44), time_stamps=True,
                   font_color=(255, 255, 255)):
    assert(columns > 1 and rows > 1), "Invalid number of rows or columns"
    title_space = 50

    # Gets images from getImages method
    total_images = columns * rows
    vidcap = cv2.VideoCapture(video_file_name)

    width = int(vidcap.get(3))
    height = int(vidcap.get(4))

    # calculated_width = (columns * width) + ((columns+1) * spacing) + ((border_size * 2) * columns)
    # calculated_height = (rows * height) + ((rows+1) * spacing) + ((border_size * 2) * rows)
    # print(calculated_width)
    # print(calculated_height)

    vwidth = int((target_width - ((columns+1) * spacing) + ((border_size * 2) * columns))/columns)
    vheight = int((height * vwidth) / width)

    images = get_images(total_images, vidcap, border_size=border_size, resize_to_height=vheight, resize_to_width=vwidth,
                        border_color=border_color, timestamps=time_stamps)

    print('Creating Preview Image\n')

    k = 0
    image_rows = []

    height, width = images[0].shape[:2]
    border = np.zeros((height, spacing, 3), np.uint8)
    border[:] = background_color

    for i in range(0, rows):
        temp_image = None

        for j in range(0, columns):
            # Concatonate images
            if temp_image is None:
                temp_image = images[k]
                x = [border, temp_image]
                temp_image = np.concatenate((x), axis=1)
            else:
                x = [temp_image, border, images[k]]
                temp_image = np.concatenate((x), axis=1)
            k += 1
        x = [temp_image, border]
        temp_image = np.concatenate((x), axis=1)
        image_rows.append(temp_image)
    # print(str(len(image_rows)) + ' rows created')

    # Create border on top for text
    row_height, row_width = image_rows[0].shape[:2]
    bottom_border = np.zeros((title_space, row_width, 3), np.uint8)
    bottom_border[:] = background_color
    image_rows.insert(0, bottom_border)

    # Numpy array of borders between rows
    row_height, row_width = image_rows[0].shape[:2]
    bottom_border = np.zeros((spacing, row_width, 3), np.uint8)
    bottom_border[:] = background_color

    # Create background in between rows
    for i in range(0, len(image_rows)):
        image_rows.insert(1+i*2, bottom_border)

    image = np.concatenate((image_rows), axis=0)

    # Rescale image size to target width
    # height, width = image.shape[:2]
    # print(width)
    # print(height)
    # target_height = (int)((height * target_width) / width)
    # image = cv2.resize(image, (target_width, target_height))

    # Get video length
    vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
    video_length = format_time(vidcap.get(cv2.CAP_PROP_FRAME_COUNT), vidcap.get(cv2.CAP_PROP_FPS))

    # Add text to image
    font = cv2.FONT_HERSHEY_SIMPLEX
    top_right = (12, 20)
    font_scale = 0.5
    line_type = 8
    cv2.putText(image, video_file_name.split('\\')[-1],
                top_right, fontFace=font, fontScale=font_scale, color=font_color, lineType=line_type)
    cv2.putText(image, video_length,
                (top_right[0], 4+top_right[1]*2), fontFace=font, fontScale=font_scale, color=font_color,
                lineType=line_type)

    cv2.imwrite(video_file_name.split('\\')[-1] + ' -- Preview Image.png', image)


def format_time(current_frame, video_fps):
    total_seconds = round(current_frame / video_fps)

    s = int(total_seconds % 60)
    m = int((total_seconds / 60) % 60)
    h = int((total_seconds / 60 / 60))

    return str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)

