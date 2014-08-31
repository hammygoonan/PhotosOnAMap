#!/usr/bin/python

from flask import Flask, request, render_template, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from PIL import Image
from PIL.ExifTags import TAGS
import os

app = Flask(__name__, static_url_path='')

class Photo(object):
	''' opens, displays and get metadata of photo '''
	def __init__(self, filename):
		self.filename = filename
		self.filepath = 'static/photos/' + filename
		self.file = Image.open(self.filepath)
		self.metadata = self.getExif()
		self.file.close()
	def __repr__(self):
		return '<Photo %r>' % self.filename
	def getFilename(self):
		return self.filename
	def getExif(self):
		d = {}
		for tag, value in self.file._getexif().iteritems():
			d[TAGS.get(tag)] = value
		return d
	def getGpsInfo(self):
		if 'GPSInfo' in self.metadata:
			return self.metadata['GPSInfo']
		else:
			return False
	def getLatLng(self):
		gps = self.getGpsInfo()
		if gps:
			lat = gps[2][0][0] + (gps[2][1][0] / 60.0) + ((gps[2][2][0] / 100.0) / 3600.0)
			lng = gps[4][0][0] + (gps[4][1][0] / 60.0) + ((gps[4][2][0] / 100.0) / 3600.0)
			if gps[1] == 'S':
				lat *= -1
			if gps[3] == 'W':
				lng *= -1
			return {'lat' : lat, 'lng' : lng}

class Map(object):
	''' Defines map objects '''
	def __init__(self):
		self.directory = 'static/photos/'
		self.photos = self.setPhotos()
	def setPhotos(self):
		files = os.listdir(self.directory)
		return [Photo(file) for file in files if file.endswith('.jpg')]
	def getPhotos(self):
		return self.photos
	def getMarkers(self):
		markers = []
		for photo in self.photos:
			markers.append({ 'name' : photo.getFilename(), 'latlng' : photo.getLatLng() })
		return markers
	def getCenter(self):
		pass


################
# Start Routes #
################

# random marker just to get an initial center poisition
photo = Photo('2014-08-24 12.17.53.jpg');

@app.route("/")
def index():
	return app.send_static_file('index.html')

@app.route("/get_center/", methods=['POST'])
def get_center():
	return jsonify(photo.getLatLng())

@app.route("/get_markers/", methods=['POST'])
def get_markers():
	map_object = Map()
	return jsonify({ 'markers' : map_object.getMarkers() })

####################
# GOOOOOOOO Flask! #
####################

if __name__ == "__main__":
	app.debug = True
	app.run()
