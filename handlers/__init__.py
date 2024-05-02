from telegram.ext import CommandHandler, CallbackQueryHandler
from .start import start as start_handler
from .signup import signup as signup_handler
from .menu import menu as menu_handler
from .buy import buy as buy_handler
from .sell import sell as sell_handler
from .transfer import transfer as transfer_handler
from .fund import fund as fund_handler
from .community import community as community_handler
from .help import help as help_handler
from .handle_queries import handle_queries as query_handler
from .settings import settings as settings_handler
from .buy_x_handler import buy_x_sol_conv_handler as buy_x_sol_handler

def setup_handlers(application):
    
    application.add_handler(buy_x_sol_handler) # This needs to be added BEFORE query handler.

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("signup", signup_handler))
    application.add_handler(CommandHandler("menu", menu_handler))
    application.add_handler(CommandHandler("buy", buy_handler))
    application.add_handler(CommandHandler("sell", sell_handler))
    application.add_handler(CommandHandler("transfer", transfer_handler))
    application.add_handler(CommandHandler("fund", fund_handler))
    application.add_handler(CommandHandler("community", community_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("settings", settings_handler))
    application.add_handler(CallbackQueryHandler(query_handler))
