# WhatsApp Clone - Real-time Django Chat App

A modern, real-time chat application inspired by WhatsApp, built using Django, Django Channels, and WebSockets.

##  Features

- **Real-time Messaging**: Instant message delivery using WebSockets.
- **WhatsApp UI**: A premium, responsive interface matching WhatsApp's aesthetic (Teal theme, bubble styles, and wallpaper).
- **User Authentication**: Secure Login and Registration system.
- **Online Presence**: Real-time "Online" status and "Last Seen" timestamps.
- **Message Deletion**: "Delete for Everyone" functionality that updates in real-time.
- **Unread Notifications**: Dynamic green badges in the sidebar showing unread message counts.
- **Sidebar Contact List**: Seamlessly switch between different conversations.

##  Tech Stack

- **Backend**: Python, Django 6.0
- **Asynchronous Layer**: Django Channels, Daphne
- **Database**: SQLite (default)
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6)
- **Icons**: Bootstrap Icons

##  Installation & Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the repository
```bash
git clone <repository-url>
cd realtime_chat/chatbox
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django channels daphne
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Optional - for Admin access)
```bash
python manage.py createsuperuser
```

##  How to Run

Since this project uses Django Channels for WebSockets, you should run it using the development server which is automatically configured to use Daphne.

```bash
python manage.py runserver
```

Once the server starts:
1. Open your browser and go to `http://127.0.0.1:8000/`.
2. Register two different accounts.
3. Open two different browsers (or one in Incognito mode).
4. Log in with both accounts and start chatting in real-time!

##  Security Features

- **AuthMiddlewareStack**: Only authenticated users can connect to the WebSocket.
- **CSRF Protection**: All forms and WebSocket actions are secured.
- **Protocol Awareness**: The frontend automatically detects `ws://` or `wss://` based on the environment.

---
Made with ❤️ for real-time communication.
