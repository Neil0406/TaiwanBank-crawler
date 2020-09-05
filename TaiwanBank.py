#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[3]:


from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime
import tkinter as tk
res = requests.get('https://rate.bot.com.tw/xrt?Lang=zh-TW')
soup = bs(res.text,'lxml')


window = tk.Tk()
window.title('即時匯率')
window.geometry('350x300')
window.configure(background='white')



def dtime():
    datetime_dt = datetime.datetime.today()
    return  datetime_dt.strftime("%Y-%m-%d %H:%M:%S")      # ("%Y-%m-%d %H:%M:%S")   取到時分秒

before = pd.read_csv('TBlog.csv')     #上次取得的檔案


update_time = []
average = []
currency = []
spread = []
data = soup.select('.print_show')
r = []
for i in data:
    r.append(i.text.split())
for i in r:
    currency.append(i[0])
#現買
purchase = []
data = soup.select('#ie11andabove > div > table > tbody > tr > td:nth-child(2)')
for i in data:
    purchase.append(i.text)
#現賣
selling = []
data = soup.select('#ie11andabove > div > table > tbody > tr > td:nth-child(3)')
for i in data:
    selling.append(i.text)
#即期買
purchase1 = []
data = soup.select('#ie11andabove > div > table > tbody > tr > td:nth-child(4)')
for i in data:
    purchase1.append(i.text) 
    
#即期賣
selling1 = []
data = soup.select('#ie11andabove > div > table > tbody > tr > td:nth-child(5)')
for i in data:
    selling1.append(i.text)

for i in range(len(selling1)):
    update_time.append(dtime())
    
for i in range(len(currency)):
    try:
        avr = (float(purchase[i]) + float(selling[i])) / 2
        average.append(f'{avr:.2f}')
    except:
        average.append('-')
        
#------------------------------價差測試--------------------------------        
for i in range(len(currency)):
    try:
        sp = float(selling[i]) - float(before['現金賣價'][i])        #本次 - 上次  正數表示貴了  
        spread.append(f'{sp:.2f}')
    except:
        spread.append('-')
                  
    
dic = {
    'TIME':update_time,
    '幣別':currency,
    '現金買價': purchase,
    '現金賣價':selling,
    '即期買價':purchase1,
    '即期賣價':selling1,
    '現金中價':average,
    '現金賣價差':spread
}

df = pd.DataFrame(dic)

df.to_csv('TBlog.csv')         #重新存檔
        

def usd():
    result = df.iloc[0]
    result_label.configure(text=result)

def jpy():
    result = df.iloc[7]
    result_label.configure(text=result)

def aud():
    result = df.iloc[3]
    result_label.configure(text=result)

def eur():
    result = df.iloc[14]
    result_label.configure(text=result)

def hkd():
    result = df.iloc[1]
    result_label.configure(text=result)
    
def cny():
    result = df.iloc[18]
    result_label.configure(text=result)

def gbp():
    result = df.iloc[2]
    result_label.configure(text=result)

def krw():
    result = df.iloc[15]
    result_label.configure(text=result)

def chf():
    result = df.iloc[6]
    result_label.configure(text=result)
    
def thb():
    result = df.iloc[11]
    result_label.configure(text=result)

#TOP
header_label = tk.Label(window, text='台灣銀行匯率')
header_label.pack()

top_frame = tk.Frame(window)
top_frame.pack()
bottom_frame = tk.Frame(window)
bottom_frame.pack(side=tk.BOTTOM)
# 以下為 top 群組
left_button = tk.Button(top_frame, text='美金',command = usd)
# 讓系統自動擺放元件，預設為由上而下（靠左）
left_button.pack(side=tk.LEFT)

middle_button = tk.Button(top_frame, text='日幣',command = jpy)
middle_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame, text='澳幣',command = aud)
right_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame, text='歐元',command = eur)
right_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame, text='港幣',command = hkd)
right_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame, text='人民幣',command = cny)
right_button.pack(side=tk.LEFT)
#------------------------------------------------------
top_frame2 = tk.Frame(window)
top_frame2.pack()
bottom_frame2 = tk.Frame(window)
bottom_frame2.pack(side=tk.BOTTOM)
# 以下為 top 群組
left_button = tk.Button(top_frame2, text='英鎊',command = gbp)
# 讓系統自動擺放元件，預設為由上而下（靠左）
left_button.pack(side=tk.LEFT)

middle_button = tk.Button(top_frame2, text='韓元',command = krw)
middle_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame2, text='瑞士法朗',command = chf)
right_button.pack(side=tk.LEFT)

right_button = tk.Button(top_frame2, text='泰銖',command = thb)
right_button.pack(side=tk.LEFT)


result_label = tk.Label(window)
result_label.pack()

window.mainloop()

