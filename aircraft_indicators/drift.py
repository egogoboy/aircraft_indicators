import numpy as np
from matplotlib import patches, pyplot as plt
from matplotlib.transforms import Affine2D


class DriftAngleIndicator:
    def __init__(self, fig, position=[0.1, 0.1, 0.25, 0.25]):
        self.ax = fig.add_axes(position)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('black')
        self.ax.axis('off')

        self.clip_circle = patches.Circle((0.5, 0.5), 0.45, transform=self.ax.transAxes)
        self.radius = 1

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

        self.drift_pointer = patches.RegularPolygon(
            (0, self.radius - 0.2), numVertices=3, radius=0.07,
            orientation=np.radians(0), color='red', zorder=10
        )
        self.ax.add_patch(self.drift_pointer)

        for angle in range(-120, 121, 10):
            rad = np.radians(angle)
            x_inner = np.sin(rad) * (self.radius - ((angle % 30 == 0) * 0.05))
            y_inner = np.cos(rad) * (self.radius - ((angle % 30 == 0) * 0.05))
            x_outer = np.sin(rad) * (self.radius + 0.1)
            y_outer = np.cos(rad) * (self.radius + 0.1)

            tick, = self.ax.plot([x_inner, x_outer], [y_inner, y_outer], color='white')

            if angle % 30 == 0:
                label = self.ax.text(
                    np.sin(rad) * 0.8,
                    np.cos(rad) * 0.8,
                    f"{angle // 3}",
                    ha='center',
                    va='center',
                    fontsize=10,
                    color='white'
                )

        # Value display
        self.value_text = self.ax.text(0, 0, "Drift: 0°", ha='center', va='top', fontsize=10, color='white')


    def update(self, drift_angle):
        self.drift_pointer.set_transform(Affine2D().rotate_deg(-drift_angle)+ self.ax.transData)
        self.value_text.set_text(f"Drift: {drift_angle:+.0f}°")
