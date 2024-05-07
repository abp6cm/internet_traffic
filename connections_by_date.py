#! /usr/bin/env python3
"""
This code provides the graph of connections by date. The lower graph and the upper graph have two different
datasets because as you can see there is a big spike around Sept 18 which made the rest of the graph very small
and hard to see the difference in traffic on other days, so I capped the connections on that day for the top graph
at 35000 (lines 80 and 81 in the counted_traffic_by_date_2.csv).
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
