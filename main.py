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

# 2. إعدادات الفحص
API_URL = "https://users.roblox.com/v1/usernames/users"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1562019919128698990/doPV-DBGiDRIsIq-e-y7hrRH8sgpwr58nN4USQJ8254JW5HuNHngz8AwCke-FgptzNjg"

def send_discord_message(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception:
        pass

def check_username(username):
    payload = {
        "usernames": [username],
        "excludeBannedUsers": True
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            users_list = data.get('data', [])
            
            # إذا القائمة فاضية، يعني مبدئياً مو مسجل بحساب عادي
            if len(users_list) == 0:
                # فحص إضافي للتأكد أن اليوزر مو محظور أو مرفوض من النظام (تحسباً للردود الوهمية)
                check_url = f"https://auth.roblox.com/v1/usernames/validation?request.username={username}&request.birthday=2000-01-01"
                val_res = requests.get(check_url, headers=headers, timeout=5)
                if val_res.status_code == 200:
                    val_data = val_res.json()
                    # الرمز 0 يعني اليوزر صالح ومتاح 100% وغير مخالف
                    if val_data.get("code") == 0:
                        return username, True, "متاح حقيقي ونظيف! 🔥"
                
                return username, False, "مخالف أو محجوز (وهمي)"
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

send_discord_message("🟢 **تم تحديث البوت وإضافة فحص التحقق الدقيق!** تم إلغاء الصيدات الوهمية...")
print("[*] البوت شغال بالفحص الحقيقي...")

total_checked = 0

while True:
    batch_usernames = generate_smart_usernames(20)
    
    for user in batch_usernames:
        user_name, is_available, details = check_username(user)
        total_checked += 1
        print(f"[{total_checked}] يوزر: {user_name} ➔ الحالة: {details}")
        
        if is_available:
            print(f"🔥 [ صيدة حقيقية ونظيفة متاحة! ] ➔ {user_name}")
            send_discord_message(f"🔥 **صيد جديد ومتاح رسمياً!**\n`{user_name}`\n@everyone")
        
        # زيادة الفاصل الزمني شوي عشان نتجنب الحظر (Rate Limit) ويعطي نتائج دقيقة
        time.sleep(1.0)

    if total_checked >= 100:
        send_discord_message(f"📊 **تقرير دوري:** تم فحص `{total_checked}` يوزر بدقة... البوت شغال 🔄")
        total_checked = 0

    time.sleep(2)
