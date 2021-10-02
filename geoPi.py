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


#meter_x, meter_y = -9757148.442088600, 5138517.444985110 # meters in Spherical Mercator EPSG:900913
#point = Point.from_meters(meter_x=meter_x, meter_y=meter_y)

zoom = 19
#FEED LAT,LONG
point = Point.from_latitude_longitude(43.2557, -79.8711)

print('Pixels: ', point.pixels(zoom=zoom))  # Pixels:  (34430592, 49899136)
print('Lat/Lon: ', point.latitude_longitude)  # Lat/Lon:  (41.84987190947754, -87.64995574951166)

level, tms_x, tms_y, zoom = 7, 134494, 329369, 19
tile = Tile.from_tms(tms_x=tms_x, tms_y=tms_y, zoom=zoom)  # Tile Map Service (TMS) X Y and zoom

print('QuadTree: ', tile.quad_tree)  # QuadTree:  0302222310303211330
print('Google: ', tile.google)  # Google:  (134494, 194918)

row = int(((90 - point.latitude) * (2 ** level)) // 288)
col = int(((180 + point.longitude) * (2 ** level)) // 288)

url = 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2016-09-03/250m/'
image_url = url + str(level) + "/" + str(row) + "/" + str(col) + ".jpg"

print('Website: ', image_url)

fileName = "satImage.jpg"
img_data = requests.get(image_url).content
with open(fileName, 'wb') as handler:
    handler.write(img_data)

img = io.imread(fileName)
plot(img, "SatImage of Us")
