# it_bot.py
import asyncio
import logging
from datetime import datetime
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import aiohttp
import os
from dotenv import load_dotenv

# Sozlamalar
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')  # Bot token
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Kanal ID (masalan: @it_dasturlash)

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


class ITContentGenerator:
    """IT va dasturlashga oid kontent generatori"""

    def __init__(self):
        self.programming_languages = [
            "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby",
            "Swift", "Kotlin", "Go", "Rust", "TypeScript", "Dart", "SQL"
        ]

        self.topics = [
            "Sun'iy intellekt", "Machine Learning", "Data Science", "Veb dasturlash",
            "Mobil dasturlash", "Kiberxavfsizlik", "Bulutli texnologiyalar",
            "Blockchain", "DevOps", "Ma'lumotlar bazasi", "API", "Microservices",
            "Testlash", "Git va GitHub", "Algoritmlar", "Ma'lumotlar tuzilmasi"
        ]

        self.fun_facts = [
            "Birinchi kompyuter dasturchisi ayol edi: Ada Lovelace (1840)",
            "Python dasturlash tili Monty Python guruhidan ilhomlangan",
            "JavaScript 10 kunda yaratilgan!",
            "Git dastlab Linux yadrosi uchun yaratilgan",
            "Stack Overflow'da eng ko'p so'raladigan til JavaScript",
            "Java dastlab interaktiv televidenie uchun yaratilgan",
            "Google dastlab 'Backrub' deb nomlangan",
            "Birinchi kompyuter virusi 1983 yilda yaratilgan",
            "HTML emoji-larni qo'llab-quvvatlaydi: 😊",
            "GitHub dunyodagi eng katta kod ombori"
        ]

        self.tips = [
            "Har kuni kamida 30 daqiqa kod yozing",
            "Git dan muntazam foydalaning",
            "Stack Overflow dan foydalanishdan qo'rqmang",
            "Kod o'qish - kod yozish kabi muhim",
            "Yangi texnologiyalarni o'rganishda davom eting",
            "Open Source loyihalarda qatnashing",
            "IT community ga qo'shiling",
            "Ingliz tilini o'rganing - bu juda muhim",
            "Algoritmlarni mukammal o'rganing",
            "Yaxshi dokumentatsiya yozishni o'rganing"
        ]

        # API orqali rasmlar olish uchun
        self.image_apis = {
            'code': 'https://source.unsplash.com/featured/?programming,coding',
            'tech': 'https://source.unsplash.com/featured/?technology,computer',
            'developer': 'https://source.unsplash.com/featured/?developer,workspace'
        }

    async def get_random_image(self):
        """Tasodifiy ITga oid rasm olish"""
        image_type = random.choice(list(self.image_apis.keys()))
        url = self.image_apis[image_type]

        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True) as response:
                if response.status == 200:
                    return response.url
        return None

    def get_daily_quote(self):
        """Dasturlash haqida iqtibos"""
        quotes = [
            "Yaxshi kod - bu o'z-o'zidan dokumentatsiya - *Unknown*",
            "Har qandaxona ahmoq kompyuter tushunadigan kod yozishi mumkin. Yaxshi dasturchilar esa odamlar tushunadigan kod yozadi - *Martin Fowler*",
            "Birinchi marta ishlaydigan kodingizni ko'rishdek zavq yo'q - *Unknown*",
            "Dasturlash - bu san'at - *Unknown*",
            "Talk is cheap. Show me the code - *Linus Torvalds*",
            "Code is like humor. When you have to explain it, it's bad - *Cory House*"
        ]
        return random.choice(quotes)

    def get_programming_joke(self):
        """Dasturlash haqida hazil"""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "There are only 10 types of people in the world: those who understand binary and those who don't",
            "SQL injection into my life, I get 'complete' error",
            "I would tell you a UDP joke, but you might not get it",
            "Why do Java developers wear glasses? Because they can't C#",
            "A QA engineer walks into a bar. Runs into a bar. Crawls into a bar. Dances into a bar...",
            "['hip', 'hip'] (hip hip array!)"
        ]
        return random.choice(jokes)

    def get_today_in_history(self):
        """IT tarixida bugun"""
        today = datetime.now()
        month = today.month
        day = today.day

        events = {
            (2, 15): "1946 - ENIAC kompyuteri taqdim etildi",
            (3, 2): "1983 - Compact Disc (CD) taqdim etildi",
            (4, 4): "1975 - Microsoft kompaniyasi tashkil etildi",
            (5, 15): "1990 - WorldWideWeb (WWW) taqdim etildi",
            (6, 5): "2007 - iPhone birinchi marta sotuvga chiqdi",
            (9, 4): "1998 - Google kompaniyasi tashkil etildi",
            (10, 1): "1982 - Sony birinchi CD player chiqardi",
            (11, 10): "1983 - Microsoft Windows taqdim etildi",
            (12, 17): "1903 - Wright brothers birinchi parvoz"
        }

        return events.get((month, day), f"{day}.{month} - IT tarixida oddiy kun")

    async def generate_post(self, post_type=None):
        """Post yaratish"""
        if not post_type:
            post_type = random.choice(['fact', 'tip', 'language', 'topic', 'joke', 'quote'])

        image_url = await self.get_random_image()

        if post_type == 'fact':
            content = f"📊 *IT Fact*\n\n{random.choice(self.fun_facts)}"
        elif post_type == 'tip':
            content = f"💡 *Dasturchi Maslahati*\n\n{random.choice(self.tips)}"
        elif post_type == 'language':
            lang = random.choice(self.programming_languages)
            content = f"🔷 *{lang} dasturlash tili*\n\n{self.get_language_info(lang)}"
        elif post_type == 'topic':
            topic = random.choice(self.topics)
            content = f"🔬 *{topic}*\n\n{self.get_topic_info(topic)}"
        elif post_type == 'joke':
            content = f"😄 *Dasturchi Hazili*\n\n{self.get_programming_joke()}"
        else:  # quote
            content = f"📝 *Dasturchi Iqtibosi*\n\n{self.get_daily_quote()}"

        # Hashteglar qo'shish
        hashtags = "\n\n#IT #Dasturlash #Programmer #Coding #Developer #Tech #Uzbekistan"

        return {
            'text': content + hashtags,
            'image': image_url
        }

    def get_language_info(self, language):
        """Dasturlash tili haqida ma'lumot"""
        info = {
            "Python": "• Oson o'rganiladi\n• Data Science va AI uchun eng yaxshi\n• Django, Flask frameworklari",
            "JavaScript": "• Veb dasturlash uchun asosiy til\n• React, Vue, Angular frameworklari\n• Frontend va Backend (Node.js)",
            "Java": "• Android dasturlash\n• Katta korxona loyihalari\n• Spring framework",
            "C++": "• O'yinlar va tizim dasturlari\n• Yuqori tezlik\n• Unreal Engine",
            "C#": "• .NET platformasi\n• Windows dasturlari\n• Unity o'yinlar uchun"
        }
        return info.get(language, f"{language} - zamonaviy dasturlash tili")

    def get_topic_info(self, topic):
        """Mavzu haqida qisqacha"""
        info = {
            "Sun'iy intellekt": "Inson aqlini taqlid qiluvchi tizimlar. Machine Learning, Deep Learning, Neural Networks.",
            "Machine Learning": "Ma'lumotlardan o'rganuvchi algoritmlar. TensorFlow, PyTorch, scikit-learn.",
            "Veb dasturlash": "Frontend (HTML, CSS, JS) va Backend (Python, PHP, Node.js)",
            "Kiberxavfsizlik": "Tizimlarni himoya qilish. Ethical Hacking, Encryption, Security protocols.",
            "DevOps": "Development va Operations. CI/CD, Docker, Kubernetes, Cloud services."
        }
        return info.get(topic, f"{topic} - muhim IT yo'nalishi")


