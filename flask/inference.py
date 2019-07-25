import json

from commons import get_tensor, get_seg_tensor
import torch

from PIL import Image
from torchvision import transforms

#recognition classes
classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def classify(img):
	# convert image to tensor
	img = get_tensor(img).cuda()
	# load saved model
	net = torch.load('saveModel.pth')
	# push image through network
	outputs = net(img).cuda()
	_, predicted = torch.max(outputs.data, 1)

	# connect prediction result to corresponding class
	result = classes[predicted[0]]

	return result

# Segmentation function, takes input image, segments through saved model, outputs colored image.
def segment(img):
	# convert image to tensor
	img = get_seg_tensor(img).cuda()
	# load saved model
	model = torch.load('segSaveModel.pth').cuda()

	# push image through network
	with torch.no_grad():
	    output = model(img)['out'][0]
	output_predictions = output.argmax(0)

	# Create color palatte for each class
	palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
	colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
	colors = (colors % 255).numpy().astype("uint8")

	# plot the semantic segmentation predictions of 21 classes in each color
	result = Image.fromarray(output_predictions.byte().cpu().numpy())
	result.putpalette(colors)

	return result