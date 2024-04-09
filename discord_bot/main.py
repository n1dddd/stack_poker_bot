import settings
import os
import discord
import asyncpg
from asyncpg.pool import create_pool
from discord import app_commands
from discord.ext.commands import Context
from discord.ext import commands
from os import environ

logger = settings.logging.getLogger("bot")
guild = settings.MY_GUILD
intents = discord.Intents.default()
intents.message_content = True


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix='/',
            intents=intents
        )
        self.logger = logger

    async def create_db_pool(self):
        self.pg_con = await asyncpg.create_pool(dsn=environ.get("DATABASE_URL"))
        self.logger.info("db connections successful")

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    async def setup_hook(self) -> None:
        self.logger.info(f"Logged in as {self.user.name}")
        await self.load_cogs()
        await self.create_db_pool()
        await self.pg_con.execute(
            'INSERT INTO users(username, bankroll) VALUES ($1, $2)',
            "n1d", 100
        )

    

    async def on_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error

        

bot = DiscordBot()
bot.run(settings.DISCORD_API_SECRET)























#     async def setup_hook(self):
#         self.logger.info(f"Logged in as {self.user.name}")
#         self.logger.info(f"discord.py API version: {discord.__version__}")
#         self.logger.info("--------------------")
#         await self.load_cogs()



# bot = commands.Bot(command_prefix="/", intents=intents)

# client = MyClient(intents=intents) 

# @client.event
# async def on_ready():
#     print(f'Logged in as {client.user} (ID: {client.user.id})')
#     print('------')
#     await bot.load_extension("cogs.tournament")


# @client.tree.command()
# async def hello(interaction: discord.Interaction):
#     """Says Hello!"""
#     await interaction.response.send_message(f"Hi, {interaction.user.mention}")

# # @client.tree.command()
# # @app_commands.describe(
# #     first_value="`start` or `end` a tournament",
# #     second_value="`$` amount buy in",
# #     third_value="`#` number of minutes until start",
# #     fourth_value="`#` number of minutes until late reg ends (from tournament start)",
# #     fifth_value="`#` amount of rebuys",
# # )

# client.run(settings.DISCORD_API_SECRET)