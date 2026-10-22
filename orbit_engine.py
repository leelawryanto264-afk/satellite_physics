import numpy as np

G = 6.67430e-11         # Gravitational constant
M_EARTH = 5.972e24      # Mass of Earth in kg
R_EARTH = 6371000       # Radius of Earth in m
GM = G * M_EARTH        # Gravitational magnitude

# explainnnn
def calculate_circular_velocity(altitude_m: float) -> float:
    r_magnitude = R_EARTH + altitude_m
    return np.sqrt(GM / r_magnitude)

def simulate_orbit(altitude_m:float, speed_factor: float, duration_hours: float, dt: float):
    # Solves the 2-Body orbital mechanics trajectories using RK4 integration vectors explainn
    duration_seconds = duration_hours * 3600
    steps = int(duration_seconds / dt)

    #
    r0_magnitude = R_EARTH + altitude_m
    v_circular = calculate_circular_velocity(altitude_m)
    v0_magnitude = v_circular * (speed_factor / 100.0)

    # Initialize State Array explain moreee
    t = np.linspace(0,duration_seconds, steps)
    r = np.zeros((steps, 2))
    v = np.zeros((steps, 2))

    r[0] = np.array([r0_magnitude, 0.0])
    v[0] = np.array([0.0, v0_magnitude])

    def get_acceleration(pos_vector):
        r_mag = np.linalg.norm(pos_vector)

        # Sets gravity to 0 if it falls into Earth
        if r_mag < R_EARTH:
            return np.array([0.0, 0.0])
        return -GM * pos_vector / (r_mag**3)

    # Core Numerical Logic Loop (Runge-Kutta 4th Order Integrator) get formullaaa and explain
    for i in range(steps - 1):
        pos = r[i]
        vel = v[i]

        k1_v = get_acceleration(pos)
        k1_p = vel

        k2_v = get_acceleration(pos + k1_p * dt / 2)
        k2_p = vel + k1_v * dt / 2

        k3_v = get_acceleration(pos + k2_p * dt / 2)
        k3_p = vel + k2_v * dt / 2

        k4_v = get_acceleration(pos + k3_p * dt)
        k4_p = vel + k3_v * dt 

        #explain
        v[i+1] = vel + (dt / 6) * (k1_v + k2_v*2 + k3_v*2 + k4_v)
        r[i+1] = pos + (dt / 6) * (k1_p + k2_p*2 + k3_p*2 + k4_p)

        if np.linalg.norm(r[i+1]) < R_EARTH:
            #explain
            r[i+1:] = r[i+1]
            break

    distance = np.linalg.norm(r,axis=1)
    altitude = distance - R_EARTH
    speed = np.linalg.norm(v, axis=1)

    return t, r, altitude, speed, R_EARTH
