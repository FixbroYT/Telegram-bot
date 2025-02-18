# Telegram Bot

This project is a Telegram bot built using `aiogram`. The bot includes various functionalities such as an in-game shop, earning coins, a casino, and an inventory system.

## Features
- 🛒 **Shop**: Purchase in-game items.
- 💰 **Balance System**: Keep track of your virtual coins.
- 🎰 **Casino**: Play a game of chance with bets.
- 🎁 **Earn Coins**: Passive income system.
- 🎒 **Inventory Management**: View and sell owned items.

## Technologies Used
- `Python 3`
- `aiogram` for Telegram bot handling
- `SQLAlchemy` for database management
- `SQLite` as the database (can be switched to PostgreSQL or MySQL)
- `asyncio` for asynchronous operations

## Installation

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from BotFather)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/your-bot.git
   cd your-bot
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables or update `config.py` with your bot token:
   ```python
   TOKEN = "your_telegram_bot_token"
   ```

4. Run database migrations:
   ```sh
   python -m app.database.models
   ```

5. Start the bot:
   ```sh
   python run.py
   ```

## License
This project is under the MIT License.

