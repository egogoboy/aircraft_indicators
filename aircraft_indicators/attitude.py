import numpy as np
from matplotlib import patches, pyplot as plt
from matplotlib.transforms import Affine2D

class AttitudeIndicator:
    def __init__(self, fig, position=[0.8, 0.6, 0.25, 0.25]):
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
        self.pitch_range = 90

        # Sky and ground layers
        self.sky = patches.Rectangle((-2, 0), 4, 2, color='skyblue', zorder=0, clip_path=self.clip_circle)
        self.ground = patches.Rectangle((-2, -2), 4, 2, color='saddlebrown', zorder=0, clip_path=self.clip_circle)
        self.ax.add_patch(self.sky)
        self.ax.add_patch(self.ground)

        # The horizon line
        self.horizon_line, = self.ax.plot([-2, 2], [0, 0], 'white', linewidth=1, clip_path=self.clip_circle)

        # Pitch
        self.pitch_lines = []
        self.pitch_labels = []
        pitch_x = 0.3
        for p in range(0, self.pitch_range + 1, 10):
            if pitch_x == 0.3:
                pitch_x = 0.5
            else:
                pitch_x = 0.3

            if p == 0:
                continue
            y = np.tan(np.radians(p)) * 1.0

            line, = self.ax.plot([-pitch_x, pitch_x], [y, y], 'white', linewidth=1, clip_path=self.clip_circle)
            self.pitch_lines.append((p, line))
            line, = self.ax.plot([-pitch_x, pitch_x], [-y, -y], 'white', linewidth=1, clip_path=self.clip_circle)
            self.pitch_lines.append((p, line))

            if p % 20 != 0:
                label_left_up = self.ax.text(-pitch_x - 0.05, y, f"{p}", va='center', ha='right', fontsize=8, color='white', clip_path=self.clip_circle)
                label_right_up = self.ax.text(pitch_x + 0.05, y, f"{p}", va='center', ha='left', fontsize=8, color='white', clip_path=self.clip_circle)
                label_left_down = self.ax.text(-pitch_x - 0.05, -y, f"{p}", va='center', ha='right', fontsize=8, color='white', clip_path=self.clip_circle)
                label_right_down = self.ax.text(pitch_x + 0.05, -y, f"{p}", va='center', ha='left', fontsize=8, color='white', clip_path=self.clip_circle)
                
                self.pitch_labels.extend([label_left_up, label_right_up, label_left_down, label_right_down])

        # Roll
        self.roll_marks = []
        self.roll_labels = []
        for angle in range(-60, 65, 15):
            rad = np.radians(angle)
            x = np.sin(rad) * self.radius
            y = np.cos(rad) * self.radius

            if angle % 30 != 0 and angle != 0:
                self.ax.plot([x * 0.95, x], [y * 0.95 - 0.15, y - 0.15], 'black', linewidth=1)
                self.roll_labels.append(
                        self.ax.text(x * 0.95 + angle * 0.0022, y - np.abs(angle) * 0.001 - 0.05, f"{abs(angle)}", va='center', ha='center',
                                     fontsize=8, color='black', rotation=-angle, clip_path=self.clip_circle)
                )
            else:
                self.ax.plot([x * 0.9, x], [y * 0.9 - 0.1, y - 0.1], 'black', linewidth=1, clip_path=self.clip_circle)


        # Roll pointer
        self.roll_pointer = patches.RegularPolygon(
            (0, self.radius), numVertices=3, radius=0.04,
            orientation=np.radians(180), color='red', zorder=10
        )
        self.ax.add_patch(self.roll_pointer)

        # Central aircraft
        self.aircraft_ref, = self.ax.plot(
            [-0.2, 0, 0.2], [-0.05, 0, -0.05], 'yellow', linewidth=2
        )
        self.aircraft_lines = [self.ax.plot([-0.85, -0.6], [0, 0], 'yellow', linewidth=2),
                                self.ax.plot([0.85, 0.6], [0, 0], 'yellow', linewidth=2)]

        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)

        # Transformation layer
        self.horizon_group = [self.sky, self.ground, self.horizon_line] \
                        + [l for _, l in self.pitch_lines] \
                        + self.pitch_labels

    def update(self, pitch, roll):
        pitch_rad = np.radians(pitch)
        pitch_offset = np.tan(pitch_rad) * 1.0

        # Transformation
        transform = (
            Affine2D()
            .translate(0, -pitch_offset)
            .rotate_deg(-roll)
            + self.ax.transData
        )

        for element in self.horizon_group:
            element.set_transform(transform)

        self.roll_pointer.set_transform(Affine2D().rotate_deg(-roll)+ self.ax.transData)
        self.ax.figure.canvas.draw_idle()
