from fastapi import FastAPI

app = FastAPI(title="Sweet Shop Management System")


@app.get("/")
async def root():
    return {"message": "Sweet Shop API is live"}