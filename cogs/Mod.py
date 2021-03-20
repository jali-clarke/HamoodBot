import os
import re
import discord
from discord.ext import commands
import asyncio

# from modules.database import *
import modules.checks as checks

try:
    DISCORDSUBHUB = os.environ["DISCORDSUBHUB"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    DISCORDSUBHUB = os.environ.get("DISCORDSUBHUB")


class Mod(commands.Cog):
    """Server Moderation"""

    def __init__(self, bot):
        self.bot = bot
        self.categories = [
            "About",
            "Avatarmemes",
            "Chance",
            "Chemistry",
            "Events",
            "Fonts",
            "Fun",
            "Games",
            "General",
            "Images",
            "Math",
            "Memes",
            "Mod",
            "Pokemon",
            "Reddit",
            "User",
            "Web",
        ]

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, content: commands.clean_content = None):
        """``prefix [new prefix]`` changes the server prefix for Hamood"""
        if content is None:
            return await ctx.send(
                f"**The Server Prefix is: **`{self.bot.prefixes_list.get(ctx.guild.id, '.')}`"
            )

        content = content.replace("@", "").replace("/", "").replace("\\", "")
        if len(content) > 10:
            content = content[:10]

        if content == "":
            return await ctx.send(f"**Cannot Change Server Prefix To: **`{content}`")

        self.bot.prefixes_list[ctx.guild.id] = content
        await self.bot.prefixdb.change_prefix(str(ctx.guild.id), content)

        await ctx.send(f"**Changed Server Prefix To:** `{content}`")

    # @commands.command()
    # @commands.has_permissions(manage_roles=True)
    # async def rainbowroles(self, ctx):
    #     """``rainbowroles`` adds a role color picker"""
    #     await server.create_role(name="it!", hoist=True)

    # @commands.command()
    # @checks.isAllowedCommand()
    # @commands.has_permissions(manage_guild=True)
    # async def subscribe(self, ctx, *, url: commands.clean_content=None):

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        """``kick [@user]`` kicks a tagged member"""
        await member.kick(reason=reason)
        await ctx.send(
            f"{member.mention} was kicked by {ctx.author.mention} | reason `{reason}`"
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        """``ban [@user]`` bans a tagged member"""
        await member.ban(reason=reason)
        await ctx.send(
            f"{member.mention} was kicked by {ctx.author.mention} | reason: `{reason}`"
        )

    @commands.command()
    @checks.isAllowedCommand()
    async def prunes(self, ctx, days: int = 7):
        """``prunes [days]`` returns how many roleless members have not been active on the server"""
        prunes = await ctx.guild.estimate_pruned_members(days=days)
        await ctx.send(
            f"`{prunes} roleless users have not been active for {days} days`"
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(kick_members=True)
    async def deprune(self, ctx, days: int = 30):
        """``deprune [days]`` kicks all pruned members within given date"""
        pruned = await ctx.guild.prune_members(
            days=days, compute_prune_count=True, reason="Inactivity"
        )
        await ctx.send(
            f"`{pruned} have been kicked from the server due to inactivity in the past {days} days!`"
        )

    @commands.command(aliases=["clear"])
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        """``purge [amount]`` deletes chat messages"""
        messages = []
        async for message in discord.abc.Messageable.history(
            ctx.message.channel, limit=int(amount) + 1
        ):
            messages.append(message)

        await ctx.message.channel.delete_messages(messages)
        await ctx.send(f"**{amount} messages were deleted**")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, member: discord.Member, amount=5):
        """``clean [@user] [amount, max=50]`` deletes chat messages from a user"""
        history = await ctx.message.channel.history(limit=100).flatten()
        messages = [msg for msg in history if msg.author.id == member.id]

        amount = int(amount)
        if ctx.message.author == member:
            amount += 1

        messages = messages[:amount] if len(messages) > amount + 1 else messages

        await ctx.message.channel.delete_messages(messages)

        await ctx.send(
            f"`{len(messages)}` of **{member.name}'s** messages have been **deleted!**"
        )

    @commands.command(aliases=["rename"])
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(
        self, ctx, member: discord.Member = None, *, name: commands.clean_content = None
    ):
        """``nickname [@user] [newname]`` changes the nickname of a member"""
        await member.edit(nick=name) if (name != None) else None

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_channels=True)
    async def quickcategory(
        self, ctx, *, name: commands.clean_content = "Quick Channels"
    ):
        """``quickcategory [category]`` Creates a '+' channel which instantly creates a quick voice channel for the user that joins it"""
        category = await ctx.author.guild.create_category(name)
        await ctx.author.guild.create_voice_channel("\u2795", category=category)
        await ctx.send(
            f"{ctx.author.mention} has setup a `quickcategory` named `{name}`"
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_channels=True)
    async def fullcategory(self, ctx, *, name: commands.clean_content = "No Category"):
        """``fullcategory [category]`` Creates a text channel and a '+' voice channel under a category which instantly creates a quick voice channel for the user that joins it"""
        category = await ctx.author.guild.create_category(name)
        await ctx.author.guild.create_voice_channel("\u2795", category=category)
        await ctx.author.guild.create_text_channel(name, category=category)
        await ctx.send(
            f"{ctx.author.mention} has setup a `fullcategory` named `{name}`"
        )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_channels=True)
    async def quickchannel(self, ctx, *, name: commands.clean_content = " "):
        """``quickchannel [name]`` Creates a '+' voice channel that creates quick voice channel for the user that joins it"""
        await ctx.author.guild.create_voice_channel(f"\u2795 {name}")
        await ctx.send(
            f"{ctx.author.mention} has setup a `quickchannel` named `\u2795 {name}`"
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if before.channel is not None:
                if str(before.channel.name) == f"{member.name}'s channel":
                    try:
                        await before.channel.delete()
                    except discord.errors.NotFound:
                        print("Could not delete channel!")

            if after.channel is not None:
                if "\u2795" in str(after.channel.name):
                    channel = await after.channel.clone(name=f"{member.name}'s channel")
                    await member.move_to(channel, reason=None)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def pinboard(self, ctx):
        """``pinboard`` Sets up a pin-board-📌 channel in the server which allows members to 'pin' messages there without needing extra permisions. Add messages to the star board by reacting to them with 📌"""
        channel = discord.utils.get(ctx.guild.channels, name="pin-board-📌")
        if channel is None:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await ctx.guild.create_text_channel(
                "pin-board-📌",
                topic="React to a message with '📌' and it will pop up here.",
                overwrites=overwrites,
            )
            await ctx.send(
                f"{ctx.author.mention} has setup the `pin-board-📌`. Add messages to it by reacting to it with 📌."
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def timeout(self, ctx, hours):
        """``timeout [hours]`` Set a break for yourself from hamood. Max=24. This action cannot be reversed and is applied to every server you are in!"""
        hours = float(hours)
        if hours > 24:
            hours = 24
        time = 3600 * hours
        self.bot.timeout_list.append(ctx.author.id)
        await ctx.send(
            f"{ctx.author.mention} is taking a break for `{self.bot.pretty_time_delta(time)}`"
        )
        await asyncio.sleep(time)
        self.bot.timeout_list.remove(ctx.author.id)
        await ctx.send(f"{ctx.author.mention} your break is done!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if str(payload.emoji) == "📌":
                channel = discord.utils.get(
                    payload.member.guild.channels, name="pin-board-📌"
                )
                if channel is not None and payload.channel_id != channel.id:
                    try:
                        c = await self.bot.fetch_channel(payload.channel_id)
                        msg = await c.fetch_message(payload.message_id)
                    except discord.errors.NotFound:
                        return

                    messages = await channel.history(limit=100).flatten()

                    for m in messages:
                        if len(m.embeds) >= 1:
                            if str(msg.id) in str(m.embeds[0].footer.text):
                                return

                    if len(msg.embeds) >= 1 and "tenor" not in msg.content:
                        embed_dict = msg.embeds[0].to_dict()

                        tit = embed_dict.get("title")
                        desc = embed_dict.get("description")
                        img = embed_dict.get("image")
                        thumb = embed_dict.get("thumbnail")
                        url = embed_dict.get("url")
                        video = embed_dict.get("video")
                        feilds = embed_dict.get("fields")

                        v = (
                            f"[**(link)**]({video['url']})'"
                            if video is not None
                            else ""
                        )
                        embed = discord.Embed(
                            title=tit if tit is not None else None,
                            description=f"{desc if desc is not None else ''}\n{f'[**(link)**]({url})' if url is not None else ''}\n{v}",
                            color=discord.Color.red(),
                            timestamp=msg.created_at,
                        )

                        if img is not None:
                            embed.set_image(url=img["url"])

                        if thumb is not None:
                            embed.set_thumbnail(url=thumb["url"])

                        if feilds is not None and len(feilds) >= 1:
                            for f in feilds:
                                embed.add_field(
                                    name=f["name"],
                                    value=f["value"],
                                    inline=f["inline"],
                                )
                    else:
                        links = re.findall(r"(https?://[^\s]+)", msg.content)
                        new_msg = str(msg.content)
                        for i in range(len(links)):
                            new_msg = new_msg.replace(links[i], f"[(link)]({links[i]})")

                        embed = discord.Embed(
                            description=f"{new_msg[:1800]}",
                            color=discord.Color.red(),
                            # timestamp=msg.created_at,
                        )

                        if len(msg.attachments) >= 1:
                            embed.set_image(url=msg.attachments[0].url)
                        else:
                            if len(links) >= 1:
                                for l in links:
                                    if (
                                        "gif" in l.lower()
                                        or "png" in l.lower()
                                        or "jpg" in l.lower()
                                        or "jpeg" in l.lower()
                                    ):
                                        embed.set_image(url=l)

                    embed.add_field(
                        name="⌵",
                        value=f"{msg.channel.mention} **|** [**#message**]({msg.jump_url}) **|** {msg.author.mention}",
                        inline=False,
                    )
                    embed.set_author(
                        name=f"{msg.author} 📌", icon_url=msg.author.avatar_url
                    )

                    embed.set_footer(
                        text=f"{payload.member} pinned this | ID: {msg.id}",
                        icon_url=payload.member.avatar_url,
                    )

                    pinned = await channel.send(embed=embed)
                    await pinned.add_reaction("<:profane:804446468014473246>")

    # @commands.command()
    # async def hooks(self, ctx):
    #     # content = "\n".join(
    #     #     [
    #     #         f"**{w.name}** - Bound To: **{w.channel.name}**"
    #     #         for w in await ctx.guild.webhooks()
    #     #     ]
    #     # )
    #     try:
    #         webhook = await ctx.channel.create_webhook(name="Hamood's Hook")
    #         print(webhook.url)
    #     except Exception:
    #         print("failed")
    #         pass

    #     bruh = [
    #         w.name for w in await ctx.guild.webhooks() if w.channel_id == ctx.channel.id
    #     ]

    #     await ctx.send(bruh)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.guild)
    async def subscribe(self, ctx, *, channel_url: commands.clean_content):
        """``subscribe [youtube channel url]`` Subscribes the current channel to a youtube channel. Any uploads from the channel will be sent here."""
        if (
            channel_url.startswith("https://www.youtube.com/channel/")
            or channel_url.startswith("https://www.youtube.com/user/")
            or channel_url.startswith("https://www.youtube.com/c/")
        ):
            webhooks = [
                w for w in await ctx.guild.webhooks() if w.channel_id == ctx.channel.id
            ]

            if len(webhooks) >= 1:
                webhook_url = webhooks[0].url
            else:
                try:
                    webhook = await ctx.channel.create_webhook(name="Hamood's Hook")
                    webhook_url = webhook.url
                except Exception:
                    return await ctx.send("`Could not setup webhook!`")

            headers = {
                "channel_url": channel_url,
                "webhook_url": webhook_url,
                "mode": "subscribe",
                "token": DISCORDSUBHUB,
            }

            async with self.bot.aioSession.post(
                "https://discordsubhub.herokuapp.com/subscribe", headers=headers,
            ) as response:
                content = await response.text()

            await ctx.send(f"**{content}**")
        else:
            return await ctx.send("`Invalid Channel Url`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.guild)
    async def unsubscribe(self, ctx, *, channel_url: commands.clean_content):
        """``subscribe [youtube channel url]`` Unsubscribes the current channel from a youtube channel."""
        if (
            channel_url.startswith("https://www.youtube.com/channel/")
            or channel_url.startswith("https://www.youtube.com/user/")
            or channel_url.startswith("https://www.youtube.com/c/")
        ):
            webhooks = [
                w for w in await ctx.guild.webhooks() if w.channel_id == ctx.channel.id
            ]

            if len(webhooks) >= 1:
                webhook_url = webhooks[0].url
            else:
                try:
                    webhook = await ctx.channel.create_webhook(name="Hamood's Hook")
                    webhook_url = webhook.url
                except Exception:
                    return await ctx.send("`Could not setup webhook!`")

            headers = {
                "channel_url": channel_url,
                "webhook_url": webhook_url,
                "mode": "unsubscribe",
                "token": DISCORDSUBHUB,
            }

            async with self.bot.aioSession.post(
                "https://discordsubhub.herokuapp.com/subscribe", headers=headers,
            ) as response:
                content = await response.text()

            await ctx.send(f"**{content}**")
        else:
            return await ctx.send("`Invalid Channel Url`")

    # @commands.command()
    # @checks.isAllowedCommand()
    # @commands.cooldown(1, 5, commands.BucketType.guild)
    # @commands.has_permissions(administrator=True)
    # async def settings(
    #     self, ctx, setting=None, *, value: commands.clean_content = None
    # ):
    #     """``settings [setting] [value]`` update your current server settings for Hamood"""

    #     collection = get_data(database_name="discord", collection_name="servers")
    #     result = collection.find_one({"_id": ctx.guild.id})
    #     categs = result["categories"]
    #     prefix = get_data(database_name="discord", collection_name="prefixes").find_one(
    #         {"_id": ctx.guild.id}
    #     )["prefix"]

    #     if setting is None or value is None:
    #         embed = discord.Embed(
    #             title=f"{ctx.guild.name}'s settings for Hamood",
    #             description=f"Use `{prefix}settings [setting] [value]` to change the value of a setting, for example `{prefix}settings categories fun`.",
    #         )
    #         cat_list = "\n".join(
    #             [f"{i} - {'[ON]' if categs[i] else 'OFF'}" for i in categs]
    #         )
    #         embed.add_field(
    #             name="Current Settings",
    #             value=f"Prefix: `{prefix}`\nCategories:```ini\n{cat_list}```",
    #         )
    #         return await ctx.send(embed=embed)

    #     setting = setting.lower()
    #     if setting == "categories":
    #         value = value.lower().capitalize()
    #         if value not in self.categories:
    #             return await ctx.send(f"`{value} is not a Category!`")

    #         if "," in value:
    #             values = value.replace(" ", "").split(", ")
    #             for v in values:
    #                 categs[v] = True if not categs[v] else False
    #         else:
    #             categs[value] = True if not categs[value] else False

    #         update_server_post(guild_id=ctx.guild.id, name=setting, value=categs)
    #     elif setting == "prefix":
    #         update_prefix_post(guild_id=ctx.guild.id, prefix=value)
    #     else:
    #         await ctx.send("`Unkown Setting`")


def setup(bot):
    bot.add_cog(Mod(bot))

