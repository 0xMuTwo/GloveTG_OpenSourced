# Open Sourced

No Longer Maintained.
No Longer Supported.
Here to show others how I did it.

Good Luck!

# GloveTG

GloveTG is a service that sits between Telegram's servers, and the rest of Glove Protocol's Internal Services.

The telegram servers send a post request via webhook to this Python Server.

This server is running an asynchronous architecture, based on the Starlette application and uvicorn ASGI (Asynchronous Server Gateway Interface), capable of interacting with Telegram's webhook to receive real-time updates and also send GET and POST requests to external servers.

## Goal for MVP

- Have a Telegram server running, that users can interact with.
- Users must be able to generate a new wallet.
- Commands
  - /createWallet
  - /buy
  - /sell
  - /balance
- This MUST BE ABLE TO HANDLE MULTIPLE USERS AT ONCE WITHOUT SLOWING DOWN.

## Goal for UVP (Unit Viable Product)

- So this is basically going to be the unit on its own, with all other systems mocked. Trying to figure out microservice architecture and this seems like it will be pretty close.

- Have a telegram bot using async + webhook architecture, that allows user interaction and sends mock requests to other parts of the app. Watch & Test carefully for signs of synchronous behavior or slowdowns.

- /start ->
  - "Welcome, {name}."
    - PATH A: It looks like it's your first time here. Generate a wallet by typing '/createWallet'—and here's a link to a quick tutorial you can watch {Sends Tutorial Link}
    - PATH B: Let's get started! {Displays Main Menu}
- /createWallet ->
  - "Wallet created. Listed below is your private key. SAVE THIS & DON'T SHARE IT. It allows you to take full control of the wallet, even without telegram access. [PKEY] {Display Main Menu}
- {Main Menu}
  - Goal of this is to have a lot of little tips given together.
  - If user has never funded one of these wallets give a tip
    - You have no money added! Transfer some ETH to Wallet 1. Type /info to learn more.
  - Your Wallets
    - Wallet 1 | Bal 0.0 ETH ($0)
  - BUTTON MENU
    - Buy Tokens
    - Sell Tokens

## How to boot up

1. Set Up Python:
   `pip install -r requirements.txt`

2. Run Script:
   copy `.env.template to .env`
   run `python GloveTG.py`

3. Expose Port:
   You should see Uvicorn running on http://127.0.0.1:8000,
   this needs to get exposed to the greater internet so telegram can access it.
   run `ngrok http 8000`
   it should create a forwarding address in the format
   `https://XXX.ngrok.io -> http://localhost:8000`
   put `https://XXX.ngrok.io` in URL of .env

   Kill GloveTG with CNTR-C, then restart.

   Telegram app should work now.

### Useful Info

id:9999999900,"is_bot":false,"first_name":"Mu","last_name":"Two"
id:8888888888,"first_name":"Mew","last_name":"One"

Had an issue with ngrok not connecting, was solved with a VPN.
It seems that some university campuses block ngrok, wasted a lot of time on that.
Look into that for future.

The only useful IP seems to be:
172.18.0.1
That's telegram.

It might mess with the webhook? Would have to allow that.
But in general...Might want to lock that soon.

## Inputs & Outputs

### Outputs:

GloveTG will send JSON requests in the following format to Glove Router. Glove Router adds these to GloveQueue, workers process them and send responses seen in the "Inputs" section.

User Buy & Sell Orders

- Buy .5 ETH of 0xGLV with Wallet 1
  {type: transaction,
  user_id: user_id,

  command: {
  "action": "buy",
  "amount": 0.1,
  "token": "0xGLV",
  "wallet": 1
  }}

- Sell half of user's 0xGLV from wallet 1
  {type: transaction,
  user_id: user_id,

  command: {
  "action": "sell",
  "amount": 50%,
  "token": "0xGLV",
  "wallet": 1
  }}
  Balance Requests

Get the balance of user's wallets
{
type: balance,
user_id: user_id,
}

Wallet Generation Requests

{
type: wallet_gen,
user_id: user_id
}

User Checking Transaction Status
{
type: status_query,
user_id: user_id
}

User Status DB Queries

- Does user exist?
  {
  type: find_user,
  user_id: user_id
  }

### Inputs:

GloveTG receives inputs via webhook, and forwards the data to users based on the chat_id received.

User's Order has been successfully placed and is pending:
{
type: order,
user_id: user_id,
status: success,
message: "Your Order for .5 ETH -> 0xGLV has been successfully placed."
}

User's Order has been rejected:
{
type: order,
user_id: user_id,
status: failed,
message: "Your Order for .5 ETH -> 0xGLV has rejected. Reason: Not enough ETH."
}

User's Order had been Filled

{
type: order,
user_id: user_id,
status: success,
message: "Your Order for .5 ETH -> 0xGLV been filled 40.32 GLV bought."
}

Wallet Generated
{
type: wallet_gen,
user_id: user_id,
status: success,
message: "Wallet 2 Generated, Priv Key: XXX, Pub Key: YYY"
}
{
type: wallet_gen,
user_id: user_id,
status: rejected,
message: "No Wallet Generated, You already have 3 wallets."
}

User Query Response
{
type: query_response,
user_id: user_id,
status: pending,
message: "Has been pending for X mins, Y seconds. Check Etherscan Here: http://Etherscan.io/txnhash
}

Does user exist?
{
type: find_user,
user_id: user_id,
status: bool
}

Get Wallets & Tokens
{
type: wallet_token_update,
user_id: user_id,
payload:
{lots of stuff}
}

## Functions that should work on Launch:

✅ /start - Welcomes You to Glove Bot
✅ /signup - Creates Glove Account
❌ /menu - Shows Main Menu
❌ /buy - Buy Tokens With Glove
❌ /sell - Sell Your Tokens
❌ /fund - Explains How to Add Money to Wallets
❌ /help - Shows This Page

lmao no ->/replacewallet

## How to start on Docker.

docker compose up --build

## User Flow

- Start

  - Glove Bot is activated, {Name}
    If User Exists
    - Welcome Back, Type /menu to go to the main menu or /commands to see all commands.
      If User Doesn't Exist
    - Looks like you're new here. Type /signup to generate your wallets.

- Signup

  - Generating 3 Wallets for you.
  - Public Keys are how you interact with the wallet. This is what you send money to.
  - Think of Private Keys like your passwords, they allow you to control the wallet even without Glove's help.
  - Save this message, do NOT share your private keys. Keep them safe.
  - Wallets 1-3 Pub + Priv
  - Type /menu to go to main menu.
  - Here's a link to a quick tutorial.

- Menu

  - If Total Bal is Empty,
    - You have 0 ETH across your wallets.
    - Send ETH to a wallet and let the fun begin. Need help? Type /fund
  - List of their 3 wallets, public keys and ETH balance.

  # Testing

  /start
  Who are you
  Welcome Back
  /signup
  Generate Wallets
  You have wallets
