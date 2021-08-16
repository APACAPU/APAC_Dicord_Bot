import discord
from discord.ext import commands
import main
import reactrole
import os

cogs = [main, reactrole]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=main.Main.get_prefix, intents=intents, help_command=None,
                      activity=discord.Activity(type=discord.ActivityType.watching, name="Data Science"))

for cog in cogs:
    cog.setup(client)

client.run(os.environ.get('TOKEN'))
