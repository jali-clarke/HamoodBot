import os
import sys
import discord
import textwrap
import random
import json
from discord.ext import commands

sys.path.insert(
    1, os.path.split(os.getcwd())[0] + "/" + os.path.split(os.getcwd())[1] + "/modules"
)

import image_functions


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
        self.edit = image_functions.Edit(
            None, f"{self.direct}/tempImages", f"{self.direct}/fonts",
        )

    async def textPrep(self, ctx, text, font, font_size, colour, wrap=80):
        async with ctx.typing():
            if text == ():
                return

            if font == "random":
                font = random.choice(list(self.fontDict.values()))
            elif font in self.fontDict:
                font = self.fontDict[font]

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

            name = f"{self.edit.randomNumber()}.png"

            textImg = self.edit.makeText(text, font, font_size, colour, name)
            await ctx.message.delete()
            await ctx.send(file=discord.File(textImg))
        os.remove(textImg)

    @commands.command()
    async def arial(self, ctx, *, content: commands.clean_content):
        """``arial [msg]`` send a message in a arial font"""
        await self.textPrep(ctx, content, "arial", 500, "black", 100)

    @commands.command(aliases=["craft"])
    async def minecraft(self, ctx, *, content: commands.clean_content):
        """``minecraft [msg]`` send a message in a minecraft font"""
        await self.textPrep(ctx, content, "minecraft", 500, "yellow2", 100)

    @commands.command(aliases=["tale"])
    async def undertale(self, ctx, *, content: commands.clean_content):
        """``undertale [msg]`` send a message in a undertale font"""
        await self.textPrep(ctx, content, "undertale", 500, "white", 100)

    @commands.command(aliases=["rick"])
    async def morty(self, ctx, *, content: commands.clean_content):
        """``morty [msg]`` send a message in a morty font"""
        await self.textPrep(ctx, content, "morty", 500, "green1", 100)

    @commands.command()
    async def gta(self, ctx, *, content: commands.clean_content):
        """``gta [msg]`` send a message in a gta font"""
        await self.textPrep(ctx, content, "gta", 500, "white", 100)

    @commands.command()
    async def enchant(self, ctx, *, content: commands.clean_content):
        """``enchant [msg]`` send a message in a enchant font"""
        await self.textPrep(
            ctx, content, "minecraft-enchantment.ttf", 500, "white", 100
        )

    @commands.command()
    async def unknown(self, ctx, *, content: commands.clean_content):
        """``unknown [msg]`` send a message in a unknown font"""
        await self.textPrep(ctx, content, "unown.ttf", 500, "black", 100)

    @commands.command()
    async def pokefont(self, ctx, *, content: commands.clean_content):
        """``pokefont [msg]`` send a message in a pokemon font"""
        await self.textPrep(ctx, content, "pokemon", 500, "steelblue2", 100)

    @commands.command(aliases=["sonic"])
    async def sega(self, ctx, *, content: commands.clean_content):
        """``sega [msg]`` send a message in a sega font"""
        await self.textPrep(ctx, content, "sega", 500, "navy", 100)

    @commands.command(aliases=["sponge"])
    async def spongebob(self, ctx, *, content: commands.clean_content):
        """``spongebob [msg]`` send a message in a spongebob font"""
        await self.textPrep(ctx, content, "spongebob", 500, "lightblue", 100)

    @commands.command()
    async def avenger(self, ctx, *, content: commands.clean_content):
        """``avenger [msg]`` send a message in a avenger font"""
        await self.textPrep(ctx, content, "avenger", 500, "red4", 100)

    @commands.command()
    async def sketch(self, ctx, *, content: commands.clean_content):
        """``sketch [msg]`` send a message in a sketch font"""
        await self.textPrep(ctx, content, "sketch", 500, "random", 100)

    @commands.command()
    async def batman(self, ctx, *, content: commands.clean_content):
        """``batman [msg]`` send a message in a batman font"""
        await self.textPrep(ctx, content, "batman", 500, "black", 100)

    @commands.command()
    async def text(self, ctx, *, content: commands.clean_content):
        """``text [msg]`` send a message in a random font"""
        await self.textPrep(ctx, content, "random", 500, "random", 100)

    @commands.command()
    async def font(self, ctx, font, colour, *, content: commands.clean_content):
        """``font [font] [colour] [msg]`` send a message in a selected font and colour"""
        await self.textPrep(ctx, content, font, 500, colour, 100)


def setup(bot):
    bot.add_cog(Fonts(bot))

