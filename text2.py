import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 设置页面标题
st.title("科研人员信用风险预警查询")

# 读取Excel文件
df_new2_2 = pd.read_excel('new2.2.xlsx')
df_new2_1 = pd.read_excel('new2.1.xlsx')

query_name = st.text_input("请输入查询名字：")

def save_pdf(result_new2_2, result_new2_1, pdf_output):
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter

    # 确保width和height为整数
    width, height = int(width), int(height)

    # 创建一个空白的PIL图像，用于绘制文字（这里使用RGB模式，背景白色）
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 设置字体（这里以Arial为例，需根据实际情况调整字体路径和名称）
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 替换为系统中存在的字体路径
    try:
        font = ImageFont.truetype(font_path, 12)
    except IOError:
        st.error("Font file not found. Please provide a valid font path.")
        return

    # 使用PIL绘制标题文字
    draw.text((100, height - 40), "科研人员信用风险预警查询", font=font, fill=(0, 0, 0))

    # 添加表格1内容
    font = ImageFont.truetype(font_path, 10)
    if not result_new2_2.empty:
        draw.text((100, height - 60), "查询结果 (new2.2):", font=font, fill=(0, 0, 0))
        y = height - 80
        for index, row in result_new2_2.iterrows():
            draw.text((100, y), f"作者: {row['作者']}, 失信指数: {row['失信指数']}", font=font, fill=(0, 0, 0))
            y -= 20

    # 添加表格2内容
    if not result_new2_1.empty:
        draw.text((100, y - 20), "查询结果 (new2.1):", font=font, fill=(0, 0, 0))
        y -= 40
        for index, row in result_new2_1.iterrows():
            draw.text((100, y), ", ".join([f"{col}: {row[col]}" for col in result_new2_1.columns if col!= '作者']), font=font, fill=(0, 0, 0))
            y -= 20

    # 将PIL图像保存为临时文件
    temp_img_path = "temp_image.png"
    img.save(temp_img_path)

    # 将临时文件绘制到PDF上
    c.drawImage(temp_img_path, 0, 0, width, height)
    c.save()

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

    # 绘制失信指数前5人的折线图
    top_5 = df_new2_2.nlargest(5, '失信指数')
    if not top_5.empty:
        fig = px.line(top_5, x='作者', y='失信指数', title='失信指数前5人的折线图')
        st.plotly_chart(fig)
    else:
        st.write("没有足够的记录来绘制图表。")

    # 添加生成PDF按钮
    if st.button('生成PDF'):
        pdf_output = "查询结果.pdf"
        save_pdf(result_new2_2, result_new2_1, pdf_output)
        
        with open(pdf_output, "rb") as file:
            btn = st.download_button(
                label="下载PDF文件",
                data=file,
                file_name=pdf_output,
                mime="application/octet-stream"
            )
