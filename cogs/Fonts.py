import os
import discord
import textwrap
import random
import json
from discord.ext import commands

from modules.image_functions import makeText


blacklist = json.load(
    open(
        f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/blacklist.json"
    )
)["commandblacklist"][f"{os.path.basename(__file__)[:-3].lower()}"]


def isAllowedCommand():
    async def predicate(ctx):
        return ctx.guild.id not in blacklist

    return commands.check(predicate)


class Fonts(commands.Cog):
    """Send Messages With Cool Fonts"""

    def __init__(self, bot):
        self.bot = bot

        self.fontDict = json.load(
            open(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/fonts.json"
            )
        )
        self.colourDict = json.load(
            open(
                f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/colours.json"
            )
        )

        self.direct = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        self.save_location = f"{self.direct}/tempImages"
        self.fonts = f"{self.direct}/fonts"

    async def text_prep(self, ctx, text, font, font_size, colour, wrap=100):
        async with ctx.typing():
            if text == ():
                return

            if font == "random":
                font = random.choice(list(self.fontDict.values()))
            elif font in self.fontDict:
                font = self.fontDict[font]

            font = f"{self.fonts}/{font}"

            if colour == "random":
                colour = tuple(random.choice(list(self.colourDict.values())))
            elif colour not in self.colourDict:
                colour = (255, 255, 255, 255)
            else:
                colour = tuple(self.colourDict[colour])

            text = [text]
            for i in range(len(text)):
                text[i] = textwrap.wrap(text[i], width=wrap)
                for a in range(1, len(text[i])):
                    text[i][a] = "\n" + text[i][a]
                text[i] = " ".join(text[i])
            text = text[0]

            name = (
                self.save_location
                + "/"
                + "".join(random.choice("123456789") for i in range(12))
                + ".png"
            )

            textImg = makeText(text, font, font_size, colour, name)

            await ctx.send(file=discord.File(textImg))

        await ctx.message.delete()
        os.remove(textImg)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def arial(self, ctx, *, content: commands.clean_content):
        """``arial [msg]`` send a message in a arial font"""
        await self.text_prep(
            ctx, content, "arial", 500, "black",
        )

    @commands.command(aliases=["craft"])
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def minec(self, ctx, *, content: commands.clean_content):
        """``minec [msg]`` send a message in a minecraft font"""
        await self.text_prep(
            ctx, content, "minecraft", 500, "yellow2",
        )

    @commands.command(aliases=["tale"])
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def undertale(self, ctx, *, content: commands.clean_content):
        """``undertale [msg]`` send a message in a undertale font"""
        await self.text_prep(
            ctx, content, "undertale", 500, "white",
        )

    @commands.command(aliases=["rick"])
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def morty(self, ctx, *, content: commands.clean_content):
        """``morty [msg]`` send a message in a morty font"""
        await self.text_prep(
            ctx, content, "morty", 500, "green1",
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gta(self, ctx, *, content: commands.clean_content):
        """``gta [msg]`` send a message in a gta font"""
        await self.text_prep(
            ctx, content, "gta", 500, "white",
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enchant(self, ctx, *, content: commands.clean_content):
        """``enchant [msg]`` send a message in a enchant font"""
        await self.text_prep(
            ctx, content, "minecraft-enchantment.ttf", 500, "white",
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unknown(self, ctx, *, content: commands.clean_content):
        """``unknown [msg]`` send a message in a unknown font"""
        await self.text_prep(ctx, content, "unown.ttf", 500, "black", 100)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pokefont(self, ctx, *, content: commands.clean_content):
        """``pokefont [msg]`` send a message in a pokemon font"""
        await self.text_prep(ctx, content, "pokemon", 500, "steelblue2", 100)

    @commands.command(aliases=["sonic"])
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sega(self, ctx, *, content: commands.clean_content):
        """``sega [msg]`` send a message in a sega font"""
        await self.text_prep(ctx, content, "sega", 500, "navy", 100)

    @commands.command(aliases=["sponge"])
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spongebob(self, ctx, *, content: commands.clean_content):
        """``spongebob [msg]`` send a message in a spongebob font"""
        await self.text_prep(ctx, content, "spongebob", 500, "lightblue", 100)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avenger(self, ctx, *, content: commands.clean_content):
        """``avenger [msg]`` send a message in a avenger font"""
        await self.text_prep(ctx, content, "avenger", 500, "red4", 100)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def batman(self, ctx, *, content: commands.clean_content):
        """``batman [msg]`` send a message in a batman font"""
        await self.text_prep(ctx, content, "batman", 500, "black", 100)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def text(self, ctx, *, content: commands.clean_content):
        """``text [msg]`` send a message in a random font"""
        await self.text_prep(ctx, content, "random", 500, "random", 100)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def font(self, ctx, font, colour, *, content: commands.clean_content):
        """``font [font] [colour] [msg]`` send a message in a selected font and colour"""
        await self.text_prep(ctx, content, font, 500, colour, 100)


def setup(bot):
    bot.add_cog(Fonts(bot))

