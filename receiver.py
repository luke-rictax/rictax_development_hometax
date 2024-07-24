from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/endpoint")
async def receive_data(request: Request):
    data = await request.json()
    print("Received data:", data)
    return {"status": "success", "data_received": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
