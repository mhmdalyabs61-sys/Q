جimport json
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
        self.wfile.write(b"Roblox Beast Sniper is Running!")

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

def generate_beast_usernames(count):
    # حروف علة وصوامت وحروف نادرة لدمج هجين يولد أسامي جديدة كلياً
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u']
    rare_chars = ['q', 'x', 'z', '1', '7', '9']
    
    unique_set = set()
    
    while len(unique_set) < count:
        choice = random.choice([1, 2, 3])
        
        if choice == 1:
            # رباعي هجين (صامت + علة + صامت + حرف نادر)
            uname = random.choice(consonants) + random.choice(vowels) + random.choice(consonants) + random.choice(rare_chars)
        elif choice == 2:
            # خماسي هجين (مقطع صوتي + حرفين عشوائيين نظيفين)
            uname = random.choice(consonants) + random.choice(vowels) + random.choice(consonants) + "".join(random.choices(string.ascii_lowercase, k=2))
        else:
            # رباعي أو خماسي بحروف متسلسلة خفيفة
            length = random.choice([4, 5])
            uname = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
            
        uname = uname.lower().strip()
        
        # شروط النظافة الأساسية لروبلوكس
        if not uname.startswith("_") and not uname.endswith("_") and "__" not in uname:
            if len(uname) in [4, 5]:
                unique_set.add(uname)
                
    return list(unique_set)

send_discord_message("🚀 **تم إطلاق وضع (Beast Sniper المهووس)!** بدأ طحن اليوزرات الحقيقية...")
print("[*] البوت شغال الآن بالطريقة الهجينة الجديدة...")

total_checked = 0

while True:
    batch_usernames = generate_beast_usernames(80) # ضخ 80 يوزر بكل دفعة
    
    with ThreadPoolExecutor(max_workers=15) as executor: # رفع السرعة إلى 15 مسار
        future_to_user = {executor.submit(check_username, user): user for user in batch_usernames}
        
        for future in as_completed(future_to_user):
            total_checked += 1
            user_name, is_available, details = future.result()
            
            size_type = "رباعي 💎" if len(user_name) == 4 else "خماسي 🌟"
            
            print(f"[{total_checked}] ({size_type}) يوزر: {user_name} ➔ الحالة: {details}")
            
            if is_available:
                print(f"🔥 [ صيدة حقيقية نارية! ] ({size_type}) ➔ {user_name}")
                send_discord_message(f"🔥 **صيد أسطوري ومتاح حقيقةً!**\n نوعه: **{size_type}**\n اليوزر: `{user_name}`\n@everyone")

    if total_checked >= 200:
        send_discord_message(f"📊 **تقرير أداء:** تم فحص `{total_checked}` يوزر بنجاح... مستمرين بالبحث ⚡")
        total_checked = 0

    time.sleep(0.5)
