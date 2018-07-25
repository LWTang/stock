import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
data=all_instruments(type='CS')
data=pd.DataFrame(data)
data=data[data['status'].str.contains('Active')]

df=data['industry_code'].unique()
df