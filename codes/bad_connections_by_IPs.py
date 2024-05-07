"""
Three interwined graphs are shown here, each connected to a bubble selector below. Because there was such a large range
of connection nnumbers (1-730000), splitting them up made the most visual sense. The y axis is the ASN and x axis the number
of connections. This is only bad traffic provided by our dataset.
"""
# category: interactive charts
import altair as alt
from vega_datasets import data

source = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/counted_bad_traffic_by_destination.csv"


IP_sources = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

base = alt.Chart(source, width=1250, height=150).mark_point(filled=True).transform_filter(
    alt.FieldOneOfPredicate(field='origin', oneOf=IP_sources)
).transform_filter(
    alt.datum.count > 100
).transform_filter(
    alt.datum.count < 10000
).encode(
    x='destination:Q',
    y='count:Q',
    tooltip="Title:N"
)

# Color changing marks
rating_radio = alt.binding_radio(options=IP_sources, name="IP source")
rating_select = alt.selection_point(fields=['origin'], bind=rating_radio)

rating_color_condition = alt.condition(
    rating_select,
    alt.Color('origin:N').legend(None),
    alt.value('clear')
)

highlight_ratings = base.add_params(
    rating_select
).encode(
    color=rating_color_condition
).properties(title="Source IP by ASN connections (between 100 and 10,000)")


base = alt.Chart(source, width=1250, height=150).mark_point(filled=True).transform_filter(
    alt.FieldOneOfPredicate(field='origin', oneOf=IP_sources)
).transform_filter(
    alt.datum.count < 100

).encode(
    x='destination:Q',
    y='count:Q',
    tooltip="Title:N"
)

rating_color_condition = alt.condition(
    rating_select,
    alt.Color('origin:N').legend(None),
    alt.value('clear')
)

highlight_ratings2 = base.add_params(
    rating_select
).encode(
    color=rating_color_condition
).properties(title="Source IP by ASN connections (less than 100)")


base = alt.Chart(source, width=1250, height=150).mark_point(filled=True).transform_filter(
    alt.FieldOneOfPredicate(field='origin', oneOf=IP_sources)
).transform_filter(
    alt.datum.count > 10000

).encode(
    x='destination:Q',
    y='count:Q',
    tooltip="Title:N"
)

rating_color_condition = alt.condition(
    rating_select,
    alt.Color('origin:N').legend(None),
    alt.value('clear')
)

highlight_ratings3 = base.add_params(
    rating_select
).encode(
    color=rating_color_condition
).properties(title="Source IP by ASN connections (more than 10,000)")

(highlight_ratings2 & highlight_ratings & highlight_ratings3).save('bad_connections_by_IPs.html')
