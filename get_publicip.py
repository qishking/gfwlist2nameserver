import urllib3

ip_txt = urllib3.request(url='https://ipapi.co/ip/', method='get').data
print(ip_txt)
