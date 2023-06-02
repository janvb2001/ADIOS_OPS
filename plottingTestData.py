from matplotlib import pyplot as plt, patches
import numpy as np

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
minimal = []
minimali = []

for i in range(15):
    minimal.append([100000,100000,100000,100000])
    minimali.append([-1,-1,-1,-1])

#Plot around these conditions
n_drones = 8
pathType = 3

for i in range(len(lines)):
    lines[i][3] = int(lines[i][3])

    d_n = int(lines[i][0])
    lines[i][0] = d_n
    if lines[i][4] < minimal[d_n][lines[i][3]]:
        minimal[d_n][lines[i][3]] = lines[i][4]
        minimali[d_n][lines[i][3]] = i

print(minimal)
print(minimali)


n_d = n_drones
plottingi = minimali[n_d][pathType]
print(lines[plottingi])
nom_v = lines[plottingi][1]
nom_spacing = lines[plottingi][2]


plotv_dev = []
plotv_time = []

plotsp_dev = []
plotsp_time = []

plotnd_dev = []
plotnd_time = []

plotpath_dev = []
plotpath_time = []

for i in range(len(lines)):
    if lines[i][1] == nom_v and lines[i][2] == nom_spacing and lines[i][3] == pathType:
        plotnd_dev.append(lines[i][0])
        plotnd_time.append(lines[i][4])
    elif lines[i][0] == n_drones and lines[i][2] == nom_spacing and lines[i][3] == pathType:
        plotv_dev.append(lines[i][1])
        plotv_time.append(lines[i][4])
    elif lines[i][0] == n_drones and lines[i][1] == nom_v and lines[i][3] == pathType:
        plotsp_dev.append(lines[i][2])
        plotsp_time.append(lines[i][4])
    elif lines[i][0] == n_drones and lines[i][1] == nom_v and lines[i][2] == nom_spacing:
        plotpath_dev.append(lines[i][3])
        plotpath_time.append(lines[i][4])


fig, axs = plt.subplots(1,3)

axs[0].set_title("Drone amount deviation")
axs[0].set_xlim([3,16])
axs[0].set_ylim([0,7500])
axs[0].set_ylabel("Total time to clean area [s]")
axs[0].set_xlabel("Amount of drones [-]")
rectangler = patches.Rectangle((3, 0), 20, 3600, edgecolor='orange',
facecolor="green", linewidth=0, alpha = 0.3)
rectangleg = patches.Rectangle((3, 3600), 20,5000, edgecolor='orange',
facecolor="Red", linewidth=0, alpha = 0.3)
axs[0].add_patch(rectangler)
axs[0].add_patch(rectangleg)
s=np.ones(len(plotnd_dev))
s = s * 15
axs[0].scatter(plotnd_dev, plotnd_time, s=s)
axs[0].scatter(n_d, minimal[n_drones][pathType], color="red")
z = np.polyfit(plotnd_dev, plotnd_time, 4)
xs = np.arange(4,15,0.2)
p = np.poly1d(z)
axs[0].plot(xs, p(xs))

axs[1].set_title("Ground drone speed deviation")
axs[1].set_xlim([0.1,1.4])
axs[1].set_ylim([3100,3800])
axs[1].set_xlabel("Speed of ground vehicle [m/s]")
rectangler = patches.Rectangle((0, 3000), 1.5, 600, edgecolor='orange',
facecolor="green", linewidth=0, alpha = 0.3)
rectangleg = patches.Rectangle((0, 3600), 1.5, 1000, edgecolor='orange',
facecolor="Red", linewidth=0, alpha = 0.3)
axs[1].add_patch(rectangler)
axs[1].add_patch(rectangleg)
s=np.ones(len(plotv_dev))
s = s * 15
axs[1].scatter(plotv_dev, plotv_time, s=s)
axs[1].scatter(nom_v, minimal[n_drones][pathType], color="red")
z = np.polyfit(plotv_dev, plotv_time, 5)
xs = np.arange(0.2,1.3,0.01)
p = np.poly1d(z)
axs[1].plot(xs, p(xs))

axs[2].set_title("Spacing of ground drone path deviation")
axs[2].set_xlim([0,20])
axs[2].set_ylim([3100,4000])
axs[2].set_xlabel("Spacing between paths [m]")
rectangler = patches.Rectangle((0, 3000), 20, 600, edgecolor='orange',
facecolor="green", linewidth=0, alpha = 0.3)
rectangleg = patches.Rectangle((0, 3600), 20, 400, edgecolor='orange',
facecolor="Red", linewidth=0, alpha = 0.3)
axs[2].add_patch(rectangler)
axs[2].add_patch(rectangleg)
s=np.ones(len(plotsp_dev))
s = s * 15
axs[2].scatter(plotsp_dev, plotsp_time, s=s)
axs[2].scatter(nom_spacing, minimal[n_drones][pathType], color="red")
z = np.polyfit(plotsp_dev, plotsp_time, 10)
xs = np.arange(0,20,0.1)
p = np.poly1d(z)
axs[2].plot(xs, p(xs))

# plt.title("Drone amount deviation")
# plt.xlim([3,16])
# plt.ylim([0,7500])
# plt.ylabel("Total time to clean area [s]")
# plt.xlabel("Amount of drones [-]")
# rectangler = patches.Rectangle((3, 0), 20, 3600, edgecolor='orange',
# facecolor="green", linewidth=0, alpha = 0.3)
# rectangleg = patches.Rectangle((3, 3600), 20,5000, edgecolor='orange',
# facecolor="Red", linewidth=0, alpha = 0.3)
# # plt.patch(rectangler)
# # plt.patch(rectangleg)
# s=np.ones(len(plotnd_dev))
# s = s * 15
# plt.scatter(plotnd_dev, plotnd_time, s=s)
# plt.scatter(n_d, minimal[n_drones][pathType], color="red")
# z = np.polyfit(plotnd_dev, plotnd_time, 4)
# xs = np.arange(4,15,0.2)
# p = np.poly1d(z)
# plt.plot(xs, p(xs))
# plt.plot([0,15],[3600,3600], color = "green")

plt.show()




