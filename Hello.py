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


def run():
    st.set_page_config(
        page_title="Data Viewer",
        page_icon="👋",
    )

    st.write("# Garden Route Mall")

    cols = st.sidebar.multiselect('Plot', ['kW','kVA','kVAr'])
    grouper = st.sidebar.selectbox('Agg Type', ['D','M','Y', 'H','M',])
    month = st.sidebar.selectbox('month', [1,2,3,4,5,6,7,8,9,10,11,12])
    df = pd.read_csv("data/garden_route_mall.csv", parse_dates={"DateTime":[0,1]})
    df = df.set_index('DateTime')
    df['H'] = df.index.hour
    df['M'] = df.index.minute
    df['D'] = df.index.day
    df['M'] = df.index.month
    df['Y'] = df.index.year

    plt_df = df.loc[df.index.month==month].groupby(by=grouper).mean()[cols]

    st.line_chart(plt_df)
    st.write(plt_df)

    for i in range(12):
        st.line_chart(df.groupby(by='kW')['kW'].agg(Mean='mean', Max='max'))


if __name__ == "__main__":
    run()
