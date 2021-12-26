import logging
import os

from discord_client import RC3EmbedBot

DISCORD_SECRET = os.environ.get('DISCORD_SECRET')


def get_secret_from_environment() -> str:
    if DISCORD_SECRET is None:
        logging.error("No discord_client secret submitted! Exiting...")
        quit()

    return DISCORD_SECRET


def main() -> None:
    bot = RC3EmbedBot()
    bot.run(get_secret_from_environment())


if __name__ == '__main__':
    main()
