#!/user/bin/env python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
import paramiko

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
	for vm in vm_list.view:
		if vm.runtime.powerState == 'poweredOn':
			HOST = vm.summary.guest.ipAddress 
			USER = args.ssh_username
			PSWD = args.ssh_password
			
			if HOST is None:
				logger.info('{:<15}'.format(vm.name) + 'VMにIPアドレスが設定されていません')
				continue

			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(HOST, username=USER, password=PSWD)

			stdin, stdout, stderr = ssh.exec_command('hostname')
 
			for line in stdout:
				print('{:<15}'.format(vm.name) + line.strip('\n'))

			ssh.close()
		else:
			logger.info('{:<15}'.format(vm.name) + 'VMの電源が入っていません')

if __name__ == '__main__':
	main()
