from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import json
from hometax_class_collection import WebHelper

options = Options()
options.headless = False  # 브라우저 창이 보이도록 설정

s = Service('/Users/jiyongpark/development/hometax/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://www.hometax.go.kr/")
time.sleep(3)  # 페이지 로드를 위해 3초 대기

web_helper = WebHelper(driver)

# 신고기간 홈택스 접속
web_helper.click_by_id("RD3A")
time.sleep(5)

# 로그인 페이지 ID를 사용하여 요소 찾기 및 클릭
web_helper.click_by_id("textbox915")

time.sleep(3)  # 클릭 후 페이지 로드를 위해 3초 대기

# 아이디 로그인 iframe으로 전환
web_helper.switch_to_iframe_by_id("txppIframe")

# ID가 anchor15인 요소를 클릭
web_helper.click_by_id("anchor15")

# 아이디 입력
web_helper.send_keys_by_id("iptUserId", "asdscv")

# 비밀번호 입력
web_helper.send_keys_by_id("iptUserPw", "qpffkwldh35%")

# 로그인 버튼 클릭
web_helper.click_by_id("anchor25")

# iframe 원복
web_helper.switch_to_default_content()
time.sleep(3)

# 세금신고 오버링 후 전자신고 결과 조회 클릭
web_helper.hover_and_click("hdGroup912","menuAtag_4101010000")
time.sleep(3)

# 전자신고 결과 조회 iframe 전환
web_helper.switch_to_iframe_by_id("txppIframe")

# 세목 선택
web_helper.select_by_visible_text("selectbox_itrfCd", "종합소득세")

# 신고일자 조회 시작시점
web_helper.double_click_by_id("rtnDtSrt_input")
web_helper.send_keys_by_id("rtnDtSrt_input" ,"20230101")

# 신고일자 조회 종료시점
web_helper.double_click_by_id("rtnDtEnd_input")
web_helper.send_keys_by_id("rtnDtEnd_input" ,"20231231")

# 사업자등록번호/주민등록번호 입력
web_helper.send_keys_by_id("input_txprRgtNo" ,"9206181103210")

# 정보 공개여부 부 클릭
web_helper.click_by_id("ntplInfpYn_input_1")

# 조회하기 클릭
web_helper.click_by_id("trigger71")

# 조회완료 팝업창 확인
web_helper.accept_popup()

# 접수번호(신고서보기) 클릭
web_helper.click_by_id("ttirnam101DVOListDes_cell_0_8")

# 창이 두 개가 뜨면, 새 창으로 전환
main_window = driver.current_window_handle
all_windows = driver.window_handles

# 새 창들이 열릴 때까지 대기
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))

# 새 창들 중 "신고서 보기 개인정보 공개여부" 창으로 전환
for window in all_windows:
    if window != main_window:
        driver.switch_to.window(window)
        if "신고서 보기 개인정보 공개여부" in driver.title:
            # 원하는 작업 수행 (예: 특정 버튼 클릭)
            web_helper.click_by_id("trigger1")
            break

# 이제 '신고서 미리보기' 창으로 전환
for window in all_windows:
    if window != main_window:
        driver.switch_to.window(window)
        if "신고서미리보기" in driver.title:
            break

time.sleep(5)

input("Press Enter to close the browser")
driver.quit()  # 사용자가 입력을 하면 브라우저를 닫습니다.