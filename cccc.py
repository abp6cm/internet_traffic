#! /usr/bin/env python3
"""
two charts:
1) IPs (time by connections)
2) IPs (time by bad connections)
"""
""""
import altair as alt
from vega_datasets import data

def run():

    uscities = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/uscities.csv"
    uscities2 = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/uscities2.csv"
    traffic = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/traffic.csv"
    just_bad_traffic = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/just_bad_traffic.csv"
    source = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/all_toegther_now.csv"


    movies = alt.UrlData(
        source,
        format=alt.DataFormat(parse={"date":"date"})
    )
    chart = alt.Chart(source, width=1250, height=150).mark_line().encode(
        x='date:T',
        y='total_count1:Q'
    )

    (chart).save('cccc.html')
    
if __name__ == "__main__":
    run()
"""

import altair as alt
from vega_datasets import data

source = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/counted_traffic_by_date.csv"
source2 = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/counted_traffic_by_date_2.csv"


brush = alt.selection_interval(encodings=['x'])

base = alt.Chart(source2, width=1250, height=200).mark_area().encode(
    x = 'date:T',
    y = 'total_connections:Q'
)

base2 = alt.Chart(source, width=1250, height=200).mark_area().encode(
    x = 'date:T',
    y = 'total_connections:Q'
)

upper = base.encode(
    alt.X('date:T').scale(domain=brush)
)

lower = base2.properties(
    height=60
).add_params(brush)


(upper & lower).save('cccc.html')