from generalFunc import *
def van_reached(lit_a, drone_data, littercoor, d, v_drone):

    # Check whether there is still litter left to be taken
    if len(lit_a[0]) > 0:
        # Choose a litter item
            # Randomly
        # nextitemi = rnd.randint(0, len(lit_a[0]) - 1)
        # nextitem = lit_a[0][nextitemi]

            # Closest to van
        mindis = min(lit_a[1])
        nexti = lit_a[1].index(mindis)
        nextitem = lit_a[0][nexti]

        # Remove the chosen litter item from the available list
        liti = lit_a[0].index(nextitem)
        lit_a[0].pop(liti)
        lit_a[1].pop(liti)

        # Calculate the time needed to get to the destination and store
        t_busy, dnext = new_d_t(drone_data[0][d], drone_data[1][d], littercoor[0][nextitem],
                                littercoor[1][nextitem], v_drone)

    else:
        # if there is no litter left, the drone is done
        nextitem = -2
        t_busy = None

    return nextitem, t_busy, lit_a

def recalc_lit_dist(lit_coor, lit_a, gs_x, gs_y):
    distances = []

    for li in range(len(lit_a[0])):
        di = dist(gs_x, lit_coor[0][lit_a[0][li]], gs_y, lit_coor[1][lit_a[0][li]])
        distances.append(di)

    return distances

def plot_update(newxdrone, newydrone, newxvan, newyvan, newxlit, newylit, litterplot, groundplot, droneplot, figure):
    # updating the plot
    litterplot.set_xdata(newxlit)
    litterplot.set_ydata(newylit)

    groundplot.set_xdata(newxvan)
    groundplot.set_ydata(newyvan)

    droneplot.set_xdata(newxdrone)
    droneplot.set_ydata(newydrone)

    figure.canvas.draw()
    figure.canvas.flush_events()