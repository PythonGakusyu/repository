#!/user/bin/env python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
import time
import paramiko
import sys
from paramiko import SSHException

def main():
	# loggerフォーマットメソッド
	logger = vm_module.logger_format()
	# parserメソッド
	args = vm_module.set_args_paramiko()
	# 接続メソッド
	si = vm_module.si_connect(args.host ,args.username ,args.password)
	# CreateContainerViewメソッド 
	vm_list = vm_module.CreateContainerView(si, vim.VirtualMachine)

	logger.info('開始します')
	logger.info('-------------------------------------------')
	for vm in vm_list.view:
		# IP取得メソッド
		get_id(vm,logger)
		if vm.summary.guest.ipAddress is None:
			logger.info('%sのIPアドレスの取得失敗' % vm.name)
			logger.info('')
			logger.info('%sへのSSH接続をスキップします' % vm.name)
			logger.info('-------------------------------------------')
			continue
		
		# 値を代入
		HOST = vm.summary.guest.ipAddress
		USER = args.ssh_username
		PSWD = args.ssh_password
		
		# SSH接続メソッド
		result = connect_ssh(HOST,USER,PSWD,'hostname',logger, vm)






# IP取得メソッド
def get_id(vm,logger):
	if vm.runtime.powerState == 'poweredOff':
		vm.PowerOnVM_Task()
		logger.info(vm.name + 'の電源をONにしました！')
		while vm.runtime.powerState == 'poweredOff':
			logger.info('接続中です')
			time.sleep(3)
	
	if vm.runtime.powerState == 'poweredOn':
		i = 0
		while vm.summary.guest.ipAddress is None and i < 3:
			logger.info('%sのIPアドレスを取得しています' % vm.name)
			time.sleep(60)
			i = i +1
		if vm.summary.guest.ipAddress is not None:
			logger.info('%sのIPアドレスの取得成功' % vm.name)
			logger.info('')
	

# ssh接続メソッド
def connect_ssh(HOST,USER,PSWD,command,logger,vm):
	try:
		logger.info('SSH接続します...')
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(HOST, username=USER, password=PSWD)
		stdin, stdout, stderr = ssh.exec_command(command)
	except SSHException as e:
		logger.info(e)
		logger.info('接続に失敗しました')
		logger.info('%sへのSSH接続でエラーが発生したのでスキップします' % vm.name)
		logger.info('-------------------------------------------')
	# 例外処理が起きなかったら出力
	else:
		logger.info('接続に成功しました')
		if vm.summary.guest.ipAddress is not None:
			for line in stdout:
				logger.info('{:<15}'.format(vm.name) + line.strip('\n'))
				logger.info('-------------------------------------------')
				ssh.close()



			
if __name__ == '__main__':
	main()
