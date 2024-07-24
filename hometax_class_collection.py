import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO)


class WebHelper:
    """웹 페이지와 상호 작용하기 위한 도우미 클래스입니다."""
    def __init__(self, driver):
        self.driver = driver

    def click_by_id(self, element_id):
        """ID를 사용하여 웹 페이지의 요소를 클릭합니다."""
        try:
            logging.info(f"Trying to click element with ID: {element_id}")
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            element.click()
            logging.info(f"Clicked element with ID: {element_id}")
        except Exception as e:
            logging.error(f"Clicking error on {element_id}: {e}")

    def send_keys_by_id(self, element_id, text):
        """ID를 사용하여 웹 페이지의 요소에 텍스트를 입력합니다."""
        try:
            logging.info(f"Trying to send keys to element with ID: {element_id}")
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            element.clear()  # 기존의 값을 삭제
            element.send_keys(text)
            logging.info(f"Sent keys to element with ID: {element_id}")
        except Exception as e:
            logging.error(f"Sending keys error on {element_id}: {e}")

    def switch_to_iframe_by_id(self, iframe_id):
        """ID를 사용하여 iframe으로 전환합니다."""
        try:
            logging.info(f"Switching to iframe with ID: {iframe_id}")
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, iframe_id))
            )
            self.driver.switch_to.frame(iframe)
            logging.info(f"Switched to iframe with ID: {iframe_id}")
        except Exception as e:
            logging.error(f"IFrame switching error on {iframe_id}: {e}")

    def switch_to_default_content(self):
        """최상위 문서로 전환합니다."""
        try:
            logging.info("Switching to default content")
            self.driver.switch_to.default_content()
            logging.info("Switched to default content")
        except WebDriverException as e:
            logging.error(f"WebDriverException while switching to default content: {e}")

    def select_by_visible_text(self, select_id, text):
        """ID를 사용하여 select 요소에서 텍스트를 선택합니다."""
        try:
            logging.info(f"Selecting '{text}' from select element with ID: {select_id}")
            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, select_id))
            )
            select = Select(select_element)
            options = [option.text for option in select.options]
            if text in options:
                select.select_by_visible_text(text)
                logging.info(f"Selected '{text}' from select element with ID: {select_id}")
            else:
                logging.warning(f"Option '{text}' not found in select element with ID '{select_id}'. Available options: {options}")
        except Exception as e:
            logging.error(f"Selecting text error on {select_id} with text {text}: {e}")

    def hover_and_click(self, hover_element_id, click_element_id):
        """ID를 사용하여 요소에 마우스를 오버링한 후 다른 요소를 클릭합니다."""
        try:
            logging.info(f"Hovering over element with ID: {hover_element_id} and clicking element with ID: {click_element_id}")
            hover_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, hover_element_id))
            )
            click_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, click_element_id))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(hover_element).perform()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, click_element_id))
            )
            click_element.click()
            logging.info(f"Hovered over element with ID: {hover_element_id} and clicked element with ID: {click_element_id}")
        except TimeoutException:
            logging.error(f"Timeout while waiting for elements {hover_element_id} or {click_element_id}.")
        except WebDriverException as e:
            logging.error(f"WebDriverException while hovering on {hover_element_id} and clicking on {click_element_id}: {e}")

    def double_click_by_id(self, element_id):
        """ID를 사용하여 웹 페이지의 요소를 더블클릭합니다."""
        try:
            logging.info(f"Double-clicking element with ID: {element_id}")
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, element_id))
            )
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
            logging.info(f"Double-clicked element with ID: {element_id}")
        except Exception as e:
            logging.error(f"Double-clicking error on {element_id}: {e}")

    def accept_popup(self):
        try:
            logging.info("Waiting for popup to accept")
            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert.accept()
            logging.info("Accepted popup")
        except TimeoutException:
            logging.warning("Popup did not appear.")
        except NoAlertPresentException:
            logging.warning("No alert present to accept.")


