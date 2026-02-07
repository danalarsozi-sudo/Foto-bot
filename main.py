import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Bot Tokeniniz
TOKEN = "8393845023:AAHPWPRAQra_3aE9wh4RDuuXUxFTBnjcUwE"

# Loglama ayarları (Botun durumunu takip etmek için)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start komutu verildiğinde çalışan fonksiyon."""
    await update.message.reply_text(
        "Merhaba! Ben rastgele fotoğraf botu. Fotoğraf almak için 'gonder' yazman yeterli!"
    )

async def send_random_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcı 'gonder' yazdığında iki adet rastgele fotoğraf gönderir."""
    text = update.message.text.lower().strip()
    
    if text == "gonder":
        # Picsum üzerinden her seferinde farklı gelmesi için rastgele bir seed ekliyoruz
        photo_url_1 = f"https://picsum.photos/800/600?sig={random.randint(1, 100000)}"
        photo_url_2 = f"https://picsum.photos/800/600?sig={random.randint(1, 100000)}"
        
        try:
            # İlk fotoğrafı gönder
            await update.message.reply_photo(
                photo=photo_url_1,
                caption="İşte birinci rastgele fotoğraf!"
            )
            # İkinci fotoğrafı gönder
            await update.message.reply_photo(
                photo=photo_url_2,
                caption="İşte ikinci rastgele fotoğraf!"
            )
        except Exception as e:
            logging.error(f"Fotoğraf gönderilirken hata oluştu: {e}")
            await update.message.reply_text("Üzgünüm, şu an fotoğraf getiremiyorum.")

if __name__ == '__main__':
    # Bot uygulamasını oluşturuyoruz
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Komut ve mesaj yakalayıcıları ekliyoruz
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), send_random_photos)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("Bot başlatıldı... Kapatmak için Ctrl+C tuşlarına basın.")
    
    # Botu sürekli çalışacak şekilde (polling) başlatıyoruz
    application.run_polling()
