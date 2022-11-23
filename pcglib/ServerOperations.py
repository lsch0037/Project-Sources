from GlobalVariables import mc

def set_block(pos, id, verbose=False):
    mc.setBlock(pos[0], pos[1], pos[2], id)

    if verbose:
        mc.postToChat("Set Block")

#Sets a rectangle between corners pos1 and pos2 to block with given id:w
def fill(pos1, pos2, id):
    mc.setBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2], id)

def query_block(pos):
    return mc.getBlock(pos[0], pos[1], pos[2])

def query_blocks(pos1, pos2):
    return mc.getBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2])