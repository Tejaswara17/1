import dash
from dash import html, dcc, Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import json

# Initial UI Elements State
initial_state = [
    {"id": "btn_picking", "type": "button", "label": "Picking", "color": "#2196f3", "x": 50, "y": 50, "width": 120, "height": 50},
    {"id": "btn_putaway", "type": "button", "label": "Put Away", "color": "#4caf50", "x": 200, "y": 50, "width": 120, "height": 50},
    {"id": "img_user", "type": "image", "src": "https://via.placeholder.com/100", "color": "#ffffff", "x": 50, "y": 150, "width": 100, "height": 100},
    {"id": "input_number", "type": "number", "value": 0, "color": "#ffffff", "x": 200, "y": 150, "width": 120, "height": 50},
]

# Dash App Initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # For deployment

# App Layout
app.layout = dbc.Container(
    [
        html.H1("Dynamic GUI Prototype", className="text-center my-4"),
        dcc.Store(id="ui-state", data=initial_state),
        dcc.Store(id="selected-element", data=None),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="ui-container",
                        style={
                            "position": "relative",
                            "height": "500px",
                            "border": "2px solid #ddd",
                            "backgroundColor": "#f9f9f9",
                        },
                    ),
                    width=9,
                ),
                dbc.Col(
                    [
                        html.H5("Element Customization"),
                        daq.ColorPicker(
                            id="color-picker",
                            label="Change Color",
                            value={"hex": "#ffffff"},
                        ),
                        html.Button(
                            "Save State",
                            id="save-state",
                            className="btn btn-primary my-3",
                        ),
                        html.Pre(
                            id="output",
                            style={
                                "border": "1px solid #ddd",
                                "padding": "10px",
                                "whiteSpace": "pre-wrap",
                                "height": "200px",
                                "overflow": "auto",
                            },
                        ),
                    ],
                    width=3,
                ),
            ]
        ),
    ],
    fluid=True,
)

# Update UI Elements Dynamically
@app.callback(
    Output("ui-container", "children"),
    Input("ui-state", "data"),
)
def render_ui(state):
    children = []
    for el in state:
        style = {
            "position": "absolute",
            "top": f"{el['x']}px",
            "left": f"{el['y']}px",
            "width": f"{el['width']}px",
            "height": f"{el['height']}px",
            "backgroundColor": el.get("color", "#ffffff"),
            "border": "1px solid #000" if el["type"] != "image" else "none",
            "cursor": "move",
            "textAlign": "center",
            "lineHeight": f"{el['height']}px",
        }

        if el["type"] == "button":
            children.append(
                html.Button(el["label"], id=el["id"], style=style)
            )
        elif el["type"] == "image":
            children.append(
                html.Img(src=el["src"], id=el["id"], style=style)
            )
        elif el["type"] == "number":
            children.append(
                dcc.Input(
                    type="number",
                    value=el["value"],
                    id=el["id"],
                    style={**style, "lineHeight": "normal"},
                )
            )
    return children


# Update Color of Selected Element
@app.callback(
    Output("ui-state", "data"),
    Input("color-picker", "value"),
    State("ui-state", "data"),
    State("selected-element", "data"),
)
def update_color(color, state, selected_id):
    if not selected_id:
        return state

    new_state = []
    for el in state:
        if el["id"] == selected_id:
            el["color"] = color["hex"]
        new_state.append(el)
    return new_state


# Save the State
@app.callback(
    Output("output", "children"),
    Input("save-state", "n_clicks"),
    State("ui-state", "data"),
)
def save_state(n_clicks, state):
    if n_clicks:
        return json.dumps(state, indent=2)


if __name__ == "__main__":
    app.run_server(debug=True)

