import streamlit as st
import pandas as pd
from calculation import crin, export, get_sheet_as_dataframe, processing
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os




st.set_page_config(layout="wide", page_title="Form Generator")

def auto_save(select_cold, choose_data, cold_store):
    

    coordinates = {
    "Company" : (410, 485),
    "Date"    : (2600, 485),
    "Total_Mc"   : (2240, 1860),
    "Total_Kg"   : (2840, 1860),
    "Form_Type"  : (3060, 280),
    "Sr_No"      : (2950, 390),
    "now"        : (2700, 2400),      
 }
    
    now = datetime.now()
    day = now.day
    month = now.month
    if choose_data == "Processing":
        formatted = f"{day}{month}-P-"
    else:
        formatted = f"{day}{month}-C-"

    if choose_data == "Processing":
        image = Image.open(r"format.jpg")
    else:
        image = Image.open(r"cs.jpg")
            
    pale_blue = (173, 216, 230)

    if choose_data == "Export":
        filtered_df2 = cold_store[cold_store["Fi_No"] == select_cold]
    else:
        filtered_df2 = cold_store[cold_store["Fi_No"] == select_cold]    
    
    filtered_df2["Total_Mc"] = pd.to_numeric(filtered_df2["Total_Mc"])
    filtered_df2["Total_Mc"].map(lambda x: round(x, 2))
    filtered_df2["Total_Kg"] = round(pd.to_numeric(filtered_df2["Total_Kg"]),2)
    

    if choose_data == "Export":
        grouped_df = filtered_df2.groupby(["Fi_No","Date","Sr_No","Company", "Item", "Form_Type"])[["Total_Mc", "Total_Kg"]].sum().reset_index()
        st.dataframe(grouped_df)
    else:
        grouped_df = filtered_df2.groupby(["Fi_No","Date","Sr_No","Company", "Item", "Form_Type"])[["Total_Mc", "Total_Kg"]].sum().reset_index()
        st.dataframe(grouped_df)
  

    fixed_inputs = {}
    input_rows = []
    fixed_inputs["Company"] = grouped_df["Company"].iloc[0]
    
    fixed_inputs["Date"] = grouped_df["Date"].iloc[0]
    fixed_inputs["Total_Mc"] = round(sum(pd.to_numeric(grouped_df["Total_Mc"])), 2)
    fixed_inputs["Total_Kg"] = round(sum(pd.to_numeric(grouped_df["Total_Kg"])), 2)
    fixed_inputs["Form_Type"] = grouped_df["Form_Type"].iloc[0]
    fixed_inputs["now"] = str(datetime.now())
    if choose_data == "Export":
        fixed_inputs["Sr_No"]   = grouped_df["Fi_No"].iloc[0]
    else:    
        fixed_inputs["Sr_No"]   = grouped_df["Fi_No"].iloc[0]

    for index, rows in grouped_df.iterrows():
        row = {
            "No"   : str(index + 1),
            "Item" : rows["Item"],
            "Total_Mc": str(rows["Total_Mc"]),
            "Total_Kg" :str(round(pd.to_numeric(rows["Total_Kg"]),2))
        }
        input_rows.append(row)


    font_size = 54  

    
    edited_image = image.copy()
    draw = ImageDraw.Draw(edited_image)
    font_path2 = "Pyidaungsu-2.5.3_Regular.ttf"
    font_path = "calibri.ttf"
    font2 = ImageFont.truetype(font_path2, font_size)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        st.error("Font not found")
        font = ImageFont.load_default()

    start_x = 300
    start_y = 720
    row_height = 100
    for key, coord in coordinates.items():
        if fixed_inputs[key]:
            if key == "now":
                font = ImageFont.truetype(font_path, font_size)
                draw.text(coord, str(fixed_inputs[key]), fill=pale_blue, font=font)
            elif key == "Form_Type" or key == "Company":
                draw.text(coord, str(fixed_inputs[key]), fill="black", font=font2)    
            else:
                font = ImageFont.truetype(font_path, font_size)
                draw.text(coord, str(fixed_inputs[key]), fill="black", font=font)
    for i, row in enumerate(input_rows):
        y_offset = start_y + i * row_height   
        draw.text((start_x, y_offset), row["No"], fill="black", font=font)
        draw.text((900, y_offset), str(row["Item"]), fill="black", font=font2)
        draw.text((2240, y_offset), row["Total_Mc"], fill="black", font=font)
        draw.text((2840, y_offset), row["Total_Kg"], fill="black", font=font)
        


    #st.image(edited_image, use_container_width=True)     
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    forms_folder = os.path.join(desktop_path, "forms")
    os.makedirs(forms_folder, exist_ok=True)       
    output_path = os.path.join(forms_folder, f"{fixed_inputs["Sr_No"]}.png")
    edited_image.save(output_path)

    st.success("Successfully Saved")

