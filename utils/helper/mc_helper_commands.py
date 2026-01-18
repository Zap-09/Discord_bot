import math

def to_number(s):
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Cannot convert {s!r} to number")


async def find_nether_fortress(ctx, player_x: float, player_y: float, player_z: float):
    if player_y:
        # this is here cause when copy from minecraft y is also given.
        # And it's annoying to delete it from the message.
        pass
    x = math.floor(player_x / 480) * 480
    z = math.floor(player_z / 480) * 480

    possible_cord1 = f"X = {x + 104}, Z = {z + 104}"
    possible_cord2 = f"X = {x + 208}, Z = {z + 208}"
    possible_cord3 = f"X = {x + 312}, Z = {z + 312}"

    await ctx.send(f"Possible Fortress at:\n {possible_cord1} \n {possible_cord2} \n {possible_cord3}")