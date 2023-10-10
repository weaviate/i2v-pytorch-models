import os
from logging import getLogger
from fastapi import FastAPI, Response, status
from vectorizer import ImageVectorizer, VectorImagePayload


app = FastAPI()
imgVec : ImageVectorizer
logger = getLogger('uvicorn')


@app.on_event("startup")
def startup_event():
	global imgVec

	cuda_env = os.getenv("ENABLE_CUDA")
	intel_gpu_env = os.getenv("ENABLE_INTEL_GPU")
	cuda_support = False
	intel_support = False
	device_core = ""

	if cuda_env is not None and cuda_env == "true" or cuda_env == "1":
		cuda_support = True
		device_core = os.getenv("CUDA_CORE")
		if device_core is None or device_core == "":
				device_core = "cuda:0"
		logger.info(f"CUDA_CORE set to {device_core}")
	elif intel_gpu_env is not None and intel_gpu_env == "true" or intel_gpu_env == "1":
		intel_support = True
		device_core = os.getenv("INTEL_GPU_CORE")
		if device_core is None or device_core == "":
				device_core = "xpu"
		logger.info(f"INTEL_CORE set to {device_core}")
	else:
		logger.info("Running on CPU")

	imgVec = ImageVectorizer(cuda_support, intel_support, device_core)

@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
def live_and_ready(response: Response):
	response.status_code = status.HTTP_204_NO_CONTENT


@app.post("/vectors")
@app.post("/vectors/")
def read_item(item: VectorImagePayload, response: Response):
	try:
		vector = imgVec.vectorize(item.id, item.image)
		return {"id": item.id, "vector": vector.tolist(), "dim": len(vector)}
	except Exception as e:
		logger.exception(
            'Something went wrong while vectorizing data.'
        )
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return {"error": str(e)}