class HometaxAgentLoginHelper(WebHelper):
    def __init__(self, driver):
        super().__init__(driver)

    def login(self, user_id, user_pw, cert_pw, agent_id, agent_pw):
        logging.info("Starting login process")
        try:
            # 홈택스 페이지 접속
            self.driver.get("https://www.hometax.go.kr/")
            time.sleep(5)  # 페이지 로드를 위해 3초 대기

            # 신고기간 홈택스 접속
            self.click_by_id("RD3A")
            time.sleep(5)

            # 로그인 페이지 ID를 사용하여 요소 찾기 및 클릭
            self.click_by_id("textbox915")
            time.sleep(5)  # 클릭 후 페이지 로드를 위해 3초 대기

            # 아이디 로그인 화면 iframe으로 전환
            self.switch_to_iframe_by_id("txppIframe")
            time.sleep(3)

            # ID가 anchor15인 요소를 클릭
            self.click_by_id("anchor15")

            # 아이디 입력
            self.send_keys_by_id("iptUserId", user_id)

            # 비밀번호 입력
            self.send_keys_by_id("iptUserPw", user_pw)

            # 로그인 버튼 클릭
            self.click_by_id("anchor25")

            # 공동인증서 로그인 iframe 전환
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "dscert")))

            # 공동인증서 클릭
            self.click_by_id("row0dataTable")

            # 공동인증서 비밀번호 입력
            self.send_keys_by_id("input_cert_pw", cert_pw)

            # JavaScript를 사용하여 공동인증서 로그인 확인 클릭
            try:
                self.driver.execute_script("document.getElementById('btn_confirm_iframe').click();")
                logging.info("Clicked confirm button for certificate")
            except WebDriverException as e:
                logging.error(f"JavaScript 예외 발생: {e}")

            # 팝업창에서 확인 버튼 클릭
            self.accept_popup()

            # 기존화면 iframe 전환
            self.switch_to_default_content()

            # 세무대리인 로그인화면 iframe 전환
            self.switch_to_iframe_by_id("txppIframe")

            # 세무대리인 id 입력
            self.send_keys_by_id("input1", agent_id)

            # 세무대리인 비밀번호 입력
            self.send_keys_by_id("input2", agent_pw)

            # 세무대리인 로그인 버튼 클릭
            self.click_by_id("trigger41")
            logging.info("Login process completed")
        except Exception as e:
            logging.error(f"Error during login process: {e}")


class DataExtractor:
    def __init__(self, driver):
        self.driver = driver

    def extract_data(self, biz_number):
        logging.info("Starting data extraction")
        try:
            data = {
                "세무대리의뢰인": {
                    "개인사업자": self.driver.find_element(By.CSS_SELECTOR, '#txprDclsCd_input_0').is_selected(),
                    "법인사업자": self.driver.find_element(By.CSS_SELECTOR, '#txprDclsCd_input_1').is_selected()
                },
                "사업자등록번호": self.driver.find_element(By.ID, 'txprDscmNoEncCntn').text or biz_number,
                "상호": self.driver.find_element(By.ID, 'textbox1754').text,
                "개업일자": self.driver.find_element(By.ID, 'txprDscmDt').text,
                "성명": self.driver.find_element(By.ID, 'textbox1755').text,
                "주민등록번호": self.driver.find_element(By.ID, 'rprsResno').text,
                "사업장전화번호": self.driver.find_element(By.ID, 'textbox1759').text,
                "전화번호": self.driver.find_element(By.ID, 'textbox1761').text,
                "사업장도로명주소": self.driver.find_element(By.ID, 'textbox1794').text,
                "사업장법정동주소": self.driver.find_element(By.ID, 'textbox1796').text,
                "업태": self.driver.find_element(By.ID, 'textbox1760').text,
                "종목": self.driver.find_element(By.ID, 'textbox1762').text,
                "주업종코드": self.driver.find_element(By.ID, 'textbox17476').text,
                "전자세금계산서 발급의무 대상자여부": {
                    "여": self.driver.find_element(By.ID, 'etxivIsnDutySbjsYn_input_0').is_selected(),
                    "부": self.driver.find_element(By.ID, 'etxivIsnDutySbjsYn_input_1').is_selected()
                },
                "현금영수증 가맹여부": {
                    "여": self.driver.find_element(By.ID, 'cshptJnnYn_input_0').is_selected(),
                    "부": self.driver.find_element(By.ID, 'cshptJnnYn_input_1').is_selected()
                },
                "신용카드 가맹여부": {
                    "여": self.driver.find_element(By.ID, 'crdcJnnYn_input_0').is_selected(),
                    "부": self.driver.find_element(By.ID, 'crdcJnnYn_input_1').is_selected()
                },
                "원천징수 의무구분": self.driver.find_element(By.ID, 'textbox17477').text,
                "(부가세)총괄납부 주사업장여부": {
                    "여": self.driver.find_element(By.ID, 'whlPmtBmanYn_input_0').is_selected(),
                    "부": self.driver.find_element(By.ID, 'whlPmtBmanYn_input_1').is_selected()
                },
                "관할세무서": self.driver.find_element(By.ID, 'textbox1804').text,
                "담당자성명(전화번호)": self.driver.find_element(By.ID, 'textbox1806').text
            }

            if not data["사업자등록번호"] or data["사업자등록번호"].isspace():
                data["사업자등록번호"] = biz_number

            logging.info("Data extraction completed")
            return data
        except Exception as e:
            logging.error(f"Error during data extraction: {e}")
            raise

    def save_to_json(self, data, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"데이터가 JSON 파일에 저장되었습니다: {filename}")
        except Exception as e:
            logging.error(f"Error saving data to JSON: {e}")


