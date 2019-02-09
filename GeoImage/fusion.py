import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
import torch.nn.functional as F


num_epochs = 5
num_classes = 10
batch_size = 100
learning_rate = 0.001

data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val_2': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]),
    'fusion':transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}

data_dir = '/home/guoqiushi/Documents/task3'
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'val','fusion','val_2']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=1,
                                             shuffle=True, num_workers=4)
              for x in ['train', 'val','fusion','val_2']}

train_loader=dataloaders['train']
val_loader=dataloaders['val']
fusion_loader=dataloaders['fusion']
val2_loader=dataloaders['val_2']

dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.cnn_1 = models.resnet18(pretrained=True)
        self.cnn_1.fc = nn.Linear(
            self.cnn.fc.in_features, 20)
        
        self.cnn_2 = models.resnet18(pretrained=True)
        self.cnn_2.fc = nn.Linear(
            self.cnn.fc.in_features, 20)

        self.fc1 = nn.Linear(20 + 20, 60)
        self.fc2 = nn.Linear(60, 2)

    def forward(self, image_1, image_2):
        x1 = self.cnn_1(image_1)
        x2 = self.cnn_2(image_2)

        x = torch.cat((x1, x2), dim=1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model=MyModel().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

total_step = len(train_loader)

for epoch in range(num_epochs):
    for i,image_pair in enumerate(zip(train_loader,fusion_loader)):

        image_1=image_pair[0][0].to(device)
        image_2=image_pair[1][0].to(device)
        label=image_pair[0][1].to(device)

        outputs = model(image_1,image_2)
        loss = criterion(outputs, label)

    # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i + 1) % 100 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))

model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
with torch.no_grad():
    correct = 0
    total = 0
    for images_pair in zip(val_loader,val2_loader):
        image_1 = images_pair[0][0].to(device)
        image_2 = images_pair[1][0].to(device)
        labels = image_pair[0][1].to(device)
        outputs = model(image_1,image_2)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print('Test Accuracy : {} %'.format(100 * correct / total))

# Save the model checkpoint
torch.save(model.state_dict(), 'model.ckpt')

