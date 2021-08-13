import discord
from discord.ext import commands
import json


class React(commands.Cog):

    def __init__(self, client):
        self.client = client

    # React role


def setup(client):
    client.add_cog(React(client))
