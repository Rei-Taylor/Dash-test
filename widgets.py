import dash_ag_grid as dg 
import pandas as pd
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc



class UI():


    def compute_rowspans(self, df: pd.DataFrame, group_col: str = "Sr_No") -> pd.DataFrame:
        pass

    def navbar(self):
        nav = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.Button(id="sidebar-trigger", children="Hello", color="secondary"))
            ],
            brand="MSLI",
            dark=True
        )
        return nav
    
    def date_input(self, id : str):
        dates = dcc.DatePickerSingle(id=id, persistence=True, clearable=True)
        
        menu = html.Div([
            dbc.Button(children="Date", id="popover-target"),
            dbc.Popover(
            
            children=[
                dbc.PopoverBody([
                    dbc.Checkbox(id=f"check{id}", label="Use multiple Date"),
                    html.Div(
                    dates, id=f"id-{id}")
            ]),
                
            ],target="popover-target", trigger="click"
        )])
        return menu

    def get_row_spans(self, df, column):
        spans = []
        current_val = None
        span_count = 0
        
        for val in df[column]:
            if val == current_val:
                span_count += 1
                spans.append(0)  # 0 means this cell will be covered by the span above it
            else:
                current_val = val
                span_count = 1
                spans.append(1)  # 1 means this cell starts a new span
        
        # Now adjust the first cell in each span to have the full span count
        result = []
        i = 0
        while i < len(spans):
            if spans[i] == 1:
                # Count how many 0s follow this 1
                span_length = 1
                j = i + 1
                while j < len(spans) and spans[j] == 0:
                    span_length += 1
                    j += 1
                result.append(span_length)
                # Add 0s for the rest of the span
                for _ in range(span_length - 1):
                    result.append(0)
                i = j
            else:
                result.append(spans[i])
                i += 1
        
        return result

# Calculate row spans for Sr_No column


# Custom JavaScript for the spanning cell renderer





    def aggrid_table(self, df : pd.DataFrame, id : str):
            row_spans = self.get_row_spans(df, 'Sr_No')
            # Create rowData with rowSpan information
            row_data = df.to_dict('records')
            for i, row in enumerate(row_data):
                row['Sr_No_rowSpan'] = row_spans[i]
             

            # Column definitions
            col = df.columns.to_list()
            col.remove("Sr_No")
            column_defs = [{"headerName" : i, "field" : i}for i in col]

            column_defs.append({"field": "Sr_No",
        "headerName": "Sr No",
        "rowGroup": True,
        "hide": True })
            
        
        
        
            
            
        
            

            aggrid = dg.AgGrid(
            id=id,
            columnDefs=column_defs,
            rowData=row_data,
            defaultColDef={"resizable": True, "sortable": True, "filter": True},
            dashGridOptions={"groupDisplayType": "groupRows"
        },
            columnSize="sizeToFit",
            style={"height": "500px"},
        )        
            
            return aggrid       

    def row(self, children : list):
        row_ = html.Div(
            className="flex gap-3",
            children=children
            

        )
        return row_
    
    def Menu(self, className : str = None, children : list = None):
        class_ = "menu"
        if className:
            class_ = class_ + " " +className
            
        menu_ = html.Div(
            className=class_,
            children=children
        )
        return menu_
    
    def Dropdown(self, options : list ,placeholder :str = None, className : str = None , id : str = None):
        class_ = ""
        if className:
            class_ = class_ + " " + className
        dropdown_ = dcc.Dropdown(
            id=id,
            className=class_,
            options=options,
            placeholder=placeholder,
            searchable=True,

        )
        return dropdown_
    
    def metric_container(self, children : list, className : list = None):
        class_ = "stats shadow"
        if className:
            class_ = class_ + " " + className
        metric_card = dbc.Card(
            className=class_,
            children=children
        )
        return metric_card
    
    def metric(self,title : str,  value : int, className : list = None, id : str = None):
        class_ = "stat place-items-center"
        if className:
            class_ = class_ + " " + className
        metric_ =  dbc.CardBody(
            className=class_,
            children=[
                html.Div(
                    className="stat-title",
                    children=title,
                ),
                html.Div(
                    className="stat-value",
                    children=value,
                    id=id
                )
            ]
        )  
        return metric_  
        

    def custom_table(self,df : pd.DataFrame):
        rowSpan = len(df["Sr_No"])
        heads = [html.Th(children=i) for i in df.columns.to_list()]
        cols = df.columns.to_list()
        print(cols)
        rows = []
        a =  df.head(1).to_dict(orient="records")
        for row in a:
            rows.append(html.Tr([html.Td(row["ID"]), html.Td(row["Sr_No"], rowSpan=rowSpan, className="sr_no"), html.Td(row["Company"])]))

        for index, row in df.iloc[1:].iterrows():
            
            rows.append([html.Tr([html.Td(row[f"{i}"])]for i in cols)])
        print(rows)    
           
        headers = html.Thead(
            html.Tr(
                heads
            )
            
        )
        data = html.Tbody(
            
                rows
            
        )
        

        table = html.Table(
            children=[headers, data],
            className="table"
        )  
        return table  
        

    
