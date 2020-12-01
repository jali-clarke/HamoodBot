import discord
from discord.ext import commands

from modules.image_functions import Modify, Modify_Gif

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


class Avatarmemes(commands.Cog):
    """Custom Avatar Memes"""

    def __init__(self, bot):
        self.bot = bot

        self.direct = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        self.memes = f"{self.direct}/memePics"
        self.save_location = f"{self.direct}/tempImages"

    async def meme_prep(self, ctx, meme_image, members, positions, size):
        async with ctx.typing():
            members = list(members)
            if len(members) == 0:
                members.append(ctx.author)

            ext = meme_image[-3:]
            if ext == "gif":
                meme = Modify_Gif(gif_location=f"{self.memes}/{meme_image}")
            else:
                meme = Modify(image_location=f"{self.memes}/{meme_image}")
                ext = "image"

            for i in range(len(members)):
                avatar = Modify(
                    image_url=str(members[i].avatar_url).replace(".webp", ".png")
                )

                getattr(meme, f"{ext}_add_image")(
                    top_image=avatar.image,
                    coordinates=positions[i][0],
                    top_image_size=size,
                    top_image_rotation=positions[i][1],
                )

            meme = getattr(meme, f"save_{ext}")(location=self.save_location)

            await ctx.send(file=discord.File(meme))
        os.remove(meme)

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def stonks(self, ctx, *avamember: discord.Member):
        """``stonks [@user]`` adds a tagged discord avatar to the 'stonks' meme"""

        await self.meme_prep(
            ctx, "stonksImage.jpg", avamember, [[(65, 20), 0]], (200, 200)
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def worthless(self, ctx, *avamember: discord.Member):
        """``worthless [@user]`` adds a tagged discord avatar to the 'this is worthless' meme"""
        await self.meme_prep(
            ctx, "worthlessImage.jpg", avamember, [[(490, 235), -10]], (450, 450)
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def neat(self, ctx, *avamember: discord.Member):
        """``neat [@user]`` adds a tagged discord avatar to the 'this is pretty neat' meme"""
        await self.meme_prep(
            ctx, "neatImage.jpg", avamember, [[(16, 210), 0]], (270, 270)
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(attach_files=True)
    async def grab(self, ctx, *avamember: discord.Member):
        """``grab [@user]`` adds a tagged discord avatar to the 'grab' meme"""
        await self.meme_prep(
            ctx, "grabImage.jpg", avamember, [[(25, 265), 0]], (150, 150)
        )

    @commands.command()
    @isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def compare(self, ctx, *avamember: discord.Member):
        """``compare [@user1] [@user2]`` compares discord avatars"""
        await self.meme_prep(
            ctx, "blankAvatar.jpg", avamember, [[(0, 0), 0], [(405, 0), 0]], (400, 400)
        )


def setup(bot):
    bot.add_cog(Avatarmemes(bot))

