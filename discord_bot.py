import asyncio
import discord
from discord.ext import commands
import os
import webserver
import dotenv

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



@bot.command(description="Hey hello")
async def hello(ctx):
    await ctx.reply(f"Hello {ctx.author}!")


async def delete_message_with_delay(ctx):
    await asyncio.sleep(DELETE_DELAY)
    await ctx.delete()


@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    if ctx.channel.id == TEMP_CHANNEL_ID:
        await delete_message_with_delay(ctx)


webserver.keep_alive()
bot.run(TOKEN)