import src.utils.warnings_cleanup
from src.alerts.cooldown import can_run_deep

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from src.config import TELEGRAM_BOT_TOKEN
from src.alerts.help_menu import help_text
from src.ai.deep_research import deep_dive
from src.scanner.run_scan import run_scan

async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        help_text()
    )

async def deep_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not context.args:

        await update.message.reply_text(
            "Usage: /deep NVDA"
        )
        return

    ticker = context.args[0].upper()

    await update.message.reply_text(
        f"Researching {ticker}..."
    )

    result = deep_dive(
        ticker
    )

    if not can_run_deep():

        await update.message.reply_text(
            "⏳ Cooldown active (30 sec)"
        )
        return   
    if not result:

        await update.message.reply_text(
            "⚠️ Gemini busy."
        )
        return

    await update.message.reply_text(
        result[:4000]
    )

async def top_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "Running scan..."
    )

    result = run_scan()

    await update.message.reply_text(
        result[:4000]
    )

app = (
    ApplicationBuilder()
    .token(
        TELEGRAM_BOT_TOKEN
    )
    .build()
)

app.add_handler(
    CommandHandler(
        "help",
        help_cmd
    )
)

app.add_handler(
    CommandHandler(
        "deep",
        deep_cmd
    )
)

app.add_handler(
    CommandHandler(
        "top",
        top_cmd
    )
)

print(
    "Running startup scan..."
)

run_scan()

print(
    "Telegram bot running..."
)

app.run_polling()
