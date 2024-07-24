import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoAlertPresentException
from hometax_class_collection import HometaxLoginHelper, WebHelper

# 브라우저 옵션 설정
options = Options()
options.headless = False  # 브라우저 창이 보이도록 설정

# 다운로드 디렉터리 설정
download_dir = "/Users/jiyongpark/Downloads"  # 실제 다운로드 경로로 변경 필요

# 드라이버 서비스 설정
s = Service('/Users/jiyongpark/development/hometax/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=s, options=options)

# 클래스 초기화
web_helper = WebHelper(driver)
login_helper = HometaxLoginHelper(driver)

# 로그인 수행
login_helper.login('luke_rictax', 'qpffkwldh35%', 'wldydgh1!!', 'Z18766', 'wldydgh1!')

time.sleep(3)

# 아이프레임 원복
web_helper.switch_to_default_content()

# 전자세금계산서 조회 클릭
web_helper.hover_and_click("hdGroup922", "menuAtag_4609050000")

# 월/분기별 목록조회
web_helper.click_by_id("menu_46_4609050300")

# iframe 전환
web_helper.switch_to_iframe_by_id("txppIframe")

# 수임사업자 전환 클릭
web_helper.click_by_id("trigger501")

# iframe 전환
web_helper.switch_to_iframe_by_id("UTEETZZA21_iframe")

# 수임납세자번호 사업자등록번호 클릭
web_helper.select_by_visible_text("selectbox5", "사업자등록번호")

# 사업자등록번호 입력
web_helper.send_keys_by_id("txprDscmNoA", "3811501917")

# 조회하기 선택
web_helper.click_by_id("trigger85")

# 사업자 선택
web_helper.click_by_id("grdResult_cell_0_0")

# 확인 클릭
web_helper.click_by_id("btnProcess")

# iframe 전환
web_helper.switch_to_default_content()
web_helper.switch_to_iframe_by_id("txppIframe")

# 기본 매출. 매입 클릭
web_helper.click_by_id("radio3_input_1")

# 반기별 클릭
web_helper.click_by_id("radio4_input_2")

# 조회하기 클릭
web_helper.click_by_id("trigger50")

# 엑셀 내려받기
web_helper.click_by_id("trigger55")

# iframe 전환
web_helper.switch_to_iframe_by_id("UTEETBDA17_iframe")

# 품목정보 추가 여부 선택 팝업창 확인 클릭
web_helper.click_by_id("btnProcess")

# 내려받기 파일 종류 선택 팝업창 엑셀 클릭
web_helper.click_by_id("trigger4")

# 엑셀 파일 다운로드 팝업창 확인 클릭
web_helper.accept_popup()

# 다운로드 완료 대기 (필요시 조정)
print("파일 다운로드 대기 중...")
time.sleep(10)  # 다운로드 시간 대기, 필요시 조정


input("Press Enter to close the browser")
driver.quit()  # 사용자가 입력을 하면 브라우저를 닫습니다.
