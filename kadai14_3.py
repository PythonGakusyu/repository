#!/user/bin/env/ python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
from kadai13 import get_ip, connect_ssh
import sys
from pexpect import pxssh
import re

def main():
	# loggerフォーマットメソッド
	logger = vm_module.logger_format()
	# parserメソッド
	args = vm_module.set_args_paramiko()
	# 接続メソッド
	si = vm_module.si_connect(args.host, args.username, args.password)
	#CreateContainerViewメソッド
	vm_list = vm_module.CreateContainerView(si, vim.VirtualMachine)


	USER = args.ssh_username
	PSWD = args.ssh_password

	vm_name = 'centos-1-g2'
	ESXi_name = 'ESXi'
	
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
		if vm.name == ESXi_name:
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

			try:
				ssh = connect_ssh(HOST, USER, PSWD)

			except pxssh.ExceptionPxssh as e:
				print('ssh接続できませんでした。終了します。')
				print(str(e))
				sys.exit()

			logger.info('ssh接続を開始します')
			logger.info('')

			command = 'touch cpuinfo.txt'
			ssh_execution(ssh, command, logger)

			command = 'cat /proc/cpuinfo'
			ssh_execution(ssh, command, logger)

			command = 'cat /proc/cpuinfo  > cpuinfo.txt'
			ssh_execution(ssh, command, logger)

			command = 'scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga'
			ssh_execution(ssh, command, logger)



			a = 'tokunaga@192.168.144.136\'s password:'
			b = 'Are you sure you want to continue connecting (yes/no)?'
			input_message = ssh.before.decode('utf-8')

			if re.search(a, input_message):
				command = 'Toku1456'
				ssh_execution(ssh, command, logger)
			elif re.search(b, input_message):
				command = 'yes'
				ssh_execution(ssh, command, logger)
				command = 'Toku1456'
				ssh_execution(ssh, command, logger)

			logger.info('--------------------------------')
			ssh.logout()



# ssh接続
def connect_ssh(HOST, USER, PSWD):
	ssh = pxssh.pxssh()
	hostname = HOST
	username = USER
	password = PSWD
	ssh.login(hostname, username, password, auto_prompt_reset=True)
	return ssh

# コマンド実行
def ssh_execution(ssh, command, logger):
	ssh.sendline(command)
	ssh.prompt()
	logger.info(ssh.before.decode('utf-8'))


if __name__ == '__main__':
	main()
