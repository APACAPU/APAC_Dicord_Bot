import discord
from discord.ext import commands
import main
import os

cogs = [main]

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=main.Main.get_prefix, intents=intents, help_command=None,
                      activity=discord.Activity(type=discord.ActivityType.competing, name="Vandyck#7726 兄ちゃん戦争"))

for cog in cogs:
    cog.setup(client)

client.run(os.environ.get('TOKEN'))
