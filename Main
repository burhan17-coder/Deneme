import telebot
import random
import time
import os
from telebot.types import Message

# ────────────────────────────────────────────────
# KONFIGÜRASYON - Render için environment'tan oku
# ────────────────────────────────────────────────

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable eksik! Render'da ekle.")

# Admin ID'ler (şu an /cekilisyap herkes için açık, ama ileride başka komutlar için kullanılabilir)
ADMIN_IDS = [8220540974]  # Senin ID'n + istersen başkaları

KUTSAL_MESAJLAR = [
    "Spektra'nın ışığı yolunu aydınlatsın, havari! 📈✨",
    "Bugün wallet'ını kontrol ettin mi? Spektra izliyor... 👀",
    "Havari olmayanlar dump eder, biz pump bekleriz! 🚀",
    "Spektra buyruğu: FOMO'ya kapılma, HODL'a sarıl! 🙏",
    "Yeni havari kazan, Spektra seni ödüllendirecek! (referral kodu: SPEKTRA123)",
    "Spektra'nın gazabı dumpçulara olsun! 😈",
    "Amin amin, pump pump, Spektra forever! 🔥",
    "Spektra dedi ki: Sabırla bekleyen cenneti bulur… chart’ta yeşil! 🌿",
    "Her düşüş bir imtihandır, havari. Çıkış yakın! 🙌",
]

START_MESSAGE = (
    "Selam {user}! Spektra'nın Havarileri'ne hoş geldin! 🙌\n"
    "Spektra seni seçti, artık havarisisin!\n\n"
    "Komutlar:\n"
    "/havariol       → Havari motivasyonu al\n"
    "/spektra        → Spektra ne diyor?\n"
    "/kutsalmesaj    → Rastgele vahiy gelsin\n"
    "/katil          → Havarilere katıl (fake referral)\n"
    "/katilcekilis   → Çekilişe katıl\n"
    "/cekilislistesi → Kaç kişi var gör\n"
    "/puanlarim      → Katılım puanlarını gör\n"
    "/cekilisyap     → Çekiliş başlat (herkes kullanabilir)\n"
    "/yardim         → Bu mesajı tekrar göster"
)

HAVARI_OL_MESSAGE = (
    "Tebrikler! Artık Spektra'nın resmi havarilerindensin.\n"
    "Görev: Her gün en az 1 kere 'Spektra pump yapsın' diye yazmak. 😇"
)

KATIL_MESSAGE_TEMPLATE = (
    "Havarilere katıldın! Senin davet kodun: {ref_code}\n"
    "Arkadaşlarını davet et, Spektra'nın sevgisini kazan! 😇"
)

VAHIY_ONCESI = "Spektra'dan vahiy geliyor...\n\n"

RANDOM_GAZ_IHTIMALI = 0.06

FAKE_ODULLER = [
    {"tip": "Spektra Token",      "emoji": "💎",  "min": 5000,  "max": 50000,  "suffix": " $SPEKTRA"},
    {"tip": "Pump Puanı",         "emoji": "🚀",  "min": 1000,  "max": 25000,  "suffix": " PP"},
    {"tip": "Havari Unvanı",      "emoji": "👑",  "min": 1,     "max": 1,      "suffix": " - Legendary Havari"},
    {"tip": "Spektra'nın Lütfu",  "emoji": "🙏",  "min": 7777,  "max": 7777,   "suffix": " (kutsal sayı)"},
    {"tip": "Wallet Boost",       "emoji": "📈",  "min": 4200,  "max": 42069,  "suffix": " moonshot puanı"},
    {"tip": "Meme NFT",           "emoji": "🖼️",  "min": 1,     "max": 1,      "suffix": " - Spektra Pepe #1337"},
]

FAKE_TX_PREFIX = "0xSpektraPump"

# ────────────────────────────────────────────────
# IN-MEMORY VERİLER
# ────────────────────────────────────────────────

cekilis_katilimcilar = set()
katilim_puanlari = {}

# ────────────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ────────────────────────────────────────────────

def get_random_kutsal_mesaj():
    return random.choice(KUTSAL_MESAJLAR)

def generate_ref_code():
    return "SPEKTRA" + str(random.randint(100, 9999))

def should_give_random_gaz():
    return random.random() < RANDOM_GAZ_IHTIMALI

def dramatic_pause(seconds=1.2):
    time.sleep(seconds)

def generate_fake_odul():
    odul = random.choice(FAKE_ODULLER)
    miktar = random.randint(odul["min"], odul["max"])
    return {
        "tip": odul["tip"],
        "emoji": odul["emoji"],
        "miktar": miktar,
        "suffix": odul["suffix"],
        "display": f"{odul['emoji']} {miktar:,} {odul['suffix']}"
    }

def generate_fake_tx_hash():
    hex_chars = "0123456789abcdef"
    hash_part = ''.join(random.choice(hex_chars) for _ in range(62))
    return f"{FAKE_TX_PREFIX}{hash_part}"

def add_katilim(user_id):
    cekilis_katilimcilar.add(user_id)
    if user_id not in katilim_puanlari:
        katilim_puanlari[user_id] = 0
    katilim_puanlari[user_id] += random.randint(10, 100)

