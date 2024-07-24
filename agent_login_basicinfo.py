import time
import json
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

# 다운로드 디렉터리 설정
# download_dir = "/Users/jiyongpark/Downloads"  # 실제 다운로드 경로로 변경 필요

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
    spreadsheet_url="https://docs.google.com/spreadsheets/d/1KMKo0PyorxP8fkK4NMyPiSuylbFGcODpaJT1q9JCO3g/edit?gid=0#gid=0"
)

# Airtable에서 사업자번호 목록 가져오기
df = airtable_company.get_records()
# biz_numbers = df["사업자번호"].tolist()
biz_numbers = ["3811501917", "1111111111"]

# 로그인 수행
login_helper.login('luke_rictax', 'qpffkwldh35%', 'wldydgh1!!', 'Z18766', 'wldydgh1!')

time.sleep(3)

# 아이프레임 원복
web_helper.switch_to_default_content()

# 전자세금계산서 조회 클릭
web_helper.hover_and_click("hdTxt548", "menuAtag_4801010000")

# iframe 전환
web_helper.switch_to_iframe_by_id("txppIframe")

time.sleep(5)

# 모든 데이터를 저장할 리스트 초기화
all_data = []

# 사업자번호 순환
for biz_number in biz_numbers:
    time.sleep(1)
    biz_number_part = [biz_number[:3], biz_number[3:5], biz_number[5:]]

    if len(biz_number_part) != 3:
        print(f"biz_number 형식이 올바르지 않습니다: {biz_number}")
        continue

    # biz_number 입력
    web_helper.send_keys_by_id("bsno1", biz_number_part[0])
    web_helper.send_keys_by_id("bsno2", biz_number_part[1])
    web_helper.send_keys_by_id("bsno3", biz_number_part[2])

    # 수임사업자 기본사항 조회하기 클릭
    web_helper.click_by_id("btnSearch")

    # 조회 완료 팝업창 확인
    web_helper.accept_popup()

    # 데이터 추출
    data = data_extractor.extract_data(biz_number)
    all_data.append(data)

# 모든 데이터 출력
for data in all_data:
    print(json.dumps(data, ensure_ascii=False, indent=4))

# 구글 시트에 업로드
google_sheets_helper.upload_to_google_sheets(all_data)

input("Press Enter to close the browser")
driver.quit()  # 사용자가 입력을 하면 브라우저를 닫습니다.
