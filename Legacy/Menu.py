# ##MENU—BETA NOT WORKING

# # Stages
# START_ROUTES, END_ROUTES = range(2)
# # Callback data
# ONE, TWO, THREE, FOUR = range(4)

# CUSTOM_ETH_INPUT, BUY_INPUT, BUY_SCREEN = 7, 8, 9


# async def menu(update: Update, context: CustomContext) -> None:
#     """Main Menu for Users"""
#     keyboard = [
#         [
#             InlineKeyboardButton("Buy", callback_data="BUY_TOKEN"),
#             InlineKeyboardButton("Sell", callback_data="SELL_TOKEN"),
#             InlineKeyboardButton("Help", callback_data="HELP"),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     menu_intro_text1 = (
#         "Welcome to Thunder.\n"
#         "We hope you enjoy.\n"
#         "You have been assigned new wallets.\n"
#         "Fund them, and start trading.\n"
#     )
#     gas = 69
#     ethPrice = 1234
#     menu_intro_text2 = f"Gas {gas} GWEI ⬩ ETH ${ethPrice}\n"
#     menu_intro_text3 = "\n\n═══ Your Wallets ═══\n"
#     menu_intro_text4 = (
#         "Wallet ⬩ w1\n"
#         "Balance 0.0 ETH ⬩ $0\n"
#         "Transactions: 0\n"
#         "Address: 0xasdf\n\n"
#         "Wallet ⬩ w2\n"
#         "Balance 0.0 ETH ⬩ $0\n"
#         "Transactions: 0\n"
#         "Address: 0xasdf\n\n"
#         "Wallet ⬩ w3\n"
#         "Balance 0.0 ETH ⬩ $0\n"
#         "Transactions: 0\n"
#         "Address: 0xasdf\n"
#     )

#     menu_intro_text = (
#         menu_intro_text1 + menu_intro_text2 + menu_intro_text3 + menu_intro_text4
#     )
#     await update.message.reply_text(menu_intro_text, reply_markup=reply_markup)
#     # Tell ConversationHandler that we're in state `FIRST` now
#     return START_ROUTES


# ##^^MENU, NOT WORKING
