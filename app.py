# TODO: Blank: Associated proteins, non protein kinases, and isoforms

import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
# import plotly.figure_factory as ff
# import numpy as np
from analyzeData import show_analyze_tab
from mergeDf import show_merge_tab
from compareDfs import showCompareTab

analyzeTab, mergeTab, compareTab = st.tabs([ "Analyze", "Merge", "Compare"])

with analyzeTab:
    show_analyze_tab()
with mergeTab:
    show_merge_tab()
with compareTab:
    showCompareTab()
