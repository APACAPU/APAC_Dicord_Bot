import discord
from discord.ext import commands
import json
import requests
from PIL import Image, ImageDraw, ImageFont


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
    @commands.Cog.listener("on_member_join")
    async def join(self, member):
        guild = self.client.get_guild(862713178717814815)
        channel = guild.get_channel(862713178717814818)
        member_count = guild.member_count

        img = Image.open("DISCORD WELCOME-01.png")
        img = img.copy()

        member_im = Image.open(requests.get(
            member.avatar_url, stream=True).raw)
        member_im = member_im.resize((310, 300), Image.LANCZOS)

        img.paste(member_im, (int(1200/3)+25, int(675/4)))
        msg = "Welcome " + member.name + \
            "\n   (Member " + str(member_count) + ")"
        draw = ImageDraw.Draw(img)
        comfortaa = ImageFont.truetype("Comfortaa-Bold.ttf", 60)
        w, h = draw.textsize(msg, font=comfortaa)
        draw.text(((1200-w)/2, (675-h)/8*7), msg,
                  fill="black", font=comfortaa)
        img.save("new.png", "PNG")

        await channel.send(f"Hey {member.mention}, welcome to **APAC!**\n**GET STARTED BY**\n1. Read the rules in <#873865040934076416>\n2. Claim your roles at <#873267204131532820>\n3. Read about the different channels and what they are for at <#873866137140600832>\n4. Read the <#873875922619613244> in case you miss any\n5. Share some stories at <#863299302029393920>, post some memes at <#873187472153149451> and enjoy yourself\n6. Send some feedback at <#863298970456162305> or provide some suggestions at <#873187514561753149>\n", file=discord.File("new.png"))

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
