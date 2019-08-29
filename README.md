## GITHUB LINK
https://github.com/madoscar65/mosaic

## SETUP

Assuming you already have python installed:

1: Create python virtual environment 
```
python3 -m virtualenv env
```

2: Activate the virtual environment

For windows:
```
/env/scripts/activate.bat
```
For Linux/MAC
```
source env/bin/activate
```

3: Install all python libraries required for this project
```
pip install -r requirements.txt
```
4: There are two different options to run the mosaic code, one from using the terminal/command line or using flask 
web UI
## Running the code in terminal
Change your directory to ```C:/path_to_project/mosaic/```.
The python code by default will be reading the configuration file located in ```/config/config.yaml``` and 
these parameters are passed through into the mosaic package. It also provides the option 
to overwrite those default parameters by specifying them via the command line

Parameters:

```--target-image``` : Name of the target image to be processed <br/>
```--target-path``` : Path to the image to be processed (The default path is ```/images/target/```<br/>
```--tile-path``` : Path of the where the tile images are stored (default = ```/images/tile```)<br/>
```--tile-folder``` : Name of the folder stored in path (default = ```/images/tile```) <br/>
```--grid-size``` : Defines the amount of pixels the output image will have (default 100 x 100) <br/>
```--resize```: Resize the input tile images before being processed into mosaic <br/>
```--mosaic-image```: Filename output after mosaic has been created. Output will be saved in ```/output/```)

Example

Using default folder location
```
python src/mosaic.py --target-image=starrynight.jpg --mosaic-image=output --grid-size 100 100 --resize 50 50
```
 
 Using target image from a different location and tile folder from different location to the project
 ```
 python src/mosaic.py --target-path C:\path_to_image\ --target-image image.jpg --tile-path C:\path_to_tile_folder 
 --grid-size 100 100 resize 30 30 
 ```
 
 ## Running the code using Flask Web Ui
 Change your directory to ```C:/path_to_project/mosaic/```.
 
 Run the flask application
 ```
 python mosaic_app.py
 ```
 
 NOTE: The flask application is restricted to use all target images and tile images from the package itself and no option
 of using images outside the project directory.
