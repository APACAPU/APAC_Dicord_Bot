import discord
from discord.ext import commands
import json
import PIL


class Main(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Prefix set up
    def get_prefix(self, message):

        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

    @commands.command(aliases=["set"])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)

        await ctx.send(f"The prefix was changed to {prefix}.")

    # Inspect users message for prefix manipulation
    @commands.Cog.listener("on_message")
    async def check_prefix(self, message):

        # Avoid bot to respond to itself
        if message.author == self.client.user:
            return

        # Prefix manipulation
        try:

            if message.mentions[0] == self.client.user:

                with open("prefixes.json", "r") as read:
                    prefixes = json.load(read)

                pre = prefixes[str(message.guild.id)]

                await message.channel.send(f"My prefix for {message.guild.name} is now {pre}.")

        except:
            pass

    # Welcome

    # Kick
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Kick",
                description=f"**{member}** was kicked.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Reason", value=f"{reason}")
            await ctx.send(embed=embed)

    # Ban

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Ban",
                description=f"**{member}** was banned.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Reason", value=f"{reason}")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Main(client))
