import pandas as pd

def filter_dataframe(df, filters) -> pd.DataFrame:
    import re
    filtered_df = df.copy()  # Use a copy to avoid modifying the original DataFrame
    text_columns = ["Company", "Item", "Type", "Size", "Fi_No"]
    numeric_columns = ["PCode", "Convertion", "Sr_No", "Conversion", "Batch_No"]
    date_columns = ["Start_Date", "End_Date"]
    code_columns = ["Start_Code", "End_Code"]


    for col, filter_values in filters.items():
        # Skip filtering if filter_values is empty or None
        if not filter_values:
            continue

        if col in text_columns:
            # Ensure filter_values is a list for text columns
            if isinstance(filter_values, str):
                filter_values = [filter_values]
            # Escape regex special characters in each filter value
            escaped_values = [re.escape(val) for val in filter_values]
            pattern = '|'.join(escaped_values)
            filtered_df = filtered_df.loc[filtered_df[col].str.contains(pattern, case=False, na=False)]
        
        elif col in numeric_columns:
            # Ensure filter_values is a list for numeric columns
            if not isinstance(filter_values, list):
                filter_values = [filter_values]
            filtered_df = filtered_df.loc[filtered_df[col].isin(filter_values)]
        
        elif col in date_columns:
            if filters["Start_Date"] is not None and filters["End_Date"] is not None:
             # Handle date range filtering
            
                start_date = filters["Start_Date"]
                end_date = filters["End_Date"]
                filtered_df = filtered_df[(pd.to_datetime(filtered_df["Date"], dayfirst=True) >= pd.to_datetime(start_date, dayfirst=True)) & (pd.to_datetime(filtered_df["Date"], dayfirst=True) <= pd.to_datetime(end_date, dayfirst=True))]  

        elif col in code_columns:
            if filters["Start_Code"] is not None and filters["End_Code"] is not None:
                start_code = filters["Start_Code"]
                end_code = filters["End_Code"]
                filtered_df = filtered_df[(pd.to_numeric(filtered_df["PCode"]) >= pd.to_numeric(start_code)) & (pd.to_numeric(filtered_df["PCode"]) <= pd.to_numeric(end_code))]        

    return filtered_df
