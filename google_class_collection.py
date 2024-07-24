import gspread
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from datetime import datetime


class GoogleSheetsHelper:
    def __init__(self, client_id, client_secret, spreadsheet_url, creds_file='creds.data'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.spreadsheet_url = spreadsheet_url
        self.creds_file = creds_file
        self.client = self._authenticate()

    def _authenticate(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive.file'
                 ]
        flow = OAuth2WebServerFlow(self.client_id, self.client_secret, scope, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        storage = Storage(self.creds_file)
        credentials = storage.get()
        if not credentials or credentials.invalid:
            credentials = run_flow(flow, storage)
        client = gspread.authorize(credentials)
        return client

    def upload_to_google_sheets(self, data):
        # 시트 이름 생성 (현재 시각 기준)
        sheet_name = datetime.now().strftime("%y%m%d %H%M")
        spreadsheet = self.client.open_by_url(self.spreadsheet_url)
        sheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")

        # 데이터 업로드
        batch_data = []
        header = []
        for entry in data:
            filtered_entry = {}
            for key, value in entry.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_value:
                            filtered_entry[key] = sub_key
                            break
                    else:
                        filtered_entry[key] = ""
                else:
                    filtered_entry[key] = value

            if not header:
                # 첫 번째 행에 키 추가
                header = list(filtered_entry.keys())
                batch_data.append(header)

            # 데이터 추가
            batch_data.append(list(filtered_entry.values()))

        sheet.update(f'A1:{chr(65 + len(header) - 1)}{len(batch_data)}', batch_data)

        # 시트를 제일 앞에 배치
        worksheets = spreadsheet.worksheets()
        reordered_worksheets = [sheet] + [ws for ws in worksheets if ws.id != sheet.id]
        spreadsheet.reorder_worksheets(reordered_worksheets)

    def _number_to_column(self, n):
        """Convert a number to an Excel-style column name."""
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string

    def upload_dataframe_to_google_sheets(self, dataframe):
        # 시트 이름 생성 (현재 시각 기준)
        sheet_name = datetime.now().strftime("%y%m%d %H%M")
        spreadsheet = self.client.open_by_url(self.spreadsheet_url)
        sheet = spreadsheet.add_worksheet(title=sheet_name, rows=str(len(dataframe) + 1),
                                          cols=str(len(dataframe.columns)))

        # 데이터프레임의 헤더와 데이터를 리스트로 변환
        data = [dataframe.columns.tolist()] + dataframe.values.tolist()

        # 열 인덱스를 계산하여 cell_range 설정
        last_col = self._number_to_column(len(dataframe.columns))
        cell_range = f"A1:{last_col}{len(data) + 1}"

        # 시트에 데이터 업로드
        sheet.update(cell_range, data)

        # 시트를 제일 앞에 배치
        worksheets = spreadsheet.worksheets()
        reordered_worksheets = [sheet] + [ws for ws in worksheets if ws.id != sheet.id]
        spreadsheet.reorder_worksheets(reordered_worksheets)

    def upload_list_to_google_sheets(self, data, header):
        # 시트 이름 생성 (현재 시각 기준)
        sheet_name = datetime.now().strftime("%y%m%d %H%M")
        spreadsheet = self.client.open_by_url(self.spreadsheet_url)
        sheet = spreadsheet.add_worksheet(title=sheet_name, rows=str(len(data) + 1), cols=str(len(header)))

        # 데이터 업로드
        batch_data = [header] + data
        last_col = self._number_to_column(len(header))
        cell_range = f"A1:{last_col}{len(batch_data)}"
        sheet.update(cell_range, batch_data)

        # 시트를 제일 앞에 배치
        worksheets = spreadsheet.worksheets()
        reordered_worksheets = [sheet] + [ws for ws in worksheets if ws.id != sheet.id]
        spreadsheet.reorder_worksheets(reordered_worksheets)
