import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  # 추가된 부분
from webdriver_manager.chrome import ChromeDriverManager
from hometax_class_collection import HometaxAgentLoginHelper, WebHelper, DataExtractor, HometaxJointCertificateLoginHelper
from google_class_collection import GoogleSheetsHelper
from airtable_get_company_data import airtable_company  # Airtable 데이터 가져오기

logging.basicConfig(level=logging.INFO)

def run_task():
    options = Options()
    options.add_argument('--headless')  # Headless 모드 옵션
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # ChromeDriver 경로 설정을 webdriver-manager로 대체
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 클래스 초기화
    web_helper = WebHelper(driver)
    login_helper = HometaxJointCertificateLoginHelper(driver)
    data_extractor = DataExtractor(driver)

    try:
        # 로그인 수행
        logging.info("Logging in...")
        login_helper.login('wldydgh1!!', 'Z18766', 'wldydgh1!')

        time.sleep(3)

        # 아이프레임 원복
        web_helper.switch_to_default_content()

        # 세금신고 오버 일반신고 클릭
        web_helper.hover_and_click("hdGroup912", "menuAtag_4106010000")

        # 새로 뜬 창을 닫고 원래 창으로 전환
        time.sleep(5)
        main_window = driver.current_window_handle
        all_windows = driver.window_handles

        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()

        driver.switch_to.window(main_window)

        # iframe 전환
        web_helper.switch_to_iframe_by_id("txppIframe")

        # 신고내역 조회(접수증납부서) 클릭
        web_helper.click_by_id("tabControl1_UTERNAAZ11_tab_tabs2_UTERNAAZ11")
        time.sleep(3)

        # 조회하기 클릭
        try:
            web_helper.click_by_id("trigger70_UTERNAAZ31")
            logging.info("Clicked on trigger70_UTERNAAZ31 successfully.")
        except Exception as e:
            logging.error(f"Error clicking trigger70_UTERNAAZ31: {e}")

        time.sleep(3)

        # 팝업창 닫기
        web_helper.accept_popup()

        # 모든 데이터를 저장할 리스트 초기화
        all_data = []

        # 세목 선택
        web_helper.select_by_visible_text("edtGrdRowNum", "100건")

        # 조회건수 변경 후 확인
        web_helper.click_by_id("trigger6_UTERNAAZ31")
        time.sleep(3)

        # 팝업 닫기
        web_helper.accept_popup()

        def extract_data_from_current_page():
            rows = driver.find_elements(By.CSS_SELECTOR, '#ttirnam101DVOListDes_body_table tr')
            if not rows:
                logging.info("No rows found on the current page.")
                return

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells and len(cells) > 38:
                    cell_data = {
                        "과세연월": cells[2].text.strip(),
                        "신고서종류": cells[3].text.strip(),
                        "신고구분": cells[4].text.strip(),
                        "신고유형": cells[5].text.strip(),
                        "상호(성명)": cells[6].text.strip(),
                        "사업자(주민)등록번호": cells[7].text.strip(),
                        "접수방법": cells[8].text.strip(),
                        "접수일시": cells[9].text.strip(),
                        "접수번호(신고서보기)": cells[10].text.strip(),
                        "접수서류": cells[11].text.strip(),
                        "접수증": "",  # 빈 값으로 설정
                        "납부서": "",  # 빈 값으로 설정
                        "제출자ID": cells[30].text.strip(),
                        "부속서류제출여부": cells[31].text.strip(),
                        "지방소득세": "",  # 빈 값으로 설정
                        "납부여부": cells[38].text.strip()
                    }
                    # Check if all important fields are empty
                    if any(value != "" for value in cell_data.values()):
                        all_data.append(cell_data)
                    else:
                        logging.info("Skipping row with all empty fields.")
                else:
                    logging.warning("Row does not contain enough cells. Skipping row.")

            logging.info(f"Extracted {len(rows)} rows from the current page.")

        def navigate_and_extract_data():
            page_num = 1
            while True:
                for page in range(page_num, page_num + 10):
                    try:
                        page_button = driver.find_element(By.CSS_SELECTOR, f'#pglNavi887_page_{page}')
                        page_button.click()
                        time.sleep(3)
                        web_helper.accept_popup()
                    except NoSuchElementException:
                        logging.info(f"No more pages to navigate. Ending at page {page}.")
                        return
                    except Exception as e:
                        logging.error(f"Error navigating to page {page}: {e}")
                        return

                    extract_data_from_current_page()
                    time.sleep(1)  # 페이지에서 1초 동안 대기

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, '#pglNavi887_next_btn[style*="visibility: visible"]')
                    next_button.click()
                    time.sleep(3)
                    web_helper.accept_popup()
                    page_num += 10
                except Exception as e:
                    logging.error(f"Error navigating to next 10 pages: {e}")
                    break

        navigate_and_extract_data()

        driver.quit()

        # 데이터를 20건씩 나누어 반환, 메타데이터 포함
        total_data_count = len(all_data)
        data_chunks = [all_data[i:i + 20] for i in range(0, total_data_count, 20)]
        total_chunks = len(data_chunks)
        json_chunks = [
            json.dumps({
                "data": chunk,
                "metadata": {
                    "total_data_count": total_data_count,
                    "total_chunks": total_chunks,
                    "current_chunk_index": i + 1
                }
            }, ensure_ascii=False, indent=4)
            for i, chunk in enumerate(data_chunks)
        ]

        return json_chunks

    except Exception as e:
        logging.error(f"Error in run_task: {e}")
        driver.quit()
        raise

# 실행 예시
if __name__ == "__main__":
    result = run_task()
    for chunk in result:
        print(chunk)
