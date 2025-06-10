from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters, ContextTypes,
    ConversationHandler
)
from datetime import datetime
from dateutil.relativedelta import relativedelta

# مراحل المحادثة
DATE, MONTHS, SYSTEM = range(3)

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*📅 أرسل تاريخ آخر تغيير عنوان وظيفي، مثال:*\n"
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
        "*📌 ملاحظات احتساب كتب الشكر:*\n\n"
        "*1️⃣* كتاب شكر من المدير العام = *1 شهر*\n"
        "*2️⃣* كتاب شكر من الوزير = *1 شهر*\n"
        "*3️⃣* كتاب شكر من رئيس الوزراء = *6 أشهر*\n\n"
        "*✏️ كم عدد أشهر كتب الشكر؟* (اكتب الرقم فقط):",
        parse_mode="Markdown"
    )
    return MONTHS

# استلام عدد كتب الشكر
async def get_months(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["thanks_months"] = int(update.message.text)
        await update.message.reply_text(
            "*❓ ما هي فترة تغيير العنوان الوظيفي؟*\n"
            "*🧮 اختر النظام:*\n"
            "*1️⃣* نظام 4 سنوات\n"
            "*2️⃣* نظام 5 سنوات\n"
            "*✍️ أرسل 4 أو 5:*",
            parse_mode="Markdown"
        )
        return SYSTEM
    except ValueError:
        await update.message.reply_text("*⚠️ أدخل رقمًا صحيحًا فقط لعدد أشهر كتب الشكر.*", parse_mode="Markdown")
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
                    "*⚠️ صيغة التاريخ غير صحيحة.*\n"
                    "*✅ استخدم أحد التنسيقات التالية:*\n"
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
            f"*✅ الموعد النهائي لتغيير العنوان:* `{final_due.strftime('%Y/%m/%d')}`\n"
            f"*📤 يمكنك رفع المعاملة اعتبارًا من:* `{submission.strftime('%Y/%m/%d')}`\n"
            f"*⏳ المتبقي من الآن:* *{remain}* شهر",
            parse_mode="Markdown"
        )

        await update.message.reply_text("*🤖 شكراً لاستخدامك هذا البوت.*", parse_mode="Markdown")
        await update.message.reply_text("*👨‍💻 مطور البوت: المهندس أحمد كاظم*", parse_mode="Markdown")

        return ConversationHandler.END

    except Exception as e:
        await update.message.reply_text(
            f"*⚠️ حدث خطأ أثناء الحساب:*\n`{e}`\n\n"
            "*🔄 يرجى إعادة إدخال تاريخ آخر تغيير عنوان وظيفي بصيغة صحيحة.*",
            parse_mode="Markdown"
        )
        return DATE

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("*🚫 تم إلغاء العملية.*", parse_mode="Markdown")
    return ConversationHandler.END

# تشغيل البوت
def main():
    app = ApplicationBuilder().token("7775916785:AAFLWjaNmTUTDVPg9-0ZDOTeJmepReYHJbM").build()

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
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
