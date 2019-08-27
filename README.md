##SETUP

1: Create python vritual environment - python3 -m virtualenv env

2: source /env/bin/activate

3: pip install -r requirements.txt

##Running the code

The python code by default will be reading the configuration file located in /config/config.yaml and 
these parameters are passed through into the mosaic package. It also provides the option 
to overwrite those default parameters by specifying them via the command line

Parameters:

--target-image : Name of the target image to be processed (The default path is /images/target/<br/>
--target-path: Path (including the image filename) to be processed <br/>
--tile-path: Path of the where the tile images are stored (default = /images/tile)
--grid-size: Defines the amount of pixels the output image will have <br/>
--resize: Resizes the tile images before being processed into mosaic <br/>
--mosaic-image: Filename output after mosaic has been created. Output will be saved in /output/)

Example

python src/mosaic.py --target-image=sunset.jpg --mosaic-image=sunset.jpg --grid-size 100 100 --resize 100 100

 