class HometaxJointCertificateLoginHelper(WebHelper):
    def __init__(self, driver):
        super().__init__(driver)

    def login(self, cert_pw, agent_id, agent_pw):
        logging.info("Starting certificate login process")
        try:
            # 홈택스 페이지 접속
            self.driver.get("https://www.hometax.go.kr/")
            time.sleep(5)  # 페이지 로드를 위해 3초 대기

            # 신고기간 홈택스 접속
            self.click_by_id("RD3A")
            time.sleep(5)

            # 로그인 페이지 ID를 사용하여 요소 찾기 및 클릭
            self.click_by_id("textbox915")
            time.sleep(5)  # 클릭 후 페이지 로드를 위해 3초 대기

            # 아이디 로그인 화면 iframe으로 전환
            self.switch_to_iframe_by_id("txppIframe")
            time.sleep(5)

            # 공동금융인증서 클릭
            self.click_by_id("anchor22")
            time.sleep(5)

            # 공동인증서 로그인 iframe 전환
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "dscert")))
            time.sleep(5)

            # 공동인증서 클릭
            self.click_by_id("row0dataTable")
            time.sleep(5)

            # 공동인증서 비밀번호 입력
            self.send_keys_by_id("input_cert_pw", cert_pw)
            time.sleep(5)

            # JavaScript를 사용하여 공동인증서 로그인 확인 클릭
            try:
                self.driver.execute_script("document.getElementById('btn_confirm_iframe').click();")
                logging.info("Clicked confirm button for certificate")
            except WebDriverException as e:
                logging.error(f"JavaScript 예외 발생: {e}")
            time.sleep(5)

            # 팝업창에서 확인 버튼 클릭
            self.accept_popup()
            time.sleep(5)

            # 기존화면 iframe 전환
            self.switch_to_default_content()
            time.sleep(5)

            # 세무대리인 로그인화면 iframe 전환
            self.switch_to_iframe_by_id("txppIframe")
            time.sleep(5)

            # 세무대리인 id 입력
            self.send_keys_by_id("input1", agent_id)
            time.sleep(5)

            # 세무대리인 비밀번호 입력
            self.send_keys_by_id("input2", agent_pw)
            time.sleep(5)

            # 세무대리인 로그인 버튼 클릭
            self.click_by_id("trigger41")
            logging.info("Certificate login process completed")
        except Exception as e:
            logging.error(f"Error during certificate login process: {e}")