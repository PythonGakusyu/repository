#!/user/bin/env python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
from kadai13 import get_ip, connect_ssh
import time
#import paramiko
#from paramiko import SSHException
#from paramiko_expect import SSHClientInteraction
#import re
import pexpect
import sys
import re

def main():
	# loggerフォーマットメソッド
	logger = vm_module.logger_format()
	# parserメソッド
	args = vm_module.set_args_paramiko()
	#接続メソッド
	si = vm_module.si_connect(args.host, args.username, args.password)
	#CreateContainerViewメソッド	
	vm_list = vm_module.CreateContainerView(si, vim.VirtualMachine)
	
	USER = args.ssh_username
	PSWD = args.ssh_password

	vm_name = 'centos-1-g2'

	logger.info('開始します')
	logger.info('--------------------------------')

	# 転送先のVM電源ON、IPアドレス取得
	for vm in vm_list.view:

		if vm.name == vm_name:
			ip_result = get_ip(vm, logger)
			if ip_result == True:
				logger.info('転送先の%sのIPアドレスの取得成功' % vm.name)
				logger.info('')
			else:
				logger.info('転送先の%sのIPアドレスの取得失敗' % vm.name)
				logger.info('')
				logger.info('転送することができないため、終了します')
				sys.exit()
	
	# 転送元のVM電源ON、IPアドレス取得
	for vm in vm_list.view:
		if vm.name == 'ESXi':
			ip_result = get_ip(vm, logger)
			if ip_result == True:
				logger.info('%sのIPアドレスの取得成功' % vm.name)
				logger.info('')
			else:
				logger.info('%sのIPアドレスの取得失敗' % vm.name)
				logger.info('')
				logger.info('%sへのSSH接続処理が実行不可のため終了します' % vm.name)
				sys.exit()

			HOST = vm.summary.guest.ipAddress

			ssh = dossh(USER, PSWD, HOST, logger)

def dossh(USER, PSWD, HOST, logger):
	child = pexpect.spawn('ssh %s@%s' % (USER, HOST))
#	index =child.expect(['Password:', '(yse/no)?'])
#	if index == 0:
#		child.sendline(PSWD)
#	elif index == 1:
#		child.sendline('yes')
#		if index == 0:
#			child.sendline(PSWD)


#	index = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'tokunaga@192.168.144.136\'s password:'])
	
#	child.expect('Password:')
#	child.sendline(PSWD)
#	print(child.buffer)
#	child.expect('[root@localhost:~]')
	child.sendline('touch cpuinfo.txt')
	print(child.readline().decode('utf-8'))
	child.sendline('cat /proc/cpuinfo')
	print(child.readline().decode('utf-8'))
	child.sendline('cat /proc/cpuinfo  > cpuinfo.txt')
	print(child.readline().decode('utf-8'))
	child.sendline('scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga')
	print(child.readline().decode('utf-8'))
	child.sendline('Toku1456')
	print(child.readline().decode('utf-8'))
	child.interact()
#	a = 'tokunaga@192.168.144.136\'s password:'
#	b = 'Are you sure you want to continue connecting (yes/no)?'
#	if re.search(a, input_message):
#		child.sendline('Toku1456')
#	elif re.search(b, input_message):
#		child.sendline('yes')
#		child.sendline('Toku1456')
		
#	child.interact()
#	child.expect('[root@localhost:~]')
	child.sendline('exit')
#	child.readline()
#	print(child.buffer)
#	child.interact()
#	print(child)
	child.close()



if __name__ == '__main__':
	main()
