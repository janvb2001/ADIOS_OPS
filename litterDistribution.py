from generalFunc import *
import random as rnd

def litterDist(simInput):

    # Setting up the litter data arrays
    lit_avail = [[], []]
    littercoor = [[], []]

    for i in range(simInput["litter_n"]):
        lit_avail[0].append(i)

        xlit = rnd.randint(0, simInput["x_size"])
        ylit = rnd.randint(0, simInput["y_size"])
        littercoor[0].append(xlit)
        littercoor[1].append(ylit)

        d_van = dist(xlit, simInput["ground_stat_pos"][0], ylit, simInput["ground_stat_pos"][1])
        lit_avail[1].append(d_van)

    simInput["lit_avail"] = lit_avail
    simInput["littercoor"] = littercoor

    return simInput
