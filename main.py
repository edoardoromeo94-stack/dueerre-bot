from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, ContextTypes, filters
import os

ZONE, ORE, RICAMBI = range(3)

ZONE_PRICES = {
    "1": 10,
    "2": 30,
    "3": 50,
    "4": 70,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Dueerre pronto.\nScrivi /nuovo")

async def nuovo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Zona 1 - 10€", callback_data="1")],
        [InlineKeyboardButton("Zona 2 - 30€", callback_data="2")],
        [InlineKeyboardButton("Zona 3 - 50€", callback_data="3")],
        [InlineKeyboardButton("Zona 4 - 70€", callback_data="4")],
    ]
    await update.message.reply_text("Seleziona zona:", reply_markup=InlineKeyboardMarkup(keyboard))
    return ZONE

async def zona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["zona"] = ZONE_PRICES[query.data]
    await query.edit_message_text("Inserisci ore:")
    return ORE

async def ore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ore"] = float(update.message.text.replace(",", "."))
    await update.message.reply_text("Inserisci ricambi:")
    return RICAMBI

async def ricambi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ricambi_val = float(update.message.text.replace(",", "."))
    totale = context.user_data["zona"] + (context.user_data["ore"] * 50) + ricambi_val
    await update.message.reply_text(f"Totale: {totale:.2f}€")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("nuovo", nuovo)],
        states={
            ZONE: [CallbackQueryHandler(zona)],
            ORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ore)],
            RICAMBI: [MessageHandler(filters.TEXT & ~filters.COMMAND, ricambi)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    print("Bot avviato")
    app.run_polling()

if __name__ == "__main__":
    main()
