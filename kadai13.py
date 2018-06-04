#!/user/bin/env python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
import time
import paramiko
import sys

def main():
	# loggerフォーマットメソッド
	logger = vm_module.logger_format()
	# parserメソッド
	args = vm_module.set_args_paramiko()
	# 接続メソッド
	si = vm_module.si_connect(args.host ,args.username ,args.password)

	vm_list = si.content.viewManager.CreateContainerView(si.content.rootFolder,
				[vim.VirtualMachine],
				True)

	logger.info('開始します')
	logger.info('-------------------------------------------')
	for vm in vm_list.view:
		if vm.runtime.powerState == 'poweredOff':
			vm.PowerOnVM_Task()
			logger.info(vm.name + 'の電源をONにしました！')
			while vm.runtime.powerState == 'poweredOff':
				logger.info('接続中です')
				time.sleep(5)

		if vm.runtime.powerState == 'poweredOn':
			i = 0
			while vm.summary.guest.ipAddress is None and i < 3:
				logger.info('%sのIPアドレスを取得しています' % vm.name)
				time.sleep(60)
				i = i +1
				if vm.summary.guest.ipAddress is not None:
					break

		HOST = vm.summary.guest.ipAddress
		USER = args.ssh_username
		PSWD = args.ssh_password
					

		# ipが取れなかったとき
		if HOST is None:
			logger.info('IPアドレスを取得できませんでした')
			logger.info('終了します')
			logger.info('-------------------------------------------')
			continue
		
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(HOST, username=USER, password=PSWD)
		stdin, stdout, stderr = ssh.exec_command('hostname')
		
		if vm.summary.guest.ipAddress is not None:
			logger.info('IPアドレスが取得できました')
			logger.info('')
			logger.info('ssh接続します')
			for line in stdout:
				logger.info('{:<15}'.format(vm.name) + line.strip('\n'))
				logger.info('-------------------------------------------')
				ssh.close()
			
if __name__ == '__main__':
	main()