# ────────────────────────────────────────────────
# BOT
# ────────────────────────────────────────────────

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'selam', 'yardim'])
def cmd_start(message: Message):
    user_name = message.from_user.first_name or "Havari"
    text = START_MESSAGE.format(user=user_name)
    bot.reply_to(message, text)

@bot.message_handler(commands=['havariol'])
def cmd_havari_ol(message: Message):
    bot.reply_to(message, HAVARI_OL_MESSAGE)

@bot.message_handler(commands=['spektra'])
def cmd_spektra(message: Message):
    bot.reply_to(message, get_random_kutsal_mesaj())

@bot.message_handler(commands=['kutsalmesaj'])
def cmd_kutsal_mesaj(message: Message):
    dramatic_pause()
    full_text = VAHIY_ONCESI + get_random_kutsal_mesaj()
    bot.reply_to(message, full_text)

@bot.message_handler(commands=['katil'])
def cmd_katil(message: Message):
    ref_code = generate_ref_code()
    text = KATIL_MESSAGE_TEMPLATE.format(ref_code=ref_code)
    bot.reply_to(message, text)

@bot.message_handler(commands=['katilcekilis'])
def cmd_katil_cekilis(message: Message):
    user_id = message.from_user.id
    if user_id in cekilis_katilimcilar:
        bot.reply_to(message, "Zaten çekilişe katılmışsın kanka! 😏 Sabırla bekle.")
        return
    
    add_katilim(user_id)
    username = message.from_user.username or message.from_user.first_name
    puan = katilim_puanlari.get(user_id, 0)
    
    bot.reply_to(message, f"Hoş geldin havari {username}! Çekilişe katıldın. 🎟️\n"
                          f"Şu an {len(cekilis_katilimcilar)} kişi yarışta.\n"
                          f"Bu katılım için +{puan} katılım puanı kazandın! 🔥")

@bot.message_handler(commands=['cekilislistesi'])
def cmd_cekilis_listesi(message: Message):
    if not cekilis_katilimcilar:
        bot.reply_to(message, "Henüz kimse katılmamış... Hadi havariler, koşun! 🏃‍♂️")
        return
    
    count = len(cekilis_katilimcilar)
    text = f"Çekilişte şu an **{count} havari** var:\n\n"
    text += "(Katılımcılar gizli tutuluyor, adil olsun diye 😈)"
    bot.reply_to(message, text)

@bot.message_handler(commands=['puanlarim'])
def cmd_puanlarim(message: Message):
    user_id = message.from_user.id
    puan = katilim_puanlari.get(user_id, 0)
    bot.reply_to(message, f"Senin Spektra Havari Puanın: **{puan}** PP 🔥\n"
                          "Daha fazla çekilişe katıl, pump'la yüksel!")

@bot.message_handler(commands=['cekilisyap'])
def cmd_cekilis_yap(message: Message):
    # Artık herkes kullanabilir, admin kontrolü kaldırıldı
    
    if len(cekilis_katilimcilar) < 2:
        bot.reply_to(message, "En az 2 havari lazım ki adil olsun kanka... 😭 Katılmak için /katilcekilis yaz!")
        return
    
    kazanan_id = random.choice(list(cekilis_katilimcilar))
    odul = generate_fake_odul()
    tx_hash = generate_fake_tx_hash()
    
    kazanan_mention = f"ID: {kazanan_id}"
    # İstersen username göstermek için ekstra logic ekleyebiliriz ama şimdilik basit
    
    sonuc_mesaji = (
        "Spektra'nın kutsal çekilişi gerçekleşti... 🎉\n"
        "Davullar çalıyor... 🥁🥁🥁\n"
        f"KAZANAN HAVARİ → {kazanan_mention} !!\n\n"
        f"KAZANDIĞI ÖDÜL: {odul['display']}\n"
        f"Transaction Hash (fake): `{tx_hash}`\n\n"
        "Tebrikler! Spektra sana göz kırptı 😉\n"
        "Ödülünü claim etmek için Spektra'ya DM at (fake ego +1000) 😈"
    )
    
    bot.reply_to(message, sonuc_mesaji)
    
    # Herkes başlatabildiği için sıfırlama yapıyoruz (yeni çekiliş başlasın)
    cekilis_katilimcilar.clear()
    bot.reply_to(message, "Çekiliş sıfırlandı. Yeni havariler bekleniyor! 🚀 Yeni çekiliş için /katilcekilis yazın!")

@bot.message_handler(func=lambda m: True)
def catch_all(message: Message):
    if should_give_random_gaz():
        bot.reply_to(message, "Spektra senin mesajını gördü... Pump yaklaşıyor! 🚀")

# ────────────────────────────────────────────────
# BAŞLAT
# ────────────────────────────────────────────────

print("Spektra'nın Havarileri botu çalışıyor...")
print(f"Adminler (gelecek özellikler için): {ADMIN_IDS}")
try:
    bot.infinity_polling(timeout=30, long_polling_timeout=10, allowed_updates=["message"])
except Exception as e:
    print(f"Polling hatası: {e}")
    time.sleep(10)  # Retry delay
