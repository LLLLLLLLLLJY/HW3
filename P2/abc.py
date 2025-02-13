#!/usr/bin/env python

from os.path import isdir
from os import mkdir, listdir
from numpy import array, meshgrid, arange, mean
from matplotlib import pyplot as plt

# 设置数据目录
data_dir = "/root/Desktop/host/HW3/P2/Local_density_of_states_near_band_edge-main"
heatmap_dir = f"{data_dir}/local_density_of_states_heatmap"
height_dir = f"{data_dir}/local_density_of_states_height"

# 确保输出目录存在
if not isdir(heatmap_dir):
    mkdir(heatmap_dir)
if not isdir(height_dir):
    mkdir(height_dir)

# 读取数据
def loadtxt(filename):
    with open(filename) as f:
        return array([list(map(float, line.split(", "))) for line in f])

# 生成热力图
print("Generating heatmaps...")
for file in listdir(data_dir):
    if file.endswith(".txt"):
        level = file.split("_")[-1].split(".")[0]
        data = loadtxt(f"{data_dir}/{file}")
        plt.imshow(data, cmap="hot")
        plt.colorbar()
        plt.title(f"Local Density of States for Level {level}")
        plt.savefig(f"{heatmap_dir}/{level}.png")
        plt.close()

# 生成 3D 高度图
print("Generating height plots...")
for file in listdir(data_dir):
    if file.endswith(".txt"):
        level = file.split("_")[-1].split(".")[0]
        data = loadtxt(f"{data_dir}/{file}")
        x, y = meshgrid(arange(data.shape[1]), arange(data.shape[0]))
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(x, y, data, cmap="hot")
        ax.set_title(f"Local Density of States for Level {level}")
        plt.savefig(f"{height_dir}/{level}.png")
        plt.close()

# 计算局部区域的 LDOS 平均值
def subregion(data):
    return data[180:220, 100:130]  # 选定的局部区域

levels = sorted([file for file in listdir(data_dir) if file.endswith(".txt")])
averages = [mean(subregion(loadtxt(f"{data_dir}/{file}"))) for file in levels]

plt.plot(averages)
plt.xlabel("Level")
plt.ylabel("Average Local Density of States in a Subregion")
plt.savefig(f"{data_dir}/local_density_trend.png")
plt.close()

print("All LDOS plots generated successfully.")
