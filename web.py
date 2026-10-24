import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import orbit_engine as engine

# Interactive Web Setup
st.set_page_config(page_title="Modular Satellite Simulation", layout="wide")
st.title("Satellite Simulator Dashboard")
st.markdown("This is a browser-based simulation that is designed to model and visualize satellite trajectories. ")
plt.style.use("dark_background")

st.sidebar.header("Settings")
view_mode = st.sidebar.radio(
    "Select Display Mode:", 
    ["2D Orbit View", "3D Orbit View", "Physics Explanations"]
)
st.sidebar.markdown("---")
st.sidebar.subheader("Initial Variables")
alt_km = st.sidebar.slider("Initial Orbital Altitude (km)", 300, 2000, 500)
alt_m = alt_km * 1000
speed_bar = st.sidebar.slider("Speed Magnitude Scale (%)", 50, 150, 100)
inc_degree = st.sidebar.slider("Orbit Inclination Angle (Degrees)", 0, 90, 45, step=5)

st.sidebar.header("Time Parameters")
dur_hours = st.sidebar.slider("Simulation Tracking Vector Scope (Hours)", 1, 12, 4)
dt_step = st.sidebar.slider("Integration Step Intervals (Seconds)", 1, 60, 5)

@st.cache_data
def get_cached_data(altitude, speed, duration, dt, inclination):
    return engine.simulate_orbit(
        altitude_m = altitude,
        speed_factor = speed,
        duration_hours = duration,
        dt = dt,
        inclination_deg = inclination
    )


t_arr, r_coords, alt_track, speed_track, earth_radius = get_cached_data(
    alt_m, speed_bar, dur_hours, dt_step, inc_degree
)

# Satellite Animation
st.sidebar.markdown("---")

st.sidebar.subheader("Animation Controls")
total_steps = len(t_arr)
current_step = st.sidebar.slider("Simulation Timeline", 0, total_steps -1, 0, help="slide to move the satellite(gonna change later)")
sat_now = r_coords[current_step] / 1000
hours_passed = t_arr[current_step] / 3600
show_label = st.sidebar.checkbox("Show Numbers", value=True)

# Tracks telementary values
re_entered = alt_track[-1] <= 0
max_alt_km = alt_track.max() / 1000
max_vel_kms = speed_track.max() / 1000

# Header Display
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Satellite Tracking Status", "Crashed" if re_entered else "Active Orbit")
metric_col2.metric("Max Altitude Recorded", f"{max_alt_km:.2f} km")
metric_col3.metric("Max Speed Trajectory Velocity", f"{max_vel_kms:,.2f} km/s")

st.info(f"Showing current satellite position at: {hours_passed:.2f} Hours")

st.markdown("---")

# 2D Toggle
if view_mode == "2D Orbit View":
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 5.5))

    earth = plt.Circle((0, 0), earth_radius / 1000, color='royalblue', alpha=0.35, label="Earth")
    ax_left.add_patch(earth)
    ax_left.plot(r_coords[:, 0] / 1000, r_coords[:, 1] / 1000, color='crimson', linewidth=2, label="Flight Path")
    ax_left.scatter(r_coords[0, 0] / 1000, r_coords[0, 1] / 1000, color='chartreuse', s=120, zorder=5, label="Deploy Point")
    ax_left.scatter(sat_now[0], sat_now[1], color="lime", edgecolor="black", marker="o", s=200, zorder=5, label="Satellite")

    bound = (np.linalg.norm(r_coords, axis=1).max() / 1000) * 1.2
    ax_left.set_title("Flat Plane View")
    ax_left.set_xlim(-bound, bound)
    ax_left.set_ylim(-bound, bound)
    ax_left.set_aspect('equal', 'box')
    ax_left.grid(True, alpha=0.3)
    ax_left.legend()
    ap = np.argmax(alt_track)
    pe = np.argmin(alt_track)
    ap_x, ap_y = r_coords[ap, 0] / 1000, r_coords[ap, 1] / 1000
    pe_x, pe_y = r_coords[pe, 0] / 1000, r_coords[pe, 1] / 1000
    ax_left.scatter(ap_x, ap_y, color="purple", s=150, zorder=5)
    ax_left.text(ap_x, ap_y, f"Apogee: {alt_track[ap] / 1000:.0f} km")
    if alt_track[pe] > 0:
        ax_left.scatter(pe_x, pe_y, color="magenta", s=150, zorder=5)
        ax_left.text(pe_x, pe_y, f"Perigee: {alt_track[pe] / 1000:.0f} km")

    fig.tight_layout(pad=3.0)

    ax_right.plot(t_arr / 3600, speed_track /1000, color='darkturquoise', linewidth=2)
    ax_right.ticklabel_format(axis="y", style="plain", useOffset=False)
    ax_right.set_title("Velocity Curve Performance")
    ax_right.set_xlabel("Time (Hours)")
    ax_right.set_ylabel("Speed (km/s)")
    ax_right.grid(True, alpha=0.3)

    if not show_label:
        ax_left.set_xticklabels([])
        ax_left.set_yticklabels([])

    st.pyplot(fig)

