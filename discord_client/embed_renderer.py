import datetime
import hashlib

import discord

from rc3 import RC3Talk


def render_embed(rc3_talk: RC3Talk, username: str):
    embed = discord.Embed(title=f"{rc3_talk.title}",
                          url=f"{rc3_talk.schedule_url}",
                          description=f"{rc3_talk.description[:100]}...",
                          color=string_to_hex(rc3_talk.room))
    embed.set_author(name=f"{rc3_talk.speakers}",
                     icon_url="https://static.rc3.world/hub/plainui/img/favicon.b83b0691003e.ico")
    embed.add_field(name="Start Date", value=f"{rc3_talk.start_date}", inline=True)
    embed.add_field(name="Duration", value=f"{rc3_talk.end_date}", inline=True)
    embed.add_field(name="Speakers", value=f"{rc3_talk.speakers}", inline=True)
    embed.add_field(name="Room", value=f"{rc3_talk.room}", inline=True)
    embed.add_field(name="Track", value=f"{rc3_talk.track}", inline=True)
    embed.add_field(name="Language", value=f"{rc3_talk.language}", inline=True)
    embed.add_field(name="Join URL", value=f"[{rc3_talk.join_url}]({rc3_talk.join_url}])", inline=False)
    embed.set_footer(text=f"fetched for {username} at {str(datetime.datetime.now())}")
    return embed


def string_to_hex(string):
    hashed_string = hashlib.md5(string.encode('utf-8')).hexdigest()
    return int(hashed_string.encode("utf-8").hex()[:6], 16)
