import numpy as np
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

# Title
st.sidebar.title("Mini-Volume-Visualizer")

# Upload file
uploaded_file = st.sidebar.file_uploader('', type='.npy')

# Load volume data
if uploaded_file is not None:
    volume = np.load(uploaded_file) # value range: [0, 1]
else:
    volume = np.load('.data/volume_in.npy') # value range: [0, 1]

x, y, z, c = volume.shape

# If show line frame
st.sidebar.write('---')
is_show_lineframe = st.sidebar.checkbox(
    'Show line frame of volume',
    value=False
)

# Slice range of volume data 
st.sidebar.write('---')
x_slider = st.sidebar.slider(
    'Select a range of x axis',
    min_value=0, max_value=x, value=(0, x), step=1
)

y_slider = st.sidebar.slider(
    'Select a range of y axis',
    min_value=0, max_value=y, value=(0, y), step=1
)

z_slider = st.sidebar.slider(
    'Select a range of z axis',
    min_value=0, max_value=z, value=(0, z), step=1
)

# Strength of volume density
st.sidebar.write('---')
density_scale = st.sidebar.slider(
    'Scale of density strength',
    min_value=0, max_value=1000, value=200, step=10
)

# Init grid
scalars = volume[x_slider[0]:x_slider[1], y_slider[0]:y_slider[1], z_slider[0]:z_slider[1]]
scalars[Ellipsis, :-1] = scalars[Ellipsis, :-1] * 255
scalars[Ellipsis, -1] = scalars[Ellipsis, -1] * density_scale
scalars = scalars.astype(np.uint8)

grid = pv.UniformGrid()
grid.dimensions = np.array(scalars[Ellipsis, -1].shape) + 1
grid.origin = (0, 0, 0)
grid.spacing = (1, 1, 1)
grid.cell_data["values"] = scalars.reshape((-1, 4), order="F")

# Show volume
plotter = pv.Plotter(window_size=[640,640])
plotter.add_axes()
plotter.add_volume(grid, show_scalar_bar=True)
if is_show_lineframe:
    plotter.add_mesh(grid, style='wireframe', color='#777777')

# Final touches
plotter.view_isometric()
plotter.set_background('black')

# Send to streamlit
stpyvista(plotter)

# print(scalars.shape)
# print(plotter.camera_position)