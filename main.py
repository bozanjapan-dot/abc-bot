import os
import datetime
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

app = Flask(__name__)

ROOT_FOLDER_NAME = os.environ.get("DRIVE_ROOT_FOLDER", "_automation_tmp")
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def get_or_create_folder(service, name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    res = service.files().list(q=q, spaces="drive", fields="files(id,name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        meta["parents"] = [parent_id]
    folder = service.files().create(body=meta, fields="id").execute()
    return folder["id"]

def upload_dummy_pdf(service, filename, parent_id):
    content = b"%PDF-1.4\n% Dummy PDF\n%%EOF"
    media = MediaInMemoryUpload(content, mimetype="application/pdf")
    meta = {"name": filename, "parents": [parent_id]}
    service.files().create(body=meta, media_body=media, fields="id").execute()

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

@app.route("/", methods=["POST"])
def process_order():
    service = get_drive_service()
    today = datetime.date.today()
    ym = today.strftime("%Y-%m")
    client = request.json.get("client", "テスト取引先")

    root_id = get_or_create_folder(service, ROOT_FOLDER_NAME)
    orders_id = get_or_create_folder(service, "Orders", root_id)
    ym_id = get_or_create_folder(service, ym, orders_id)
    client_id = get_or_create_folder(service, client, ym_id)

    upload_dummy_pdf(service, "出荷依頼書.pdf", client_id)
    upload_dummy_pdf(service, "納品書.pdf", client_id)
    upload_dummy_pdf(service, "請求書.pdf", client_id)

    print("完了")
    return jsonify({"status": "完了"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))