# 3D Toggle
elif view_mode == "3D Orbit View":
    fig = plt.figure(figsize=(14, 6))
    ax_left = fig.add_subplot(1, 2, 1, projection='3d')

    st.sidebar.markdown("---")
    st.sidebar.subheader("3D Camera Controls")
    rotate_vert = st.sidebar.slider("Vertical rotation", -90, 90, 30, step=5)
    rotate_horiz = st.sidebar.slider("Horizontal rotation", -180, 180, -60, step=5)
    ax_left.view_init(elev=rotate_vert, azim=rotate_horiz)

    u = np.linspace(0, 2 * np.pi, 15)
    v = np.linspace(0, np.pi, 15)
    earth_x = (earth_radius / 1000) * np.outer(np.cos(u), np.sin(v))
    earth_y = (earth_radius / 1000) * np.outer(np.sin(u), np.sin(v))
    earth_z = (earth_radius / 1000) * np.outer(np.ones(np.size(u)), np.cos(v))
    ax_left.plot_wireframe(earth_x, earth_y, earth_z, color='royalblue', alpha=0.2, linewidth=0.8, label='Earth')

    sat_x = r_coords[:, 0] / 1000
    sat_y = r_coords[:, 1] / 1000
    sat_z = r_coords[:, 2] / 1000
    ax_left.plot(sat_x, sat_y, sat_z, color='crimson', linewidth=2, label='Flight Path')
    
    ax_left.scatter(sat_x[0], sat_y[0], sat_z[0], color='chartreuse', s=100, zorder=5, label='Deployment Point')
    ax_left.scatter(sat_now[0], sat_now[1], sat_now[2], color="lime", edgecolor="black", marker="o", s=200, zorder=5, label="Satellite")

    max_bound = (np.linalg.norm(r_coords, axis=1).max() / 1000) * 1.1
    ax_left.set_title("3D Space Domain Map")
    ax_left.set_xlim(-max_bound, max_bound)
    ax_left.set_ylim(-max_bound, max_bound)
    ax_left.set_zlim(-max_bound, max_bound)
    ax_left.legend()

    ax_right = fig.add_subplot(1, 2, 2)
    ax_right.plot(t_arr / 3600, speed_track / 1000, color='darkturquoise', linewidth=2)
    ax_right.ticklabel_format(axis="y", style="plain", useOffset=False)
    ax_right.set_title("Velocity Curve Performance")
    ax_right.set_xlabel("Time (Hours)")
    ax_right.set_ylabel("Speed (km/s)")
    ax_right.grid(True, alpha=0.3)

    ap = np.argmax(alt_track)
    pe = np.argmin(alt_track)
    ap_x, ap_y, ap_z = r_coords[ap, 0] / 1000, r_coords[ap, 1] / 1000, r_coords[ap] / 1000
    pe_x, pe_y, pe_z = r_coords[pe, 0] / 1000, r_coords[pe, 1] / 1000, r_coords[pe] / 1000
    ax_left.scatter(ap_x, ap_y, ap_z, color="purple", s=150, zorder=5)
    ax_left.text(ap_x, ap_y, f"Apogee: {alt_track[ap] / 1000:.0f} km")
    if alt_track[pe] > 0:
        ax_left.scatter(pe_x, pe_y, pe_z, color="magenta", s=150, zorder=5)
        ax_left.text(pe_x, pe_y, pe_z, f"Perigee: {alt_track[pe] / 1000:.0f} km")

    fig.tight_layout(pad=3.0)

    if not show_label:
        ax_left.set_xticklabels([])
        ax_left.set_yticklabels([])
        ax_left.set_zticklabels([])

    st.pyplot(fig)

