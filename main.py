from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
from config import TOKEN, KASPI_PAYMENT_LINK, REVIEW_CHANNEL, CONSULTATION_PRICE
from doctors import doctors

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Добро пожаловать в Doctor Chat!\n\n"
        "Здесь вы сможете начать чат со специалистом и получить онлайн консультацию врача.\n\n"
        "Не стесняйтесь спрашивать - наши доктора отвечают на любые вопросы "
        "и никогда не нарушают врачебную тайну."
    )
    
    keyboard = [[InlineKeyboardButton("Выбрать врача", callback_data="choose_doctor")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def choose_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    for doctor_name in doctors.keys():
        keyboard.append([InlineKeyboardButton(doctor_name, callback_data=f"doctor_{doctor_name}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Here you would send doctor images
    for doctor_name, doctor_info in doctors.items():
        # In a real implementation, you would use:
        # await query.message.reply_photo(photo=open(doctor_info['image'], 'rb'))
        pass
    
    await query.message.reply_text("Выберите врача для консультации:", reply_markup=reply_markup)

async def doctor_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    doctor_name = query.data.replace("doctor_", "")
    payment_message = (
        f"Для начала чата с врачом необходимо внести 100% предоплату.\n"
        f"Стоимость онлайн консультации: {CONSULTATION_PRICE} тг\n\n"
        f"Если вы согласны с условиями, перейдите по ссылке для оплаты:"
    )
    
    keyboard = [[InlineKeyboardButton("Оплатить", url=KASPI_PAYMENT_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(payment_message, reply_markup=reply_markup)

async def payment_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # In a real implementation, you would verify the payment
    success_message = (
        "✅ Ваш платеж успешно совершен!\n\n"
        "❗️Формат консультации:\n"
        "Получение ответа в реальном времени (скорость ответа в течении от минуты до 2-х часов) "
        "в порядке «онлайн живая очередь» с учетом часового времени вашего врача.\n\n"
        "Пожалуйста, сформируйте свой консультационный вопрос и отправьте ваши данные "
        "(анализы, описание состояния, снимки исследований и т.д.)"
    )
    
    doctor_link = doctors[context.user_data['selected_doctor']]['chat_link']
    keyboard = [[InlineKeyboardButton("Перейти к консультации", url=doctor_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(success_message, reply_markup=reply_markup)

async def end_consultation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    end_message = (
        "Спасибо за использование Doctor Chat!\n\n"
        "🌟 Поделитесь своим опытом в нашем канале отзывов.\n"
        "💎 Получите скидку 50% на следующую консультацию (действительна 2 месяца)!"
    )
    
    keyboard = [[InlineKeyboardButton("Оставить отзыв", url=REVIEW_CHANNEL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(end_message, reply_markup=reply_markup)

async def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(choose_doctor, pattern="^choose_doctor$"))
    application.add_handler(CallbackQueryHandler(doctor_selected, pattern="^doctor_"))
    
    await application.initialize()
    await application.start()
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())