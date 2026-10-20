import urllib.request
import json
import urllib.parse
import random
import string
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. سيرفر ويب وهمي لمنع نوم السيرفر
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
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. إعدادات الفحص والتنبيهات
API_URL = "https://auth.roblox.com/v1/usernames/validation"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1561938766317486110/gcHtpPCx0AwOc94a61F9_TAcR8PUxwLr73bWofwswLSTYU4DHj1NkW3LITq11oeVeraH"

def send_discord_message(msg):
    """إرسال رسالة إلى ديسكورد"""
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

batch_size = 50 
total_checked = 0

# إرسال تنبيه في ديسكورد أول ما يشتغل البوت
send_discord_message("🟢 **تم تشغيل البوت بنجاح!** جاري بدء فحص اليوزرات الرباعية 24/7...")
print("[*] تم تشغيل البوت والسيرفر بنجاح، جاري بدء الصيد...")

while True:
    usernames = generate_unique_usernames(batch_size)
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(check_username, user): user for user in usernames}
        
        for future in as_completed(futures):
            user, is_available = future.result()
            total_checked += 1
            
            if is_available:
                print(f"🔥 [ متاح ومصيد! ] ➔  {user}")
                send_discord_message(f"🔥 **صيد جديد ومتاح!**\n`{user}`\n@everyone")
            else:
                print(f"[-] فحص: {user} (مأخوذ)")

    # إرسال إشعار في ديسكورد كل 2000 يوزر يفحصهم عشان تتأكد إنه شغال
    if total_checked % 2000 == 0:
        send_discord_message(f"⚙️ **تحديث حالة:** البوت شغال وتم فحص `{total_checked}` يوزر حتى الآن وما زال البحث مستمراً...")

    time.sleep(1.5)
