from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Request
import requests
from joint_certificate_login_withholdingtax_payment import run_task
import asyncio
import logging
import json  # 추가된 부분

app = FastAPI()

API_KEY = "akfj8slf9s8f7gkfl98sjf7klsdfj9s8fj7kls"  # 무작위 API 키

logging.basicConfig(level=logging.INFO)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI service!"}


@app.get("/result")
def get_results():
    return {"message": "This endpoint is no longer used."}


@app.post("/trigger")
async def trigger_task(request: Request, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    data = await request.json()
    external_url = data.get("url")

    if not external_url:
        raise HTTPException(status_code=400, detail="URL is required")

    loop = asyncio.get_event_loop()
    try:
        logging.info("Trigger task 시작")
        data_chunks = await loop.run_in_executor(None, run_task)
        logging.info("Trigger task 완료, data_chunks 전송 시도")

        for chunk in data_chunks:
            # json.dumps로 변환된 데이터를 문자열로 변환
            json_string = json.dumps(chunk, ensure_ascii=False)
            response = send_data_to_external_url(json_string, external_url)
            logging.info("data_chunk 전송 완료")

        return {"message": "All data chunks sent successfully"}
    except Exception as e:
        logging.error(f"Error in trigger_task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def send_data_to_external_url(data_chunk, external_url):
    headers = {"Content-Type": "application/json"}
    payload = {"data": data_chunk}  # JSON 문자열을 파이썬 객체로 변환


    # 로깅 추가
    logging.info(f"Sending payload to external URL: {payload}")

    response = requests.post(external_url, json=payload, headers=headers)

    # 응답 로깅
    logging.info(f"Response from external URL: {response.text}")

    return response.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
