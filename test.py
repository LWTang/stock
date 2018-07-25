import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
data=all_instruments(type='CS')
data=pd.DataFrame(data)
data.drop(['board_type','de_listed_date','exchange','abbrev_symbol','listed_date','round_lot','sector_code','sector_code_name','special_type','type'],axis=1,inplace=True)
order_book_id = data['symbol']
data.drop(labels=['symbol'], axis=1,inplace = True)
data.insert(0, 'symbol', order_book_id)
order_book_id = data['order_book_id']
data.drop(labels=['order_book_id'], axis=1,inplace = True)
data.insert(0, 'order_book_id', order_book_id)

data=data[data['status'].str.contains('Active')]
data.drop(['status'],axis=1,inplace=True)
data

