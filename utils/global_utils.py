import asyncio
import discord

async def delete_message_with_delay(message, delete_delay: int = 5):
    delete_delay *= 60
    await asyncio.sleep(delete_delay)

    try:
        await message.delete()
    except (discord.NotFound, discord.Forbidden):
        pass