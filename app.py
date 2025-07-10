# TODO: Blank: Associated proteins, non protein kinases, and isoforms

import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.figure_factory as ff
# import numpy as np
from analyzeData import show_analyze_tab
from mergeDf import show_merge_tab

analyzeTab, mergeTab = st.tabs([ "Analyze", "Merge"])

with analyzeTab:
    show_analyze_tab()
with mergeTab:
    show_merge_tab()
    # st.text("hi")