import torch.nn as nn
from torchvision import models

def get_model(num_classes=4):
    model = models.mobilenet_v2(weights=None)
    num_ftrs = model.last_channel # 1280
    model.classifier[1] = nn.Sequential(
        nn.Linear(num_ftrs, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes)
    )
    return model
