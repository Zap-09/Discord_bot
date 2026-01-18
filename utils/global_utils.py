import asyncio

async def delete_message_with_delay(ctx,delete_delay:int = 5):
    """ Deletes a message with a delay. 'delete_delay' is the delay time in mins """
    delete_delay = delete_delay * 60
    await asyncio.sleep(delete_delay)
    await ctx.delete()