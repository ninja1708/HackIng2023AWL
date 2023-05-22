import json
import numpy as np
from PIL import Image
import torch
from torch.autograd import Variable
from torchvision import transforms
import torch.nn.functional as F


IMG_PATH = 'validate/14/aea3a70d-ecca-4cf6-89cb-fc5bed19e3b5.tiff'
CHKPOINT_PATH = 'checkpoints/checkpoint_ing.pth'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

ckpt = torch.load(CHKPOINT_PATH, map_location=torch.device('cpu'))
ckpt.keys()

def load_checkpoint(filepath):
    checkpoint = torch.load(filepath, map_location=torch.device('cpu'))
    model = checkpoint['model']
    model.classifier = checkpoint['classifier']
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['class_to_idx']

    for param in model.parameters():
        param.requires_grad = False

    return model, checkpoint['class_to_idx']



model, class_to_idx = load_checkpoint(CHKPOINT_PATH)
idx_to_class = {v: k for k, v in class_to_idx.items()}


def pil_loader(path):
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')
def process_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    image = preprocess(image)
    return image


def predict2(image_path, model, topk=3):


    img = pil_loader(image_path)
    img = process_image(img)

    img = np.expand_dims(img, 0)

    img = torch.from_numpy(img)

    model.eval()
    inputs = Variable(img).to(device)
    logits = model.forward(inputs)

    ps = F.softmax(logits, dim=1)
    topk = ps.cpu().topk(topk)

    return (e.data.numpy().squeeze().tolist() for e in topk)


with open('assets/cat_to_name.json', 'r') as f:
    cat_to_name = json.load(f)


data_transforms = {
    'train': transforms.Compose([
        transforms.RandomRotation(30),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'valid': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
}

class_names = ['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '3', '4', '5', '6', '7',
               '8', '9']

if __name__ == "__main__":
    probs, classes = predict2(IMG_PATH, model.to(device))
    print(probs)
    signs = [cat_to_name[class_names[e]] for e in classes]
    print(signs)
