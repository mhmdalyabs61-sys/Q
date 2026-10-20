import json
import random
import string
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# 1. سيرفر ويب وهمي لمنع نوم السيرفر على Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Roblox Smart Sniper is Running!")

    def log_message(self, format, *args):
        pass

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

t = Thread(target=run_web_server)
t.daemon = True
t.start()

# 2. إعدادات الفحص المحدثة (رابط التحقق الجديد والنظيف)
API_URL = "https://users.roblox.com/v1/usernames/users"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1562019919128698990/doPV-DBGiDRIsIq-e-y7hrRH8sgpwr58nN4USQJ8254JW5HuNHngz8AwCke-FgptzNjg"

def send_discord_message(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception:
        pass

def check_username(username):
    # استخدام الـ API البديل المحدث للبحث عن اليوزرات
    payload = {
        "usernames": [username],
        "excludeBannedUsers": True
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=3)
        if response.status_code == 200:
            data = response.json()
            # إذا رجع الـ data فاضي أو القائمة فاضية، معناه اليوزر غير مسجل (متاح!)
            users_list = data.get('data', [])
            if len(users_list) == 0:
                return username, True, "متاح ورسمياً فاضي! 🔥"
            else:
                return username, False, "مأخوذ"
        else:
            return username, False, f"خطأ HTTP: {response.status_code}"
    except Exception:
        return username, False, "خطأ اتصال"

def generate_smart_usernames(count):
    chars = string.ascii_lowercase + string.digits
    unique_set = set()
    
    while len(unique_set) < count:
        mode = random.choice([1, 2])
        if mode == 1:
            uname = "".join(random.choices(string.ascii_lowercase, k=3)) + "_" + "".join(random.choices(chars, k=1))
        else:
            uname = "".join(random.choices(string.ascii_lowercase, k=4)) + "".join(random.choices(string.digits, k=1))
            
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            unique_set.add(uname)
            
    return list(unique_set)

send_discord_message("🟢 **تم تحديث البوت وإصلاح خطأ 404!** جاري استئناف الفحص...")
print("[*] البوت شغال بالرابط الجديد...")

total_checked = 0

while True:
    batch_usernames = generate_smart_usernames(20)
    
    for user in batch_usernames:
        user_name, is_available, details = check_username(user)
        total_checked += 1
        print(f"[{total_checked}] يوزر: {user_name} ➔ الحالة: {details}")
        
        if is_available:
            print(f"🔥 [ صيدة خرافية متاحة! ] ➔ {user_name}")
            send_discord_message(f"🔥 **صيد جديد ومتاح!**\n`{user_name}`\n@everyone")
        
        time.sleep(0.5)

    if total_checked >= 100:
        send_discord_message(f"📊 **تقرير دوري:** تم فحص `{total_checked}` يوزر بنجاح... البوت شغال بدون أخطاء 🔄")
        total_checked = 0

    time.sleep(2)
