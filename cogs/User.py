import random
import urllib.request
import json
import discord
from discord.ext import commands

class User(commands.Cog):
    """Get a User's Information"""
    def __init__(self, bot):
        self.bot = bot
        self.url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
        self.words = json.loads(self.url.read())

    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        """``joined [@user]`` says when a member joined the server"""
        member = ctx.author if not member else member
        await ctx.send(f'{member.name} joined in {member.joined_at}')

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def avatar(self, ctx, member : discord.Member = None):
        """``avatar [@user]`` sends the profile picture of a tagged user"""
        member = ctx.author if not member else member
        
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Avatar - {member}")

        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def roles(self, ctx, member : discord.Member = None):
        """``roles [@user]`` lists the roles of a tagged user"""
        member = ctx.author if not member else member
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Roles - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def userinfo(self, ctx, member: discord.Member = None):
        """``userinfo [@user]`` sends allot of info on a user"""

        member = ctx.author if not member else member
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Nick name:", value=member.display_name)

        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)

        embed.add_field(name="Bot:", value=member.bot)
        embed.add_field(name="Vibe:", value=random.choice(self.words))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(User(bot))  
