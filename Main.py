import telebot
import random
import time
import os
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN eksik!")

bot = telebot.TeleBot(BOT_TOKEN)

# ── Global durumlar ──
cekilis_aktif = False
cekilis_katilimcilar = set()
cekilis_kazanan_sayisi = 1  # varsayılan 1 kazanan
cekilis_baslatan_msg_id = None
cekilis_son_mesaj_zamani = None

gunluk_sozler = [
    "Sabır, en güçlü stratejidir.",
    "Piyasa düşer, kalkar; sen kalkmayı bil.",
    "Risk almadan ödül olmaz.",
    "Duygularla değil, planla hareket et.",
    "Zaman her şeyin ilacıdır – ve en büyük getirisi.",
    "Korku satar, açgözlülük alır.",
    "En iyi yatırım bilgidir.",
    "Düşüşler fırsat, yükselişler testtir."
]
gunluk_soz_index = 0

son_oto_mesaj = datetime.now() - timedelta(hours=4)  # ilk başta hemen göndermesin

# ── Yardımcı fonksiyonlar ──
def guncel_katilim_butonu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Katıl", callback_data="cekilis_katil"))
    return markup

def gunun_sozu():
    global gunluk_soz_index
    soz = gunluk_sozler[gunluk_soz_index]
    gunluk_soz_index = (gunluk_soz_index + 1) % len(gunluk_sozler)
    return soz

# ── Komutlar ──

@bot.message_handler(commands=['start', 'yardim'])
def cmd_start(message):
    bot.reply_to(message,
        "Merhaba! Komutlar:\n"
        "/çekiliş → Yeni çekiliş başlat\n"
        "/. → Aktif çekilişi bitir\n"
        "/sayı <rakam> → Kaç kişi kazanacak (örn: /sayı 3)\n"
        "/selam, /naber → Ufak sohbet\n"
        "/spektra → Küfür mod :D\n"
        "/gününsözü → Günün sözü\n"
        "Çekilişe katılmak için butona basman yeterli.")

@bot.message_handler(commands=['çekiliş'])
def cmd_cekilis_baslat(message):
    global cekilis_aktif, cekilis_katilimcilar, cekilis_baslatan_msg_id, cekilis_son_mesaj_zamani

    if cekilis_aktif:
        bot.reply_to(message, "Zaten aktif bir çekiliş var! Bitirmek için /. yaz.")
        return

    cekilis_aktif = True
    cekilis_katilimcilar.clear()
    cekilis_baslatan_msg_id = message.message_id

    text = f"🎉 Çekiliş başladı!\nKazanan sayısı: {cekilis_kazanan_sayisi}\nKatılmak için aşağıdaki butona bas."
    msg = bot.send_message(message.chat.id, text, reply_markup=guncel_katilim_butonu())
    cekilis_son_mesaj_zamani = datetime.now()

@bot.message_handler(commands=['.'])
def cmd_cekilis_bitir(message):
    global cekilis_aktif

    if not cekilis_aktif:
        bot.reply_to(message, "Aktif çekiliş yok.")
        return

    if not cekilis_katilimcilar:
        bot.reply_to(message, "Kimse katılmadı ki...")
        cekilis_aktif = False
        return

    kazananlar = random.sample(list(cekilis_katilimcilar), min(cekilis_kazanan_sayisi, len(cekilis_katilimcilar)))
    kazanan_text = "\n".join([f"@{bot.get_chat_member(message.chat.id, uid).user.username or 'ID:'+str(uid)}" for uid in kazananlar])

    bot.send_message(message.chat.id,
        f"🎉 Çekiliş sona erdi!\n"
        f"Kazanan(lar):\n{kazanan_text}\n"
        f"Tebrikler! Ödül detayları yakında...")

    cekilis_aktif = False
    cekilis_katilimcilar.clear()

@bot.message_handler(commands=['sayı'])
def cmd_sayi(message):
    global cekilis_kazanan_sayisi

    try:
        sayi = int(message.text.split()[1])
        if sayi < 1 or sayi > 20:
            bot.reply_to(message, "1-20 arası bir sayı yaz.")
            return
        cekilis_kazanan_sayisi = sayi
        bot.reply_to(message, f"Çekilişte {sayi} kişi kazanacak.")
    except:
        bot.reply_to(message, "Örnek: /sayı 3")

@bot.callback_query_handler(func=lambda call: call.data == "cekilis_katil")
def callback_katil(call):
    global cekilis_katilimcilar, cekilis_son_mesaj_zamani

    if not cekilis_aktif:
        bot.answer_callback_query(call.id, "Çekiliş bitti.", show_alert=True)
        return

    uid = call.from_user.id
    if uid in cekilis_katilimcilar:
        bot.answer_callback_query(call.id, "Zaten katılmışsın!")
        return

    cekilis_katilimcilar.add(uid)
    bot.answer_callback_query(call.id, "Katıldın! Bol şans.")

    # Mesajı güncelle (kişi sayısı artsın)
    count = len(cekilis_katilimcilar)
    yeni_text = f"🎉 Çekiliş devam ediyor!\nKatılımcı: {count}\nKazanan sayısı: {cekilis_kazanan_sayisi}\nKatılmak için butona bas."
    bot.edit_message_text(yeni_text, call.message.chat.id, call.message.message_id, reply_markup=guncel_katilim_butonu())

    cekilis_son_mesaj_zamani = datetime.now()

@bot.message_handler(commands=['selam'])
def cmd_selam(message):
    cevaplar = ["Selam kral!", "N'aber lan?", "Hoş geldin aslan parçası", "Selamün aleyküm"]
    bot.reply_to(message, random.choice(cevaplar))

@bot.message_handler(commands=['naber'])
def cmd_naber(message):
    cevaplar = ["İyi valla, sen naber?", "Sıkıntı yok, pump bekliyoruz", "Nasılsın lan?", "Burdayım kanka 🔥"]
    bot.reply_to(message, random.choice(cevaplar))

@bot.message_handler(commands=['spektra'])
def cmd_spektra(message):
    kufurler = [
        "Amına koyayım piyasanın, yine mi düştü?",
        "Sikeyim böyle işi ya, herkes satıyor",
        "Bu ne lan, dump mu bu?",
        "Ananı satmış gibi satıyorlar valla",
        "Bok gibi piyasa, hepiniz bok yiyin"
    ]
    bot.reply_to(message, random.choice(kufurler))

@bot.message_handler(commands=['gününsözü'])
def cmd_gununsözü(message):
    bot.reply_to(message, f"📜 Günün sözü:\n{gunun_sozu()}")

# Otomatik 3 saatte 1 mesaj (sadece grupta)
@bot.message_handler(func=lambda m: True)
def oto_mesaj(message):
    global son_oto_mesaj
    if message.chat.type in ['group', 'supergroup']:
        now = datetime.now()
        if now - son_oto_mesaj > timedelta(hours=3):
            bot.send_message(message.chat.id, "Haydi nerdesiniz lan, ekran açan yok mu? 🚀")
            son_oto_mesaj = now

print("Bot çalışıyor...")
bot.infinity_polling(timeout=20, long_polling_timeout=10)
