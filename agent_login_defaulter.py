import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from hometax_class_collection import HometaxAgentLoginHelper, WebHelper, DataExtractor
from google_class_collection import GoogleSheetsHelper
from airtable_get_company_data import airtable_company  # Airtable 데이터 가져오기

# 브라우저 옵션 설정
options = Options()
options.headless = False  # 브라우저 창이 보이도록 설정

# 드라이버 서비스 설정
s = Service('/Users/jiyongpark/development/hometax/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=s, options=options)

# 클래스 초기화
web_helper = WebHelper(driver)
login_helper = HometaxAgentLoginHelper(driver)
data_extractor = DataExtractor(driver)

# Google Sheets Helper 초기화
google_sheets_helper = GoogleSheetsHelper(
    client_id="8882977163-p8g91695270p07r8hedfqvd6k47u5nkq.apps.googleusercontent.com",
    client_secret="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",
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1K_5MB5J9Sk7SmLR-Oy94118RcIbrHk4xtrEjoGtIb8E/edit?gid=0#gid=0"
)

# Airtable에서 사업자번호 목록 가져오기
df = airtable_company.get_records()

# test
# biz_numbers = ["3811501917", "1758602704"]
biz_numbers = df["사업자번호"].tolist()


# 로그인 수행
login_helper.login('luke_rictax', 'qpffkwldh35%', 'wldydgh1!!', 'Z18766', 'wldydgh1!')

time.sleep(3)

# 아이프레임 원복
web_helper.switch_to_default_content()

# 세무대리납세관리 오버 수임사업자 기본사항 조회 클릭
web_helper.hover_and_click("hdTxt548", "menuA_48_4803030000")

# iframe 전환
web_helper.switch_to_iframe_by_id("txppIframe")

time.sleep(5)

# 모든 데이터를 저장할 리스트 초기화
all_data = []

# 사업자번호 순환
for biz_number in biz_numbers:
    # 주민(사업자)등록번호 입력
    web_helper.send_keys_by_id("edtTxprNo", biz_number)

    # 조회하기 클릭
    web_helper.click_by_id("trigger15")

    time.sleep(3)

    # 테이블 데이터 찾기
    try:
        table = driver.find_element(By.ID, 'grdList_body_table')
    except:
        print(f"테이블을 찾을 수 없습니다: {biz_number}")
        continue

    # 테이블 헤더 찾기
    header_elements = driver.find_elements(By.CSS_SELECTOR, '#grdList_head_table th span')
    header_list = [header.text for header in header_elements]

    # 테이블 행 찾기
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # 각 행에 대한 데이터 추출
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        cell_data = [cell.text if cell.text.strip() else None for cell in cells]
        if any(cell_data):
            all_data.append(cell_data)

# 데이터프레임으로 변환
df = pd.DataFrame(all_data, columns=header_list)

# 데이터 출력
for index, row in df.iterrows():
    row_data = [str(item) if item is not None else "" for item in row]
    print("/".join(row_data))

# 구글 시트에 업로드
google_sheets_helper.upload_dataframe_to_google_sheets(df)

input("Press Enter to close the browser")
driver.quit()  # 사용자가 입력을 하면 브라우저를 닫습니다.
