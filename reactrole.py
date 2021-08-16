import discord
from discord.ext import commands
import json


class React(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.react_messages = [875602307033739285,
                               875602205804216321, 875601733819187240]

    # Add reaction
    @commands.command(pass_context=True)
    async def addreact(self, ctx, message_id, emoji):
        if message_id in self.react_messages:
            await self.client.add_reaction(ctx.message, emoji)
            await self.client.say("Reaction added")
        else:
            await self.client.say("Invalid message ID")

    # React role
    @commands.Cog.listener("on_raw_reaction_add")
    async def add_role(self, payload):
        if int(payload.message_id) in self.react_messages:
            guild_id = payload.guild_id
            guild = discord.utils.find(
                lambda g: g.id == guild_id, self.client.guilds)

            with open("reactrole.json") as f:
                data = json.load(f)

                for info in data:
                    if info["emoji"] == payload.emoji.name:
                        role = discord.utils.get(
                            guild.roles, name=info["role"])
                        await payload.member.add_roles(role)

    @commands.Cog.listener("on_raw_reaction_remove")
    async def remove_role(self, payload):
        if int(payload.message_id) in self.react_messages:
            guild_id = payload.guild_id
            guild = discord.utils.find(
                lambda g: g.id == guild_id, self.client.guilds)

            with open("reactrole.json") as f:
                data = json.load(f)
                for info in data:
                    if info["emoji"] == payload.emoji.name:
                        role = discord.utils.get(
                            guild.roles, name=info["role"])
                        await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


def setup(client):
    client.add_cog(React(client))
