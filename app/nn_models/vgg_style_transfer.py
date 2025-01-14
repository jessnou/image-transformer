import torch
from torchvision import models
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms.v2 as tfs
from PIL import Image
import numpy as np

class ModelStyle(nn.Module):
    def __init__(self):
        super().__init__()
        _model = models.vgg19(weights=models.VGG19_Weights.DEFAULT)
        self.mf = _model.features
        self.mf.requires_grad_(False)
        self.requires_grad_(False)
        self.mf.eval()
        self.idx_out = (0, 5, 10, 19, 28, 34)
        self.num_style_layers = len(self.idx_out) - 1

    def forward(self, x):
        outputs = []
        for indx, layer in enumerate(self.mf):
            x = layer(x)
            if indx in self.idx_out:
                outputs.append(x.squeeze(0))
        return outputs

def gram_matrix(x):
    channels = x.size(dim=0)
    g = x.view(channels, -1)
    gram = torch.mm(g, g.mT) / g.size(dim=1)
    return gram

def get_content_loss(base_content, target):
    return torch.mean(torch.square(base_content - target))

def get_style_loss(base_style, gram_target):
    style_weights = [1.0, 0.8, 0.5, 0.3, 0.1]

    _loss = 0
    i = 0
    for base, target in zip(base_style, gram_target):
        gram_style = gram_matrix(base)
        _loss += style_weights[i] * get_content_loss(gram_style, target)
        i += 1

    return _loss

def transfer_style(content_image, style_image, epochs=100, content_weight=1, style_weight=1000, lr=0.01):
    transforms = tfs.Compose([tfs.ToImage(),
        tfs.ToDtype(torch.float32, scale=True),
    ])

    content_image = transforms(content_image).unsqueeze(0)
    style_image = transforms(style_image).unsqueeze(0)

    img_create = content_image.clone()
    img_create.requires_grad_(True)

    model = ModelStyle()
    content_features = model(content_image)
    style_features = model(style_image)

    gram_matrix_style = [gram_matrix(x) for x in style_features[:model.num_style_layers]]

    optimizer = optim.Adam(params=[img_create], lr=lr)
    best_img = img_create.clone()
    best_loss = -1

    for _ in range(epochs):
        outputs_img_create = model(img_create)

        loss_content = get_content_loss(outputs_img_create[-1], content_features[-1])
        loss_style = get_style_loss(outputs_img_create, gram_matrix_style)
        loss = content_weight * loss_content + style_weight * loss_style

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        img_create.data.clamp_(0, 1)

        if loss < best_loss or best_loss < 0:
            best_loss = loss
            best_img = img_create.clone()

    return best_img
