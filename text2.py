import streamlit as st  
import mysql.connector  
import pandas as pd  
# 数据库配置信息  
config = {  
    'user': 'root',  
    'password': '123456',  
    'host': '192.168.56.1',  
    'database': 'test',  
    'raise_on_warnings': True  
}  
def get_db_connection():  
    """建立数据库连接"""  
    cnx = mysql.connector.connect(**config)  
    return cnx  
def fetch_authors_data(author):  
    """从new2表获取作者相关数据（注意：这里我假设是new2表，因为您的代码中有这个）"""  
    query = """  
    SELECT DISTINCT  
        作者,  
        领域,  
        失信指数,  
        相关学者,  
        研究机构  
    FROM new2  
    WHERE 作者 LIKE %s  
    """  
    Authors_like = f"%{author}%"  
    cnx = get_db_connection()  
    cursor = cnx.cursor(dictionary=True)  
    cursor.execute(query, (Authors_like,))  
    columns = [column[0] for column in cursor.description]  
    data = cursor.fetchall()  
    df = pd.DataFrame(data, columns=columns)
    cursor.close()  
    cnx.close()  
    return df
def fetch_withdrawn_papers_data(author):  
    """从new1表获取撤稿论文相关数据"""  
    query = """  
    SELECT  
        作者,  
        撤稿论文名称,  
        发表时间,  
        撤稿时间,  
        被引频次,  
        撤稿原因  
    FROM new1  
    WHERE 作者 LIKE %s  
    """  
    Authors_like = f"%{author}%"  
    cnx = get_db_connection()  
    cursor = cnx.cursor(dictionary=True)  
    cursor.execute(query, (Authors_like,))  
    columns = [column[0] for column in cursor.description]  
    data = cursor.fetchall()  
    df = pd.DataFrame(data, columns=columns)  
    cursor.close()  
    cnx.close()  
    return df
def main(): 
    st.title("查询") 
    # 用户输入  
    Authors = st.text_input("请输入作者姓名（部分或全部）进行搜索：")  
    if Authors:  
        authors_data = fetch_authors_data(Authors)  
        withdrawn_papers_data = fetch_withdrawn_papers_data(Authors)  
        withdrawn_papers_data = withdrawn_papers_data.drop(columns=['作者'])  
        # 第一个表格：作者数据
        html_table1 = """  
        <style>  
            table {  
                width: 100%;  
                border-collapse: collapse;  
                font-family: Arial, sans-serif; /* 选择一个合适的字体 */  
                font-size: 14px; /* 设置字体大小 */  
                margin-top: 20px; /* 与上方内容的间距 */  
            }  
            th, td {  
                border: 1px solid #ddd; /* 边框颜色 */  
                padding: 12px; /* 单元格内边距 */  
                text-align: left;  
            }  
            th {  
                background-color: #f2f2f2; /* 表头背景色 */  
                color: #333; /* 表头文字颜色 */  
            }  
            tr:nth-child(even) {  
                background-color: #f9f9f9; /* 隔行变色 */  
            }  
            tr:hover {  
                background-color: #f1f1f1; /* 鼠标悬停变色 */  
            }
            .highlight {  
                background-color: yellow; /* 高亮背景色 */  
                animation: blink 1s infinite; /* 尝试的闪烁动画，但可能不起作用 */  
            }  
            @keyframes blink {  
                0%, 100% { background-color: yellow; }  
                50% { background-color: transparent; } /* 由于Streamlit的限制，这可能不会按预期工作 */  
            }  
        </style>  
        <table>  
            <tr>  
                <th>姓名</th>  
                <th>领域</th>  
                <th>失信指数</th>   
                <th>相关学者</th>  
                <th>研究机构</th>  
            </tr>  
            """    
        for index, row in authors_data.iterrows():  
            highlight_class = 'highlight' if float(row['失信指数']) > 100 else ''  
            html_table1 += f"<tr><td>{row['作者']}</td>"  
            html_table1 += f"<td>{row['领域']}</td>"  
            html_table1 += f"<td class='{highlight_class}'>{row['失信指数']}</td>"  
            html_table1 += f"<td>{row['相关学者']}</td>"  
            html_table1 += f"<td>{row['研究机构']}</td></tr>"  
        html_table1 += "</table>"  
        # 第二个表格：撤稿论文数据  
        html_table2 = withdrawn_papers_data.to_html(index=False, classes='dataframe', header="true")  
        # 显示表格  
        st.write(html_table1, unsafe_allow_html=True)  
        st.write(html_table2, unsafe_allow_html=True)  
if __name__ == "__main__":  
    main()