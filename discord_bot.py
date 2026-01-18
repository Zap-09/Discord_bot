import os

import dotenv

import discord
from discord.ext import commands

import flask_server
from utils import delete_message_with_delay
from utils.helper import find_nether_fortress, to_number


dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]

DELETE_DELAY = 5

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


TEMP_CHANNEL_ID = int(os.getenv("TEMP_CHANNEL_ID"))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,count:str|None = None, by_admin = False):
    """
    Clear messages in the current channel. Use a number or 'all'.
    If 'all' is used 'True' be there after 'all'.

     Examples:
         /clear all True

         /clear 10
    """

    if count is None:
        await ctx.reply("The count must be a number or 'all'", delete_after=5)
        await ctx.message.delete()
        return

    if count == "all":
        if not by_admin:
            await ctx.reply("Please add True after 'all' to confirm",delete_after=5)
            return
        await ctx.channel.purge()
        return

    try:
        count = int(count) + 1
    except ValueError:
        await ctx.reply("The count must be a number", delete_after=5)
        await ctx.message.delete()
        return

    await ctx.channel.purge(limit=count)



@bot.command()
async def fortress(ctx, x: str, y: str, z: str):
    """ Finds 3 possible position where a Fortress/Bastion can generate """
    if ctx.author.bot:
        return

    try:
        x = to_number(x)
        y = to_number(y)
        z = to_number(z)
    except ValueError:
        await ctx.reply("Invalid argument. Please provide a number.", delete_after=10)
        await ctx.message.delete()
        return
    except Exception as e:
        await ctx.reply(f"Unexpected error: {e}")
        return

    await find_nether_fortress(ctx, x, y, z)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == TEMP_CHANNEL_ID:
        await delete_message_with_delay(message,DELETE_DELAY)
    await bot.process_commands(message)


if __name__ == "__main__":
    flask_server.keep_alive()
    bot.run(TOKEN)