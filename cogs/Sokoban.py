import os
import sys
import asyncio
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import sokoban_functions

class Sokoban(commands.Cog):
    """A simple box pushing game"""
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.themes = [[':black_large_square:', ':red_square:', ':white_large_square:', ':red_square:', ':x:', ':pensive:', ':sweat_smile:'],
        [':black_large_square:', ':orange_square:', ':white_large_square:', ':orange_square:', ':x:', ':sunglasses:', ':sweat_smile:'],
        [':black_large_square:', ':yellow_square:', ':white_large_square:', ':yellow_square:', ':x:', ':partying_face:', ':sweat_smile:'],
        [':black_large_square:', ':green_square:', ':white_large_square:', ':green_square:', ':x:', ':star_struck:', ':sweat_smile:'],
        [':black_large_square:', ':blue_square:', ':white_large_square:', ':blue_square:', ':x:', ':face_with_monocle:', ':sweat_smile:'],
        [':black_large_square:', ':purple_square:', ':white_large_square:', ':purple_square:', ':x:', ':nerd:', ':sweat_smile:'], 
        [':black_large_square:', ':white_large_square:', ':cheese:', ':fork_knife_plate:', ':hole:', ":mouse:", ":mouse_three_button:"],
        [':black_large_square:', ':red_square:', ':white_heart:', ':heart:', ':kiss:', ":kissing:", ":kissing_heart:"],
        [':black_large_square:', ':green_square:', ':carrot:', ':moon_cake:', ':hole:', ":rabbit2:", ":rabbit:"],
        [':black_large_square:', ':orange_square:', ':shell:', ':beach:', ':beach_umbrella:', ":crab:", ":shrimp:"],
        [':black_large_square:', ':milky_way:', ':ringed_planet:', ':star2:', ':sparkles:', ":alien:", ":space_invader:"]]

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def sokoban(self, ctx):
        """``sokoban`` starts a new sokoban game (games auto delete if theres no input for 10 minutes)"""
        game_id = str(ctx.guild.id) + str(ctx.author.id)# if ctx.guild != None else str(ctx.author.id)
        
        try:
            await self.games[game_id].message.delete()
        except KeyError:
            print('new game')

        #max [9, 7]
        self.games[game_id] = sokoban_functions.Soko_ban([5,3], ctx.author, None)

        msg = await ctx.send(embed=discord.Embed(title='Loading... :arrows_counterclockwise:'))
        #await ctx.send(f"{ctx.author.mention}'s Game:")

        currentGame = self.games[game_id]
        currentGame.message = msg 
        currentGame.sprites = self.themes[currentGame.theme_num]
        
        await currentGame.message.add_reaction(u"\u2B05")
        await currentGame.message.add_reaction(u"\u2B06")
        await currentGame.message.add_reaction(u"\u2B07")
        await currentGame.message.add_reaction(u"\u27A1")
        await currentGame.message.add_reaction(u"\U0001F504")
        await currentGame.message.add_reaction(u"\u267B")
        await currentGame.message.add_reaction(u"\U0001F440")
        await currentGame.message.add_reaction('❌')
        
        await self.create_board(game_id)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            game_id = str(payload.guild_id) + str(payload.user_id)# if payload.guild_id != None else str(payload.user_id)
            
            if game_id in self.games:
                currentGame = self.games[game_id]

                if payload.message_id == currentGame.message.id:
                    if (str(payload.emoji) == u"\u2B06"):
                        currentGame.move = 'up'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\u2B06")
                    elif (str(payload.emoji) == u"\u2B07"):
                        currentGame.move = 'down'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\u2B07")
                    elif (str(payload.emoji) == u"\u2B05"):
                        currentGame.move = 'left'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\u2B05")
                    elif (str(payload.emoji) == u"\u27A1"):
                        currentGame.move = 'right'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\u27A1")
                    elif (str(payload.emoji) == u"\U0001F504"):
                        currentGame.move = 'reset'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\U0001F504")
                    elif (str(payload.emoji) == u"\u267B"):
                        currentGame.move = 'shuffle'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\u267B")
                    elif (str(payload.emoji) == u"\U0001F440"):
                        currentGame.move = None

                        currentGame.theme_num += 1
                        if currentGame.theme_num >= len(self.themes):
                            currentGame.theme_num = 0

                        currentGame.sprites = self.themes[currentGame.theme_num]
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\U0001F440")
                    elif (str(payload.emoji) == '❌'):
                        await currentGame.message.delete()
                        self.games.pop(game_id)
                        currentGame.timer.cancel()
                        return
                    elif (str(payload.emoji) == u"\u23E9"):
                        currentGame.move = 'next'
                        await currentGame.message.remove_reaction(member=currentGame.user, emoji=u"\u23E9")

                    await self.create_board(game_id)

    async def overtime(self, gameID):
        await asyncio.sleep(600)
        game = self.games[gameID]
        await game.message.delete()
        self.games.pop(gameID)
                

    async def create_board(self, gameID):

        currentGame = self.games[gameID]
        currentGame.player_move()
        currentGame.draw_board()
        if currentGame.run_level == False:
            currentGame.game_start()
            msg = f"Click Any Button To Go To Level {currentGame.level}:"
            currentGame.moves -= 1
        else:
            msg = f"Sokoban Level {currentGame.level}:"

        embed = discord.Embed(title=msg, description=f"{currentGame.game_grid}", color=currentGame.user.color)
        embed.set_author(name=f"{currentGame.user}'s game", icon_url=currentGame.user.avatar_url)
        # embed.set_thumbnail(url=currentGame.user.avatar_url)
        embed.add_field(name=f"{currentGame.sprites[2]} Boxes Left: {len(currentGame.box_pos) - currentGame.completed}     {currentGame.sprites[5]} Moves: {currentGame.moves}",
        value="------------------------------------")
        #embed.add_field(name=f"{currentGame.user.mention}")
        await currentGame.message.edit(embed=embed)

        try:
            currentGame.timer.cancel()
        except Exception:
            print('no game to delete')

        currentGame.timer = asyncio.create_task(self.overtime(gameID))



def setup(bot):
    bot.add_cog(Sokoban(bot))  