import urllib.request
import json
import urllib.parse
import random
import string
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. سيرفر ويب وهمي لمنع نوم السيرفر على Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Roblox Debug Sniper is Running!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. إعدادات الفحص
API_URL = "https://auth.roblox.com/v1/usernames/validation"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1561938766317486110/gcHtpPCx0AwOc94a61F9_TAcR8PUxwLr73bWofwswLSTYU4DHj1NkW3LITq11oeVeraH"

def send_discord_message(msg):
    payload = {"content": msg}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5):
            pass
    except Exception:
        pass

def check_username(username):
    params = urllib.parse.urlencode({
        'request.username': username,
        'request.birthday': '2000-01-01'
    })
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            status_code = response.status
            body = response.read().decode()
            data = json.loads(body)
            
            # طباعة الرد الحقيقي عشان نشوف وش تبي روبلوكس
            code_val = data.get('code')
            message_val = data.get('message', '')
            
            if code_val == 0:
                return username, True, f"تاح! (Code: 0)"
            else:
                return username, False, f"مأخوذ/مرفوض (Code: {code_val}, Msg: {message_val})"
                
    except urllib.error.HTTPError as e:
        return username, False, f"خطأ HTTP: {e.code}"
    except Exception as e:
        return username, False, f"خطأ اتصال:ريست/تأخير"

def generate_targeted_usernames(count):
    chars = string.ascii_lowercase + string.digits
    unique_set = set()
    
    while len(unique_set) < count:
        mode = random.choice([1, 2, 3])
        if mode == 1:
            uname = "".join(random.choices(string.ascii_lowercase, k=2)) + "".join(random.choices(string.digits, k=2))
        elif mode == 2:
            uname = "".join(random.choices(string.ascii_lowercase, k=1)) + "".join(random.choices(chars, k=2)) + "_"
        else:
            uname = "".join(random.choices(chars, k=4))
            
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            unique_set.add(uname)
            
    return list(unique_set)

batch_size = 20 # خفضناها مؤقتاً عشان نراقب اللوغز بوضوح
max_threads = 5
total_checked = 0

send_discord_message("🔍 **بدء وضع الفحص التجريبي (Debug Mode)** لكشف استجابات روبلوكس الحقيقية...")
print("[*] بدأ البطء الفاحص للمراقبة...")

while True:
    usernames = generate_targeted_usernames(batch_size)
    
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(check_username, user): user for user in usernames}
        
        for future in as_completed(futures):
            user, is_available, details = future.result()
            total_checked += 1
            
            print(f"[{total_checked}] يوزر: {user} ➔ الرد: {details}")
            
            if is_available:
                print(f"🔥 [ صيدة تاريخية متاحة! ] ➔ {user}")
                send_discord_message(f"🔥 **صيد جديد ومتاح!**\n`{user}`\n@everyone")

    time.sleep(2) # مهلة بسيطة عشان نقدر نقرا اللوغز صح بدون عجلة
