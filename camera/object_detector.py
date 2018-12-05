import cv2
import pickle
import numpy as np
import sklearn.naive_bayes
import skimage.measure

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

PIXELS_PER_CM = 7.344
IMAGE_SIZE = (288, 352)
CAMERA_ORIGIN = (IMAGE_SIZE[0]/2, IMAGE_SIZE[1]-15)


class ObjectDetector(object):
	def __init__(self, model_filepath='camera/object_detector.model'):
		self.model_filepath = model_filepath
		with open(model_filepath) as model_file:
			self.model = pickle.load(model_file)

	def preprocess(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)[1] / 255

		return frame

	def labeled_regions(self, frame):
		frame = self.preprocess(frame)
		frame = skimage.measure.label(frame, background=1)
		regions = skimage.measure.regionprops(frame)
		def filter_fn(region):
			return (
				(12 < region.major_axis_length and region.major_axis_length < 55) and
				(10 < region.minor_axis_length and region.minor_axis_length < 35)
			)
		return filter(filter_fn, regions)

	def region_properties(self, region):
		return [
			region.major_axis_length,
			region.minor_axis_length,
			region.area,
			region.convex_area,
			region.perimeter,
			region.solidity,
			region.filled_area,
			region.eccentricity,
		]

	def clasified_regions(self, stream.read()[1]):
		regions = self.labeled_regions(frame)
		if regions == []:
			return []
		region_features = []
		for region in regions:
			region_features.append(self.region_properties(region))

		predictions = self.model.predict_proba(np.array(region_features))
		region_classes = []
		for index, prediction in enumerate(predictions):
			minr, minc, maxr, maxc = regions[index].bbox
			center = (
				PIXELS_PER_CM*(minc + ((maxc - minc) / 2)),
				PIXELS_PER_CM*(minr + ((maxr - minr) / 2))
			)
			minor_axis_orientation = np.rad2deg(regions[index].orientation + np.pi/2)
			region_classes.append({
				'class': self.model.classes_[prediction.argmax()],
				'confidence': prediction.max(),
				'orientation': minor_axis_orientation,
				'center': center,
			})

		return region_classes

	def train(self, regions, labels):
		region_features = []
		for region in regions:
			region_features.append(self.region_properties(region))

		self.model.fit(np.array(region_features), np.array(labels))

	def save(self):
		with open(self.model_filepath, 'w+') as model_file:
			pickle.dumps(self.model, model_file)

if __name__ == '__main__':
	from camera.stream import stream
	object_detector = ObjectDetector(model_filepath='camera/object_detector.model')
	sample_frame = stream.read()[1]
	regions = object_detector.clasified_regions(sample_frame)
	fig, ax = plt.subplots(figsize=(10, 6))
	ax.imshow(object_detector.preprocess(sample_frame))

	for index, region in enumerate(regions):
		marker = mpatches.Circle(region['center'], 5, color='red')
		ax.add_patch(marker)
		ax.annotate('{}'.format(index), region['center'])

		print 'confidence: {}; class: {}; location {}; orientation'.format(region['confidence'], region['class'], region['position'], region['orientation'])

	plt.show()
