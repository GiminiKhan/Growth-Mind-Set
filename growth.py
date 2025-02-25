import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "Data Sweeper", layout='wide')

#custom css
st.markdown(
    """
    <style>
    .stApp{
     backgroung-color: black 
     color: white;
     } 
     </style>
     """,
     unsafe_allow_html=True
)

#title and discription
st.title("Datasweeper Sterling by Qurat")
st.write("Transfer your files between CSV and Excel formats with built-in data cleaning and visualization Creating the project for quarter 3!")

#file uploder

upload_files = st.file_uploader("Upload your files(accepts CSV or Excel):", type=["cvs","xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".CSV":
            df = pd.read_CSV(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
           st.error(f"unsupported file type: {file_ext}")
           continue
 #file details
        st.write(" Preview the head of the Dataframe")
        st.dataframe(df.head())

#data cleaning option
        st.subheader("Data Cleaing Options")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(" Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        st.subheader("Select Columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]   


#data visulization
        st.subheader("Data Visulazation")
        if st.checkbox(f"Show Visulation for {file.name}"):
           st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

    #conversion option 

        st.subheader("Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CVS" , "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CVS":
                df.to.csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officialdocument.spreadsheetml.sheet"
            buffer.seek(0)
   
            st.download_button(
                label=f"Dowload {file.name}  as {coversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
                  )
                  
st.success(" All files processed successfully!")



