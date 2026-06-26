# Certs Manager
import os
import ssl
import httpx
from datetime import datetime, timezone


BASE_DIR = os.path.dirname(__file__)
CERT_PATH = os.path.join(BASE_DIR, "certs", "russian_chain.pem")


def is_cert_bundle_safe(file_path: str = CERT_PATH) -> bool:
    if not os.path.exists(file_path):
        print(f"[ERROR] Certificate file not found at: {file_path}")
        return False
    try:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(cafile=file_path)
        
        # парсим даты всех сертификатов и находим самую раннюю
        dates = [datetime.strptime(c['notAfter'], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc) 
                 for c in ctx.get_ca_certs() if 'notAfter' in c]
        # print(dates)
        
        days_left = (min(dates) - datetime.now(timezone.utc)).days
        # print(f"left: {days_left}")
        
        if days_left <= 0:
            print(f"[ERROR] SSL certificate has EXPIRED!")
            return False
        elif days_left <= 14:
            print(f"[WARNING] SSL certificate expires in {days_left} days.")
            return False
            
        return True
    except Exception as e:
        print(f"[ERROR] Failed to parse SSL certificates: {e}")
        return False

# print(is_cert_bundle_safe())
# print(BASE_DIR, CERT_PATH)

def download_file(url: str, output_path: str):
    """скачать файл"""
    with httpx.Client(follow_redirects=True) as client:
        with client.stream("GET", url) as response:
            response.raise_for_status() 
            
            # записываем файл чанками (кусочками) 
            with open(output_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)

def get_ssl_context(download: bool, url: str):
    url = "https://raw.githubusercontent.com/kakao-bob/yamaxa/master/src/yamaxa/certs/russian_chain.pem" if url == 'default' else url

    safe = is_cert_bundle_safe()
    if not safe:
        if download:
            print("[*] Downloading certs. Please wait... ", end='')
            download_file(url, CERT_PATH)
            print("ok")
        else:
            print("└  Auto certificate download is disabled right now. Enable it in bot settings, or update <yamaxa> manually.")
        
        print("\n")

    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(cafile=CERT_PATH)
    return ssl_context