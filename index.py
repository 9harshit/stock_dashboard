import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app, server

# Connect to your app pages
from apps import currency_tracker, error, price_predictor

SIDEBAR_STYLE = {
    "position": "relative",
    "top": "8%",
    "left": "2rem",
    # "height": "15%",
    "width": "100%",
    # "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

app.layout = html.Div(
    [
        # location will help us to know which page we are on. It is the input of the callback (id='url', refresh=False, pathname='/') path name will be populated with href value
        dcc.Location(id="url", refresh=False, pathname="/"),
        html.Div(
            html.H2("Stock Dashboard", className="display-4"),
            style={"text-align": "center"},
        ),
        # html.Hr(),
        html.Div(
            [
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                "Stock Price Predictor",
                                href="/apps/price_predictor",
                                active="exact",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "Currency Tracker",
                                href="/apps/currency_tracker",
                                active="exact",
                            )
                        ),
                    ],
                    pills=True,
                    fill=True,
                    justified=True,
                ),
            ],
            style=SIDEBAR_STYLE,
        ),
        # This is where the output will be displayed. All the pages will be rendered here by passing in children=[].
        html.Div(id="page-content", children=[]),
    ],
    style={"width": "95%", "display": "inline-block"},
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    print(pathname)
    if pathname in ["/apps/price_predictor", "/"]:
        return price_predictor.layout
    elif pathname in ["/apps/currency_tracker"]:
        return currency_tracker.layout
    else:
        return error.layout


if __name__ == "__main__":
    app.run_server(debug=True)
