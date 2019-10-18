
# Video Preview Generator

Generates video preview image for video files.

  - Generate individual previews or for entire folders of videos
  - Easily configurable through JSON


### Dependencies
* [opencv-python](https://pypi.org/project/opencv-python/) - Open Image Processing


### Installation

Install [Python3](https://www.python.org/downloads/)

Install the dependencies if not already installed

```sh
$ pip install opencv-python
```

### Usage

After installing, the Driver can be run in console.
```sh
$ python Driver.py --path "E:\Video\Movies\blade-runner.mp4" --save "E:\Tests\" --config default
```
### Config File
Templates for previews can be created in config.json
```sh
{
	"weird_green": {
		"rows": 6,  
		"columns": 5,  
		"border_size": 2,  
		"spacing": 8,  
		"target_width": 1920,  
		"time_stamps": true,  
		"background_color": [22, 160, 133],  
		"border_color": [26, 188, 156],  
		"font_color": [255, 255, 255]
	}
}
```

### Generated Images
**Note that the pictures's aspect ratio is based on video's resolution and how many rows/columns are generated while the picture's resolution is based on the "target_width" in config.json.**

![enter image description here](https://i.imgur.com/qlfwlwW.png)
![enter image description here](https://i.imgur.com/bsmOR82.png)
![enter image description here](https://i.imgur.com/R3JyXCJ.png)
### Todos

 - Write tests
 - Add more configurations
 - Add more customization
