import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import orbit_engine as engine

# Interactive Web Setup
st.set_page_config(page_title="Modular Satellite Simulation", layout="wide")
st.title("Satellite Simulator Dashboard")
st.markdown("Description do later")

# Used m so have to convert km -> m
st.sidebar.header("Settings")
alt_km = st.sidebar.slider("Initial Orbital Altitude (km)", 300, 2000, 500)
alt_m = alt_km * 1000

speed_bar = st.sidebar.slider("Speed Magnitude Scale", 50, 150, 100)

st.sidebar.header("Parameters")
dur_hours = st.sidebar.slider("Simulation Tracking Vector Scope (Hours)", 1, 12, 4)
dt_step = st.sidebar.slider("Integration Step Intervals (Seconds)", 1, 60, 5)

# Resurfacing Core Logic Variables
t_arr, r_coords, alt_track, speed_track, earth_radius = engine.simulate_orbit(
    altitude_m = alt_m,
    speed_factor=speed_bar,
    duration_hours = dur_hours,
    dt=dt_step
)

# Tracks telementary values
re_entered = alt_track[-1] <= 0
max_alt_km = alt_track.max() / 1000
max_vel_kms = speed_track.max() / 1000

# Header Display
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Satellite Tracking Status", "Crahed" if re_entered else "Active Orbit")
metric_col2.metric("Max Altitude Recorded", f"{max_alt_km:.2f} km")
metric_col3.metric("Max Speed Trajectory Velocity", f"{max_vel_kms} km/s")

# Canvas Row Layout
graph, (plot_left, plot_right) = plt.subplots(1, 2, figsize=(14, 5.5)) 

# Plot Axis 1: Geo Orbit
earth_patch = plt.Circle((0, 0), earth_radius / 1000, color='royalblue', alpha=0.35, label='Earth')
plot_left.add_patch(earth_patch)
plot_left.plot(r_coords[:, 0] / 1000, r_coords[:, 1] / 1000, color='crimson')
plot_left.scatter(r_coords[0, 0] / 1000, r_coords[0, 1] / 1000, color='chartreuse', s=120, zorder=5, label='Deploy Point')


frame_limit = (np.linalg.norm(r_coords, axis=1).max() / 1000) * 1.3
plot_left.set_xlim(-frame_limit, frame_limit)
plot_left.set_ylim(-frame_limit, frame_limit)
plot_left.set_aspect('equal', 'box')
plot_left.set_title("Orbital Path")
plot_left.grid(True, alpha=0.3)

plot_right.plot(t_arr / 3600, speed_track / 1000, color='darkturquoise', linewidth=2)
plot_right.set_title("Velocity Curve Profile")
plot_right.set_xlabel("Time (Hours)")
plot_right.set_ylabel("Speed (km/s)")
plot_right.grid(True, alpha=0.3)

st.pyplot(graph)
