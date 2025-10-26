import discord
from discord.ext import commands
import os
import webserver

CHANNEL_ID = int(os.environ["CHANNEL_ID"])

TOKEN = os.environ["TOKEN"]


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.message.delete()
        await ctx.send("This command cannot be used in this channel.", delete_after=5)
        return
    await ctx.channel.purge(limit=None)


webserver.keep_alive()

bot.run(TOKEN)