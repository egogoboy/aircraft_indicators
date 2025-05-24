import numpy as np
from matplotlib import patches, pyplot as plt
from matplotlib.transforms import Affine2D

class AttitudeIndicator:
    def __init__(self, fig, position=[0.8, 0.6, 0.25, 0.25]):
        self.ax = fig.add_axes(position)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.radius = 1

        self.clip_circle = patches.Circle((0.5, 0.5), 0.48, transform=self.ax.transAxes)

        # Draw frame
        border = patches.Circle((0.5, 0.5), 0.48, transform=self.ax.transAxes,
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
                self.ax.plot([x * 0.95, x], [y * 0.95 - 0.1, y - 0.1], 'black', linewidth=1)
                self.roll_labels.append(
                        self.ax.text(x * 0.95 + angle * 0.0022, y - np.abs(angle) * 0.001, f"{abs(angle)}", va='center', ha='center',
                                     fontsize=8, color='black', rotation=-angle, clip_path=self.clip_circle)
                )
            else:
                self.ax.plot([x * 0.9, x], [y * 0.9 - 0.1, y - 0.1], 'black', linewidth=1, clip_path=self.clip_circle)


        # Roll pointer
        self.roll_pointer = patches.RegularPolygon(
            (0, self.radius + 0.1), numVertices=3, radius=0.04,
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
