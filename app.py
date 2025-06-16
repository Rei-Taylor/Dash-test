from dash import Dash, html, callback, Input, Output, dcc , State
from dash_ag_grid import AgGrid
import database as db
from flaskwebgui import FlaskUI
import widgets as comp
import calc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import pandas as pd
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
ui = comp.UI()
df = db.show_crin(db.connect_to_db())
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").fillna(pd.to_datetime("2025-01-04")).dt.strftime('%d/%m/%Y')
df["Batch_No"] = df['Fi_No'].str.split('-').str[0] 
df2 = df


app.index_string = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/styles/ag-grid.css"> 
        <link rel="stylesheet" href="https://unpkg.com/ag-grid-community/styles/ag-theme-material.css">
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

app.layout = html.Div(
    children=[
        ui.navbar(),
        
        
        html.Div([
            html.Div(
                children=[
                    html.P(
                        "Cold Store",
                        className="text-lg"
                    ),
                ],
                className="flex-7"
            ),
            html.Div([
                ui.metric_container(
                                    children=[dbc.Row([
                                        dbc.Col(ui.metric(
                                            title="Total_Mc",
                                            value=df["Total_Mc"].sum(),
                                            id = "Total_Mc"
                                        )),
                                        dbc.Col(ui.metric(
                                            title="Total_Kg",
                                            value=round(df["Total_Kg"].sum(),2),
                                            id = "Total_Kg"
                                        ))
                                    ])]
                                )], className="flex-1 bg-base-200")
        ], className="flex flex-row w-full rounded-box"
        ),
        html.Div(   
            className="card bg-base-300",
            children=[
                dbc.Row(
                        children=[
                            dbc.Col(ui.Dropdown(options=df["Company"].unique().tolist(), placeholder="Company", id="Company", className="text-primary select-secondary dash-dropdown")),
                            dbc.Col(ui.Dropdown(options=df["Item"].unique().tolist(), placeholder="Item", id="Item", className="text-primary select-secondary ")),
                            dbc.Col(ui.Dropdown(options=df["Type"].unique().tolist(), placeholder="Type", id="Type", className="text-primary select-secondary ")),
                            dbc.Col(ui.Dropdown(options=df["Size"].unique().tolist(), placeholder="Size", id="Size", className="text-primary select-secondary ")),
                            dbc.Col(ui.Dropdown(options=df["Conversion"].unique().tolist(), placeholder="Conversion", id="Conversion", className="text-primary select-secondary ")),
                            dbc.Col(ui.Dropdown(options=df["Sr_No"].unique().tolist(), placeholder="Sr_No", id="Sr_No", className="text-primary select-secondary ")),
                            dbc.Col(ui.Dropdown(options=df["Fi_No"].unique().tolist(), placeholder="Fi_No", id="Fi_No", className="text-primary select-secondary ")),
                            dbc.Col(ui.Dropdown(options=df["Batch_No"].unique().tolist(), placeholder="Batch_No", id="Batch_No", className="text-primary select-secondary ")),
                            dbc.Col(ui.date_input("Date")),
                            dcc.Store(id="NONe"),
                            dbc.Col(dbc.Button(
                                id="filter-trigger",
                                children=["Filter", DashIconify(icon="material-symbols:database-search", height=20)],
                                className="btn btn-secondary btn-soft grow-y "
                            ))

                        ],class_name="g-1"
                        ),
                ui.aggrid_table(df, id="first-table")
                

            ]
        ),
        html.Div([
            html.Div(
                children=[
                    html.P(
                        "Export",
                        className="text-lg"
                    ),
                ],
                className="flex-7"
            ),
            html.Div([
                ui.metric_container(
                                    children=[
                                        ui.metric(
                                            title="Total_Mc",
                                            value=df2["Total_Mc"].sum(),
                                            id = "Total_Mc_exp"
                                        ),
                                        ui.metric(
                                            title="Total_Kg",
                                            value=round(df2["Total_Kg"].sum(),2),
                                            id = "Total_Kg_exp"
                                        )
                                    ]
                                )], className="flex-1 bg-base-200")
        ], className="flex flex-row w-full rounded-box mt-5"
        ),
        html.Div(   
            className="card bg-base-300",
            children=[
                ui.Menu(className="menu-horizontal gap-4 justify-center bg-base-300 p-5",
                        children=[
                            ui.Dropdown(options=df2["Company"].unique().tolist(), placeholder="Company", id="Company_exp", className="text-primary select-secondary "),
                            ui.Dropdown(options=df2["Item"].unique().tolist(), placeholder="Item", id="Item_exp", className="text-primary select-secondary "),
                            ui.Dropdown(options=df2["Type"].unique().tolist(), placeholder="Type", id="Type_exp", className="text-primary select-secondary "),
                            ui.Dropdown(options=df2["Size"].unique().tolist(), placeholder="Size", id="Size_exp", className="text-primary select-secondary "),
                            ui.Dropdown(options=df2["Conversion"].unique().tolist(), placeholder="Conversion_exp", id="Conversion_exp", className="text-primary select-secondary "),
                            ui.Dropdown(options=df2["Sr_No"].unique().tolist(), placeholder="Sr_No", id="Sr_No_exp", className="text-primary select-secondary "),
                            ui.Dropdown(options=df2["Fi_No"].unique().tolist(), placeholder="Fi_No", id="Fi_No_exp", className="text-primary select-secondary "),
                            html.Button(
                                id="filter-trigger_exp",
                                children=["filter", DashIconify(icon="material-symbols:database-search")],
                                className="btn btn-primary btn-soft grow-y "
                            )

                        ]
                        ),
                ui.aggrid_table(df2, id="second-table"),
                

                

            ]
        )
              
        
    ]
)
@callback(
        [Output("first-table", "rowData"),Output("Total_Mc", "children"), Output("Total_Kg","children")],
        State("Company", "value"),
        State("Item", "value"),
        State("Type", "value"),
        State("Size", "value"),
        State("Conversion", "value"),
        State("Sr_No", "value"),
        State("Fi_No", "value"),
        State("Batch_No", "value"),
        State("Date", "start_date"),State("Date","end_date"),State("Date", "date"),
        State("checkDate","value"),
        Input("filter-trigger", "n_clicks"),
        prevent_initial_call = True
)
def filter_return(company, item, type, size, conversion,sr_no, fi_no,batch_no, start_date, end_date,date,check_date, n_clicks):
    filters = {}
    if company:
        filters["Company"] = company
    if item:
        filters["Item"] = item
    if type:
        filters["Type"] = type
    if size:
        filters["Size"] = size
    if conversion:
        filters["Conversion"] = conversion
    if fi_no:
        filters["Fi_No"] = fi_no
    if sr_no:
        filters["Sr_No"] = sr_no 
    if batch_no:
        filters["Batch_No"] = batch_no 
    if check_date:      
        if start_date and end_date:
            filters["Start_Date"] = pd.to_datetime(start_date).strftime('%d/%m/%Y')
            filters["End_Date"] = pd.to_datetime(end_date, errors="coerce").strftime('%d/%m/%Y')
            print([start_date ,end_date])
    else:
        if date:
            filters["Start_Date"] = pd.to_datetime(date).strftime('%d/%m/%Y')
            filters["End_Date"] = pd.to_datetime(date, errors="coerce").strftime('%d/%m/%Y')

    if n_clicks:
        df_ = calc.filter_dataframe(df, filters=filters)
        total_mc = df_["Total_Mc"].sum()
        total_kg = round(df_["Total_Kg"].sum(), 2)

    return [df_.to_dict(orient="records"), total_mc, total_kg]              

@callback(
        Output("id-Date", "children"),
        Input("checkDate","value"),
        prevent_init_call=True
)
def update_(value):
    if value == True:
        child = [
           
            dcc.DatePickerRange(id="Date", persistence=False, clearable=True)
        ]
        
    else:
        child = [
                    
                    dcc.DatePickerSingle(id="Date", persistence=False, clearable=True)
            ]
    return child    
    




def runner(**kwargs):
    app.run(**kwargs)

if __name__ =="__main__":
    FlaskUI(
        server=runner,
        server_kwargs={"port":8088}
    )
    app.run(debug=True)
    