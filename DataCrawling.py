import requests
import pandas as pd
import time


# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
# url = "https://stock.xueqiu.com/v5/stock/quote.json?symbol=SZ000858&extend=detail"
# req = urllib.request.Request(url=url, headers=headers)
# context = urllib.request.urlopen(req).read()
# print(context.decode("utf8"))
# headers = {}
# url = Request(url, headers=headers)


# https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH601360&begin=1648275698562&end=1679811698386&period=day&type=before&indicator=kline

# 白酒
# https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=30&order=desc&order_by=percent&exchange=CN&market=CN&ind_code=S3405
# 教育
# https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=30&order=desc&order_by=percent&exchange=CN&market=CN&ind_code=S4611



def timeStamp2time(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    date = time.strftime("%Y-%m-%d", timeArray)
    return date



# 获取索引页
def get_index_page():
    url = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=30&order=desc&order_by=percent&exchange=CN&market=CN&ind_code=S4611"
    session = requests.Session()
    session.headers = {
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    session.get('https://xueqiu.com/')

    r = session.get(url=url)
    r = r.json()
    return r


# begin 1648275698562
# end 1679811698386
#
def get_k_line(symbol, begin, end):
    url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin={}&end={}&period=day&type=before&indicator=kline".format(
        str(symbol), str(begin), str(end))
    session = requests.Session()
    session.headers = {
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    session.get('https://xueqiu.com/')

    r = session.get(url=url)
    r = r.json()

    return r


#  ["timestamp","volume","open","high","low","close","chg","percent","turnoverrate","amount","volume_post","amount_post"]
def parse_page(json):
    data_list = json['data']['list']
    data_list_csv = []
    for data in data_list:
        data_dict = {}
        name = data['name']
        symbol = data['symbol']
        # 获取该股票从2022-3-26到2023-3-25的k每日数据
        result = get_k_line(symbol, 1648275698562, 1679811698386)
        column = result['data']['column']
        dict = {}
        for i in range(len(column)):
            dict[column[i]] = i
        item_list = result['data']['item']
        for item in item_list:
            timestamp = item[dict['timestamp']]
            date = timeStamp2time(timestamp)
            volume = item[dict['volume']]
            open = item[dict['open']]
            high = item[dict['high']]
            low = item[dict['low']]
            close = item[dict['close']]
            chg = item[dict['chg']]
            percent = item[dict['percent']]
            turnover_rate = item[dict['turnoverrate']]
            amount = item[dict['amount']]
            data_dict = {"股票代码": symbol,
                         "股票名称": name,
                         "日期": date,
                         "开盘价": open,
                         "最高价": high,
                         "最低价": low,
                         "收盘价": close,
                         "涨跌额": chg,
                         "涨跌幅度": percent,
                         "成交量": volume,
                         "成交额": amount,
                         "换手率": turnover_rate,
                         }
            data_list_csv.append(data_dict)
            print(f"++++++++++++已获取【{name}】的数据++++++++++++")
    save_csv(data_list_csv, mode='w')


def save_csv(data, name=None, mode='a', header=True):
    df = pd.DataFrame(data)
    if name is None:
        path = './dataset/data.csv'
    else:
        path = './dataset/' + name + '.csv'
    df.to_csv(path, encoding='utf8', mode=mode, header=header)


def main():
    # 1 获取数据，保存至data.csv
    print("++++++++++++正在获取教育的股票数据++++++++++++")
    json = get_index_page()
    parse_page(json)


if __name__ == '__main__':
    main()
