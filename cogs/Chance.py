import random
import discord
from discord.ext import commands

import os
import json

blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"][f"{os.path.basename(__file__)[:-3].lower()}"]


def isAllowedCommand():
    async def predicate(ctx):
        return ctx.guild.id not in blacklist

    return commands.check(predicate)


class Chance(commands.Cog):
    """Take a Chance"""

    def __init__(self, bot):
        self.bot = bot
        self.possible_responses = [
            "hell naw",
            "i highley doubt it",
            "how am i supposed to know",
            "i guess its possible",
            "fo sho",
            "maybe",
            "stop asking",
            "yeah",
            "nah",
            "i dont care",
            "ofcourse",
            "not really",
        ]

    @commands.command(
        aliases=[
            "8ball",
            "does",
            "would",
            "should",
            "could",
            "can",
            "will",
            "am i",
            "is",
        ]
    )
    @isAllowedCommand()
    async def eightball(self, ctx):
        """``eightball`` Hamood shakes his magic 8ball"""
        await ctx.send(
            f"{ctx.author.mention}, {random.choice(self.possible_responses)}"
        )

    @commands.command(aliases=["coin"])
    @isAllowedCommand()
    async def flip(self, ctx):
        """``flip`` flips a coin"""
        possible_responses = ["heads", "tails"]
        await ctx.send(f"**{random.choice(possible_responses)}**, {ctx.author.mention}")

    @commands.command(aliases=["dice"])
    @isAllowedCommand()
    async def roll(self, ctx, dice: str):
        """``roll [NdN]`` Rolls a dice in NdN format."""
        rolls, limit = map(int, dice.split("d"))
        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description="For when you wanna settle the score some other way")
    @isAllowedCommand()
    async def choose(self, ctx, *, content: commands.clean_content):
        """``choose [choice1], [choice2], [choice3]`` Chooses between multiple choices."""
        content = content.split(", ")
        await ctx.send(random.choice(content))


def setup(bot):
    bot.add_cog(Chance(bot))

