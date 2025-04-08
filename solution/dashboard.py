"""
Credentially Dashboard app created using Dash from Plotly

"""

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

import manage_data

conn = manage_data.load_data()
manage_data.create_view(conn)

# Load the dataframes here
refs_per_month = manage_data.references_handled_by_month(conn)
refs_per_assignee = manage_data.references_approved_by_assignee_by_month(conn)
refs_per_package = manage_data.references_handled_by_package_by_month(conn)
average_completion_in_days = manage_data.average_completion_in_days(conn)

app = Dash()

# References per month - with 3 month rolling average trendline (trivially added)
px_refs_per_month = px.scatter(refs_per_month, x='m', y="request_count", trendline="rolling", trendline_options=dict(window=3),
                            title="References Requested Per Month - 3-month trendline in red",
                            labels={
                                "request_count": "Requests",
                                "m": "Month"
            })
px_refs_per_month.update_traces(mode='lines')
px_refs_per_month.data[-1].line.color = 'red'

px_references_per_assignee = px.bar(refs_per_assignee, x="m", y="request_count", color="assigned_to",
                                     title="References Approved Per Assignee by Month",
                                    labels={
                                        "request_count": "Requests",
                                        "m": "Month"
                                    }
                                    )

px_references_per_package = px.bar(refs_per_package, x="m", y="request_count", color="package_name",
                                     title="References Sent By Package by Month",
                                    labels={
                                        "request_count": "Requests",
                                        "m": "Month"
                                    })

px_average_completion_in_days = px.pie(average_completion_in_days, names="assigned_to", values="average_completion_days",
                                       title="Average Completion in Days",
                                       labels={
                                           "assigned_to": "Assigned To",
                                           "average_completion_days": "Average Completion in Days"
                                       })

app.layout = [
    html.H1(children='Credentially Dashboard', style={'textAlign':'center'}),

    dcc.Graph(figure=px_refs_per_month),
    dcc.Graph(figure=px_references_per_assignee),
    dcc.Graph(figure=px_references_per_package),
    dcc.Graph(figure=px_average_completion_in_days),

    html.Div(children='Ian Lewis (2025)', style={'textAlign':'center'}),
]


if __name__ == '__main__':
    app.run(debug=True)
