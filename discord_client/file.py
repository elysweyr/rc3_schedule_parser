import discord


def get_file(ical, title):
    scrubbed_file_name = f"{title.lower().replace(' ', '_')}.ics"
    return discord.File(fp=ical, filename=scrubbed_file_name)
