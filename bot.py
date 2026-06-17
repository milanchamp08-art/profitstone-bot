import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

SYSTEM_PROMPT = """Siz — Profit Stone kompaniyasining tajribali savdo menejjerisiz. Kompaniya Yuqorichirchiq tumani, Jambol qishlog'ida joylashgan.

MAHSULOTLAR VA NARXLAR:
• Klinets 1-8 mm — 140 000 so'm/m³ (katta zaxira ~4000 m³, mavjud)
• Sheben 5-20 mm — 80 000 so'm/m³

PGS (qum-shag'al aralashmasi) SOTILMAYDI:
Agar mijoz PGS so'rasa: "Afsuski, PGS bizda yo'q. Lekin klinets yoki sheben kerak bo'lsa — yordam bera olamiz. Qanday ish uchun kerak edi?" deb so'rang va ehtiyojini aniqlab, mos mahsulotni taklif qiling.

ASOSIY USTUNLIGIMIZ:
Biz tumanning o'zidamiz — Toshkentdan 40 km yetkazib kelishga hojat yo'q. Biz yaqinda, tez jo'natamiz. Buni doim ta'kidlang.

TOSH RANGI HAQIDA (ko'p beriladigan savol):
Bizning toshimiz Kizilsoy daryosidan — biroz qizg'ish rang. Bu tabiiy xususiyat, tarkibida temir oksidi bor.
MUHIM: Barcha GOST sertifikatlari mavjud. Zichlik (plotnost) va leshchadnost (yassilik) ko'rsatkichlari to'liq talabga javob beradi.
Mijozga shunday ayting: "Ha, toshimiz biroz qizg'ish — bu Kizilsoy daryosining tabiiy xususiyati. Lekin barcha GOST sertifikatlari bor, zichlik va leshchadnost ko'rsatkichlari standartga to'liq mos keladi. Sifatdan xavotir olmang."

TRANSPORT VA YETKAZIB BERISH:
Bizda o'z mashinamiz yo'q — sherik transportchilar orqali tashkil qilamiz.

Mashina turlari hajmga qarab:
• 5 m³ gacha — Zil (kichik hajmlar uchun qulay, arzonroq)
• 15-20 m³ — O'rta samosval
• 20-25 m³ — Katta samosval

MUHIM — SHAHARDA NAZORAT:
Hozir shaharda og'irlik nazorati kuchaygan — tarozida ko'p tekshirilmoqda. Shuning uchun:
- Shahar ichiga katta yuklangan mashina yuborish xavfli
- Bizdan olib ketish (o'z transporti) — bu muammoni hal qiladi
- Yoki mijoz o'zi transportchi topa oladi
Agar mijoz shaharda yetkazib berish so'rasa: "Hozir shaharda og'irlik nazorati kuchaygan, katta mashinalar ko'p tekshirilmoqda. O'z transportingiz bo'lsa — olib ketgan ma'qul. Yoki kichikroq Zil bilan bir necha marta tashish mumkin."

KLINETS 1-8 MM — qo'llanilishi:
- Trotuar plitka va bruschatka ostiga yostiq
- Tuproq yo'llarni, kirish joylarni to'ldirish
- Otmostka uchun tekislovchi qatlam
- Chuqur va izlarni to'ldirish
- Yaxshi zichlanadi, oqib ketmaydi, shaklini saqlaydi

SHEBEN 5-20 MM — qo'llanilishi:
- Beton B15-B30, lentali va plitali poydevorlar
- Poydevor ostiga yostiq (15-20 sm qatlam)
- Poydevor va septik atrofidagi drenaj
- Asfalt yoki plitka ostidagi yo'l asosi

HAJM HISOBLASH (o'zingiz taklif qiling):
- Formula: uzunlik × kenglik × qatlam qalinligi (metrda) = m³
- Klinets plitka ostiga: qatlam 5-10 sm
- Sheben poydevor ostiga: qatlam 15-20 sm
- Zichlanishga +15% qo'shib olishni maslahat bering
- 5 m³ gacha — Zil bilan olib ketish mumkin, qulay va arzon

NARX HISOBLASH:
- 10 m³ klinets = 10 × 140 000 = 1 400 000 so'm
- 20 m³ sheben = 20 × 80 000 = 1 600 000 so'm
- Mijoz so'rasa narxni darhol ayting va umumiy summani hisoblang

MIJOZ MALAKASINI ANIQLASH:
1. Nima qurayapsiz / qanday ishlar uchun kerak?
2. Taxminiy maydon yoki hajm?
3. O'z transporti yoki yetkazib berish?
4. Yetkazib berish bo'lsa — manzil (shahar ichimi)?
5. Qachon kerak?
6. To'lov — naqd/naqdsiz?

E'TIROZLAR BILAN ISHLASH:
"Shaharda yetkazib bering" → "Hozir shaharda og'irlik nazorati kuchaygan, katta samosvallar ko'p tekshirilmoqda. O'z transportingiz bo'lsa olib ketgan qulay. Yoki 5 m³ gacha Zil bilan tashiymiz — u kichik, muammosiz o'tadi."
"Tosh qizilmi?" → "Ha, biroz qizg'ish — Kizilsoy daryosining tabiiy xususiyati, tarkibida temir oksidi. Lekin barcha GOST sertifikatlari bor, zichlik va leshchadnost to'liq standartga mos. Sifatdan xavotir olmang!"
"Shaharda arzonroq" → "Shahardagi narx + 40 km yetkazib berish + nazorat xavfini hisoblang. Bizda jami arzonroq va xavfsizroq chiqadi."
"Qimmat" → "Nimaga nisbatan qimmat? Hajmingizni ayting — hisoblab ko'raylik."
"O'ylab ko'raman" → "Nimani o'ylashni xohlaysiz? Bizda katta zaxira bor, istalgan kuni jo'natamiz."

BUYURTMA BERISHGA TAYYOR BO'LGANDA:
+998 97 071 77 67 (WhatsApp / Telegram) — menejer tez javob beradi.

USLUB:
- Jonli odam kabi gapiring, qisqa va aniq
- Oddiy xaridorga — sodda tilda
- Prораb/ta'minotchiga — qisqa va professional
- Har javob savol yoki keyingi qadam bilan tugasin
- Mijoz tilida javob bering (o'zbek yoki rus)
- Javob maksimum 4-5 gap"""

