import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io 

st.set_page_config(page_title="Analyze Your Data",page_icon="📊",layout="wide")

st.title("📊 Analyze your data")
st.write("Upload your file csv or excel")

# for uploading file 
upload_file = st.file_uploader("Upload a CSV or An Excel File", type=["csv",'xlsx'])

if upload_file is not None: 
    try:
        file_extension = upload_file.name.split('.')[-1].lower()

        if file_extension == 'csv':
            data = pd.read_csv(upload_file)
        elif file_extension == 'xlsx':
            data = pd.read_excel(upload_file)
        else:
            st.error("Unsupported file format")
            st.stop()

        # convert bool column as str
        bool_cols = data.select_dtypes(include=['bool']).columns
        data[bool_cols] = data[bool_cols].astype('str')

    except Exception as e:
        st.error('I could not read excel/csv file format')
        st.exception(e)
        st.stop()

    st.success("File Uploaded Successfully ✅ ")
    st.write("### Preview of data")
    st.dataframe(data.head())

    st.write("### Data Overview")
    st.write("Number of Rows : ", data.shape[0]) 
    st.write("Number of Column : ", data.shape[1])
    st.write("Number of Missing Value : ", data.isnull().sum().sum())
    st.write("Number of Duplicated Records : ", data.duplicated().sum()) 

    st.write("### 📝 Complete summary of the data set")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    st.write("### 🗓️ Statistical summary of the data set")
    st.dataframe(data.describe())

    st.write("### 🗓️ Statistical summary of the data set")
    non_numeric_cols = data.select_dtypes(include=['bool', 'object']).columns
    if len(non_numeric_cols) > 0:
        st.dataframe(data.describe(include=['bool','object']))
    else:
        st.info("No non-numerical (object/bool) columns found.")

    st.write("### 🗓️ Select the desire column for analysis")
    selected_columns = st.multiselect("Choose Columns",data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.dataframe(data.head())

    # ===========================
    # 📊 DATA VISUALIZATION
    # ===========================
    st.write("## 📊 Data Visualization")

    columns = data.columns.tolist()
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()

    x_axis = st.selectbox("Select Column for X axis", options=columns)
    y_axis = st.selectbox("Select Column for Y axis", options=numeric_cols)

    col1, col2, col3 = st.columns(3)
    with col1:
        line_btn = st.button("Line Graph")
        bar_btn = st.button("Bar Chart")
    with col2:
        scatter_btn = st.button("Scatter Graph")
        hist_btn = st.button("Histogram")
    with col3:
        pie_btn = st.button("Pie Chart")
        heatmap_btn = st.button("Heatmap")

    # 📈 Line Chart
    if line_btn:
        fig, ax = plt.subplots()
        ax.plot(data[x_axis], data[y_axis])
        ax.set_title("Line Chart")
        st.pyplot(fig)

    # 🔵 Scatter Chart
    if scatter_btn:
        fig, ax = plt.subplots()
        ax.scatter(data[x_axis], data[y_axis])
        ax.set_title("Scatter Chart")
        st.pyplot(fig)

    # 📊 Bar Chart
    if bar_btn:
        fig, ax = plt.subplots()
        data.groupby(x_axis)[y_axis].mean().plot(kind='bar', ax=ax)
        ax.set_title("Bar Chart (Mean Aggregation)")
        st.pyplot(fig)

    # 📈 Histogram
    if hist_btn:
        fig, ax = plt.subplots()
        ax.hist(data[y_axis].dropna(), bins=20)
        ax.set_title("Histogram")
        st.pyplot(fig)

    # 🥧 Pie Chart
    if pie_btn:
        fig, ax = plt.subplots()
        pie_data = data[x_axis].value_counts().head(10)
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        ax.set_title("Pie Chart (Top 10)")
        st.pyplot(fig)

    # 🔥 Heatmap
    if heatmap_btn:
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots()
            corr = data[numeric_cols].corr()
            im = ax.imshow(corr)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticklabels(corr.columns)
            fig.colorbar(im)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)
        else:
            st.warning("Need at least 2 numeric columns for heatmap.")

    # ===========================
    # 📊 DASHBOARD
    # ===========================
    st.write("## 📊 Mini Dashboard")

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Rows", data.shape[0])
    kpi2.metric("Columns", data.shape[1])
    kpi3.metric("Missing Values", data.isnull().sum().sum())

    if len(numeric_cols) > 0:
        fig, ax = plt.subplots()
        data[numeric_cols].mean().plot(kind='bar', ax=ax)
        ax.set_title("Average of Numeric Columns")
        st.pyplot(fig)

else:
    st.info("Please upload a csv or excel file to get started")
