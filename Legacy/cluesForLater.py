     # From Webhook_Update
     # Using Context
     # chat_member = await context.bot.get_chat_member(
    #     chat_id=update.user_id, user_id=update.user_id
    # )
    # if update.type == "test":
    #     await context.bot.send_message(
    #         chat_id=update.user_id, text="Test Sent.", parse_mode=ParseMode.HTML
    #     )
    # if update.type == "order":
    #     await context.bot.send_message(
    #         chat_id=update.user_id, text="Buy Sent", parse_mode=ParseMode.HTML
    #     )
    # if update.type == "cats":
    #     # This logic will be how we populate tokens and wallets later
    #     print(context.user_data.get("cats", "notSet"))
    #     context.user_data["cats"] = update.status
    #     print(context.user_data.get("cats", "notSet"))
    #     await context.bot.send_message(
    #         chat_id=update.user_id, text="cats context set", parse_mode=ParseMode.HTML
    #     )
    # payloads = context.user_data.setdefault("payloads", [])
    # payloads.append(update.payload)
    # combined_payloads = "</code>\n• <code>".join(payloads)
    # text = (
    #     f"The user {chat_member.user.mention_html()} has sent a new payload. "
    #     f"So far they have sent the following payloads: \n\n• <code>{combined_payloads}</code>"
    # )

# In /sell
    # This is going to be cool, using context to store tokens,
    # but it's going to be complex to implement
    # if "user_tokens_and_wallets" not in context.user_data:
    #     context.user_data[
    #         "user_tokens_and_wallets"
    #     ] = await get_user_wallet_and_token_list(user_id)
    # user_tokens = context.user_data["user_tokens_and_wallets"]["tokens"]
    # formatted_message = await format_tokens_message(user_tokens)
    # await update.message.reply_text(
    #     f"Your Tokens:\n{formatted_message}\n\n"
    #     "Sell with /sell [percent] [token] [wallet]\n"
    #     "Example: /sell 50 Sol 1 will sell 50% of the Sol in Wallet 1 "
    # )
        # wallet_tokens = user_tokens[wallet_index]

    # if token not in wallet_tokens:
    #     await update.message.reply_text(
    #         f"Token '{token}' Not Found in Wallet {wallet}. Please Try Again.\n"
    #     )
    #     return


# In register Handlers
    # application.add_handler(CommandHandler("context", context)) # For debugging w cats



    # WalletGen
    # newPriv, newPublic = WalletGen()
    # await update.message.reply_text(
    #     f"Wallet created. Listed below is your private key. "
    #     f"SAVE THIS & DON'T SHARE IT. It allows you to take full "
    #     f"control of the wallet, even without telegram access.\n\n"
    #     f"Private Key = {newPriv}\nPublic Key = {newPublic}"
    # )




# From /menu

    # fiat = 1500

    # # Getting Fresh Data, Adding to Context, Then Using It.
    # user_tokens_wallets = context.user_data[
    #     "user_tokens_and_wallets"
    # ] = await get_user_wallet_and_token_list(user_id)

    # tokens, users = user_tokens_wallets["tokens"], user_tokens_wallets["wallets"]
    # header_msg = f"Welcome {name}, great to see you."

    # your_wallets_breaker = "\n\n═══ Your Wallets ═══\n"
    # poverty_check = ""

    # no_eth = all(wallet_data.get("ETH", 0) == 0 for wallet_data in tokens)
    # if no_eth:
    #     poverty_check = (
    #         f"\n\nYou have 0 ETH across your wallets.\n"
    #         "Send ETH to a wallet and let the fun begin.\n"
    #         "Need help? Type /fund\n"
    #     )

    # # Conjured by GPT. It works but I have no idea how.
    # wallet_msg = "\n\n".join(
    #     [
    #         f"Wallet {i + 1} * {wallet_data.get('ETH', 0)} ETH * "
    #         f"${wallet_data.get('ETH', 0)*fiat}\n{wallet_addr}\n"
    #         + "\n".join(
    #             f"{token}: {amount}"
    #             for token, amount in wallet_data.items()
    #             if token != "ETH"
    #         )
    #         for i, (wallet_data, wallet_addr) in enumerate(zip(tokens, users))
    #     ]
    # )

    # response_msg = header_msg + poverty_check + your_wallets_breaker + wallet_msg
    # await update.message.reply_text(response_msg)




# async def replacewallet(update: Update, context: CustomContext) -> None:
#     """Generates Wallet for Users"""
#     user_id = update.message.chat.id
#     instruct_text = "/replacewallet [wallet number]"
#     example_text = "Example: /replacewallet 2"
#     args = context.args
#     if len(args) == 0:
#         await update.message.reply_text(f"{instruct_text}\n{example_text}")
#         return
#     wallet_number = args[0]
#     try:
#         wallet_number = int(wallet_number)
#     except ValueError:
#         await update.message.reply_text(
#             "Invalid Wallet Number:\n" f"{instruct_text}\n" f"{example_text}"
#         )
#         return
#     if not 1 <= wallet_number < 4:
#         await update.message.reply_text(
#             "Invalid Wallet Number:\n" f"{instruct_text}\n" f"{example_text}"
#         )
#         return
#     if len(args) == 1:
#         await update.message.reply_text(
#             f"🚨 By replacing your wallet you will no longer be able to control it through Glove.🚨 \n"
#             f"This may mean loss of funds. If you accept this risk\nType: /replacewallet [wallet number] yes"
#         )
#         return
#     if len(args) == 2 and args[1] == "yes":
#         await update.message.reply_text(f"replacing wallet.")
#         current_time = datetime.now().isoformat()
#         await send_task("WalletGen", str(user_id), current_time, str(wallet_number))
#     return




# async def is_user_recognized(userid) -> bool:
#     """Checks if the user is in the database or not"""
#     userids = [1234, 6350723118, 5]
#     if userid in userids:
#         return True
#     else:
#         return False



# async def balance(update: Update, context: CustomContext) -> None:
#     user_id = update.message.chat.id
#     await update.message.reply_text(
#         "Fetching your balance..."
#     )
#     current_time = datetime.now().isoformat()
#     await send_task("BalanceRequest", str(user_id), current_time)
#     return



# async def context(update: Update, context: CustomContext) -> None:
#     fund_video = "https://www.youtube.com/watch?v=Dzslefsew4A"
#     await update.message.reply_text(
#         f"Local Context abt cats: {context.user_data['cats']}"
#     )

#     await update.message.reply_text(fund_video)



# async def webhook_update(update: WebhookUpdate, context: CustomContext) -> None:
#     """Handle custom updates."""
#     await context.bot.send_message(
#         chat_id=update.user_id, text=f"{update.message, update.status, update.payload}", parse_mode=ParseMode.HTML
#     )



# elif operation == "BalanceRequest":
#     payload = {
#         "platform": platform_id,
#         "operation": operation,
#         "user_id": user_id,
#         "origin_timestamp": origin_timestamp,
#     }