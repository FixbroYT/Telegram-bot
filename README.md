
---

# 🚀 Telegram Bot

This project is a Telegram bot built using `aiogram`. The bot includes various functionalities such as an in-game shop, earning coins, a casino, and an inventory system.

---

## 📌 Features
- 🛒 **Shop**: Purchase in-game items.
- 💰 **Balance System**: Keep track of your virtual coins.
- 🎰 **Casino**: Play a game of chance with bets.
- 🎁 **Earn Coins**: Passive income system.
- 🎒 **Inventory Management**: View and sell owned items.

---

## 📌 Technologies Used
- `Python 3`
- `aiogram` for Telegram bot handling
- `SQLAlchemy` for database management
- `SQLite` as the database (can be switched to PostgreSQL or MySQL)
- `asyncio` for asynchronous operations

---

# 🔧 Installation Guide  

## 📌 1. Clone the Repository  

Clone the repository from GitHub:
```
git clone https://github.com/FixbroYT/Telegram-bot.git
```
Navigate to the project directory:  
```
cd Telegram-bot
```

---

## 📌 2. Create a Virtual Environment  
Create a virtual environment:  
```bash
python -m venv .venv
```
Activate the virtual environment:  
- **Windows**:  
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/macOS**:  
  ```bash
  source .venv/bin/activate
  ```

---

## 📌 3. Install Dependencies  
Install the required packages:  
```bash
pip install -r requirements.txt
```

---

## 📌 4. Set Up Environment Variables  
The bot uses environment variables stored in a `.env` file.  

Create a `.env` file in the root directory and add:  
```
TOKEN=your_telegram_bot_token
```

📌 **How to Get a Token?**  
1. Open Telegram and search for **@BotFather**.  
2. Use the `/newbot` command and follow the instructions.  
3. Copy the generated token and paste it into the `.env` file.  

---

## 📌 5. Run the Bot  
Ensure the virtual environment is active and run:  
```bash
python run.py
```
If the bot starts successfully, you will see a confirmation message in the terminal.

---

## 📌 Additional Commands  

🔹 **Deactivate the Virtual Environment**  
```bash
deactivate
```

🔹 **Update Dependencies**  
```bash
pip freeze > requirements.txt
```

🔹 **Update the Bot (if changes are made)**  
```bash
git pull origin main
```

---

## 📌 Troubleshooting  

🔸 **Error: `ModuleNotFoundError`**  
👉 Make sure the virtual environment is activated before running the bot.  

🔸 **Error: `TokenInvalid` or `Unauthorized`**  
👉 Check that the token in `.env` is correct.  

🔸 **Error: `aiogram.exceptions.TelegramConflictError`**  
👉 The bot is already running somewhere else. Stop the previous instance before starting a new one.  

---

## 📌 Contact  
If you have any questions, feel free to reach out to **@Bobik6k**.  

🎉 **Your bot is now ready to use!**
```
