import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 设置页面标题
st.title("科研人员信用风险预警查询")

# 读取Excel文件
df_new2_2 = pd.read_excel('new2.2.xlsx')
df_new2_1 = pd.read_excel('new2.1.xlsx')

# 合并两个数据表（根据实际情况，这里假设以行的形式简单合并，如果有更复杂的合并逻辑需调整）
combined_df = pd.concat([df_new2_2, df_new2_1], ignore_index=True)

# 输入查询名字之前，展示失信指数前5的人对应的折线图
if not query_name:
    top_5 = combined_df.sort_values(by='失信指数', ascending=False).head(5)
    plt.plot(top_5['作者'], top_5['失信指数'])
    plt.xlabel('科研人员（作者）')
    plt.ylabel('失信指数')
    plt.title('失信指数前5的科研人员情况')
    plt.xticks(rotation=45)
    st.pyplot(plt)

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
