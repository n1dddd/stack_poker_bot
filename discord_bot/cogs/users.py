import discord
import settings
import asyncpg
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from os import environ

guild = settings.MY_GUILD
logger = settings.logging.getLogger("bot")

class JoinTournamentButton(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.logger = logger
        self.db_conn = None
    
    async def create_db_connect(self):
        self.db_conn = await asyncpg.connect(dsn=environ.get("DATABASE_URL"))
        logger.info("db connections successful")

    @discord.ui.button(label="Join Poker Database", style=discord.ButtonStyle.green, custom_id='join_pk_db')
    async def join_pk_db(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You are now registered to compete against degenerate gamblers.", ephemeral=True)
        logger.info(f"{interaction.user.id} -- {interaction.id} -- {interaction.data}")
        await self.create_db_connect()
        await self.db_conn.execute('INSERT INTO users(discord_name, discord_id, bankroll) VALUES ($1, $2, $3)', interaction.user.name, interaction.user.id, 0)


class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logger 
        self.db_conn = None

    
    async def create_db_connect(self):
        self.db_conn = await asyncpg.connect(dsn=environ.get("DATABASE_URL"))
        logger.info("db connections successful")

    @commands.hybrid_command(
        name="joinpkdb",
        description="Button to join Discord Poker Database -- Tracks stats"
    )
    @app_commands.guilds(discord.Object(id=guild))
    async def joinpkdb(self, context: Context):
        view = JoinTournamentButton(self)
        embed = discord.Embed(
            colour=discord.Color.dark_gold(),
            title="♥️♣️Join the Poker Database as a Player♠️♦️",
        )
        await context.send(embed=embed, view=view)
        await view.wait()

async def setup(bot) -> None:
    await bot.add_cog(Users(bot))