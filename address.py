# encoding:utf-8
import requests

# 此处需要ak，ak申请地址：https://lbs.amap.com/dev/key/app
ak = "ada77f29833d2bf09512e9aecb739d9b"

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'https://restapi.amap.com/'
}


def geocode(address):
    parameters = {'address': address, 'key': ak}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print(address + "的经纬度：", answer)


if __name__ == '__main__':
    # address = input("请输入地址:")
    address = '北京市海淀区'
    geocode(address)