def get_datecode(data : pd.DataFrame, col_name : str):
    data["code"] = data[f"{col_name}"].str.slice(0,4)

    return data



def filters(data: pd.DataFrame, filter : str, col: str):
    filtered_df = data[data[f"{col}"].str.contains(f"{filter}", na=False)]
    return filtered_df



if __name__ == "__main__":
    choose_data = choose_data = st.segmented_control("Choose Datasource", ["Cold_Store", "Export", "Processing","RP"], default="Cold_Store")
    if choose_data == "Cold_Store":
        cold_store = crin()
        cold_store["Date"] = pd.to_datetime(cold_store["Date"], errors="coerce")
        cold_store["Date"] = cold_store["Date"].dt.strftime('%d/%m/%Y')
    elif choose_data == "Export":
        cold_store = export()    
        cold_store = cold_store.sort_values(by=["Sr_No"])
        cold_store["Date"] = pd.to_datetime(cold_store["Date"], errors="coerce")
        cold_store["Date"] = cold_store["Date"].dt.strftime('%d/%m/%Y')
        cold_store["Item"].apply(lambda x: x.encode('utf-8').decode('utf-8') if isinstance(x, str) else x)
    elif choose_data == "Processing":
        #path = r"processing.json"
        #cold_store = get_sheet_as_dataframe("MSLI_TEST_CRIN","Airblast",path) 
        #cold_store.dropna()
        file = "processing.xlsx"
        cold_store = pd.read_excel(file) 
        
        cold_store["Sr_No"] = cold_store["PCode"]
        cold_store["Conversion"] = cold_store["Convertion"]
        cold_store["Date"] = pd.to_datetime(cold_store["Date"], errors="coerce")
        cold_store["Date"] = cold_store["Date"].dt.strftime('%d/%m/%Y')
        cold_store["Total_Mc"] = cold_store["Total MC"]
        cold_store["Total_Kg"] = pd.to_numeric(cold_store["Total Kg"]).astype(float).round(2)
        cold_store["Form_Type"] = str("F7")

    elif choose_data == "RP":
        cold_store = processing()
        
        
        cold_store["Date"] = pd.to_datetime(cold_store["Date"])
        cold_store = cold_store.loc[cold_store["Form_Type"].str.contains('|'.join(["Repacking", "Repacking In"]), case=False, na=False)]
        cold_store["Date"] = pd.to_datetime(cold_store["Date"], errors="coerce")
        cold_store["Date"] = cold_store["Date"].dt.strftime('%d/%m/%Y')
        st.write(cold_store)


        
        
     
    main_df = get_datecode(cold_store, col_name="Fi_No" if choose_data == "Export" else "Fi_No")
    filt = st.selectbox("choose serial", options=main_df["code"].unique())   
    data = filters(cold_store, filt, col="Fi_No"    if choose_data == "Export" else "Fi_No")    
    st.dataframe(data, use_container_width=True)
    key_col = "Fi_No" if choose_data == "Export" else "Fi_No"
    sr_no_date_counts = data.groupby("Sr_No")["Date"].nunique()
    sr_no_with_multiple_dates = sr_no_date_counts[sr_no_date_counts > 1].index.tolist()

    if sr_no_with_multiple_dates:
        for sr_no in sr_no_with_multiple_dates:
            # Filter rows for the current Sr_No
            mask = data["Sr_No"] == sr_no
            subset = data[mask]
            unique_dates = subset["Date"].unique()
            
            # Assign suffixes to the key column for each date
            suffix = "A"
            for date in unique_dates:
                date_mask = (data["Sr_No"] == sr_no) & (data["Date"] == date)
                data.loc[date_mask, key_col] = (
                    data.loc[date_mask, key_col].astype(str) + f"-{suffix}"
                )
                suffix = chr(ord(suffix) + 1)  # Increment suffix (A → B → C...)

    if st.button("Save"):
        select_cold = list(data["Fi_No"].unique()) if choose_data == "Export" else list(data["Fi_No"].unique())
        for i in select_cold:
            auto_save(choose_data=choose_data, cold_store=data, select_cold=i)
            print(i)




        