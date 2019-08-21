import VideoImageReader as vir
import json
import os
import argparse


def get_video_files_from_folder(folder_path, formats):
    if not folder_path[-1] == '\\':
        folder_path += '\\'
    files_in_path = os.listdir(folder_path)
    videos = []
    for file in files_in_path:
        if os.path.isdir(folder_path + file):
            videos += get_video_files_from_folder(folder_path + file, formats)
        if os.path.splitext(folder_path + file)[1].lower() in formats:
            videos.append(folder_path + file)
    return videos


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates preview thumbnail image from video files.')

    parser.add_argument('--path', help='Path to folder or files')
    parser.add_argument('--config', help='Specify the config you want to use. Defaults to default')
    parser.add_argument('--save', help='Specify where you want to save the created images. If blank, files will save to'
                                       'the same directory as the video.')
    args = parser.parse_args()

    config_json = json.load(open('config.json'))

    config = ''
    if not str(args.config) in config_json:
        if args.config is None:
            config = config_json['default']
        else:
            raise Exception('Configuration {} does not exist in config.json'.format(args.config))
    else:
        config = config_json[str(args.config)]

    supported_video_types = ['.mp4', '.wmv', 'flv', '.webm', '.avi', '.mov', '.m4a', '.mkv']
    path = str(args.path)
    expected_default_path = ''
    videos = []

    if os.path.isdir(path):
        print('Scanning for files in folder')
        videos += get_video_files_from_folder(path, supported_video_types)
        expected_default_path = path
    elif os.path.isfile(path):
        videos.append(path)
        # Removes file_name from path
        expected_default_path = ''.join(str(e)+'\\' for e in path.split('\\')[:-1])
    elif not os.path.exists(path):
        raise Exception('Path {} does not exist'.format(path))
    for x in videos:
        print(str(x))

    print(expected_default_path)

    save_location = str(args.save)
    if args.save is None:
        print('No path selected. Saving next to video files. Set save path with --save C:\\example\\')
        if len(expected_default_path) > 0 and expected_default_path[-1] == '\\':
            save_location = str(expected_default_path)
        else:
            save_location = str(expected_default_path) + '\\'
    else:
        if os.path.exists(save_location):
            if not str(save_location)[-1] == '\\':
                save_location = str(save_location) + '\\'
        else:
            os.mkdir(save_location)

    for video in videos:
        try:
            vir.create_preview(config['columns'], config['rows'], video, border_size=config['border_size'],
                               spacing=config['spacing'], target_width=config['target_width'],
                               time_stamps=config['time_stamps'], background_color=tuple(config['background_color']),
                               border_color=tuple(config['border_color']), font_color=tuple(config['font_color']),
                               save_location=save_location)
        except ZeroDivisionError:
            print('Error downloading {}'.format(video))
        except ValueError:
            print('Error downloading {}'.format(video))
