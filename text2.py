from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def save_pdf(result_new2_2, result_new2_1, pdf_output):
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter

    # 创建一个空白的PIL图像，用于绘制文字（这里使用RGB模式，背景透明）
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 设置字体（这里以宋体为例，需根据实际情况调整字体路径和名称）
    font = ImageFont.truetype('simhei.ttf', 12)  # 黑体字体文件，需确保存在该字体文件，可替换为其他字体

    # 使用PIL绘制标题文字
    draw.text((100, height - 40), "科研人员信用风险预警查询", font=font, fill=(0, 0, 0))

    # 添加表格1内容
    font = ImageFont.truetype('simhei.ttf', 10)
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

    # 将PIL图像转换为numpy数组，再转换为reportlab能识别的格式并绘制到PDF上
    img_np = np.array(img)
    img_rgb = Image.fromarray(img_np[:, :, :3])
    c.drawImage(img_rgb, 0, 0, width, height, mask='auto')

    c.save()
