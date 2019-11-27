import torchvision.models as models
from torchvision import transforms
from PIL import Image
import torch
densenet121 = models.densenet121(pretrained=True)


transform = transforms.Compose([            #[1]
transforms.Resize(256),                    #[2]
transforms.CenterCrop(224),                #[3]
transforms.ToTensor(),                     #[4]
transforms.Normalize(                      #[5]
mean=[0.485, 0.456, 0.406],                #[6]
std=[0.229, 0.224, 0.225]                  #[7]
)])

x  = Image.open('dog.jpg')
img_t = transform(x)
batch_t = torch.unsqueeze(img_t, 0)

densenet121.eval()

output = densenet121(batch_t)
print(output.shape)


with open('classnames.txt') as f:
  classes = [line.strip() for line in f.readlines()]

labels = {int((x.split(':')[0]).replace('"',"").replace("'","")):x.split(':')[1].replace('"',"").replace("'","") for x in classes}

_, idx = torch.max(output,1)

print(labels[int(idx)])

print(torch.sum(output))