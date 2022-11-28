from GlobalVariables import mc
import numpy as np

def set_block(pos, id, replacing=-1):
    if replacing != -1 and query_block(pos) != replacing:
        return

    mc.setBlock(pos[0], pos[1], pos[2], id)

#Sets a rectangle between corners pos1 and pos2 to block with given id
def fill(pos1, pos2, id, replacing=-1):
    if replacing != -1:
        for i in range(pos1[0],pos2[0]+1):
            for j in range(pos1[1],pos2[1]+1):
                for k in range(pos1[2],pos2[2]+1):
                    current_pos = [i,j,k]
                    print(current_pos)
                    set_block(current_pos, id, replacing)

        return
    print("set blocks from ", pos1, " to ", pos2, " to ", id)

    mc.setBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2], id)

def query_block(pos):
    return mc.getBlock(pos[0], pos[1], pos[2])

def query_blocks(pos1, pos2):
    return mc.getBlocks(pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2])



# TODO: TEST THIS
# def set_line(pos1, pos2, id):

#     direction = np.subtract(pos2,pos1)

#     length = get_length(direction)

#     direction = direction / length

#     current_pos = pos1

#     for a in range(0, int(length)):
#         current_pos = current_pos + direction
#         basicOperations.set_block(mc, current_pos, id)