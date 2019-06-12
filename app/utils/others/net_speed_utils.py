# coding=utf-8
'''
  Created by lyy on 2019-06-10
'''

__author__ = 'lyy'

import speedtest

servers = []
# If you want to test against a specific server
# servers = [1234]

s = speedtest.Speedtest()
print('开始查找最佳测速服务器...')
s.get_servers(servers)
s.get_best_server()
print('开始测试下载速度...')
s.download()
print('开始测试上传速度...')
s.upload(pre_allocate=False)
print(type(s.results))
print(s.results.ping)
print(s.results.download)
print(s.results.upload)
print(s.results.share())
print(s.results.client)

results_dict = s.results.dict()

print("测试结果为：")
print(results_dict)