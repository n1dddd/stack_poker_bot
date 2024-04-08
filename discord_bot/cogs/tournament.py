import discord
import settings
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime, timedelta

guild = settings.MY_GUILD


class Tournaments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.hybrid_group(
        name="tournament",
        description="Use to see info for bot usage"
    )
    @app_commands.guilds(discord.Object(id=guild))
    async def tournament(self, context: Context) -> None:
        embed = discord.Embed(
            title="**Tournament Command Use**",
            description=(f"....example: /tournament start 10 30 30 2")
        )
        embed.add_field(name="Option 1 (choice)", value="start/end", inline=False)
        embed.add_field(name="Option 2 (Integer)", value="$ Buy In Whole #", inline=False)
        embed.add_field(name="Option 3 (Integer)", value="Minutes to Tournament Start", inline=False)
        embed.add_field(name="Option 4 (Integer)", value="Minutes to Late registration End", inline=False)
        embed.add_field(name="Option 5 (Integer)", value="Number of Allowed Rebuys", inline=False)
        embed.set_footer(text=f"command used was /tournament")
        await context.send(embed=embed)

    @tournament.command(
            name="start",
            description="Used to start a poker tournaments, needs all options....example /tournament start 10 30 30 2"
    )
    @app_commands.guilds(discord.Object(id=guild))
    async def start(self, context: Context, stake : int, add_minutes : int, late_reg_minutes : int, rebuys: int):
        start_time = datetime.now() + timedelta(minutes=add_minutes)

        formatted_start_time = '{:%I:%M %p}'.format(start_time)

        end_time = start_time + timedelta(minutes=late_reg_minutes)

        formatted_end_time = '{:%I:%M %p}'.format(end_time)

        embed = discord.Embed(
            colour=discord.Color.dark_gold(),
            title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
        )
        embed.add_field(name="Tournament Start", value=formatted_start_time, inline=False)
        embed.add_field(name="Buy In", value=(f"${stake} CAD"), inline=False)
        embed.add_field(name="Late registration", value=formatted_end_time, inline=False)
        embed.add_field(name="Allowed Rebuys", value=rebuys, inline=False)

        await context.send(embed=embed)
    
    @tournament.command(
            name="end",
            description="End a poker tournament....example /tournament end 1stplacename 2ndplacename 3rdplacename split"
    )
    @app_commands.guilds(discord.Object(id=guild))
    async def end(self, context: Context, first : str, second : str, third : str, deal : bool):

        embed = discord.Embed(
            colour=discord.Color.dark_gold(),
            title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
        )
        embed.add_field(name="Deal Made?", value=deal, inline=False)
        embed.add_field(name="🥇First Place", value=first, inline=False)
        embed.add_field(name="🥈Second Place", value=second, inline=False)
        embed.add_field(name="🥉Third Place", value=third, inline=False)

        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Tournaments(bot))
