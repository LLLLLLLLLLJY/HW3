#!/usr/bin/env python

import os
from numpy import loadtxt, linspace, meshgrid
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# (a) 生成 LDOS 热力图
def generate_heatmap(file_path):
    data = loadtxt(file_path)
    plt.imshow(data, cmap='hot', origin='lower')
    plt.colorbar(label='LDOS Intensity')
    plt.title(f"LDOS Heatmap: {os.path.basename(file_path)}")

    output_path = os.path.splitext(file_path)[0] + "_heatmap.png"
    plt.savefig(output_path)
    plt.close()

# (b) 生成 LDOS 3D 表面图
def generate_3d_surface(file_path):
    data = loadtxt(file_path)
    x = linspace(0, data.shape[1], data.shape[1])
    y = linspace(0, data.shape[0], data.shape[0])
    X, Y = meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, data, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('LDOS Intensity')
    ax.set_title(f"LDOS 3D Surface: {os.path.basename(file_path)}")

    output_path = os.path.splitext(file_path)[0] + "_3d_surface.png"
    plt.savefig(output_path)
    plt.close()

# (c) 局部区域 LDOS 分析
def analyze_local_region(file_path, region):
    data = loadtxt(file_path)
    x_start, x_end, y_start, y_end = region
    local_ldos = data[y_start:y_end, x_start:x_end]

    avg_ldos = local_ldos.mean(axis=1)
    plt.plot(range(y_start, y_end), avg_ldos)
    plt.xlabel('Position')
    plt.ylabel('Average LDOS')
    plt.title(f"Local LDOS Analysis: {os.path.basename(file_path)}")

    output_path = os.path.splitext(file_path)[0] + "_local_analysis.png"
    plt.savefig(output_path)
    plt.close()

# 处理 `P2` 目录中的所有 .txt 文件
script_dir = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(script_dir):
    if file.endswith(".txt"):
        file_path = os.path.join(script_dir, file)
        generate_heatmap(file_path)
        generate_3d_surface(file_path)
        analyze_local_region(file_path, (10, 30, 10, 30))
