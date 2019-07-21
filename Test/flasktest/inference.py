import json

from commons import get_tensor
import torch

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