else:
    st.header("Physics Explained")
    st.write("Here is how the mathematical formulas and code model real orbital mechanics: ")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Circular Orbit")
        st.markdown(
        """
        To stay in orbit, the satellite must travel at an exact speed. 
        The function (calculate_circular_velocity) balances the pull 
        from Earth's gravitational pull with the centrifugal force of the satellite's speed
        """
    )
        st.latex(r"G \frac{M \cdot m}{r^2} = \frac{m \cdot v^2}{r}")
        st.markdown("**Note: Space distances are measured from the Earth's core (6,371 km) and adds the satellite's surface altitude.")

        st.subheader("Inclination Degree (Tilt)")
        st.markdown(
        """
        Orbits don't stay parallel to Earth's equator, they tilt. Using Trignometry (X, Y, Z)
        the orbit in the flat 2D plane can tilt into the coordinate system of the 3D plane. 
        By passing the inclination angle ($\\theta$) converted into radians for the velocity 
        vector to break into horizontal or vertical components: 
        """
    )
        st.latex(r"v_x = 0.0")
        st.latex(r"v_y = v_{\text{total}} \cdot \sin\theta")
        st.latex(r"v_z = v_{\text{total}} \cdot \cos\theta")

        st.markdown(
        """
        If inclination is 0 degrees: $\\cos(0)=1$ and $\\sin(0)=0$ creating an orbit on the equator.
        If inclination is 90 degrees: $\\cos(0)=0$ and $\\sin(90)=1$ launches the satellite over the North and South pole.
        """
        )
        st.subheader("Safety Shield & Freeze Check")
        st.markdown(
        """
        If the satellite crashes, its distance to the core ($r$) shrinks toward zero. The gravity formula is divided by $r_3$, so if it reaches zero it would cause a large crash
        To protect it from crashing, the engine uses a **freeze check** every frame:
        ```python
        if np.linalg.norm(r[i+1]) < R_EARTH:
        r[i+1:] = r[i+1]
        v[i+1:] = np.array([0, 0, 0])
        break
        ```
        r is the giant matrix containing all the satellite's positions.
        Checks if the satellite is crashing into Earth, if yes then it freezes all the coordinates and breaks the calculation loop early.
        """
        )

    with col_right:
        st.subheader("RK4 Math Engine & Timesteps")
        st.markdown(
        """
        Physics formulas shows one exact moment for acceleration, but the computer needs to simulate in snapshots called Time steps ($Delta t$)
        To avoid glitches and simulation drifts, the engine uses Runge-Kutta 4th Order (RK4) integration. It uses 4 mini points inside one step to find an accurate weighted average:

        $k_1$ Checks acceleration at the start of the interval
        $k_2$ Takes a half-step using $k_1$'s slope to test the graity at the  midpoint
        $k_3$ Resets and takes another second half step front based on $k_2$
        $k_4$ Takes a full step across the interval using $k_3$'s slope
        
        Combine the slopes using the weighted average formula where the mid steps get double weights:
        """
        )
        st.latex(r"y_{i+1} = y_i + \frac{\Delta t}{6}(k_1 + 2*k_2 + 2*k_3 + k_4)")

        st.subheader("Computer Memory & Pre-allocation")
        st.markdown(
        """
        Instead of calculating the numbers one by one, the storage data grid can be allocated using numpy arrays to process the numbers faster.
        The matrix grids track the channels for every timestep snapshot. It ensures that the graphics load in a fraction of  second.

        ```python
        t = np.linspace(0, duration_seconds, steps)
        r = np.zeros((steps, 3))
        v = np.zeros((steps, 3))
        ```
        """
        )
      