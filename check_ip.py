#!/user/bin/env python3
#coding: UTF-8
import re

def main():
	ip = '1.0.0.0'
	result = check_ip(ip)
	print(result)


def check_ip(ip):
	ip_pattern = "\.".join(["\d{1,3}"] * 4)
	# ip_pattern = '(^((\d{1,3})\.){3}(\d{1,3})$)'
	private_ip = '(^10\.)|(^172\.1[6-9]|2[0-9]|3[0-1]\.)|(^192\.168\.)'
	if not re.fullmatch(ip_pattern, ip):
		return False
	if re.search(private_ip, ip):
		return 'private'
	else:
		return 'global'

if __name__ == '__main__':
	main()
