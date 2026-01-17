import asyncio
import discord
from discord.ext import commands
import os
import webserver
import dotenv
import math

dotenv.load_dotenv()
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

TOKEN = os.environ["TOKEN"]

DELETE_DELAY = 5 * 60

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


TEMP_CHANNEL_ID = int(os.getenv("TEMP_CHANNEL_ID"))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.message.delete()
        await ctx.send("This command cannot be used in this channel.", delete_after=5)
        return
    await ctx.channel.purge(limit=None)


def to_number(s):
    try:
        return float(s)
    except ValueError:
        pass
    try:
        return int(s)
    except ValueError:
        raise ValueError(f"Cannot convert {s!r} to int or float")



@bot.command()
async def fortress(ctx, x: float|int, y: float|int, z: float|int):
    if ctx.author.bot:
        return

    if x is None or y is None or z is None:
        await ctx.reply("This command need 3 args (x, y, z). Please send all 3.",delete_after=10)
        await ctx.message.delete()
    if x and y and z:
        try:
            x = to_number(x)
            y = to_number(y)
            z = to_number(z)
        except ValueError:
            await ctx.reply("Invalid argument. Please a number or a floating number", delete_after=10)
            await ctx.message.delete()
            return
        except Exception as e:
            await ctx.reply(f"Unexpected error: {e}")
            return

        await find_nether_fortress(ctx,x,y,z)



async def find_nether_fortress(ctx,player_x, player_y, player_z):
    x = math.floor(player_x / 480) * 480
    z = math.floor(player_z / 480) * 480
    if player_y:
        pass

    possible_cord1 = f"X = {x + 104} , Z = {z + 104}"
    possible_cord2 = f"X = {x + 208} , Z = {z + 208}"
    possible_cord3 = f"X = {x + 312} , Z = {z + 312}"

    await ctx.send(f"Possible Fortress at:\n {possible_cord1} \n {possible_cord2} \n {possible_cord3}")


async def delete_message_with_delay(ctx):
    await asyncio.sleep(DELETE_DELAY)
    await ctx.delete()


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == TEMP_CHANNEL_ID:
        await delete_message_with_delay(message)
    await bot.process_commands(message)


webserver.keep_alive()
bot.run(TOKEN)