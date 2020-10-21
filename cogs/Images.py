import os
import discord
from discord.ext import commands

from modules.image_functions import Edit
from modules.web_scraping import scrape


class Images(commands.Cog):
    """Image & Gif Manipulation"""

    def __init__(self, bot):
        self.bot = bot
        self.path = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        self.edit = Edit(None, f"{self.path}/tempImages")

    @commands.command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def deepfry(self, ctx):
        message = await ctx.message.channel.history(limit=20).find(
            lambda m: ".jpg" in str(m.attachments)
            or ".png" in str(m.attachments)
            or ".jpeg" in str(m.attachments)
        )
        exts = ["jpg", "png", "jpeg"]

        for e in exts:
            if e in message.attachments[0].url:
                end = e

        name = f"{self.edit.randomNumber()}.{end}"
        save = f"{self.path}/tempImages/{name}"

        new = f"{self.edit.randomNumber()}.{end}"

        scrape(message.attachments[0].url, save)

        rgbb = self.edit.deep_fry(name, new, end)

        await ctx.send(file=discord.File(rgbb))

        os.remove(rgbb)
        os.remove(save)

    # @commands.command()
    # # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.has_permissions(attach_files=True)
    # async def rgb(self, ctx, image=None):
    #     message = await ctx.message.channel.history(limit=20).find(
    #         lambda m: ".gif" in m.content
    #     )

    #     name = f"{self.edit.randomNumber()}.gif"
    #     save = f"{self.path}/tempImages/{name}"

    #     new = f"{self.edit.randomNumber()}.gif"

    #     scrape(message.content, save)

    #     rgbb = self.edit.gif_rgb(name, new)

    #     await ctx.send(file=discord.File(rgbb))

    #     os.remove(rgbb)
    #     os.remove(save)


def setup(bot):
    bot.add_cog(Images(bot))