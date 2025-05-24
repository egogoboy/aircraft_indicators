import numpy as np
from matplotlib import patches, pyplot as plt
from matplotlib.transforms import Affine2D


class SpeedIndicator:
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

        self._draw_speed_zones()

        self.drift_pointer = patches.RegularPolygon(
            (0, self.radius - 0.2), numVertices=3, radius=0.07,
            orientation=np.radians(0), color='red', zorder=10
        )
        self.ax.add_patch(self.drift_pointer)

        for speed in range(0, 241, 5):
            if speed < 40:
                angle = -150 + speed * (30 / 40)
            else:
                angle = -120 + (speed - 40) * (240 / 200)

            rad = np.radians(angle)
            x_inner = np.sin(rad) * (self.radius + (speed % 20 != 0) * 0.03)
            y_inner = np.cos(rad) * (self.radius + (speed % 20 != 0) * 0.03)
            x_outer = np.sin(rad) * (self.radius + 0.13)
            y_outer = np.cos(rad) * (self.radius + 0.13)
            self.ax.plot([x_inner, x_outer], [y_inner, y_outer], color=('white' if speed != 200 else 'red'), clip_path=self.clip_circle)

            if speed % 20 == 0:
                self.ax.text(
                    np.sin(rad) * 0.85,
                    np.cos(rad) * 0.85,
                    f"{speed}",
                    ha='center',
                    va='center',
                    fontsize=8,
                    color='white',
                    clip_path=self.clip_circle
                )

        # Value display
        self.value_text = self.ax.text(0, 0, "Speed: 0 km/h", ha='center', va='top', fontsize=8, color='white')

    def update(self, speed):
        if speed <= 40:
            angle = -150 + speed * (30 / 40)  # от -150° до -120°
        else:
            angle = -120 + (speed - 40) * (240 / 200)  # от -120° до +120°
        self.drift_pointer.set_transform(Affine2D().rotate_deg(-angle)+ self.ax.transData)
        if speed < 60:
            text_color = 'white'
        elif speed >= 60 and speed < 150:
            text_color = 'lime'
        elif speed >=150 and speed < 200:
            text_color = 'yellow'
        else:
            text_color = 'red'

        self.value_text.set_text(f"Speed: {round(speed, 1)} km/h")
        self.value_text.set_color(text_color)

    def _draw_speed_zones(self):
        def angle_for_speed(speed):
            return -210 + (speed - 40) * (240 / 200)

        # Green zone
        start_angle = angle_for_speed(60)
        end_angle = angle_for_speed(150)
        green_zone = patches.Wedge(
            center=(0, 0),
            r=self.radius + 0.12,
            theta1=-end_angle,
            theta2=-start_angle,
            width=0.1,
            facecolor='green',
            alpha=0.7,
            zorder=-1
        )
        self.ax.add_patch(green_zone)

        # Yellow zone
        start_angle = angle_for_speed(150)
        end_angle = angle_for_speed(200)
        yellow_zone = patches.Wedge(
            center=(0, 0),
            r=self.radius + 0.12,
            theta1=-end_angle,
            theta2=-start_angle,
            width=0.1,
            facecolor='yellow',
            alpha=0.7,
            zorder=-1
        )

        self.ax.add_patch(yellow_zone)
