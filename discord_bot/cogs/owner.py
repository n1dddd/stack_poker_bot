import discord
import settings
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

logger = settings.logging.getLogger("bot")

class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logger 

    
    @commands.command(
        name="sync",
        description="Synchronizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be global or guild", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
    name="members",
    description="Grabs all member info",
    )
    @app_commands.describe(scope="Only is scope of guild")
    @commands.is_owner()
    async def members(self, context: Context) -> None:
        for guild in self.bot.guilds:
            for member in guild.members:
                logger.info(f"{member}")

async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))