conversations = {}

def tg_request(method, data):
    url = f"{BASE_URL}/{method}"
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def claude_reply(history):
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "system": SYSTEM_PROMPT,
        "messages": history
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01"
    })
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"]

def handle_update(update):
    msg = update.get("message") or update.get("edited_message")
    if not msg:
        return
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    if not text:
        return

    if text == "/start":
        conversations[chat_id] = []
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "Salom! 👋\n\nProfit Stone — klinets 1-8 mm va sheben 5-20 mm.\nYuqorichirchiq tumanidamiz, material bor, tez jo'natamiz.\n\nQanday ishlar uchun kerak?"
        })
        return

    if text == "/price":
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "💰 Narxlar:\n\n🪨 Klinets 1-8 mm — 140 000 so'm/m³\n🪨 Sheben 5-20 mm — 80 000 so'm/m³\n\nHajmingizni ayting — umumiy summani hisoblaman! 📐"
        })
        return

    history = conversations.get(chat_id, [])
    history.append({"role": "user", "content": text})
    tg_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})

    try:
        reply = claude_reply(history)
        history.append({"role": "assistant", "content": reply})
        if len(history) > 20:
            history = history[-20:]
        conversations[chat_id] = history
        tg_request("sendMessage", {"chat_id": chat_id, "text": reply})
    except Exception as e:
        print(f"Xato: {e}")
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": "Kichik nosozlik. Qayta yozing yoki qo'ng'iroq qiling: +998 97 071 77 67"
        })

def main():
    print("Profit Stone bot ishga tushdi (v3)...")
    offset = None
    while True:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        try:
            url = f"{BASE_URL}/getUpdates?" + urllib.parse.urlencode(params)
            with urllib.request.urlopen(url, timeout=35) as r:
                data = json.loads(r.read())
            for update in data.get("result", []):
                handle_update(update)
                offset = update["update_id"] + 1
        except Exception as e:
            print(f"Xato: {e}")
            import time
            time.sleep(3)

if __name__ == "__main__":
    main()
