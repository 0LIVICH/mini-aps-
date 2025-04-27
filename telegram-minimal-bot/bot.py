import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or "7728251954:AAFl16-_heP6wtwlR2OnphwNWWWo7lVf334"  # Резервный вариант

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню с кнопкой Mini App"""
    keyboard = [
        [InlineKeyboardButton("📱 Открыть Mini App", web_app={"url": "https://2cde-85-192-40-180.ngrok-free.app"})],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
    ]
    
    await update.message.reply_text(
        "🔒 *VPN Подписки*\n\n"
        "Управляйте своими подписками через наше мини-приложение:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "about":
        await query.edit_message_text(
            "🤖 *О боте VPN*\n\n"
            "Возможности:\n"
            "▫️ Управление подписками\n"
            "▫️ История транзакций\n"
            "▫️ Приглашение друзей\n\n"
            "Используйте Mini App для полного функционала",
            parse_mode="Markdown"
        )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из Mini App"""
    data = update.message.web_app_data.data
    await update.message.reply_text(
        f"Получены данные из Mini App:\n`{data}`",
        parse_mode="Markdown"
    )

def main():
    """Запуск бота"""
    if not TOKEN:
        raise ValueError("Токен бота не найден! Проверьте .env файл или укажите токен в коде.")
    
    app = Application.builder().token(TOKEN).build()
    
    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    
    print("🟢 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()