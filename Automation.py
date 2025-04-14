import gspread 
from google.oauth2.service_account import Credentials 
from datetime import datetime
# 建立 Google Sheets 連接
def setup_google_sheet(creds_file="credentials.json", sheet_id="1C9r6sqoK5Vr0GmzrLGGmB-rSIkuW729TcFdNhYDd0Vs", sheet_name="Model Test"):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    client = gspread.authorize(creds)

    workbook = client.open_by_key(sheet_id)

    try:
        sheet = workbook.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet = workbook.add_worksheet(title=sheet_name, rows="1000", cols="10")

    # Set headers if empty
    if not sheet.get_all_values() or not any(sheet.get_all_values()[0]):
        headers = ['Date', 'Model Name', 'System Prompt', 'User Prompt', 'Model Response', 'Character Emotion', 'Test Notes']
        sheet.append_row(headers)

    return sheet

# 記錄測試資料到 Google Sheets
def record_test(sheet, data):
    try:
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data['model_name'],
            data['system_prompt'],
            data['user_prompt'],
            data['model_response'],
            data['emotion'],
            data['test_notes']
        ])
        return True
    except Exception as e:
        print(f"Error recording test data: {e}")
        return False
