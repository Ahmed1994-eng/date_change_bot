from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters, ContextTypes,
    ConversationHandler
)
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

# مراحل المحادثة
DATE, MONTHS, SYSTEM = range(3)

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*\ud83d\uddd3 \u0623\u0631\u0633\u0644 \u062a\u0627\u0631\u064a\u062e \u0622\u062e\u0631 \u062a\u063a\u064a\u064a\u0631 \u0639\u0646\u0648\u0627\u0646 \u0648\u0638\u064a\u0641\u064a\u060c \u0645\u062b\u0627\u0644:*\n"
        "`2021-11-01`\n"
        "`01-11-2021`\n"
        "`2021/11/01`\n"
        "`01/11/2021`",
        parse_mode="Markdown"
    )
    return DATE

# استلام التاريخ
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["last_date"] = update.message.text
    await update.message.reply_text(
        "*\ud83d\udccc \u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0627\u062d\u062a\u0633\u0627\u0628 \u0643\u062a\u0628 \u0627\u0644\u0634\u0643\u0631:*\n\n"
        "*1\ufe0f\u20e3* \u0643\u062a\u0627\u0628 \u0634\u0643\u0631 \u0645\u0646 \u0627\u0644\u0645\u062f\u064a\u0631 \u0627\u0644\u0639\u0627\u0645 = *1 \u0634\u0647\u0631*\n"
        "*2\ufe0f\u20e3* \u0643\u062a\u0627\u0628 \u0634\u0643\u0631 \u0645\u0646 \u0627\u0644\u0648\u0632\u064a\u0631 = *1 \u0634\u0647\u0631*\n"
        "*3\ufe0f\u20e3* \u0643\u062a\u0627\u0628 \u0634\u0643\u0631 \u0645\u0646 \u0631\u0626\u064a\u0633 \u0627\u0644\u0648\u0632\u0631\u0627\u0621 = *6 \u0623\u0634\u0647\u0631*\n\n"
        "*\u270f\ufe0f \u0643\u0645 \u0639\u062f\u062f \u0623\u0634\u0647\u0631 \u0643\u062a\u0628 \u0627\u0644\u0634\u0643\u0631\u061f* (\u0627\u0643\u062a\u0628 \u0627\u0644\u0631\u0642\u0645 \u0641\u0642\u0637):",
        parse_mode="Markdown"
    )
    return MONTHS

