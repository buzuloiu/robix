import cv2
import numpy as np
from camera.stream import stream

class ObjectDetector(object):
	def __init__(self):

	def preprocess(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)[1] / 255

		return frame

	def labeled_regions(self, frame):
		frame = self.preprocessed_frame(frame)
		frame =

	def clasified_regions(self, frame):
		
