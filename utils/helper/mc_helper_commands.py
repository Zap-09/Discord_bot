import math

def to_number(s):
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Cannot convert {s!r} to number")


async def find_nether_fortress(ctx, player_x: float, player_y: float, player_z: float):
    if player_y:
        # this is here cause when you copy from minecraft y is also given.
        # And it's annoying to delete it from the message.
        pass
    base_x = math.floor(player_x / 480) * 480
    base_z = math.floor(player_z / 480) * 480

    offsets = (100, 200, 300)
    cords = []

    for dx in offsets:
        for dz in offsets:
            cords.append(f"X = {base_x + dx}, Z = {base_z + dz}")

    message = "Possible Fortress/Bastion locations:\n" + "\n".join(cords)
    await ctx.send(message)