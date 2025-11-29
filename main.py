import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto, FSInputFile 

# 1. Load Token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN:
    print("Error: .env ဖိုင်ထဲမှာ BOT_TOKEN ထည့်ဖို့ မေ့နေတယ် သားကြီးရေ!")
    exit()

# 2. Setup Bot
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 🖼️ LOCAL IMAGE PATHS ---
PATH_MAIN = "images/main.jpg"
PATH_GEMINI = "images/gemini.jpg"
PATH_PERP = "images/perp.jpg"
PATH_ORDER = "images/order.jpg"

# --- Handlers ---

# 1. Start Command (/start)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 ဝန်ဆောင်မှုများ", callback_data="services_menu")
    builder.button(text="✍️ အော်ဒါတင်ရန်", callback_data="order_general")
    builder.button(text="💬 Admin နှင့် စကားပြောရန်", url="https://t.me/minkhant070")
    builder.adjust(1)
    
    welcome_text = (
        f"🙏 မင်္ဂလာပါ **{message.from_user.full_name}** ခင်ဗျာ။\n\n"
        "**MK Service & Seller** မှ ကြိုဆိုပါတယ်။\n"
        "Gemini Advanced နှင့် Perplexity Pro အကောင့်များကို "
        "စိတ်ချယုံကြည်စွာ ဝယ်ယူနိုင်ပါသည်။"
    )
    
    # Start မှာတော့ answer_photo ကို သုံးတာ မှန်တယ်
    photo = FSInputFile(PATH_MAIN)
    await message.answer_photo(photo=photo, caption=welcome_text, reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

# 2. Services Menu
@dp.callback_query(F.data == "services_menu")
async def show_services_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="✨ Gemini Advanced", callback_data="menu_gemini")
    builder.button(text="🔍 Perplexity Pro", callback_data="menu_perplexity")
    builder.button(text="🔙 မူလစာမျက်နှာ", callback_data="main_menu")
    builder.adjust(2, 1)

    text = "မိမိ လိုချင်သော ဝန်ဆောင်မှုကို ရွေးချယ်ပေးပါ ခင်ဗျာ။ 👇"
    
    # FIXED: edit_message_media မဟုတ်ဘဲ edit_media လို့ ပြောင်းလိုက်ပြီ ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_MAIN), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- GEMINI SECTION ---

@dp.callback_query(F.data == "menu_gemini")
async def show_gemini_types(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Ready Made Account", callback_data="detail_gemini_ready")
    builder.button(text="⬆️ Upgrade Your Account", callback_data="detail_gemini_upgrade")
    builder.button(text="🔙 နောက်သို့", callback_data="services_menu")
    builder.adjust(1)

    text = "**✨ Gemini Advanced**\n\nဝယ်ယူလိုသော ပုံစံကို ရွေးချယ်ပေးပါ 👇"
    
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_GEMINI), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "detail_gemini_ready")
async def detail_gemini_ready(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 ဈေးနှုန်းကြည့်မည်", callback_data="price_gemini_ready")
    builder.button(text="🔙 နောက်သို့", callback_data="menu_gemini")
    builder.adjust(1)

    text = (
        "**🆕 Gemini Advanced (Ready Made)**\n\n"
        "• Gmail အသစ်တစ်ခုဖြင့် ၁ နှစ်စာ လျှောက်ထားပြီးသား အကောင့်ကို ရရှိပါမည်။\n"
        "• ဝယ်ယူပြီး ချက်ချင်း အသုံးပြုနိုင်ပါသည်။ ✅"
    )
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_GEMINI), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "detail_gemini_upgrade")
async def detail_gemini_upgrade(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 ဈေးနှုန်းကြည့်မည်", callback_data="price_gemini_upgrade")
    builder.button(text="🔙 နောက်သို့", callback_data="menu_gemini")
    builder.adjust(1)

    text = (
        "**⬆️ Gemini Advanced (Upgrade)**\n\n"
        "• လူကြီးမင်း၏ လက်ရှိသုံးနေသော Gmail ကို ၁ နှစ်စာ Premium ဖြစ်အောင် လုပ်ပေးခြင်း ဖြစ်ပါသည်။\n"
        "• Password ပေးရန် မလိုပါ။ ✅"
    )
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_GEMINI), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- PERPLEXITY SECTION ---

