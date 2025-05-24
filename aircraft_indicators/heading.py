import numpy as np
from matplotlib import patches, pyplot as plt
from matplotlib.transforms import Affine2D


class HeadingIndicator:
    def __init__(self, fig, position=[0.1, 0.1, 0.25, 0.25]):
        self.ax = fig.add_axes(position)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.radius = 1

        self.clip_circle = patches.Circle((0.5, 0.5), 0.45, transform=self.ax.transAxes)

        # Draw frame
        border = patches.Circle((0.5, 0.5), 0.45, transform=self.ax.transAxes,
                                facecolor='none', edgecolor='gray', linewidth=2)
        self.ax.add_patch(border)

        self.radius = 1.0
        self.background = patches.Rectangle(
            (-1.2, -1.2), 2.4, 2.4,
            facecolor='black', edgecolor='black', linewidth=1,
            zorder=-2, clip_path=self.clip_circle
        )

        self.ax.add_patch(self.background)

        # Rotating course scale
        self.tick_labels = []
        for angle in range(0, 360, 10):
            rad = np.radians(angle)
            x_inner = np.sin(rad) * (self.radius - 0.14)
            y_inner = np.cos(rad) * (self.radius - 0.14)
            x_outer = np.sin(rad) * (self.radius - 0.07 + ((angle % 30 == 0) * 0.04))
            y_outer = np.cos(rad) * (self.radius - 0.07 + ((angle % 30 == 0) * 0.04))

            tick, = self.ax.plot([x_inner, x_outer], [y_inner, y_outer], color='white')

            label_text = ''
            label = self.ax.text(0, 0, '')
            if angle % 30 == 0:
                if angle in [0, 90, 180, 270]:
                    label_text = {0: 'N', 90: 'E', 180: 'S', 270: 'W'}[angle]
                else:
                    label_text = angle // 10

                label = self.ax.text(
                    np.sin(rad) * 1.05,
                    np.cos(rad) * 1.05,
                    f"{label_text}",
                    ha='center',
                    va='center',
                    fontsize=10,
                    color='white',
                    rotation=-angle,
                    rotation_mode='anchor'
                )
            self.tick_labels.append((angle, label, tick))

        # Central crosshair
        self.pointer, = self.ax.plot([0, 0], [-0.8, 0.8], color='white', linewidth=1)
        self.pointer, = self.ax.plot([-0.8, 0.8], [0, 0], color='white', linewidth=1)
        self.pointer, = self.ax.plot([-0.05, 0, 0.05], [0.7, 0.8, 0.7], color='white', linewidth=1)

        # Exact direction text
        self.heading_text = self.ax.text(
            0.43, 0.4, '000°', ha='center', va='center',
            fontsize=10, color='white'
        )

        self.pointer, = self.ax.plot([0.3, 0.4, 0.5], [0.18, 0.28, 0.18], color='red', linewidth=2)

    def update(self, heading_degrees):
        transform = Affine2D().rotate_deg(-heading_degrees) + self.ax.transData
        for angle, label, item in self.tick_labels:
            item.set_transform(transform)
            label.set_transform(transform)
            label.set_rotation(-angle - heading_degrees)

        heading_str = f"{int(heading_degrees) % 360:03d}°"
        self.heading_text.set_text(heading_str)

        self.ax.figure.canvas.draw_idle()
