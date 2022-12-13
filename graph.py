import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import scipy as sp

FINAL_FILE = '4mm_staircase_v1_raw_data.txt'


def graph():
    file_data_path = "output.txt"

    xs = []
    ys = []
    zs = []
    arrays = []

    with open(FINAL_FILE, 'r') as f:
        all_txt = f.read()
        points = all_txt.split('\n')

        for point in points:
            subs = point.split(',')

            print(subs)

            if '' not in subs:
                point_arr = np.array([float(subs[0]), float(subs[1]), float(subs[2])])

                # point_arr = np.array([float(subs[0]), float(subs[1]),
                #                       np.array([float(subs[2]), float(subs[2])-0.01])])
                arrays.append(point_arr)

    point_cloud = np.array(arrays)

    # graphy bit
    ax = plt.axes(projection='3d')
    # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2])

    ax.plot_trisurf(point_cloud[:, 0],
                    point_cloud[:, 1],
                    point_cloud[:, 2],
                    cmap='viridis', edgecolor='none')

    plt.show()

    # z_smooth = sp.ndimage.zoom(point_cloud[:, 2], 1)
    #
    # ax = plt.axes(projection='3d')
    # # ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2])
    #
    # ax.plot_trisurf(point_cloud[:, 0],
    #                 point_cloud[:, 1],
    #                 z_smooth,
    #                 cmap='viridis', edgecolor='none')
    #
    # plt.show()


if __name__ == '__main__':
    graph()