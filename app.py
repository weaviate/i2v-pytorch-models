from fastapi import FastAPI, Response, status
from vectorizer import ImageVectorizer, VectorImagePayload

app = FastAPI()

imgVec = ImageVectorizer()

@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
def live_and_ready(response: Response):
  response.status_code = status.HTTP_204_NO_CONTENT

@app.post("/vectors")
def read_item(item: VectorImagePayload, response: Response):
  try:
    vector = imgVec.vectorize(item.id, item.image)
    return {"id": item.id, "vector": vector.tolist(), "dim": len(vector)}
  except Exception as e:
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"error": str(e)}
