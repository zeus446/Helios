import fastapi

app = fastapi.FastAPI()

@app.get("/")
def get_root():
    return {"message":"root initialized"}