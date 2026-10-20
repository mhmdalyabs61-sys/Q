import json
import random
import string
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# 1. سيرفر ويب وهمي لمنع نوم السيرفر على Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Roblox Fast Sniper is Running!")

    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. إعدادات الديسكورد
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1562019919128698990/doPV-DBGiDRIsIq-e-y7hrRH8sgpwr58nN4USQJ8254JW5HuNHngz8AwCke-FgptzNjg"

def send_discord_message(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception:
        pass

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validation?request.username={username}&request.birthday=2000-01-01"
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                return username, True, "متاح حقيقي 100% 🔥"
            else:
                return username, False, "مأخوذ أو محجوز"
        else:
            return username, False, f"خطأ HTTP: {response.status_code}"
    except Exception:
        return username, False, "خطأ اتصال"

def generate_smart_usernames(count):
    chars = string.ascii_lowercase + string.digits
    unique_set = set()
    
    while len(unique_set) < count:
        mode = random.choice([1, 2, 3, 4])
        
        if mode == 1:
            uname = "".join(random.choices(string.ascii_lowercase, k=4))
        elif mode == 2:
            uname = "".join(random.choices(string.ascii_lowercase, k=3)) + "".join(random.choices(string.digits, k=1))
        elif mode == 3:
            uname = "".join(random.choices(string.ascii_lowercase, k=4)) + "".join(random.choices(string.digits, k=1))
        else:
            uname = "".join(random.choices(string.ascii_lowercase, k=3)) + "_" + "".join(random.choices(chars, k=1))
            
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            unique_set.add(uname)
            
    return list(unique_set)

send_discord_message("⚡ **تم تشغيل وضع السرعة العالية (Multithreading)!** البوت يطير الآن...")
print("[*] البوت شغال بالسرعة القصوى والمضمونة...")

total_checked = 0

while True:
    # نولد دفعة أسرع وأكبر (مثلاً 50 يوزر دفعة وحدة)
    batch_usernames = generate_smart_usernames(50)
    
    # استخدام ThreadPoolExecutor لفحص 10 يوزرات بنفس الثانية
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(future_to_user):
            total_checked += 1
            user_name, is_available, details = future.result()
            print(f"[{total_checked}] يوزر: {user_name} ➔ الحالة: {details}")
            
            if is_available:
                print(f"🔥 [ صيدة حقيقية ونظيفة! ] ➔ {user_name}")
                send_discord_message(f"🔥 **صيد جديد ومتاح حقيقةً!**\n`{user_name}`\n@everyone")

    if total_checked >= 150:
        send_discord_message(f"📊 **تقرير دوري:** تم فحص `{total_checked}` يوزر بسرعة عالية... البوت شغال 🚀")
        total_checked = 0

    # راحة بسيطة جداً بين الدفعات عشان ما يلقطنا السيرفر
    time.sleep(1)
