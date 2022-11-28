from GlobalVariables import mc

# TODO: ALLOW THE FUNCTION TO REPLACE THINGS
def set_block(pos, id, replacing=-1):
    if replacing != -1 and query_block(pos) != replacing:
        return

    mc.setBlock(pos[0], pos[1], pos[2], id)

#Sets a rectangle between corners pos1 and pos2 to block with given id
# TODO: ALLOW THE FUNCTION TO REPLACE THINGS
def fill(pos1, pos2, id, replacing=-1):
    if replacing != -1:
        for i in range(pos1[0],pos2[0]):
            for j in range(pos1[1],pos2[1]):
                for k in range(pos1[2],pos2[2]):
                    current_pos = [i,j,k]
                    set_block(current_pos, id, replacing)

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