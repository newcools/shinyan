from fastapi import FastAPI

app = FastAPI()

@app.get("/card")
async def root():
    return {"message": "card"}