import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title='Analyze Your Data',page_icon='📊',layout='wide')

st.title('📊 Analyze Your Data')
st.write('Upload A **CSV** Or An **Excel** File To Explore Your Data Interactively!')

# for uploading file
uploaded_file = st.file_uploader('Upload a CSV Or An Excel File', type=['csv','xlsx'])


if uploaded_file is not None:
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension == 'csv':
            data = pd.read_csv(uploaded_file)

        elif file_extension == 'xlsx':
            data = pd.read_excel(uploaded_file)
            
        else:
            st.error('Unsupported file format')
            st.stop()
       
        # converting bool columns as str
        bool_cols = data.select_dtypes(include=['bool']).columns
        data[bool_cols] = data[bool_cols].astype('str')

    except Exception as e:
        st.error('Could Not Read Excel / CSV File. Please Check The File Format')
        st.exception(e)
        st.stop()
    
    st.success('✅ File Uploaded Successfully !')
    st.write('### Preview Of Data')
    st.dataframe(data.head())

    st.write('### 📋 Data Overview')
    st.write('Number Of Rows : ',data.shape[0])
    st.write('Number Of Columns : ',data.shape[1])
    st.write('Number Of Missing Values :',data.isnull().sum().sum())
    st.write('Number Of Duplicate Records : ',data.duplicated().sum().sum())

    st.write('### 📜 Complete Summary Of Dataset')
    # st.dataframe(data.info())   # data.info() method show empty dataset
    buffer = io.StringIO()
    data.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    st.write('### 📝 Statistical Summary Of Dataset')
    st.dataframe(data.describe())

    st.write('### 📝 Statistical Summary For Non-Numerical Features Of Dataset')
    non_numeric_cols = data.select_dtypes(include=["object", "bool"]).columns
    if len(non_numeric_cols) > 0:
        st.dataframe(data.describe(include=['bool','object']))
    else:
        st.info('No non-numerical features found in this dataset')

    st.write('### ✂️ Select The Desired Columns For Analysis')
    selected_columns = st.multiselect('Choose Column',data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info('No Columns Selected. Showing Full Dataset')
        st.dataframe(data.head())
    
    st.write('### 📈 Data Visualization')
    st.write('Select **Columns** For Data Visualization')
    columns = data.columns.tolist()
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    x_axis = st.selectbox('Select Column For X=Axis',options=columns)
    y_axis = st.selectbox('Select Column For Y=Axis',options=columns)

    # Create Buttons For Diff Diff Charts
    col1 , col2 , col3 = st.columns(3)

    with col1:
        line_btn = st.button('Line Graph')
        bar_btn = st.button('Bar Graph')
    with col2:
        hist_btn = st.button('Histogram Graph')
        scatter_btn = st.button('Scatter Graph')
    with col3:
        pie_btn = st.button('Pie Graph')
        heatmap_btn = st.button('Heatmap')
    
    if line_btn:
        st.write('### Showing A Line Graph')
        fig,ax = plt.subplots()
        ax.plot(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Line Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)    # it will show the graph
    
    if bar_btn:
        st.write('### Showing A Bar Graph')
        fig,ax = plt.subplots()
        ax.bar(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Bar Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)    # it will show the graph
    
    if hist_btn:
        st.write('### Showing A Histogram Graph')
        fig,ax = plt.subplots()
        ax.hist(data[y_axis].dropna(), bins=20)
        ax.set_title(f'Histogram Graph')
        st.pyplot(fig)    # it will show the graph
    
    if scatter_btn:
        st.write('### Showing A Scatter Graph')
        fig,ax = plt.subplots()
        ax.scatter(data[x_axis],data[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Scatter Graph Of {x_axis} Vs {y_axis}')
        st.pyplot(fig)    # it will show the graph

    if pie_btn:
        st.write('### Showing A Pie Graph')
        fig,ax = plt.subplots()
        pie_data = data[x_axis].value_counts().head(10)
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        ax.set_title(f'Pie Graph')
        st.pyplot(fig)    # it will show the graph

    if heatmap_btn:
        st.write('### Showing A Heatmap')
        if len(numeric_cols) > 1:
            fig,ax = plt.subplots()
            corr = data[numeric_cols].corr()
            im = ax.imshow(corr)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=90)
            ax.set_yticklabels(corr.columns)
            fig.colorbar(im)
            ax.set_title(f'Correlation Heatmap')
            st.pyplot(fig)    # it will show the graph
        else:
            st.warning('Need atleast 2 numeric columns for heatmap')
else:
    st.info('Please Upload A CSV Or An Excel File To Get Started')

