import torch
import torchvision.models as models
import torchvision.transforms as transforms
import threading
from PIL import Image

class Img2VecPytorch(object):

  def __init__(self, cuda=False):
    self.device = torch.device("cuda" if cuda else "cpu")

    self.model = models.resnet50(pretrained=True)
    self.layer_output_size = 2048
    self.extraction_layer = self.model._modules.get('avgpool')

    self.model = self.model.to(self.device)

    self.model.eval()

    self.scaler = transforms.Scale((224, 224))
    self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                          std=[0.229, 0.224, 0.225])
    self.to_tensor = transforms.ToTensor()
    self.lock = threading.Lock()

  def get_vec(self, image_path):
    img = Image.open(image_path).convert('RGB')

    with self.lock:
        image = self.normalize(self.to_tensor(self.scaler(img))).unsqueeze(0).to(self.device)
        my_embedding = torch.zeros(1, self.layer_output_size, 1, 1)

        def copy_data(m, i, o):
            my_embedding.copy_(o.data)

        h = self.extraction_layer.register_forward_hook(copy_data)
        self.model(image)
        h.remove()

        return my_embedding.numpy()[0, :, 0, 0]
