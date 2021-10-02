#https://github.com/geometalab/pyGeoTile

import requests
import matplotlib.pyplot as plt
from skimage import io

from pygeotile.point import Point
from pygeotile.tile import Tile


def plot(img, title):
    """
    using the title and image provide plot the image and display it to the user with the custom title
    """
    plt.figure()
    plt.title(title)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def getSatImage(zoom, level, lat, long) :
    point = Point.from_latitude_longitude(lat, long)
    print('Pixels: ', point.pixels(zoom=zoom))  # Pixels:  (34430592, 49899136)
    print('Lat/Lon: ', point.latitude_longitude)  # Lat/Lon:  (41.84987190947754, -87.64995574951166)

    tms_x, tms_y = 134494, 329369
    tile = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)  # Tile Map Service (TMS) X Y and zoom

    row = int(((90 - point.latitude) * (2 ** level)) // 288)
    col = int(((180 + point.longitude) * (2 ** level)) // 288)

    url = 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2016-09-03/250m/'
    return url + str(level) + "/" + str(row) + "/" + str(col) + ".jpg"

fileName = "satImage.jpg"
img_data = requests.get(getSatImage(19, 7, 43.2557, -79.8711)).content
with open(fileName, 'wb') as handler:
    handler.write(img_data)

img = io.imread(fileName)
plot(img, "SatImage of Us")
