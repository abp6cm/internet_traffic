#! /usr/bin/env python3
"""
This document contains four visualizations. Three are graphs of the United States and one bar graph. 
The first is a graph connecting local IP addresses (which are anonymous so are kept outside of the US boarder)
to ASNs via a dataset of connections spanning over three months.
The next is also a graph of the United States, but just the specified connections that are considered "bad".
The bar graph shows how many bad connections there are by local IP address.
The previous three graophs are all connected by local IP, so when hovering over any graph, the other two will change
in accordance with it.

The last graph of the United States is just the ASN locations and the size of the dots is the size of how many connections
to it there are.
"""
import altair as alt
from vega_datasets import data


def run():

    uscities = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/ASN_locations.csv"
    uscities2 = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/origin_IP_locatio.csv"
    traffic = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/traffic.csv"
    just_bad_traffic = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/bad_traffic.csv"


    states = alt.topo_feature(data.us_10m.url, feature="states")

    background = alt.Chart(states).mark_geoshape(
        fill="lightgray",
        stroke="white"
    ).properties(
        width=600,
        height=450
    ).project("albersUsa")
    # Create pointerover selection
    
    select_city = alt.selection_point(
        on="pointerover", nearest=True, fields=["origin"], empty=False
    )
    select_city2 = alt.selection_point(
        on="pointerover", nearest=True, fields=["destination"], empty=False
    )
    

    lookup_data = alt.LookupData(
        uscities, key="ASN", fields=["latitude", "longitude"]
    )

    lookup_data2 = alt.LookupData(
        uscities2, key="origin_IP", fields=["latitude", "longitude"]
    )

    connections = alt.Chart(traffic).mark_rule(opacity=0.35).encode(
        latitude="latitude:Q",
        longitude="longitude:Q",
        latitude2="lat2:Q",
        longitude2="lon2:Q"
    ).transform_lookup(
        lookup="origin",
        from_=lookup_data2
    ).transform_lookup(
        lookup="destination",
        from_=lookup_data,
        as_=["lat2", "lon2"]
    ).transform_filter(
        select_city
    )
    
    bad_connections = alt.Chart(just_bad_traffic).mark_rule(opacity=0.35, color = "red").encode(
        latitude="latitude:Q",
        longitude="longitude:Q",
        latitude2="lat2:Q",
        longitude2="lon2:Q",
    ).transform_lookup(
        lookup="origin",
        from_=lookup_data2
    ).transform_lookup(
        lookup="destination",
        from_= lookup_data,
        as_=["lat2", "lon2"]
    ).transform_filter(
        select_city
    )
  
    points1 = alt.Chart(traffic).mark_circle().encode(
        latitude="latitude:Q",
        longitude="longitude:Q",
        size=alt.Size("outgoing_routes:Q").legend(None).scale(range =[0, 1000]),
        order=alt.Order("outgoing_routes:Q").sort("descending"),
        tooltip=["origin:N", "outgoing_routes:Q"]
    ).transform_aggregate(
        outgoing_routes="count()",
        groupby=["origin"]
    ).transform_lookup(
        lookup="origin",
        from_=lookup_data2
    ).add_params(
        select_city
    )
    chart1 = (background + connections + points1)

    points2 = alt.Chart(just_bad_traffic).mark_circle(size = 2000).encode(
        latitude="latitude:Q",
        longitude="longitude:Q",
        size=alt.Size("bad_outgoing_routes:Q").legend(None).scale(range=[1,2000]),
        order=alt.Order("bad_outgoing_routes:Q").sort("descending"),
        tooltip=["origin:N", "bad_outgoing_routes:Q"]
    ).transform_aggregate(
        bad_outgoing_routes="count()",
        groupby=["origin"]
    ).transform_lookup(
        lookup="origin",
        from_=lookup_data2  
    ).add_params(
        select_city
    )
    chart2 = (background + bad_connections + points2)

    points3 = alt.Chart(traffic).mark_circle(size = 20000).encode(
        latitude="latitude:Q",
        longitude="longitude:Q",
        size=alt.Size("incoming_routes:Q").legend(None).scale(range=[1,2000]),
        order=alt.Order("incoming_routes:Q").sort("descending"),
        tooltip=["destination:N", "incoming_routes:Q"]
    ).transform_aggregate(
        incoming_routes="count()",
        groupby=["destination"]
    ).transform_lookup(
        lookup="destination",
        from_=lookup_data  
    ).add_params(
        select_city2
    )

    chart3 = (background + points3)

    points4 = alt.Chart(just_bad_traffic).mark_circle(color = "red").encode(
        latitude="latitude:Q",
        longitude="longitude:Q",
        size=alt.Size("bad_incoming_routes:Q").legend(None).scale(range=[1,2000]),
        order=alt.Order("bad_incoming_routes:Q").sort("descending"),
        tooltip=["destination:N", "bad_incoming_routes:Q"]
    ).transform_aggregate(
        bad_incoming_routes="count()",
        groupby=["destination"]
    ).transform_lookup(
        lookup="destination",
        from_=lookup_data 
    ).add_params(
        select_city2
    )

    chart4 = (background + points4)

    bar_chart = alt.Chart(just_bad_traffic).mark_bar().encode(
        x='total_bad_connections:Q',
        y='origin:N',
        text = "total_bad_connections:Q"
    ).transform_aggregate(
        total_bad_connections = "count()",
        groupby=["origin"]
    ).transform_lookup(
        lookup = "origin",
        from_=lookup_data2
    )
    bar_chart = bar_chart + bar_chart.mark_text(align='left', dx=2).transform_filter(select_city)
        
    combined_maps = chart1 | chart2
    combined_maps2 = chart3 | bar_chart

    

    (combined_maps & combined_maps2 ).save('aaaa.html')

    

if __name__ == "__main__":
    run()
