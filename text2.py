import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
from io import BytesIO

# 设置页面标题
st.title("科研人员信用风险预警查询")
# 读取Excel文件
df_new2_2 = pd.read_excel('new2.2.xlsx')
df_new2_1 = pd.read_excel('new2.1.xlsx')

query_name = st.text_input("请输入查询名字：")

def save_pdf(result_new2_2, result_new2_1, pdf_output):
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter

    # 确保字体文件存在并加载字体
    font_path = os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf')
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    else:
        st.error(f"Font file not found: {font_path}")
        return

    c.setFont("DejaVuSans", 12)
    c.drawString(100, height - 40, "科研人员信用风险预警查询")

    # 添加表格1内容
    c.setFont("DejaVuSans", 10)
    if not result_new2_2.empty:
        c.drawString(100, height - 60, "查询结果 (new2.2):")
        y = height - 80
        for index, row in result_new2_2.iterrows():
            c.drawString(100, y, f"作者: {row['作者']}, 失信指数: {row['失信指数']}")
            y -= 20

    # 添加表格2内容
    if not result_new2_1.empty:
        c.drawString(100, y - 20, "查询结果 (new2.1):")
        y -= 40
        for index, row in result_new2_1.iterrows():
            c.drawString(100, y, ", ".join([f"{col}: {row[col]}" for col in result_new2_1.columns if col != '作者']))
            y -= 20

    c.save()


def generate_excel(df1, df2):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name='new2.2', index=False)
        df2.to_excel(writer, sheet_name='new2.1', index=False)
    return output.getvalue()

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
        .dataframe th, .dataframe td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }
        .dataframe th {
            background-color: #f2f2f2;
        }
        .highlight {
            background-color: yellow;
        }
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
        columns_to_display = [col for col in result_new2_1.columns if col != '作者']
        html_table2 = result_new2_1[columns_to_display].to_html(index=False, classes='dataframe')
        st.markdown(html_table2, unsafe_allow_html=True)
    
    else:
        st.write("暂时没有相关记录。")
    
    # 添加Excel下载按钮
    if not result_new2_2.empty or not result_new2_1.empty:
        excel_data = generate_excel(result_new2_2, result_new2_1)
        st.download_button(
            label="下载Excel文件",
            data=excel_data,
            file_name='查询结果.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    
    # 绘制失信指数前5人的折线图
    top_5 = df_new2_2.nlargest(5, '失信指数')
    if not top_5.empty:
        fig = px.line(top_5, x='作者', y='失信指数', title='失信指数前5人的折线图')
        st.plotly_chart(fig)
    else:
        st.write("没有足够的记录来绘制图表。")
