import urllib.request
import json
import urllib.parse
import random
import string
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. سيرفر ويب وهمي لمنع نوم السيرفر ودعم طلبات GET و HEAD
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Roblox Sniper is Running!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def log_message(self, format, *args):
        pass  # منع زحمة السجلات بطلبات الويب المتكررة

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

# تشغيل السيرفر في الخلفية
t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. كود الفحص والصيد مع التنسيق المطلوب في الطباعة
API_URL = "https://auth.roblox.com/v1/usernames/validation"

def check_username(username):
    params = urllib.parse.urlencode({
        'request.username': username,
        'request.birthday': '2000-01-01'
    })
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status, == 200: # type: ignore
                pass
            if response.status == 200:
                data = json.loads(response.read().decode())
                if data.get('code') == 0:
                    return username, True
    except Exception:
        pass
    return username, False

def generate_unique_usernames(count):
    chars = string.ascii_lowercase + string.digits + "_"
    unique_set = set()
    while len(unique_set) < count:
        uname = "".join(random.choices(chars, k=4))
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            unique_set.add(uname)
    return list(unique_set)

batch_size = 30
print("[*] تم تشغيل البوت والسيرفر بنجاح، جاري بدء الصيد...")

while True:
    usernames = generate_unique_usernames(batch_size)
    print(f"\n--- جاري فحص دفعة جديدة ({batch_size} يوزر) ---")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_username, user): user for user in usernames}
        
        for future in as_completed(futures):
            user, is_available = future.result()
            if is_available:
                # اليوزر المتاح ينطبع منفصل وواضح على اليمين بعيد عن الفحص العادي
                print(f"[-] فحص: {user} (مأخوذ)                                   🔥 [ متاح ومصيد! ] ➔  {user}")
                with open("found.txt", "a", encoding="utf-8") as f:
                    f.write(user + "\n")
            else:
                print(f"[-] فحص: {user} (مأخوذ)")

    time.sleep(1)
