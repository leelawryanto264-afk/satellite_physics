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
    v0_mag = v_circular * (spd_factor / 100)

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

    def acceleration(pos_vector):
        px, py, pz = pos_vector[0], pos_vector[1], pos_vector[2]
        r_mag = math.sqrt(px**2 + py**2 + pz**2)

        if r_mag < R_EARTH:
            return np.array([0.0, 0.0, 0.0])

        ax = -GM * px / (r_mag**3)
        ay = -GM * py / (r_mag**3)
        az = -GM * pz / (r_mag**3)
        return np.array([ax, ay, az])

    for i in range(steps - 1):
        pos = r[i]
        vel = v[i]

        k1_v = acceleration(pos)
        k1_p = vel

        k2_v = acceleration(pos + k1_p * dt / 2.0)
        k2_p = vel + k1_v * dt / 2.0

        k3_v = acceleration(pos + k2_p * dt / 2.0)
        k3_p = vel + k2_v * dt / 2.0

        k4_v = acceleration(pos + k3_p * dt)
        k4_p = vel + k3_v * dt 

        v[i+1] = vel + (dt / 6.0) * (k1_v + k2_v*2 + k3_v*2 + k4_v)
        r[i+1] = pos + (dt / 6.0) * (k1_p + k2_p*2 + k3_p*2 + k4_p)

    return t, r, np.zeros(steps), np.zeros(steps), R_EARTH