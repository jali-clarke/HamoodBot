import random
import discord
import asyncio
from discord.ext import commands

import modules.checks as checks
from modules.games.trivia_functions import _Trivia


class Jobs(commands.Cog):
    """Make some money `NEW`"""

    def __init__(self, bot):
        self.bot = bot
        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"
        self.jobs = {}
        self.triviaEmojis = {
            "<:chessA:776347125272412161>": 0,
            "<:chessB:776347122341249044>": 1,
            "<:chessC:776347121694539777>": 2,
            "<:chessD:776347122496831498>": 3,
        }
        self.categs = {
            "General Knowledge": "Gameshow Host",
            "Entertainment: Books": "Librarian",
            "Entertainment: Film": "Director",
            "Entertainment: Music": "Muscian",
            "Entertainment: Musicals & Theatres": "Brodway Director",
            "Entertainment: Television": "Director",
            "Entertainment: Video Games": "Esports Player",
            "Entertainment: Board Games": "Toy Tester",
            "Science & Nature": "Biologist",
            "Science: Computers": "Computer Scientist",
            "Science: Mathematics": "Mathematician",
            "Mythology": "Mythologist",
            "Sports": "Sports Reporter",
            "Geography": "Geologist",
            "History": "History Teacher",
            "Politics": "Politician",
            "Art": "Artist",
            "Celebrities": "Celebrity",
            "Animals": "Veterinarian",
            "Vehicles": "Mechanic",
            "Entertainment: Comics": "Comic Book Store Owner",
            "Science: Gadgets": "Engineer",
            "Entertainment: Japanese Anime & Manga": "Weeb",
            "Entertainment: Cartoon & Animations": "Animator",
        }

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def work(self, ctx):
        """``work`` earn some money"""
        game_id = str(ctx.guild.id) + str(ctx.author.id)
        payout = await self.bot.currency.get_currency(ctx.guild.id, ctx.author.id)
        payout = (
            167
            if payout is None
            else round((payout["bank_max"] // 3) * random.uniform(1.1, 1.5))
        )

        game = _Trivia().get_questions(category="any", difficulty="any", amount=1)[0]

        category = game["category"]

        job_title = self.categs[category]

        embed = discord.Embed(
            title=f"Work | {job_title}",
            description=f"**{game['question']}**",
            timestamp=ctx.message.created_at,
            color=ctx.author.color,
        )

        embed.set_thumbnail(url=ctx.author.avatar_url)

        embed.add_field(name=f"Options", value=f"{game['options_str']}", inline=False)
        embed.add_field(
            name=f"<:blank:794679084890193930>",
            value=f"{ctx.author.mention} you have 15 seconds to answer!\n**Payout:** {self.cash(payout)}",
            inline=False,
        )

        msg = await ctx.send(embed=embed)
        self.jobs[game_id] = {
            "member": ctx.author,
            "msg": msg,
            "game": game,
            "payout": payout,
        }
        for e in self.triviaEmojis:
            await msg.add_reaction(e)

        await asyncio.sleep(15)

        if game_id in self.jobs:
            embed = discord.Embed(
                title="Out Of Time",
                description=f"{ctx.author.mention} you failed the job :(",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at,
            )
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text="You can work again soon")

            try:
                await msg.edit(embed=embed)
                await msg.clear_reactions()
                self.jobs.pop(game_id)
            except Exception:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            game_id = str(payload.guild_id) + str(payload.user_id)
            work = self.jobs.get(game_id)
            if work is not None:
                if payload.message_id == work["msg"].id:
                    if str(payload.emoji) in self.triviaEmojis:
                        if (
                            work["game"]["options"][str(payload.emoji)]
                            == work["game"]["correct_answer"]
                        ):
                            await self.bot.currency.add_member(
                                work["member"].guild.id, work["member"].id
                            )
                            await self.bot.currency.update_wallet(
                                work["member"].guild.id,
                                work["member"].id,
                                work["payout"],
                            )
                            tit = "Correct"
                            desc = f"{work['member'].mention} you completed the job and earned {self.cash(work['payout'])}"
                            color = discord.Color.green()
                        else:
                            tit = "Incorrect"
                            desc = f"{work['member'].mention} you failed the job :("
                            color = discord.Color.red()

                        embed = discord.Embed(
                            title=f"{tit}",
                            description=f"{desc}",
                            color=color,
                            timestamp=work["msg"].created_at,
                        )
                        embed.set_thumbnail(url=work["member"].avatar_url)
                        embed.set_footer(text="You can work again soon")

                        try:
                            await work["msg"].edit(embed=embed)
                            await work["msg"].clear_reactions()
                            self.jobs.pop(game_id)
                        except Exception:
                            return

        # print(game)
        # self.jobs[game_id] = _Trivia(
        #     ctx.author, member, ctx.guild, category, difficulty
        # )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member = None):
        """``steal [@member]`` stealing isn't very nice"""
        if member is not None and member.id != ctx.author.id:
            ran = random.randint(1, 100)

            if ran >= 50:
                victim_bal = await self.bot.currency.get_currency(
                    ctx.guild.id, member.id
                )
                attacker_bal = await self.bot.currency.get_currency(
                    ctx.guild.id, ctx.author.id
                )

                if victim_bal is not None and victim_bal["wallet"] != 0:
                    if ran <= 80:
                        amount = victim_bal["wallet"] * (
                            random.uniform(0.1, 0.7)
                            if random.randint(1, 10) > 5
                            else 0.2
                        )
                    else:
                        amount = attacker_bal["wallet"] * -1 * random.uniform(0.2, 0.8)

                    amount = round(amount)

                    await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
                    await self.bot.currency.add_member(ctx.guild.id, member.id)

                    await self.bot.currency.update_wallet(
                        ctx.guild.id, ctx.author.id, amount
                    )
                    await self.bot.currency.update_wallet(
                        ctx.guild.id, member.id, -1 * amount
                    )

                    if amount > 0:
                        await ctx.send(
                            f"{ctx.author.mention} stole `⌬ {amount:,}` from {member.mention}"
                        )
                    else:
                        await ctx.send(
                            f"{ctx.author.mention} was caught trying to steal from {member.mention} and had to pay them `⌬ {-1*amount:,}`"
                        )

                else:
                    return await ctx.send(
                        f"{ctx.author.mention} you can't steal from someone that's broke"
                    )
            else:
                return await ctx.send(
                    f"{ctx.author.mention} you failed at stealing from {member.mention}"
                )
        else:
            return await ctx.send(
                f"{ctx.author.mention}, who are you trying to steal from?"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def daily(self, ctx):
        """``daily`` Get your daily reward."""
        ready, time, streak = await self.bot.members.is_daily_ready(ctx.author.id)
        if ready:
            await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
            bal = await self.bot.currency.get_currency(ctx.guild.id, ctx.author.id)

            reward = round((bal["bank_max"] / 2) + (100 * streak))

            await self.bot.currency.update_all_wallets(ctx.author.id, reward)

            await self.bot.members.add_member(ctx.author.id)
            await self.bot.members.reset_daily(ctx.author.id)

            embed = discord.Embed(
                title=f"Daily Reward Collected |  `⌬ {reward:,}`",
                description=f"{ctx.author.mention}, {self.cash(reward)} was added to all your wallets.\n \nUse `.daily` again in 24 hours.\n \nYou can vote for Hamood using `.vote` for cooler rewards!",
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
            )
        else:
            embed = discord.Embed(
                title=f"Daily Reward Unavailable",
                description=f"{ctx.author.mention} your daily reward can be collected in ```{time}```\nYou can vote for Hamood using `.vote` for cooler rewards!",
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
            )

        embed.set_footer(text=f"Streak: {streak} Days")
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def fish(self, ctx):
        """``fish`` Maybe you'll catch something"""
        items = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)
        if items is not None:
            if items.get("fishing_rod") is not None:
                await self.bot.inventories.decr_item_amount(
                    ctx.guild.id, ctx.author.id, "fishing_rod", 1
                )

                ran = random.randint(1, 100)

                if ran <= 70:
                    choice = None
                elif ran <= 85:
                    choice = self.bot.common_items
                elif ran <= 95:
                    choice = self.bot.uncommon_items
                elif ran <= 98:
                    choice = self.bot.rare_items
                elif ran <= 99:
                    choice = self.bot.epic_items
                else:
                    ran2 = random.randint(1, 10)
                    if ran2 <= 8:
                        choice = "rare_crate"
                    else:
                        choice = "blackmarket_crate"

                if choice is not None:
                    if choice not in ["rare_crate", "blackmarket_crate"]:
                        reward, v = random.choice(list(choice.items()))
                    else:
                        reward = choice

                    await self.bot.inventories.incr_item_amount(
                        ctx.guild.id, ctx.author.id, reward, 1
                    )

                    embed = discord.Embed(
                        title=f"You Fished `x1` {reward.replace('_', ' ').title()} | ***{self.bot.all_items[reward]['rarity'].upper()}***",
                        description=f"{ctx.author.mention} recieved `{reward}` from fishing!",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(url=self.bot.all_items[reward]["image"])

                else:
                    embed = discord.Embed(
                        title=f"You Fished Out Nothing",
                        description=f"{ctx.author.mention} you fished out nothing :(",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )

                return await ctx.send(embed=embed)

        await ctx.send("`You do not own a fishing rod`")


def setup(bot):
    bot.add_cog(Jobs(bot))
