import cv2
import pickle
import numpy as np
from camera.stream import stream
import skimage.measure

class ObjectDetector(object):
	def __init__(self):
		with open('camera/object_detector.model') as model_file:
			self.model = pickle.load(model_file)

	def preprocess(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)[1] / 255

		return frame

	def labeled_regions(self, frame):
		frame = self.preprocess(frame)
		frame = skimage.measure.label(frame, background=1)
		return skimage.measure.regionprops(frame)

	def clasified_regions(self, frame):
		regions = self.labeled_regions(frame)
		def filter_fn(region):
			return (
				(17 < region.major_axis and region.major_axis < 49) and
				(15 < region.minor_axis and region.minor_axis < 30) and
				(70 < region.area and region.area < 540) and
				(144 < region.convex_area and region.convex_area < 540) and
			)
		regions = filter(filter_fn, regions)

		import pdb; pdb.set_trace()

        'area': region.area,
        'orientation': region.orientation,
        'perimeter': region.perimeter,
        'minor_axis': region.minor_axis_length,
        'major_axis': region.major_axis_length,
        'convex_area': region.convex_area,
        'filled_area': region.filled_area,
        'solidity': region.solidity,
        'image': region.image

if __name__ == '__main__':
	sample_frame = np.load('images/sample-1.npy')
	object_detector = ObjectDetector()
	object_detector.clasified_regions(sample_frame)
