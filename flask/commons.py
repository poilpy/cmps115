import io

import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms


def get_tensor(image):
	my_transforms = transforms.Compose([
		transforms.Resize(256),
	    transforms.CenterCrop(224),
	    transforms.ToTensor(),
	    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
         					  std=[0.229, 0.224, 0.225])])
	# image = Image.open(io.BytesIO(image_bytes))
	return my_transforms(image).unsqueeze(0)

def get_seg_tensor(image):
	my_transforms = transforms.Compose([
		transforms.Resize(256),
	    transforms.ToTensor(),
	    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
         					  std=[0.229, 0.224, 0.225])])
	# image = Image.open(io.BytesIO(image_bytes))
	return my_transforms(image).unsqueeze(0)