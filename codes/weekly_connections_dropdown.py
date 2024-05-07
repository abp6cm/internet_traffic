#! /usr/bin/env python3
"""

"""
import altair as alt
from vega_datasets import data

import numpy as np
import pandas as pd

alt.data_transformers.disable_max_rows()

def label_week(row):
    week_number = (row.date.day - 1) // 7 + 1
    return f"{row.date.strftime('%B')}: Week_{week_number}"    
    
    
    
def run():    
    uscities = pd.read_csv("https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/ASN_locations.csv")
    uscities2 = pd.read_csv("https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/origin_IP_location.csv")
    traffic = pd.read_csv("https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/traffic.csv")
    just_bad_traffic = pd.read_csv("https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/bad_traffic.csv")


    traffic = traffic.rename(columns={'count': 'outgoing_routes'})
    traffic.columns = [col.lower() for col in traffic.columns]

    traffic['date'] = pd.to_datetime(traffic['date'])
    dates = np.unique(traffic['date'])
    traffic['month'] = traffic['date'].dt.month_name().astype(str)
    traffic['week'] = traffic.apply(label_week, axis=1)


# A dropdown filter
    destination_options = np.sort(traffic['destination'].unique())
    destination_dropdown = alt.binding_select(options=destination_options, name="Destination")
    destination_select = alt.selection_single(fields=['destination'], bind=destination_dropdown)
    
    weeks = traffic['week'].unique()

    week_base = alt.Chart(traffic).mark_bar().encode(
        x='total_connections:Q',
        y=alt.Y('week:O', sort=weeks),
        color=alt.Color('week:O', legend=None), 
        tooltip=['total_connections:Q']  
    ).transform_aggregate(
        total_connections='count()',  
        groupby=['week', 'destination']
    )

    week_filtered_chart = week_base.add_params(
        destination_select
    ).transform_filter(
        destination_select
    ).properties(
        title="Weekly Incoming Traffic Connections"
    )

    (week_filtered_chart ).save('weekly_connections_dropdown.html')

if __name__ == "__main__":
    run()
