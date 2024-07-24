import requests
import pandas as pd
import time


class AirtableCompanyContract:
    def __init__(self, personal_access_token, base_id, table_id, view_id):
        self.personal_access_token = personal_access_token
        self.base_id = base_id
        self.table_id = table_id
        self.view_id = view_id
        self.headers = {
            "Authorization": f"Bearer {self.personal_access_token}",
        }

    def get_records(self):
        records = []
        offset = None

        while True:
            url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_id}?view={self.view_id}"
            if offset:
                url += f"&offset={offset}"

            response = requests.get(url, headers=self.headers)
            data = response.json()

            for record in data['records']:
                fields = record['fields']
                biz_number = fields.get('사업자(주민)번호', '').replace('-', '')  # 사업자번호에서 '-' 제거
                records.append({
                    "Record ID": record['id'],
                    "사업장명": fields.get('사업장명', ''),
                    "사업자번호": biz_number,
                    "홈택스아이디_사업자": fields.get('홈택스아이디_사업자', ''),
                    "홈택스비밀번호_사업자": fields.get('홈택스비밀번호_사업자', ''),
                    "홈택스아이디_개인": fields.get('홈택스아이디_개인', ''),
                    "홈택스비밀번호_개인": fields.get('홈택스비밀번호_개인', '')
                })

            offset = data.get('offset')
            if not offset:
                break

            time.sleep(1.2)

        return pd.DataFrame(records)


# AirtableCompanyContract 클래스 인스턴스 생성 및 데이터 가져오기
airtable_company = AirtableCompanyContract(
    personal_access_token="patnNFGh5Jb9bOG5a.1db8f8f9829d96ef54bd20279f47d696625b22b733ce31d529338902ddc0a24a",
    base_id="apphTQurZM8dAvVdn",
    table_id="tblVxjgQVtkJemxeB",
    view_id="viwzOePHtY6i2f8Sx"
)

# 데이터 조회 및 데이터프레임 생성
df = airtable_company.get_records()

# JSON 파일로 저장
# json_filename = "airtable_data.json"
# df.to_json(json_filename, orient='records', force_ascii=False)

# 사업자번호 목록 추출
# biz_numbers = df["사업자번호"].tolist()
