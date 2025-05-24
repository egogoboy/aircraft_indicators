# Aircraft Indicators on Matplotlib

## Instalation
In root run
``` bash
pip install .
```
## Usage
### Import
``` python
from aircraft_indicators import AttitudeIndicator, HeadingIndicator, DriftAngleIndicator, SpeedIndicator
```

### Initialization
``` python
attitude_widget = AttitudeIndicator(fig, position=[0.7, 0.2, 0.35, 0.35])
heading_widget = HeadingIndicator(fig, position=[0.7, 0.6, 0.35, 0.35])
drift_widget = DriftAngleIndicator(fig, position=[0.01, 0.2, 0.35, 0.35])
speed_widget = SpeedIndicator(fig, position=[0.01, 0.6, 0.35, 0.35])
```

### Update
In your cycle
``` python
attitude_widget.update(pitch, roll)
heading_widget.update(heading)
drift_widget.update(drift)
speed_widget.update(speed_kmh)
```
