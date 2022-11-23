from mcpi.minecraft import Minecraft
from time import sleep

mc = Minecraft.create(address="localhost", port=4711)

# Constantly grab the player's position and create
# a new stone block underneath him/her
while True:
    x,y,z = mc.player.getPos()

    # Debug
    print("x: {}, y: {}, z: {}".format(x,y,z))
    
    mc.setBlock(x,y-1,z,1)
    sleep