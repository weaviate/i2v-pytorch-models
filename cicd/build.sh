#!/usr/bin/env bash

set -e

local_repo=${LOCAL_REPO?Variable LOCAL_REPO is required}
model_name=${MODEL_NAME?Variable MODEL_NAME is required}

if [ "$BUILD_INTEL" == "1" ]
then
	docker build --build-arg "MODEL_NAME=$model_name" -t "$local_repo" -f Dockerfile-intel .

else
	docker build --build-arg "MODEL_NAME=$model_name" -t "$local_repo" .
fi
