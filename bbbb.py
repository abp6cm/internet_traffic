"""
Multiple Interactions
=====================
This example shows how multiple user inputs can be layered onto a chart. The four inputs have functionality as follows:

* Dropdown: Filters the movies by genre
* Radio Buttons: Highlights certain films by Worldwide Gross
* Mouse Drag and Scroll: Zooms the x and y scales to allow for panning
* Checkbox: Scales the marker size of big budget films

"""
# category: interactive charts
import altair as alt
from vega_datasets import data

source = "https://cdn.jsdelivr.net/gh/abp6cm/internet_traffic@main/counted_traffic_by_destination.csv"


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

(highlight_ratings2 & highlight_ratings & highlight_ratings3).save('bbbb.html')