from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Request
import requests
from joint_certificate_login_withholdingtax_payment import run_task
import asyncio
import logging
import json
from datetime import datetime, timedelta

app = FastAPI()

API_KEY = "akfj8slf9s8f7gkfl98sjf7klsdfj9s8fj7kls"

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
    start_date = data.get("start_date")

    if not external_url:
        raise HTTPException(status_code=400, detail="URL and start_date are required")

    # 종료일은 시작일로부터 30일 후로 설정
    start_date_obj = datetime.strptime(start_date, "%Y%m%d")
    end_date_obj = start_date_obj + timedelta(days=30)
    end_date = end_date_obj.strftime("%Y%m%d")

    loop = asyncio.get_event_loop()
    try:
        logging.info("Trigger task 시작")
        data_chunks = await loop.run_in_executor(None, run_task, start_date, end_date)
        logging.info("Trigger task 완료, data_chunks 전송 시도")

        for chunk in data_chunks:
            json_string = json.dumps(chunk, ensure_ascii=False)
            response = send_data_to_external_url(json_string, external_url)
            logging.info("data_chunk 전송 완료")

        return {"message": "All data chunks sent successfully"}
    except Exception as e:
        logging.error(f"Error in trigger_task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def send_data_to_external_url(data_chunk, external_url):
    headers = {"Content-Type": "application/json"}
    payload = {"data": data_chunk}

    logging.info(f"Sending payload to external URL: {payload}")

    try:
        response = requests.post(external_url, json=payload, headers=headers)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 일으킴
        logging.info(f"Response from external URL: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Request to external URL failed: {e}")

@app.post("/run-task-test")
async def run_task_endpoint(start_date: str, end_date: Optional[str] = None):
    try:
        logging.info("Running task")

        # 종료일이 제공되지 않은 경우 시작일로부터 30일 후로 설정
        if not end_date:
            start_date_dt = datetime.strptime(start_date, "%Y%m%d")
            end_date_dt = start_date_dt + timedelta(days=30)
            end_date = end_date_dt.strftime("%Y%m%d")

        data_chunks = run_task(start_date, end_date)
        logging.info("Task completed")

        # 각 chunk를 JSON 문자열로 변환하여 반환
        results = [json.dumps(chunk, ensure_ascii=False) for chunk in data_chunks]

        return {"message": "Task completed successfully", "results": results}
    except Exception as e:
        logging.error(f"Error running task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
