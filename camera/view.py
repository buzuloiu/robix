from PIL import Image
import numpy as np

w, h = 512, 512
data = np.load('images/sample-1.npy')
img = Image.fromarray(data, 'RGB')
img.save('images/my.png')
img.show()
