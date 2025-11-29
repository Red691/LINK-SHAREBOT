# Link Share Bot ✨

<p align="center">
  <img src="assets/img1.jpg" alt="Bot Channels" width="700"/>
</p>

A powerful and dynamic Telegram bot designed to share links from specific channels, protecting them from copyright issues. It features a fully interactive, button-based UI and can be configured dynamically by the owner.

---

## 🚀 Features

-   **🔗 Advanced Link Sharing:** Securely share links from your channels.
-   **FORCE SUBSCRIBE:** Ensure users join designated channels before they can access links.
-   **Button-Based UI:** Modern, easy-to-use interface with inline buttons instead of text commands.
-   **Dynamic Content:** Rich messages with images and styled text using blockquotes.
-   **⚙️ In-Bot Configuration:** The bot owner can manage all important settings directly from the bot's UI.
    -   Manage Force-Subscribe channels (add, remove, list, toggle modes).
    -   Set the MongoDB URL and other settings on the fly.
-   **🔐 Secure:** No hardcoded credentials. All sensitive information is loaded from environment variables.

---

## 🤖 Bot Commands

The bot is primarily controlled through a user-friendly button interface. Here are the initial commands to get started:

-   `/start` - The main command to start the bot and open the main menu.
-   `/fsub` - (Owner only) Opens the Force-Subscribe settings menu.
-   `/settings` - (Owner only) Opens the general bot settings menu.

---

## 🛠️ How to Deploy

You can easily deploy this bot yourself. Follow the steps below.

### **Prerequisites**

-   A Telegram Bot Token. Get one from [@BotFather](https://t.me/BotFather).
-   Your Telegram API ID and API Hash. Get them from [my.telegram.org](https://my.telegram.org).
-   A MongoDB database URL. Get one for free from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### **Deployment Steps**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file in the root directory or set the following environment variables in your deployment environment:

    | Variable           | Description                                             |
    | ------------------ | ------------------------------------------------------- |
    | `TG_BOT_TOKEN`     | Your Telegram bot token from @BotFather.                |
    | `API_ID`           | Your Telegram App ID.                                   |
    | `API_HASH`         | Your Telegram App Hash.                                 |
    | `DB_URI`           | Your MongoDB connection URL.                            |
    | `OWNER_ID`         | Your numerical Telegram User ID.                        |
    | `DATABASE_CHANNEL` | The ID of the channel where the bot will send logs/notifications. |

    **Optional Variables:**
    You can customize the bot further with these optional variables: `DB_NAME`, `START_PIC`, `FSUB_PIC`, `HELP_PIC`, etc.

4.  **Run the bot:**
    ```bash
    python3 bot.py
    ```

---

## 🙏 Credits & Acknowledgements

This bot was made possible with the help and support of the following individuals:

-   **[ABHINAI](https://t.me/about_zani)**
-   **[ABHINAV](https://t.me/adityaabhinav)**
-   **[MASTER](https://t.me/V_Sbotmaker)**

A special thanks to the **[REx BOTs](https://t.me/RexBots_Official)** channel for their inspiration and support!
A special thanks to the **[REx BOTs](https://t.me/RexBots_Official)** channel for their inspiration and support!
---