# Kontent generator
content_gen = ITContentGenerator()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        "👋 Assalomu alaykum! IT Dasturlash boni ishga tushdi.\n"
        "Har soatda IT va dasturlash haqida qiziqarli postlar kanalga joylanadi!\n\n"
        "Kanal: @it_dasturlash"
    )


@dp.message_handler(commands=['post_now'])
async def post_now_command(message: types.Message):
    """Test uchun hoziroq post yuborish"""
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        post = await content_gen.generate_post()
        await send_post(post)
        await message.reply("✅ Post yuborildi!")
    else:
        await message.reply("❌ Siz admin emassiz!")


async def send_post(post):
    """Postni kanalga yuborish"""
    try:
        if post['image']:
            # Rasm bilan yuborish
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=post['image'],
                caption=post['text'],
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Faqat matn
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=post['text'],
                parse_mode=ParseMode.MARKDOWN
            )
        logging.info(f"Post yuborildi: {datetime.now()}")
    except Exception as e:
        logging.error(f"Xatolik: {e}")


async def scheduler():
    """Har soatda post yuborish"""
    while True:
        now = datetime.now()
        # Birinchi postni ertalab 8 da boshlash
        if now.hour >= 8 and now.hour <= 23:
            post = await content_gen.generate_post()
            await send_post(post)

        # 1 soat kutish (3600 sekund)
        await asyncio.sleep(3600)


async def on_startup(dp):
    """Bot ishga tushganda"""
    asyncio.create_task(scheduler())
    await bot.send_message(
        CHANNEL_ID,
        "🤖 *Bot ishga tushdi!*\nEndi har soatda IT va dasturlash haqida postlar joylanadi.",
        parse_mode=ParseMode.MARKDOWN
    )


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)