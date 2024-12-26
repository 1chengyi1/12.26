!pip install weasyprint
import streamlit as st
import pandas as pd
from io import BytesIO
from weasyprint import HTML

# 设置页面标题
st.title("科研人员信用风险预警查询")

# 读取Excel文件
df_new2_2 = pd.read_excel('new2.2.xlsx')
df_new2_1 = pd.read_excel('new2.1.xlsx')

query_name = st.text_input("请输入查询名字：")
if query_name:
    # 在new2.2表中寻找作者等于查询输入的名字
    result_new2_2 = df_new2_2[df_new2_2['作者'] == query_name]
    # 在new2.1表中寻找作者等于查询输入的名字
    result_new2_1 = df_new2_1[df_new2_1['作者'] == query_name]

    # 生成表格1，不显示行索引
    if not result_new2_2.empty:
        st.markdown("""
        <style>
       .dataframe {
            border: 1px solid #ccc;
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
       .dataframe th,.dataframe td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }
       .dataframe th {
            background-color: #f2f2f2;
        }
       .highlight {
            background-color: yellow;
            animation: blink 1s infinite; /* 尝试的闪烁动画，但可能不起作用 */ 
        }
        @keyframes blink {  
                0%, 100% { background-color: yellow; }  
                50% { background-color: transparent; } /* 由于Streamlit的限制，这可能不会按预期工作 */  
        }  
        </style>  
        </style>
        """, unsafe_allow_html=True)
        # 添加高亮类
        for index, row in result_new2_2.iterrows():
            if float(row['失信指数']) > 100:
                result_new2_2.at[index, '失信指数'] = f'<span class="highlight">{row["失信指数"]}</span>'
        
        html_table1 = result_new2_2.to_html(index=False, escape=False, classes='dataframe')
        st.markdown(html_table1, unsafe_allow_html=True)
    # 生成表格2，不显示行索引和作者列
    if not result_new2_1.empty:
        columns_to_display = [col for col in result_new2_1.columns if col!= '作者']
        html_table2 = result_new2_1[columns_to_display].to_html(index=False, classes='dataframe')
        st.markdown(html_table2, unsafe_allow_html=True)
    else:
        st.write("暂时没有相关记录。")

    # 添加保存按钮功能，用于下载为PDF
    if not (result_new2_2.empty and result_new2_1.empty):
        if st.button("保存为PDF"):
            # 创建一个BytesIO对象来临时存储PDF数据
            pdf_buffer = BytesIO()
            combined_html = ""
            if not result_new2_2.empty:
                combined_html += html_table1
            if not result_new2_1.empty:
                combined_html += html_table2
            # 使用weasyprint将HTML转换为PDF并写入到BytesIO对象中
            HTML(string=combined_html).write_pdf(pdf_buffer)
            # 设置下载的文件名和类型
            st.download_button(
                label="点击下载PDF",
                data=pdf_buffer.getvalue(),
                file_name="科研人员信用信息.pdf",
                mime="application/pdf"
            )
