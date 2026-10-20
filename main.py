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
        self.wfile.write(b"Roblox Ultra-Smart Sniper is Running!")

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

def generate_ultra_smart_usernames(count):
    # مقاطع لغوية وتقنية حديثة وقصيرة جداً (تطلع أسامي فخمة ونادرة)
    roots = ["syn", "flux", "xyn", "vyn", "kox", "zex", "nex", "rix", "vex", "zix", "ion", "lux", "nox", "dex", "kyn", "ryn", "nyx", "aux"]
    modifiers = ["ai", "ix", "ox", "ex", "ed", "un", "ov", "az", "uz"]
    
    unique_set = set()
    
    while len(unique_set) < count:
        pattern = random.choice([1, 2, 3, 4, 5])
        
        if pattern == 1:
            # دمج جذور تقنية مع حروف علة ذكية (خماسي فخم)
            uname = random.choice(roots) + random.choice(['y', 'i', 'o', 'x'])
        elif pattern == 2:
            # رباعي بتنسيق صوتي حديث (صامت + علة + صامت + حرف نادر)
            c1 = random.choice(['s', 'v', 'k', 'z', 'm', 'r', 'n', 'f', 't', 'd'])
            v1 = random.choice(['a', 'e', 'i', 'o', 'u'])
            c2 = random.choice(['x', 'q', 'z', 'k', 'v', 'n'])
            end_c = random.choice(string.ascii_lowercase)
            uname = c1 + v1 + c2 + end_c
        elif pattern == 3:
            # ثلاثي فخم مضاف له حرف خفيف بالبداية والنهاية (خماسي)
            uname = random.choice(string.ascii_lowercase) + "".join(random.choices(string.ascii_lowercase, k=3)) + random.choice(string.ascii_lowercase)
        elif pattern == 4:
            # مقطع حديث مع رقم مميز ونظيف
            uname = random.choice(roots)[:3] + random.choice(['1', '7', '9', 'x', 'z'])
        else:
            # دمج مقطعين قصيرين جداً (رباعي أو خماسي)
            uname = random.choice(roots)[:2] + random.choice(modifiers)
            
        uname = uname.lower().strip()
        # شروط نظافة روبلوكس الأساسية
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            if len(uname) in [4, 5]:
                unique_set.add(uname)
                
    return list(unique_set)

send_discord_message("🧠 **تم تفعيل وضع (الذكاء الخارق والصيد المخفي)!** البوت يبحث بطرق لا تتوقعها...")
print("[*] البوت شغال بنظام التوليد الذكي والمتقدم جداً...")

total_checked = 0

while True:
    batch_usernames = generate_ultra_smart_usernames(60)
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_user = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(future_to_user):
            total_checked += 1
            user_name, is_available, details = future.result()
            
            size_type = "رباعي 💎" if len(user_name) == 4 else "خماسي 🌟"
            
            print(f"[{total_checked}] ({size_type}) يوزر: {user_name} ➔ الحالة: {details}")
            
            if is_available:
                print(f"🔥 [ صيدة تاريخية ونظيفة! ] ({size_type}) ➔ {user_name}")
                send_discord_message(f"🔥 **صيد أسطوري ومتاح حقيقةً!**\n نوعه: **{size_type}**\n اليوزر: `{user_name}`\n@everyone")

    if total_checked >= 180:
        send_discord_message(f"📊 **تقرير ذكي:** تم فحص `{total_checked}` يوزر بنجاح... البوت مستمر بالبحث 🚀")
        total_checked = 0

    time.sleep(0.8)
