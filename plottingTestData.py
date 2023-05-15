import matplotlib.pyplot as plt

f = open("testdata.txt", "r")
lines = []
for x in f:
    x = " " + x
    x = x.split(",")
    data = []
    for l in x:
        l = l.split(" ")
        data.append(float(l[1]))
    lines.append(data)
f.close()

# # of drone, Speed of ground drone, spacing, pathtype, time
drone_n = []
v_ground = []
spacing = []
pathtype = []
times = []
minimal = [10000, 10000, 10000, 10000]

drone_ns = [[],[],[],[]]
v_grounds = [[],[],[],[]]
spacings = [[],[],[],[]]
timess = [[],[],[],[]]

for i in lines:
    i[3] = int(i[3])
    drone_n.append(i[0])
    v_ground.append(i[1])
    spacing.append(i[2])
    pathtype.append(i[3])
    times.append(i[4])

    drone_ns[i[3]].append(i[0])
    v_grounds[i[3]].append(i[1])
    spacings[i[3]].append(i[2])
    timess[i[3]].append(i[4])

    if i[4] < minimal[i[3]]:
        minimal[i[3]] = i[4]

print(minimal)


fig, axs = plt.subplots(3, 3)

axs[0,0].scatter(drone_ns[0], timess[0])
axs[1,0].scatter(v_grounds[0], timess[0])
axs[2,0].scatter(spacings[0], timess[0])

axs[0,1].scatter(drone_ns[1], timess[1])
axs[1,1].scatter(v_grounds[1], timess[1])
axs[2,1].scatter(spacings[1], timess[1])

axs[0,2].scatter(drone_ns[2], timess[2])
axs[1,2].scatter(v_grounds[2], timess[2])
axs[2,2].scatter(spacings[2], timess[2])


plt.show()




