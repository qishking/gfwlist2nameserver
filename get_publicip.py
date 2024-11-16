import urllib.request

ip_txt = urllib.request.urlopen(url='https://ipapi.co/ip/').read()

print(ip_txt)
with open('public_ip.txt', 'w') as f:
    f.write(str(ip_txt))
