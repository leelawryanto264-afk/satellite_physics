import numpy as np
import math

G = 6.67430e-11         # Gravitational constant
M_EARTH = 5.972e24      # Mass of Earth in kg
R_EARTH = 6371000       # Radius of Earth in m
GM = G * M_EARTH        # Gravitational Parameter of Earth

def circular_vel(alt_m: float) -> float:
    r_mag = R_EARTH + alt_m
    return np.sqrt(GM / r_mag)

def sim_orbit(alt_m: float, spd_factor: float, dur_hrs: float, dt: float, inc_deg: float=45.0):
    dur_secs = dur_hrs * 3600
    steps = int(dur_secs / dt)

    r0_mag = R_EARTH + alt_m
    v_circular = circular_vel(alt_m)
    v0_mag = v_circular * (spd_factor)

    t = np.linspace(0, dur_secs, steps)
    r = np.zeros((steps, 3))
    v = np.zeros((steps, 3))

    inc_rads = math.radians(inc_deg)

    r[0, 0] = r0_mag
    r[0, 1] = 0.0
    r[0, 2] = 0.0
    v[0, 0] = 0.0
    v[0, 1] = v0_mag * math.cos(inc_rads)
    v[0, 2] = v0_mag * math.sin(inc_rads)

    return t, r, np.zeros(steps), np.zeros(steps), R_EARTH