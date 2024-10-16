import numpy as np
import matplotlib.pyplot as plt
import argparse

# Include the parent direcotry of GEP in python path (not nice looking)
import os, sys
sys.path.append(os.path.join(os.getcwd(), ".."))

from Envs.randomMapGenerator import Generator
from Sensors.lidarSensor import Lidar

STEPS = 10

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", help="Map width")
    parser.add_argument("-t", "--height", help="Map height")
    parser.add_argument("-n", "--number", help="Number of obstacles")
    args = parser.parse_args()

    # print(f"W={args.width} H={args.height} N={args.number}")
    gen = Generator(size=[30,30],
                    number_rows=3, number_columns=3,
                    noise=[0.04,0.04],
                    margins=[0.2, 0.2],
                    obstacle_size=[0.1, 0.1])

    map = gen.get_map()

    ldr = Lidar(r=6, channels=32, map=map)

    for step in range(STEPS):

        ego_position = np.array([10+step,10])

        ldr.update(ego_position)
        thetas, ranges = ldr.thetas, ldr.ranges
        indexes = ldr.idx

        xObs = (ego_position[0]+ranges*np.cos(thetas)).astype(float)
        yObs = (ego_position[1]+ranges*np.sin(thetas)).astype(float)
        plt.scatter(yObs, xObs, c='r', alpha=0.6)

        for x,y in zip(xObs, yObs):
            plt.plot([y,ego_position[1]], [x, ego_position[0]],
                     c='r', linewidth=1, alpha=0.6)

        map_copy = map.copy()
        map_copy[indexes[:,0], indexes[:,1]] = 0.5

        plt.imshow(map_copy)
        # plt.show()
        plt.savefig(f"Visible_{step}.png")
        plt.close()
