# pytorch image to vector (for Weaviate)
The inference container for the img2vec module

## Documentation

Documentation for this module can be found [here](https://weaviate.io/developers/weaviate/current/retriever-vectorizer-modules/img2vec-neural.html).

## Build Docker container

```
LOCAL_REPO="img2vec-pytorch" MODEL_NAME="resnet50" ./cicd/build.sh
```

or to include Intel GPU Support for Intel Flex, Max, Arc, integrated GPU (iGPU)

```
BUILD_INTEL=1 LOCAL_REPO="img2vec-pytorch" MODEL_NAME="resnet50" ./cicd/build.sh
```

## Run the Docker container with access to Intel GPUs

```
source ./enable_intel_gpu_permissions.sh
```

```
docker run --ipc=host $DOCKER_ADD_GROUPS --device /dev/dri -itp "8000:8080" -e ENABLE_INTEL_GPU=1 img2vec-pytorch
```

## Run the Docker Container with access to a specific Intel GPU (container is isolated to a single GPU )
```
source ./enable_intel_gpu_permissions.sh
```

```
docker run --ipc=host $DOCKER_ADD_GROUPS --device /dev/dri/renderD129 -itp "8000:8080" -e ENABLE_INTEL_GPU=1 img2vec-pytorch
```