@dp.callback_query(F.data == "menu_perplexity")
async def show_perplexity_types(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="🆕 Ready Made Account", callback_data="detail_perp_ready")
    builder.button(text="⬆️ Upgrade Your Account", callback_data="detail_perp_upgrade")
    builder.button(text="🔙 နောက်သို့", callback_data="services_menu")
    builder.adjust(1)

    text = "**🔍 Perplexity Pro**\n\nဝယ်ယူလိုသော ပုံစံကို ရွေးချယ်ပေးပါ 👇"
    
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_PERP), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "detail_perp_ready")
async def detail_perp_ready(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 ဈေးနှုန်းကြည့်မည်", callback_data="price_perp_ready")
    builder.button(text="🔙 နောက်သို့", callback_data="menu_perplexity")
    builder.adjust(1)

    text = (
        "**🆕 Perplexity Pro (Ready Made)**\n\n"
        "• Mail အသစ်ဖြင့် ၁ နှစ်စာ အဆင်သင့်သုံး အကောင့် ရရှိပါမည်။ ✅"
    )
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_PERP), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "detail_perp_upgrade")
async def detail_perp_upgrade(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 ဈေးနှုန်းကြည့်မည်", callback_data="price_perp_upgrade")
    builder.button(text="🔙 နောက်သို့", callback_data="menu_perplexity")
    builder.adjust(1)

    text = (
        "**⬆️ Perplexity Pro (Upgrade)**\n\n"
        "• လူကြီးမင်း၏ ကိုယ်ပိုင် Mail ကို ၁ နှစ်စာ Pro အဆင့်မြှင့်တင်ပေးပါသည်။ ✅"
    )
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_PERP), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- PRICE SECTION ---

@dp.callback_query(F.data.startswith("price_"))
async def show_price(callback: types.CallbackQuery):
    data_parts = callback.data.split("_") 
    service = data_parts[1]   
    plan_type = data_parts[2] 
    
    price_text = "XX,XXX Ks"
    current_img = PATH_MAIN 
    
    if service == "gemini":
        price_text = "45,000 Ks"
        current_img = PATH_GEMINI
    elif service == "perp":
        price_text = "50,000 Ks"
        current_img = PATH_PERP

    order_callback = f"order_{service}_{plan_type}"
    back_target = f"detail_{service}_{plan_type}"

    builder = InlineKeyboardBuilder()
    builder.button(text="✍️ အော်ဒါတင်မည် (Order Now)", callback_data=order_callback)
    builder.button(text="🔙 နောက်သို့", callback_data=back_target)
    builder.adjust(1)

    text = (
        f"**💰 ဈေးနှုန်း - {price_text} (1 Year)**\n\n"
        "ယခုပဲ အော်ဒါတင်ပြီး ဝန်ဆောင်မှု ရယူလိုက်ပါ။ 👇"
    )
    
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(current_img), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- SMART NOTIFICATION HANDLER ---

@dp.callback_query(F.data.startswith("order_"))
async def notify_admin_smart(callback: types.CallbackQuery):
    user = callback.from_user
    username = f"@{user.username}" if user.username else "No Username"
    full_name = user.full_name
    user_id = user.id
    
    data_parts = callback.data.split("_") 
    
    service_name = "General Inquiry"
    service_type = "Not Specified"

    if len(data_parts) == 3:
        s_code = data_parts[1]
        t_code = data_parts[2]
        if s_code == "gemini": service_name = "Gemini Advanced"
        if s_code == "perp": service_name = "Perplexity Pro"
        if t_code == "ready": service_type = "Ready Made Account"
        if t_code == "upgrade": service_type = "Upgrade Your Account"

    alert_text = (
        f"🚨 **New Order Alert!** 🚨\n\n"
        f"Customer အသစ်တစ်ယောက် Order တင်ခဲ့ပါတယ်။\n"
        f"--------------------------------\n"
        f"💎 **Service:** {service_name}\n"
        f"📋 **Service Type:** {service_type}\n"
        f"--------------------------------\n"
        f"👤 **User:** {username}\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"📛 **Name:** {full_name}"
    )
    
    try:
        if ADMIN_ID:
            await bot.send_message(chat_id=ADMIN_ID, text=alert_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Error sending to admin: {e}")

    reply_text = (
        "✅ **Admin ထံသို့ အကြောင်းကြားပြီးပါပြီ။**\n\n"
        "လူကြီးမင်း၏ အော်ဒါကို ဆက်လက်ဆောင်ရွက်ရန် Admin Account သို့ Screen Shot ရိုက်ပြီး ဆက်သွယ်ပေးပါခင်ဗျာ။ 👇"
    )
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Admin သို့ Chat Box တွင်ပြောရန်", url="https://t.me/minkhant070")
    kb.button(text="🔙 မူလစာမျက်နှာ", callback_data="main_menu")
    kb.adjust(1)
    
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_ORDER), caption=reply_text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=kb.as_markup())


# --- GENERAL NAVIGATION ---

@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 ဝန်ဆောင်မှုများ", callback_data="services_menu")
    builder.button(text="✍️ အော်ဒါတင်ရန်", callback_data="order_general")
    builder.button(text="💬 Admin နှင့် စကားပြောရန်", url="https://t.me/minkhant070")
    builder.adjust(1)
    
    text = (
        "**MK Service & Seller** မှ ကြိုဆိုပါတယ်။\n"
        "Gemini Advanced နှင့် Perplexity Pro အကောင့်များကို "
        "စိတ်ချယုံကြည်စွာ ဝယ်ယူနိုင်ပါသည်။"
    )
    # FIXED ✅
    media = InputMediaPhoto(media=FSInputFile(PATH_MAIN), caption=text, parse_mode=ParseMode.MARKDOWN)
    await callback.message.edit_media(media=media, reply_markup=builder.as_markup())

# --- RUN ---
async def main():
    print("✅ MK Service Bot is running with LOCAL IMAGES (FIXED)...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped.")