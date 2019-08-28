from flask import Flask, render_template, request
from src.utils.image import TargetImage, TileImages, MosaicImage
from src.config.config import MosaicConfig
import os
import time

app = Flask(__name__, static_folder='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
@app.route('/home')
def mosaic_main():
    tile_folders = os.listdir(os.path.join(os.getcwd(), 'images/tile'))
    return render_template('mosaic.html', tile_folders=tile_folders)

@app.route('/result', methods = ['POST', 'GET'])
def result():

     if request.method == 'POST':
        start_time = time.time()
        target_path = None
        target_image = None
        grid_size = None
        tile_path = None
        tile_folder = None
        save = None
        resize = None

        result = request.form
        config = MosaicConfig()


        target_image = result['target image']
        if not '' in request.form.getlist('grid size[]'):
            grid_size = [int(i) for i in request.form.getlist('grid size[]')]

        if not '' in request.form.getlist('resize[]'):
            resize = [int(i) for i in request.form.getlist('resize[]')]

        tile_folder = result['folder']
        target = TargetImage(grid_size=grid_size, target_path=target_path, config=config)
        tile_image = TileImages(tile_path=tile_path, config=config, resize=resize, folder=tile_folder)
        target_image = target.get_target_image(target_image)
        cropped_images = target.target_image_split()
        tile_fit = tile_image.get_tile_fit(cropped_images, reuse=True)
        mosaic = MosaicImage(tile_images=tile_fit, grid_size=target.grid_size)
        mosaic_image = mosaic.build_mosaic()

        if not result['mosaic image']:
            image = '/output/mosaic.jpg'
        else:
            save = result['mosaic image']
            image = '/output/' + result['mosaic image'] + '.jpg'
        mosaic.save(mosaic_image, filename=save)
        finish_time = round(time.time() - start_time, 2)
        return render_template("result.html", result=result, time=finish_time, image=image)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True)