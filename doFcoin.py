import requests
from prettytable import PrettyTable
from bs4 import BeautifulSoup as bs


# 获取币圈行情，数据来源：非小号网站
# def getDigitalCurrencyQuotes():
#     header = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36"
#                       " (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
#     }
#     # url = 'https://www.feixiaohao.com/'
#     url = 'https://www.feixiaohao.com/exchange/fcoin/'
#     # url = 'https://exchange.fcoin.com/ex/main/btc/usdt'
#     web_data = requests.get(url, headers=header)
#     web_data.encoding = 'utf-8'
#     # print(web_data.text)
#     soup = bs(web_data.text, 'html.parser')
#     # print(bitprice)
#     sumdata = soup.select('#table > tbody')  # 得到列表
#     pt = PrettyTable()
#     pt._set_field_names(('名称 价格 跌幅 成交额 流通市值 流通数量').split())
#     filter = 'BTC-比特币 | ETH-以太坊 | EOS-柚子 '
#     for onedata in sumdata[0].find_all('tr'):
#         # print(onedata)        # 其值如:<tr id="pura"><td>100</td><td><a href="/currencies/pura/" target="_blank"> <img alt="PURA" src="//static.feixiaohao.com/coin/6126b465f9bf4b8fedc6f01dbbcc1741_small.png"/>PURA </a></td><td class="market-cap" data-btc="2358" data-cny="119227259" data-usd="17423244">¥1.19亿</td><td><a class="price" data-btc="0.00001351" data-cny="0.6832" data-usd="0.0998" href="/currencies/pura/#markets" target="_blank">¥0.6832</a></td><td>17,452万</td><td><a class="volume" data-btc="1.91301414537796" data-cny="96603.6389065968" data-usd="28917.3816725" href="/currencies/pura/#markets" target="_blank">¥96,604</a></td><td class="change"><span class="new-text-red">-0.43%</span></td><td class="char"><span class="line2" data-peity='{"stroke": "#3ca316"}'>0.0973,0.1008,0.1053,0.1012,0.1025,0.1008,0.0999,0.0986,0.0981,0.0957,0.0945,0.0923,0.0928,0.0950,0.0931,0.0956,0.0973,0.0978,0.1039,0.1031,0.1018,0.1034,0.1023,0.1002,0.1002,0.1001,0.1000,0.0993</span></td></tr>
#         # print('test')
#         # print(type(onedata))  # 其类型为<class 'bs4.element.Tag'>
#         # print(onedata.name)   # 其标签为tr,例如tr为标签,<tr>这里是内容</tr>这个全部就表示元素,以标签开头以标签结束
#         # print(onedata.attrs)  # 获取属性，如{'id': 'pura'}
#         data = onedata.find_all(
#             'td')  # 如 [<td>1</td>, <td><a href="/currencies/bitcoin/" target="_blank"> <img alt="BTC-比特币" src="//static.feixiaohao.com/coin/7033f2f2c2a16094bbb3bafc47205ba8_small.png"/>BTC-比特币 </a></td>, <td class="market-cap" data-btc="17250187" data-cny="868294521519" data-usd="126902692770">¥8,683亿</td>, <td><a class="price" data-btc="1" data-cny="50335" data-usd="7357" href="/currencies/bitcoin/#markets" target="_blank">¥50,335</a></td>, <td>1,725万</td>, <td><a class="volume" data-btc="545716.806224186" data-cny="27443015903.4148" data-usd="4010688184.27393" href="/currencies/bitcoin/#markets" target="_blank">¥2,744,302万</a></td>, <td class="change"><span class="new-text-green">0.87%</span></td>, <td class="char"><span class="line2" data-peity='{"stroke": "#3ca316"}'>6933,7019,7074,7015,7051,7009,6928,6866,6927,7000,6951,7032,7051,7091,7174,7193,7211,7274,7268,7275,7212,7251,7246,7250,7313,7367,7349,7354</span></td>]
#         # print(data)
#         name = data[1].get_text()  # 名称
#         # print(name)
#         if (filter.find(name.strip()) > -1):  # 私人定制自己关注的币
#             for pos in range(len(data)):
#                 # print(data[pos].get_text())
#                 # name = data[1].get_text()         # 名称
#                 marketvalue = data[2].get_text()  # 流通市值
#                 price = data[3].get_text()  # 价格
#                 amount = data[4].get_text()  # 流通数量
#                 turnover = data[5].get_text()  # 成交额
#                 changerange = data[6].get_text()  # 涨跌
#             pt.add_row([name, price, changerange, turnover, marketvalue, amount])
#     print(pt)


if __name__ == '__main__':
    # getDigitalCurrencyQuotes()
    pass