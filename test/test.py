# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''
import requests


def get_ip_info(ip):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    r = requests.get(url)
    print(r.json())


if __name__ == '__main__':
    get_ip_info('119.23.212.45')