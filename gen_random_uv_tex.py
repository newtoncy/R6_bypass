# -*- coding: utf-8 -*-
# @File    : decode_from_m3u8.py
# @Date    : 2023-07-20
# @Author  : 王超逸
# @Brief   :

from math import ceil
import random
from pathlib import Path

from PIL import Image
import numpy as np

cell_size = 8
width = 1920
height = 1080
num_of_random = ceil(width / cell_size) * ceil(height / cell_size)
col_per_row = ceil(width / cell_size)
random_list = list(range(num_of_random))
random.shuffle(random_list)


def get_rev_random_list():
    global random_list
    ret = [None for i in range(num_of_random)]
    for index, num in enumerate(random_list):
        ret[num] = index
    return ret


rev_random_list = get_rev_random_list()


def coord_to_index(row, col):
    return col_per_row * int(row // cell_size) + int(col // cell_size)


def index_to_coord(index):
    row = int(index // col_per_row)
    col = index % col_per_row
    return row * cell_size, col * cell_size


def get_cell_base_coord(row, col):
    row = row // cell_size * cell_size
    col = col // cell_size * cell_size
    return row, col


def coord_to_uv(row, col):
    u = (col + 0.5) / width
    v = (row + 0.5) / height
    return u, v


def uv_to_coord(u, v):
    row = int(v * height)
    col = int(u * width)
    return row, col


def get_mapped_uv(row, col, map_rule):
    org_index = coord_to_index(row, col)
    org_base_coord = get_cell_base_coord(row, col)
    org_offset = (row - org_base_coord[0], col - org_base_coord[1])
    new_index = map_rule(org_index)
    new_base_coord = index_to_coord(new_index)
    new_coord = (new_base_coord[0] + org_offset[0], new_base_coord[1] + org_offset[1])
    return coord_to_uv(*new_coord)


def save_to_img(data, path: Path):
    # 将 Python 数组转换为 NumPy 数组
    numpy_array = np.array(data)

    # RG两个通道保存U，BA两个通道保存V，这样UV可以达到16位精度
    R = numpy_array[:, :, 0] * 255
    R_int = R.astype(np.uint8)
    G_int = ((R - R_int) * 255).astype(np.uint8)
    B = numpy_array[:, :, 1] * 255
    B_int = B.astype(np.uint8)
    A_int = ((B - B_int) * 255).astype(np.uint8)
    numpy_array = np.dstack([R_int, G_int, B_int, A_int])
    numpy_array = numpy_array.astype(np.uint8)

    # 创建 PIL 图像对象
    image = Image.fromarray(numpy_array)

    # 保存为 PNG 图像
    with path.open("wb") as fp:
        image.save(fp)


uv_map = [[... for _ in range(width)] for _ in range(height)]
rev_uv_map = [[... for _ in range(width)] for _ in range(height)]

if __name__ == '__main__':
    for i in range(height):
        for j in range(width):
            uv_map[i][j] = get_mapped_uv(i, j, lambda x: random_list[x])
            rev_uv_map[i][j] = get_mapped_uv(i, j, lambda x: rev_random_list[x])
    # 测试
    # r, c = uv_to_coord(*uv_map[0][0])
    # assert (0, 0) == uv_to_coord(*rev_uv_map[r][c])
    # r, c = uv_to_coord(*uv_map[10][10])
    # assert (10, 10) == uv_to_coord(*rev_uv_map[r][c])
    save_dir = Path(__file__).resolve().parent
    save_to_img(uv_map, save_dir / "uv_map.png")
    save_to_img(rev_uv_map, save_dir / "rev_uv_map.png")
