import torch
import torchvision
import torchvision.transforms as transforms
from torchvision import datasets, models
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # load vgg16 model
    net = models.vgg16(pretrained=True).cuda()
    # set loss function
    criterion = nn.CrossEntropyLoss()
    # set optimizer
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    # define transformations to get image in right format
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


    #load train and test sets
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64,
                                              shuffle=True, num_workers=2)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                           download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=64,
                                             shuffle=False, num_workers=2)

    # set classes
    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    for epoch in range(5):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs
            inputs, labels = data
            inputs, labels = inputs.cuda(), labels.cuda()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 20 == 19:# print every 2000 mini-batches
	            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss))
	            running_loss = 0.0	

    print('Finished Training')

    # save model
    torch.save(net, 'saveModel.pth')


if __name__ == '__main__':
    main()