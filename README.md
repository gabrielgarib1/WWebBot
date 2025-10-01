# WhatsApp Bot for Company Management

A Python-based WhatsApp automation bot designed for small business management (4+ people). The bot helps organize tasks, communication, and scheduling through WhatsApp Web automation.

## Features

- **Message Scheduling**: Schedule messages for specific dates and times
- **Timer-based Messages**: Send messages after a specified delay
- **Contact Management**: Restrict bot access to specific groups/contacts
- **Database Integration**: JSON-based storage for tasks, processes, clients, and employees
- **Multiple Operation Modes**: Test mode and scheduled mode

<!-- ![alt text](Currículo-1991-1automacaoUFSC.png) -->
<!-- *Bot interface showing scheduled messages and commands* -->

## Project Structure

```
WWebBot/
├── main.py                 # Main entry point and command interface
├── whatsapp_bot.py        # Core bot functionality and WhatsApp automation
├── test.py                # Testing and development scripts
├── me_next_features.txt   # Planned features and improvements
├── DB_enterprise/         # JSON database files (auto-created)
├── User_Data/            # Firefox profile data (auto-created)
└── requirements.txt      # Python dependencies
```

## Installation

1; Clone the repository:

```bash
git clone <repository-url>
cd WWebBot
```

2; Install dependencies:

```bash
pip install -r requirements.txt
```

3; Install Firefox and ensure it's in your PATH (required for WhatsApp Web automation)

## Configuration

### Important Files (in .gitignore)

⚠️ **Note**: Some configuration files may be excluded from version control for security reasons:

- API keys and credentials
- Personal contact lists
- User-specific settings
- Browser session data

<!-- ![Configuration Setup](images/config_setup.png) -->
<!-- *Example configuration file structure* -->

## Usage

### Basic Setup

```python
from whatsapp_bot import CompanyWhatsAppBot

groups = ["Your-Group-Name"]
bot = CompanyWhatsAppBot(groups)
bot.set_mode('schedule')  # or 'test'
```

<!-- ![WhatsApp Web Login](images/whatsapp_login.png) -->
<!-- *QR Code scan required for first-time setup* -->

### Available Commands by Terminal

- `s` - Schedule a message for specific date/time
- `t` - Schedule a message with timer (minutes delay)
- `d` - Delete a scheduled message
- `l` - List all scheduled messages
- `c` - Clear all scheduled messages
- `q` - Quit the bot

### Dependencies

- `selenium` - Web automation
- `schedule` - Task scheduling
- `inputimeout` - Timeout-enabled input
- `webdriver-manager` - Automatic driver management

### Browser Automation

You may need to install the browser webdriver.
The bot uses Firefox with a persistent profile to maintain WhatsApp Web sessions.

<!-- ![Webdriver install website](www.webdriverchrome.blablabla) -->
<!-- ![Browser Automation](images/browser_automation.png) -->
<!-- *Firefox automation handling WhatsApp Web interface* -->

## Security Notes

- Keep your .gitignore updated to exclude sensitive data
- Review configuration files before sharing
- Use environment variables for sensitive credentials
- Regularly backup your database files

## Support

For issues and questions, please check the existing issues or create a new one.

## Next features

- server adapt, bot 24/7 working
- Read messages by itself
