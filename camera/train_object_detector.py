from camera.object_detector import ObjectDetector
from camera.stream import stream
from threading import Thread
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

LABELS=[
	'rectangle_slot',
	'circle_slot',
	'triangle_slot',
	'square_slot',
	'rectangle_block',
	'circle_block',
	'triangle_block',
	'square_block',
]

if __name__ == '__main__':
	training_labels=[]
	training_regions=[]
	for label in LABELS:
		print 'Show me a {}'.format(label)
		for i in range(50):
			raw_input()
			sample_frame = stream.read()[1]
			if sample_frame is None:
				pass
			regions = object_detector.labeled_regions(sample_frame)
			if len(regions) != 1:
				print 'Clean the workspace!'
			else:
				print 'Sucess'
				training_labels.append(label)
				training_regions.append(regions[0])
	import pdb; pdb.set_trace()
