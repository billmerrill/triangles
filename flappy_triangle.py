import math, random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


edges = np.array(
    [[[-0.5, 1.0], [0.5, 1.0]], [[-0.5, 1.0], [0.0, 0.0]], [[0.5, 1.0], [0.0, 0.0]]]
)
paused = False


class FlappyTriange:

    def __init__(self, edges):
        self.edges = edges
        self.angles = [45.0, 90.0]
        self.lengths = [1.0, 1.0]
        self.angular_velocity = [3, 6]
        self.linear_velocity = [0.01, -0.01]
        self.compute()

    def compute_arm(self, base, angle, length):
        angle_radians = math.radians(angle)
        x_comp = length * math.cos(angle_radians)
        y_comp = length * math.sin(angle_radians)
        return (base[0] + x_comp, base[1] + y_comp)

    def compute(self):
        self.edges[1][1] = np.array(
            self.compute_arm(self.edges[1][0], self.angles[0], self.lengths[0])
        )
        self.edges[2][1] = np.array(
            self.compute_arm(self.edges[2][0], self.angles[1], self.lengths[1])
        )

    def is_triangle(self):
        threshold = 0.01
        x_test = abs(self.edges[1][1][0] - self.edges[2][1][0])
        y_test = abs(self.edges[1][1][1] - self.edges[2][1][1])

        return (x_test < threshold) and (y_test < threshold)

    def tick(self):
        global paused
        if self.is_triangle():
            paused = True

        if not paused:
            self.lengths[0] += self.linear_velocity[0]
            self.lengths[1] += self.linear_velocity[1]
            self.angles[0] = (self.angles[0] + self.angular_velocity[0]) % 360
            self.angles[1] = (self.angles[1] + self.angular_velocity[1]) % 360
            self.compute()

    def update_velocities(self):
        self.linear_velocity[0] = random.uniform(-1, 1) / 100.0
        self.linear_velocity[1] = random.uniform(-1, 1) / 100.0
        self.angular_velocity[0] = random.uniform(-10, 10)
        self.angular_velocity[1] = random.uniform(-10, 10)


def tick(frame):
    # global ax, ft, line
    # ax.clear()
    if not frame % 60:
        ft.update_velocities()
    ft.tick()
    for i, l in enumerate(ft.edges):
        line_objects[i].set_data(ft.edges[i][:, 0], ft.edges[i][:, 1])

    return line_objects


fig, ax = plt.subplots()
ax.set_xlim(-4, 4)
ax.set_ylim(-3, 5)
ax.set_aspect("equal")
ax.axis("off")
line_objects = [ax.plot([], [], lw=2)[0] for _ in range(3)]
for line in line_objects:
    line.set_data([], [])

ft = FlappyTriange(edges)
animation = FuncAnimation(fig, tick, blit=True, interval=20, cache_frame_data=False)
plt.show()
