import baostock as bs
import pandas as pd
from datetime import date


pattern_shIndex = r'^sh\.000\d{3}$'
pattern_szIndex = r'^sz\.399\d{3}$'


#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)


#### 获取历史K线数据 ####
rs=bs.query_all_stock(day=date.today())
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)


#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

result['tradeStatus'] = pd.to_numeric(result['tradeStatus'], errors='coerce')
clean_index_result = result[~result['code'].str.match(pattern_shIndex) & ~result['code'].str.match(pattern_szIndex)]
clean_index_delist_result = clean_index_result[clean_index_result['tradeStatus']!=0]

clean_index_delist_result.drop(['tradeStatus'], axis=1,inplace=True)

#### 结果集输出到csv文件 ####
clean_index_delist_result.to_csv("../asset/stock_info.csv", encoding="gbk", index=False)
print(clean_index_delist_result)

#### 登出系统 ####
bs.logout()