# استلام عدد كتب الشكر
async def get_months(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["thanks_months"] = int(update.message.text)
        await update.message.reply_text(
            "*\u2753 \u0645\u0627 \u0647\u064a \u0641\u062a\u0631\u0629 \u062a\u063a\u064a\u064a\u0631 \u0627\u0644\u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u0648\u0638\u064a\u0641\u064a\u061f*\n"
            "*\ud83e\uddf2 \u0627\u062e\u062a\u0631 \u0627\u0644\u0646\u0638\u0627\u0645:*\n"
            "*1\ufe0f\u20e3* \u0646\u0638\u0627\u0645 4 \u0633\u0646\u0648\u0627\u062a\n"
            "*2\ufe0f\u20e3* \u0646\u0638\u0627\u0645 5 \u0633\u0646\u0648\u0627\u062a\n"
            "*\u270d\ufe0f \u0623\u0631\u0633\u0644 4 \u0623\u0648 5:*",
            parse_mode="Markdown"
        )
        return SYSTEM
    except ValueError:
        await update.message.reply_text("*\u26a0\ufe0f \u0623\u062f\u062e\u0644 \u0631\u0642\u0645\u0627\u064b \u0635\u062d\u064a\u062d\u0627\u064b \u0641\u0642\u0637.*", parse_mode="Markdown")
        return MONTHS

# استلام النظام وحساب الموعد
async def get_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        system_years = int(update.message.text)
        if system_years not in (4, 5):
            raise ValueError("النظام يجب أن يكون 4 أو 5")

        last_date_str = context.user_data["last_date"].replace("/", "-")
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
        except ValueError:
            try:
                last_date = datetime.strptime(last_date_str, "%d-%m-%Y")
            except ValueError:
                await update.message.reply_text(
                    "*\u26a0\ufe0f \u0635\u064a\u063a\u0629 \u0627\u0644\u062a\u0627\u0631\u064a\u062e \u063a\u064a\u0631 \u0635\u062d\u064a\u062d\u0629.*\n"
                    "*\u2705 \u0627\u0633\u062a\u062e\u062f\u0645 \u0623\u062d\u062f \u0627\u0644\u062a\u0646\u0633\u064a\u0642\u0627\u062a \u0627\u0644\u062a\u0627\u0644\u064a\u0629:*\n"
                    "`2024-06-09`\n"
                    "`09-06-2024`\n"
                    "`2024/06/09`\n"
                    "`09/06/2024`",
                    parse_mode="Markdown"
                )
                return DATE

        thanks_months = context.user_data["thanks_months"]

        base_due = last_date + relativedelta(years=system_years)
        final_due = base_due - relativedelta(months=thanks_months)
        submission = final_due - relativedelta(months=3)

        today = datetime.today()
        remain = max(0, (submission.year - today.year) * 12 + (submission.month - today.month))

        await update.message.reply_text(
            f"*\u2705 \u0627\u0644\u0645\u0648\u0639\u062f \u0627\u0644\u0646\u0647\u0627\u0626\u064a \u0644\u062a\u063a\u064a\u064a\u0631 \u0627\u0644\u0639\u0646\u0648\u0627\u0646:* `{final_due.strftime('%Y/%m/%d')}`\n"
            f"*\ud83d\udce4 \u064a\u0645\u0643\u0646\u0643 \u0631\u0641\u0639 \u0627\u0644\u0645\u0639\u0627\u0645\u0644\u0629 \u0627\u0639\u062a\u0628\u0627\u0631\u0627\u064b \u0645\u0646:* `{submission.strftime('%Y/%m/%d')}`\n"
            f"*\u23f3 \u0627\u0644\u0645\u062a\u0628\u0642\u064a \u0645\u0646 \u0627\u0644\u0622\u0646:* *{remain}* \u0634\u0647\u0631",
            parse_mode="Markdown"
        )

        await update.message.reply_text("*\ud83e\udd16 \u0634\u0643\u0631\u0627\u064b \u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645\u0643 \u0647\u0630\u0627 \u0627\u0644\u0628\u0648\u062a.*", parse_mode="Markdown")
        await update.message.reply_text("*\ud83d\udc68\u200d\ud83d\udcbb \u0645\u0637\u0648\u0631 \u0627\u0644\u0628\u0648\u062a: \u0627\u0644\u0645\u0647\u0646\u062f\u0633 \u0623\u062d\u0645\u062f \u0643\u0627\u0638\u0645*", parse_mode="Markdown")

        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"*\u26a0\ufe0f \u062d\u062f\u062b \u062e\u0637\u0623 \u0623\u062b\u0646\u0627\u0621 \u0627\u0644\u062d\u0633\u0627\u0628:*\n`{e}`\n\n"
            "*\ud83d\udd04 \u064a\u0631\u062c\u0649 \u0625\u0639\u0627\u062f\u0629 \u0625\u062f\u062e\u0627\u0644 \u062a\u0627\u0631\u064a\u062e \u0622\u062e\u0631 \u062a\u063a\u064a\u064a\u0631 \u0639\u0646\u0648\u0627\u0646 \u0648\u0638\u064a\u0641\u064a \u0628\u0635\u064a\u063a\u0629 \u0635\u062d\u064a\u062d\u0629.*",
            parse_mode="Markdown"
        )
        return DATE

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("*\u274c \u062a\u0645 \u0625\u0644\u063a\u0627\u0621 \u0627\u0644\u0639\u0645\u0644\u064a\u0629.*", parse_mode="Markdown")
    return ConversationHandler.END

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            MONTHS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_months)],
            SYSTEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_system)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    print("\u2705 Bot is running...")
    app.run_polling()
