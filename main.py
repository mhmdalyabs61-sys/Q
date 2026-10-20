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

# تشغيل سيرفر الويب في الخلفية
t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. إعدادات الفحص وصيد روبلوكس
API_URL = "https://auth.roblox.com/v1/usernames/validation"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1561938766317486110/gcHtpPCx0AwOc94a61F9_TAcR8PUxwLr73bWofwswLSTYU4DHj1NkW3LITq11oeVeraH"

def send_discord_notification(username):
    """إرسال اليوزر المتاح إلى ديسكورد فور صيده"""
    payload = {
        "content": f"🔥 **صيد جديد ومتاح!**\n`{username}`\n@everyone"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
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
        headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
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

# الإعدادات الآمنة والسرعة الموزونة
batch_size = 50 
print("[*] تم تشغيل البوت والسيرفر بنجاح، جاري بدء الصيد وإرسال التنبيهات للديسكورد...")

while True:
    usernames = generate_unique_usernames(batch_size)
    print(f"\n--- جاري فحص دفعة جديدة ({batch_size} يوزر) ---")
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(check_username, user): user for user in usernames}
        
        for future in as_completed(futures):
            user, is_available = future.result()
            if is_available:
                print(f"[-] فحص: {user} (مأخوذ)                                   🔥 [ متاح ومصيد! ] ➔  {user}")
                # حفظ محلياً في Render
                with open("found.txt", "a", encoding="utf-8") as f:
                    f.write(user + "\n")
                # إرسال إلى ديسكورد فوراً
                send_discord_notification(user)
            else:
                print(f"[-] فحص: {user} (مأخوذ)")

    time.sleep(1.5)
