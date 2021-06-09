#!/usr/bin/env python3

import sys
import os
import torchvision.models as models

model_name = os.getenv("MODEL_NAME") 
if model_name != "resnet50":
    print("only resnet50 supported at the moment, selected: {}".format(model_name))
    sys.exit(1)

_ = models.resnet50(pretrained=True)
