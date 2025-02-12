# Rob-Bot - Discord Game Bot

Rob-Bot is a Discord bot that allows users to play a simple grid-based game in a Discord chat. Players navigate a grid to collect food and avoid enemies, competing for the highest score. The bot uses interactive buttons to control the player's movement and provides real-time updates on the game state.

## Features

- **Grid-based Game**: A player navigates a grid to collect food and avoid an enemy.
- **Interactive Buttons**: Players can move up, down, left, or right using emoji-based buttons.
- **Score Tracking**: Collecting food increases the score, while colliding with an enemy decreases the score.
- **Randomized Game Elements**: Food and enemy positions are randomized each time they interact with the player.
- **Discord Integration**: Fully integrated with Discord using the `discord.py` library, so players can enjoy the game directly in a chat.

## Requirements

- Python 3.7 or higher
- `discord.py` library
- `.env` file with the following variables:
  - `TOKEN`: Your Discord bot token (get it from the [Discord Developer Portal](https://discord.com/developers/applications)).
  - `USER`: The username of the user you want to interact with the bot (used to react to messages).

To install the required dependencies, run:

```bash
pip install discord.py python-dotenv
