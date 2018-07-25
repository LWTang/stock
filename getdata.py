import pandas as pd
import numpy as np
import datetime

data=all_instruments(type='CS')
data=pd.DataFrame(data)
data.drop(['board_type','de_listed_date','exchange','industry_code','listed_date','round_lot','sector_code','sector_code_name','special_type','type'],axis=1,inplace=True)

s_date='2018-05-01'
e_date='2018-05-20'
n_days=28

def get_data( data, s_date, day_list, idx):
  #前100id
  data=data[data['status'].str.contains('Active')]
  id = list(data['order_book_id'].values)
  id_value = dict.fromkeys(id, 0)
  for order_book_id in id:
    tmp=get_price(order_book_id, start_date=s_date, end_date=s_date, frequency='1d', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    #tmp=get_price(order_book_id, start_date='2018-01-04', end_date='2018-01-04', frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    value=np.array((tmp['high']-tmp['open'])/tmp['open'])
    s_flag = 1
    cnt = 0
    if value :
      tp=get_price(order_book_id, start_date=s_date, end_date=s_date, frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
      for index,select in tp.iterrows() :
        h_va=(select['high']-tmp['open'])/tmp['open']
        l_va=(select['low']-tmp['open'])/tmp['open']
        if ((h_va[0] >= 0.1) or (l_va[0] <= -0.1)):
            s_flag = 0
            cnt = cnt + 1
        else :
          pass
    else :
      s_flag = 0
    if ( s_flag and (cnt < 120) ) :
      id_value[order_book_id] = value[0]
    else :
      id_value[order_book_id] = 0
  
  sort_d=sorted(id_value.items(),key = lambda id_value:id_value[1],reverse=True)
  m_id=[]
  count=0
  for key,value in sort_d:
    count=count+1
    m_id.append(key)
    if count>=100 :
      break

  #前100 当天的总数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=s_date, end_date=s_date, frequency='1d', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    tmp['increase']=id_value[order_book_id]
    #tmp['Timestr']=tmp.index.values#.astype(str)
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%9f').timestamp())
    #del(tmp['Timestr'])
    tmp['Time']=s_date
    if flag == 1 :
      df=tmp
      flag = 0
    else :
      df=df.append(tmp)
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df=pd.DataFrame(df)
  id = df['order_book_id']
  df.drop(labels=['order_book_id'], axis=1,inplace = True)
  df.insert(0, 'order_book_id', id)

  df.index = range(1,len(df)+1) 
  df.to_csv('first.csv',header=None,index=None,mode='a+')

  #前100 当天的数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=s_date, end_date=s_date, frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    #tmp['Timestr']=tmp.index.values#.astype(str)
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%9f').timestamp())
    #del(tmp['Timestr'])
    tmp['Time']=s_date
    if flag == 1 :
      df0=tmp
      flag = 0
    else :
      df0=df0.append(tmp)
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df0=pd.DataFrame(df0)
  id = df0['order_book_id']
  df0.drop(labels=['order_book_id'], axis=1,inplace = True)
  df0.insert(0, 'order_book_id', id)

  df0.index = range(1,len(df0)+1) 
  df0.insert(0, 'id', df0.index)
  df0.to_csv('stock.csv',header=None,index=None,mode='a+')

  #前100 前1天的数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=day_list[cnt+1], end_date=day_list[cnt+1], frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    #tmp['Timestr']=tmp.index.values#.astype(str)
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%9f').timestamp())
    #del(tmp['Timestr'])
    tmp['Time']=s_date
    if flag == 1 :
      df1=tmp
      flag = 0
    else :
      df1=df1.append(tmp)
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df1=pd.DataFrame(df1)
  id = df1['order_book_id']
  df1.drop(labels=['order_book_id'], axis=1,inplace = True)
  df1.insert(0, 'order_book_id', id)

  df1.index = range(1,len(df1)+1) 
  df1.insert(0, 'id', df1.index)
  df1.to_csv('stock1.csv',header=None,index=None,mode='a+') 

  #前100 前2天的数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=day_list[cnt+2], end_date=day_list[cnt+2], frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    #tmp['Timestr']=tmp.index.values#.astype(str)
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%9f').timestamp())
    #del(tmp['Timestr'])
    pydate_array = tmp.index.to_pydatetime()
    date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydate_array )
    tmp['Time']=s_date
    if flag == 1 :
      df2=tmp
      flag = 0
    else :
      df2=df2.append(tmp)
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df2=pd.DataFrame(df2)
  id = df2['order_book_id']
  df2.drop(labels=['order_book_id'], axis=1,inplace = True)
  df2.insert(0, 'order_book_id', id)

  df2.index = range(1,len(df2)+1) 
  df2.insert(0, 'id', df2.index)
  df2.to_csv('stock2.csv',header=None,index=None,mode='a+')

  #前100 前3天的数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=day_list[cnt+3], end_date=day_list[cnt+3], frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    #tmp['Timestr']=tmp.index.values#.astype(str)	
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%9f').timestamp())
    #del(tmp['Timestr'])
    tmp['Time']=s_date
    if flag == 1 :
      df3=tmp
      flag = 0
    else :
      df3=df3.append(tmp)
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df3=pd.DataFrame(df3)
  id = df3['order_book_id']
  df3.drop(labels=['order_book_id'], axis=1,inplace = True)
  df3.insert(0, 'order_book_id', id)

  df3.index = range(1,len(df3)+1) 
  df3.insert(0, 'id', df3.index)
  df3.to_csv('stock3.csv',header=None,index=None,mode='a+') 

  #前100 前4天的数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=day_list[cnt+4], end_date=day_list[cnt+4], frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    #tmp['Timestr']=tmp.index.values#.astype(str)	
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%9f').timestamp())
    #del(tmp['Timestr'])
    tmp['Time']=s_date
    if flag == 1 :
      df4=tmp
      flag = 0
    else :
      df4=df4.append(tmp)      
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df4=pd.DataFrame(df4)
  id = df4['order_book_id']
  df4.drop(labels=['order_book_id'], axis=1,inplace = True)
  df4.insert(0, 'order_book_id', id)

  df4.index = range(1,len(df4)+1) 
  df4.insert(0, 'id', df4.index)
  df4.to_csv('stock4.csv',header=None,index=None,mode='a+') 

  #前100 前5天的数据   list(data['order_book_id'])
  flag = 1
  for order_book_id in m_id:
    tmp=get_price(order_book_id, start_date=day_list[cnt+5], end_date=day_list[cnt+5], frequency='1m', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    tmp['order_book_id']=str(order_book_id)
    #tmp['Timestr']=tmp.index.values#.astype(str)
    #tmp['Time'] = tmp.Timestr.apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.000000000').timestamp())
    #del(tmp['Timestr'])
    #pydate_array = tmp.index.to_pydatetime()
    #date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydate_array )
    #tmp['Timestr'] = date_only_array
    tmp['Time']=s_date
    if flag == 1 :
      df5=tmp
      flag = 0
    else :
      df5=df5.append(tmp)
  #data = pd.merge(df, data, on='order_book_id', how='inner')
  #data.sort_values(['order_book_id','Timestr'], inplace=True)
  df5=pd.DataFrame(df5)
  id = df5['order_book_id']
  df5.drop(labels=['order_book_id'], axis=1,inplace = True)
  df5.insert(0, 'order_book_id', id)

  df5.index = range(1,len(df5)+1) 
  df5.insert(0, 'id', df5.index)
  df5.to_csv('stock5.csv',header=None,index=None,mode='a+')
  
  
def get_day (date, days):
  day=[]
  for i in range(days) :
    s_date=datetime.datetime.strptime(date,'%Y-%m-%d')-datetime.timedelta(days = i)
    re=get_price('000001.XSHE', start_date=s_date, end_date=s_date, frequency='1d', fields=None, adjust_type='pre', skip_suspended=False, country='cn')
    if np.array(re['high']) :
      day.append(s_date)
  return day 

day_list = get_day(e_date, n_days)
cnt = 0
for date in day_list :
  if str(date) < s_date :
    break;
  else :
    get_data( data, date ,day_list, cnt)
    cnt = cnt + 1
