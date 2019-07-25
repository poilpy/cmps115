import torch
import io

# load model
model = torch.hub.load('pytorch/vision', 'fcn_resnet101', pretrained=True)
# save model
model.save("segSaveModel.pth")