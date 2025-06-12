import streamlit as st

selected = st.segmented_control(
    "Select a topic from the list:",
    options=["Topic 1", "Topic 2", "Topic 3"],
    key="selected_trends",
    default="Topic 1",
    help="Click to select a topic you resonate with.",
    selection_mode="single",
)

st.write(f"You selected: {selected}")