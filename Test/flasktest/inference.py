import json

from commons import get_tensor, get_seg_tensor
import torch

from PIL import Image
from torchvision import transforms

# with open('cat_to_name.json') as f:
# 	cat_to_name = json.load(f)

# with open('class_to_idx.json') as f:
# 	class_to_idx = json.load(f)


# idx_to_class = {v:k for k, v in class_to_idx.items()}

# model = get_model()

# def get_flower_name(image_bytes):
# 	tensor = get_tensor(image_bytes)
# 	outputs = model.forward(tensor)
# 	_, prediction = outputs.max(1)
# 	category = prediction.item()
# 	class_idx = idx_to_class[category]
# 	flower_name = cat_to_name[class_idx]
# 	return category, flower_name
classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def classify(img):
	img = get_tensor(img).cuda()
	net = torch.load('saveModel.pth')
	outputs = net(img).cuda()
	_, predicted = torch.max(outputs.data, 1)
	cool = classes[predicted[0]]

	return cool




def segment(img):
	img = get_seg_tensor(img).cuda()
	model = torch.load('segSaveModel.pth')
	# preprocess = transforms.Compose([
	#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	# ])

	print('lol')

	# input_tensor = preprocess(input_image)
	# input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model
	# input_batch = input_image.unsqueeze(0)

	# move the input and model to GPU for speed if available
	if torch.cuda.is_available():
	    input_batch = img.to('cuda')
	    model.to('cuda')

	with torch.no_grad():
	    output = model(input_batch)['out'][0]
	output_predictions = output.argmax(0)
	# r =output_predictions


	palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
	colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
	colors = (colors % 255).numpy().astype("uint8")

	# plot the semantic segmentation predictions of 21 classes in each color
	r = Image.fromarray(output_predictions.byte().cpu().numpy())
	r.putpalette(colors)

	return r