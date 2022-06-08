# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger
import pandas
from datetime import time

LOGGER = get_logger(__name__)

long_names = {
        "H": 'Hour',
        "D": 'Day',
        "M": 'Month',
        "Y": 'Year',
}

season_names = {
        'High': [5, 6, 7],
        'Low' : [1, 2, 3, 4, 8, 9, 10, 11, 12]
}


def freq_label(input):
    return long_names[input]


def months_chosen(month_array):
    if len(month_array) == 1:
        return season_names[month_array[0]]
    else:
        return season_names['High'] + season_names['Low']


@st.cache
def return_data():
    return pd.read_csv("data/garden_route_mall.csv", parse_dates={"DateTime": [0, 1]})


def run():
    st.set_page_config(
            page_title="Data Viewer",
            page_icon="👋",
    )

    st.write("# Garden Route Mall")

    # cols = st.sidebar.multiselect('Plot', ['kW', 'kVA', 'kVAr'], ['kW'])
    season = st.sidebar.multiselect('Season', ['High', 'Low'], ['High', 'Low'])
    sun_hours = st.sidebar.slider('Hours', 0, 23, (0, 23))
    grouper = st.sidebar.selectbox('Agg Type', ['H', 'D', 'M', 'Y', ], format_func=freq_label)

    orig_df = return_data()
    df = orig_df.set_index('DateTime')
    df['H'] = df.index.hour
    df['D'] = df.index.day
    df['M'] = df.index.month
    df['Y'] = df.index.year
    sun_limits = ((df.index.hour >= sun_hours[0]) & (df.index.hour <= sun_hours[1]))
    season_limits = (df.index.month.isin(months_chosen(season)))

    plt_df = (df
    .loc[sun_limits & season_limits & (df.kW>0)]
    .groupby(by=grouper)
    .agg({'kW': ['mean', 'min', 'max']})
    )['kW']

    total_energy = plt_df.sum(axis=0)*2
    st.line_chart(plt_df)

    st.markdown('### Mean')
    st.write(f'Maximum Demand {plt_df["mean"].max():,.2f} kW')
    st.write(f'Energy {total_energy["mean"]:,.1f} kWh per day')

    st.write(plt_df)


if __name__ == "__main__":
    run()
