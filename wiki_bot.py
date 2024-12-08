import asyncio
import logging
import wikipediaapi
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

# .env faylni yuklash
load_dotenv()

# Bot tokenini o‘qish
TOKEN = os.getenv("BOT_TOKEN")

# Wikipedia API sozlamalari
wiki = wikipediaapi.Wikipedia(
    language='uz',  # Wikipedia tilini o‘zbekchaga sozlash
    user_agent="WikiBot/1.0 (https://t.me/Wikibot01bot)"  # Foydalanuvchi agenti
)

# Dispatcher yaratamiz
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Botga start buyrug‘ini jo‘natganda ishlaydi."""
    await message.answer(
        f"Assalomu alaykum, {html.bold(message.from_user.full_name)}! 😊\n"
        "Wikipedia'dan ma'lumot izlash uchun mavzuni yozib yuboring."
    )


@dp.message()
async def wikipedia_handler(message: Message) -> None:
    """Foydalanuvchi yuborgan matnni Wikipedia'dan izlaydi."""
    search_term = message.text
    page = wiki.page(search_term)

    if page.exists():
        # Topilgan maqolani qisqacha chiqaradi
        summary = page.summary[:1000]  # Maqolaning birinchi 1000 ta belgisi
        await message.answer(f"📄 {html.bold(page.title)}\n\n{summary}")
    else:
        await message.answer("Kechirasiz, bu mavzu bo‘yicha ma’lumot topilmadi. ❌")


async def main():
    """Asosiy botni ishga tushirish funksiyasi."""
    logging.basicConfig(level=logging.INFO)

    # Bot obyektini to'g'ri konfiguratsiya qilamiz
    bot = Bot(
        token=TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")  # Yangi usulda parse_mode
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
