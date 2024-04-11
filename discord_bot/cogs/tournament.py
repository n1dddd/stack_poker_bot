import discord
import settings
import asyncpg
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from os import environ

guild = settings.MY_GUILD
logger = settings.logging.getLogger("bot")

class Confirm(discord.ui.View):
    def __init___(self, bot):
        self.bot = bot
        self.logger = logger
        self.db_conn = None

    async def create_db_connect(self):
        self.db_conn = await asyncpg.connect(dsn=environ.get("DATABASE_URL"))
        logger.info(f"db connections successful")

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        logger.info(f"{interaction.user} -- {interaction.id} -- {interaction.data}")
        await self.create_db_connect()
        await self.db_conn.execute('INSERT INTO participants(username) VALUES ($1)', interaction.user.name)
        self.value=True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        logger.info(f"{interaction.user} -- {interaction.id} -- {interaction.data}")
        self.value=False
        self.stop()
    
class Tournaments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logger 
        self.db_conn = None

    async def create_db_connect(self):
        self.db_conn = await asyncpg.connect(dsn=environ.get("DATABASE_URL"))
        logger.info("db connections successful")
            
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
        
        await self.create_db_connect()

        is_ongoing_game = await self.db_conn.fetch(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )

        if len(is_ongoing_game) >= 1:
            embed = discord.Embed(
            colour=discord.Color.red(),
            title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
        )
            embed.add_field(name="1 Tournament at a Time", value="Hold your horses", inline=False)
            await context.send(embed=embed)

        elif len(is_ongoing_game) == 0:

            view = Confirm()
            start_time = datetime.now(ZoneInfo("Canada/Eastern")) + timedelta(minutes=add_minutes)

            formatted_start_time = '{:%I:%M %p}'.format(start_time)

            end_time = start_time + timedelta(minutes=late_reg_minutes)

            formatted_end_time = '{:%I:%M %p}'.format(end_time)

            await self.db_conn.execute(
                'INSERT INTO tournaments(stake, payout, first, second, third, ongoing) VALUES ($1, $2, $3, $4, $5, $6)',
                stake, 0, "", "", "", True
            )

            embed = discord.Embed(
                colour=discord.Color.dark_gold(),
                title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
            )
            embed.add_field(name="Tournament Start", value=formatted_start_time, inline=False)
            embed.add_field(name="Buy In", value=(f"${stake} CAD"), inline=False)
            embed.add_field(name="Late registration", value=formatted_end_time, inline=False)
            embed.add_field(name="Allowed Rebuys", value=rebuys, inline=False)

            logger.info(f"attempting db connection")

            await context.send(embed=embed, view=view)
            await view.wait()
 
    
    @tournament.command(
            name="end",
            description="End a poker tournament....example /tournament end 1stplacename 2ndplacename 3rdplacename split"
    )
    @app_commands.guilds(discord.Object(id=guild))
    async def end(self, context: Context, first : str, second : str, third : str, deal : bool):
        
        await self.create_db_connect()
        is_ongoing_game = await self.db_conn.fetch(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )
        if len(is_ongoing_game) == 0:
            embed = discord.Embed(
            colour=discord.Color.red(),
            title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
        )
            embed.add_field(name="No Tournaments to End", value="Start One and Invite Mans", inline=False)
            await context.send(embed=embed)
        else:
            game = []
            for ongoing_game in is_ongoing_game:
                game.append(dict(ongoing_game))
            
            await self.db_conn.execute(
            'UPDATE tournaments SET first = $1, second = $2, third = $3, ongoing = $4 WHERE id = $5', first, second, third, False, game[0]['id']
            )
            logger.info(f"{game}")

            
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
