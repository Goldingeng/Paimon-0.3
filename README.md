Genshin Spin Simulator Bot
This is a Telegram bot that simulates spins (gacha pulls) from the popular game Genshin Impact. The bot allows users to simulate obtaining characters with varying rarities, keep track of their pulls, and interact with a fully functional gacha system.

🚀 Features
Spin Simulation: Users can simulate spins and receive characters of different rarities.
Character Management: Track your character collection, including legendaries, epics, and more.
Banner Rotation: The bot automatically updates the current banner, ensuring that users can always pull from the most up-to-date banners.
History Tracking: Keep track of your pull history and banner participation.
Spin Relevance Check: Ensure banners are still valid and up-to-date within their time limits.
🛠️ Tech Stack
Python: The bot is written in Python, leveraging its powerful asynchronous capabilities.
AIOgram 3: Asynchronous Telegram bot framework for Python that handles the communication between the bot and users.
SQLAlchemy: For database management and working with various models such as users, characters, and banners.
Asyncio: Efficient handling of asynchronous operations, making the bot fast and responsive.
PostgreSQL/MySQL/SQLite: The bot is compatible with different SQL databases.
📦 Installation
Clone the repository:
bash
Копировать код
git clone https://github.com/yourusername/genshin-spin-simulator-bot.git
Install dependencies:
bash
Копировать код
pip install -r requirements.txt
Set up your environment variables for database connection and Telegram bot token:
bash
Копировать код
export BOT_TOKEN='your-telegram-bot-token'
export DATABASE_URL='your-database-url'
Run the bot:
bash
Копировать код
python main.py
📝 Usage
/start - Start interacting with the bot.
/spin - Simulate a spin and see which characters you get.
/characters - View your collection of characters.
/banner - View the current banner and its featured characters.
/history - Review your pull history.
🌟 How It Works
Spin Mechanics: The bot uses pre-defined rarity levels to simulate pulls.
Banners: Rotating banners offer different sets of characters for users to obtain, with legendary and epic rarity characters being the most sought after.
Backend: SQLAlchemy handles all database interactions asynchronously, ensuring efficient and fast operations.
🤝 Contributions
Feel free to submit issues, create pull requests, or suggest new features!
