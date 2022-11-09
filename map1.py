map1 = [
    "                                                                                                 ",
    "                                                                                                 ",
    "                                                                                                 ",
    "                                                                                                 ",
    "                                                                                                 ",
    "              A                                                                                  ",
    "                                                                                                 ",
    "       A                                                                                         ",
    "                                                                                                 ",
    "                                                                                                 ",
    "        DDDDDDD                                                                                  ",
    "                                                                                                 ",
    "S  P           UUUU                       C                                                   F  ",
    "GGGGGGGGSSSSSSSGGGGGGGGGGGGGaGGGGGGGGGGGGGGGGGGGGG   GGGGGGGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   GGGGGGGGGGG   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   DDDDDDDDDDD   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   DDDDDDDDDDD   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   DDDDDDDDDDD   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "                                                     GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG       "
]

barrier1 = [0, 30, 200,3]
vertices1 = [0, 97*30, 0 , 18*30]
# from mario import *
print(len("GGGGGGGGSSSSSSSGGGGGGGGGGGGGaGGGGGGGGGGGGGGGGGGGGG   GGGGGGGGGGG   "))

# def parseMap(self: Map, map: list):
    
#     self.dead_zone.append((relativeCoor2DeCoor(barrier[0]), relativeCoor2DeCoor(barrier[1]), barrier[2]*BLOCKSIZE[0], barrier[3]*BLOCKSIZE[1]))
    
#     for r_num, row in enumerate(map):
#         for c_num, col in enumerate(row):
#             if col == "G":
#                 ground = Ground((relativeCoor2DeCoor(r_num), relativeCoor2DeCoor(c_num)))
#                 self.groundSpriteGroup.add(ground)
#                 self.tileGroup.add(ground)
                
#             elif col == "D":
#                 disappear_tile = DisappearBlock((relativeCoor2DeCoor(r_num), relativeCoor2DeCoor(c_num)))
#                 self.disappear_tiles.append(disappear_tile)
            
#             elif col == "A":
#                 appear_tile = Appear_block((relativeCoor2DeCoor(r_num), relativeCoor2DeCoor(c_num)))
#                 self.tileGroup.add(appear_tile)
                
#             elif col == "a":
#                 airTile = AirTile((relativeCoor2DeCoor(r_num), relativeCoor2DeCoor(c_num)))
#                 self.tileGroup.add(airTile)
                
#             elif col == "F":
#                 self.finish_point = FinishPoint((relativeCoor2DeCoor(r_num-4), relativeCoor2DeCoor(c_num)))
            
#             elif col == "C":
#                 tile = Check_point((relativeCoor2DeCoor(r_num), relativeCoor2DeCoor(c_num)))
#                 self.checkpoint_group.append(tile)