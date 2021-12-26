import discord

from discord_client.file import get_file
from rc3 import url
from rc3.parser import RC3TalkParser
from discord_client import file
from discord_client import embed_renderer


class RC3EmbedBot(discord.Client):
    async def on_ready(self) -> None:
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message) -> None:
        if url.message_is_rc3_schedule_link(message.content):
            rc3_schedule_url = message.content

            parser = RC3TalkParser(rc3_schedule_url)
            rc3_talk = await parser.parse_rc3_schedule_url(rc3_schedule_url)

            embed = embed_renderer.render_embed(rc3_talk, message.author)
            ical = get_file(rc3_talk.get_ical_byte_list(), rc3_talk.title)

            await message.channel.send(embed=embed)
            await message.channel.send(file=ical)
            await message.delete()
