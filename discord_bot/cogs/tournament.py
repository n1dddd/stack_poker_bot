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
        super().__init__(timeout=None)
        self.bot = bot
        self.logger = logger
        self.db_conn = None

    async def create_db_connect(self):
        self.db_conn = await asyncpg.connect(dsn=environ.get("DATABASE_URL"))
        logger.info(f"db connections successful")

    @discord.ui.button(label="Register for Tournament", style=discord.ButtonStyle.green, row=1)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info(f"{interaction.user} -- {interaction.id} -- {interaction.data}")
        await self.create_db_connect()

        get_tourney_information = await self.db_conn.fetchrow(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )

        tournament_information = dict(get_tourney_information)

        logger.info(f"{tournament_information}")

        get_discord_id = await self.db_conn.fetchrow(
            'SELECT * FROM participants WHERE discord_id = $1 AND tournament_id = $2', interaction.user.id, tournament_information["id"]
        )

        if get_discord_id is None:
            await self.db_conn.execute('INSERT INTO participants(discord_id, discord_name, tournament_id) VALUES ($1, $2, $3)', interaction.user.id, interaction.user.name, tournament_information['id'])
            await self.db_conn.execute('UPDATE users SET bankroll = bankroll - $1 WHERE discord_id = $2', tournament_information["stake"], interaction.user.id)
            await self.db_conn.execute('UPDATE tournaments SET payout = payout + $1 WHERE id = $2', tournament_information["stake"], tournament_information["id"])
            await interaction.response.send_message('Registration confirmed', ephemeral=True)
        else:
            await interaction.response.send_message('Already registered for tournament', ephemeral=True)

    @discord.ui.button(label="Un-Register for Tournament", style=discord.ButtonStyle.danger, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info(f"{interaction.user} -- {interaction.id} -- {interaction.data}")

        get_tournament_information = await self.db_conn.fetchrow(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )

        tournament_information = dict(get_tournament_information)

        logger.info(f"{tournament_information}")

        get_discord_id = await self.db_conn.fetchrow(
            'SELECT * FROM participants WHERE discord_id = $1 AND tournament_id = $2', interaction.user.id, tournament_information["id"]
        )

        if get_discord_id:
            await self.db_conn.execute(
                'DELETE FROM participants WHERE discord_id = $1 AND tournament_id = $2', interaction.user.id, tournament_information['id']
                )
            await self.db_conn.execute(
                'UPDATE users SET bankroll = bankroll + $1 WHERE discord_id = $2', tournament_information["stake"], interaction.user.id
                ) 
            await self.db_conn.execute('UPDATE tournaments SET payout = payout - $1 WHERE id = $2', tournament_information["stake"], tournament_information["id"])
            await interaction.response.send_message('You have been unregistered from the tournament', ephemeral=True)
        else:
            await interaction.response.send_message('You are not currently registered for this tournaments', ephemeral=True)

    @discord.ui.button(label="Rebuy into Tournament", style=discord.ButtonStyle.primary, row=3)
    async def rebuy(self, interaction: discord.Interaction, button: discord.ui.Button):
        logger.info(f"{interaction.user} -- {interaction.id} -- {interaction.data}")
        await self.create_db_connect()

        get_tourney_information = await self.db_conn.fetchrow(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )

        tournament_information = dict(get_tourney_information)

        logger.info(f"{tournament_information}")

        get_discord_id = await self.db_conn.fetchrow(
            'SELECT * FROM participants WHERE discord_id = $1 AND tournament_id = $2', interaction.user.id, tournament_information["id"]
        )

        if get_discord_id is None:
            
            await interaction.response.send_message('Not registered for this tournament', ephemeral=True)
        else:
            await self.db_conn.execute('UPDATE participants rebuy_amt = rebuy_amt + 1 WHERE discord_id = $1', interaction.user.id)
            await self.db_conn.execute('UPDATE users SET bankroll = bankroll - $1 WHERE discord_id = $2', tournament_information["stake"], interaction.user.id)
            await self.db_conn.execute('UPDATE tournaments SET payout = payout + $1 WHERE id = $2', tournament_information["stake"], tournament_information["id"])
            await interaction.response.send_message('You have successfully rebought into the tournament', ephemeral=True)

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

        is_ongoing_game = await self.db_conn.fetchrow(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )

        if is_ongoing_game:
            embed = discord.Embed(
            colour=discord.Color.red(),
            title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
        )
            embed.add_field(name="1 Tournament at a Time", value="Hold your horses", inline=False)
            await context.send(embed=embed)

        elif is_ongoing_game is None:
            timeout_seconds = (add_minutes + late_reg_minutes) * 60
            view = Confirm(timeout=timeout_seconds)
            start_time = datetime.now(ZoneInfo("Canada/Eastern")) + timedelta(minutes=add_minutes)

            formatted_start_time = '{:%I:%M %p}'.format(start_time)

            end_time = start_time + timedelta(minutes=late_reg_minutes)

            formatted_end_time = '{:%I:%M %p}'.format(end_time)

            await self.db_conn.execute(
                'INSERT INTO tournaments(stake, payout, ongoing) VALUES ($1, $2, $3)',
                stake, 0, True
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
    async def end(self, context: Context, first : str, second : str, third : str, fourth: str, fifth: str, sixth: str, deal : bool):
        
        await self.create_db_connect()
        get_tournament_information = await self.db_conn.fetchrow(
            'SELECT * FROM tournaments WHERE ongoing = $1', True
        )
        if get_tournament_information is None:
            embed = discord.Embed(
            colour=discord.Color.red(),
            title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
        )
            embed.add_field(name="No Tournaments to End", value="Start One and Invite Mans", inline=False)
            await context.send(embed=embed)
        else:
            tournament_information = dict(get_tournament_information)
            logger.info(tournament_information)

            scrubbed_first_place_id = [int(char) for char in first if char.isdigit()]
            scrubbed_second_place_id = [int(char) for char in second if char.isdigit()]
            scrubbed_third_place_id = [int(char) for char in third if char.isdigit()]
            joined_first_place_id = int(''.join(str(num) for num in scrubbed_first_place_id))
            joined_second_place_id = int(''.join(str(num) for num in scrubbed_second_place_id))
            joined_third_place_id = int(''.join(str(num) for num in scrubbed_third_place_id))


            logger.info(f"{joined_first_place_id}, {joined_second_place_id}, {joined_third_place_id}")



            await self.db_conn.execute(
            'UPDATE tournaments SET first = $1, second = $2, third = $3, ongoing = $4 WHERE id = $5', joined_first_place_id, joined_second_place_id,  joined_third_place_id, False, tournament_information['id']
            )
            if deal == True:
                first_place_payout = int(get_tournament_information["payout"] * 0.65)
                second_place_payout = int(get_tournament_information["payout"] * 0.35)
                await self.db_conn.execute(
                    'UPDATE users SET bankroll = bankroll + $1 WHERE discord_id = $2', first_place_payout, joined_first_place_id
                )
                await self.db_conn.execute(
                    'UPDATE users SET bankroll = bankroll + $1 WHERE discord_id = $2', second_place_payout, joined_second_place_id
                )

            elif deal == False:
                first_place_payout = int(get_tournament_information["payout"])
                await self.db_conn.execute(
                    'UPDATE users SET bankroll = bankroll + $1 WHERE discord_id = $2', first_place_payout, joined_first_place_id
                )
            
            
            embed = discord.Embed(
                colour=discord.Color.dark_gold(),
                title="♥️♣️Boink Gang North American Poker Tour♠️♦️",
            )
            embed.add_field(name="Deal Made?", value=deal, inline=False)

            if deal == True:
                embed.add_field(name="Payout", value=f"First Place: {int(tournament_information['stake'] * 0.65)} || Second Place: {int(tournament_information['stake'] * 0.35)}", inline=False)
            else:
                embed.add_field(name="Payout", value=f"First Place: {(tournament_information['stake'])}", inline=False)

            embed.add_field(name="🥇First Place", value=first, inline=False)
            embed.add_field(name="🥈Second Place", value=second, inline=False)
            embed.add_field(name="🥉Third Place", value=third, inline=False)

            await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Tournaments(bot))
