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
    args = parser.parse_args()

    config_json = json.load(open('config.json'))
    if not str(args.config) in config_json:
        raise Exception('Configuration {} does not exist in config.json'.format(args.config))
    config = config_json[str(args.config)]

    supported_video_types = ['.mp4', '.wmv', 'flv', '.webm', '.avi', '.mov', '.m4a', '.mkv']
    path = str(args.path)
    videos = []

    if os.path.isdir(path):
        print('Scanning for files in folder')

        videos += get_video_files_from_folder(path, supported_video_types)

        # if not path[-1] == '\\':
        #     path += '\\'
        # files_in_path = os.listdir(path)
        # for file in files_in_path:
        #     print(path + file)
        #     if os.path.splitext(path + file)[1].lower() in supported_video_types:
        #         videos.append(path + file)
    elif os.path.isfile(path):
        videos.append(path)
    elif not os.path.exists(path):
        raise Exception('Path {} does not exist'.format(path))

    # print(os.path.basename(args.path))
    print(videos)

    for video in videos:
        try:
            vir.create_preview(config['columns'], config['rows'], video, border_size=config['border_size'],
                               spacing=config['spacing'], target_width=config['target_width'],
                               time_stamps=config['time_stamps'], background_color=tuple(config['background_color']),
                               border_color=tuple(config['border_color']), font_color=tuple(config['font_color']))
        except ZeroDivisionError:
            print('Error downloading {}'.format(video))
        except ValueError:
            print('Error downloading {}'.format(video))
