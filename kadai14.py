#!/user/bin/env python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
from kadai13 import get_ip, connect_ssh
import time
import paramiko
from paramiko import SSHException

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
	command = args.command

	
	logger.info('開始します')
	logger.info('--------------------------------')
	for vm in vm_list.view:
		if vm.name == 'ESXi':
			ip_result = get_ip(vm, logger)
			if ip_result == True:
				logger.info('%sのIPアドレスの取得成功' % vm.name)
				logger.info('')
			else:
				logger.info('%sのIPアドレスの取得に失敗' % vm.name)
				logger.info('')
				logger.info('%sへのSSH接続処理をスキップします')
				logger.info('--------------------------------')
				continue
		
			HOST = vm.summary.guest.ipAddress
		
			ssh = connect_ssh(HOST,USER,PSWD,logger,vm)
			if ssh == False:
				pass
			else:
				result = check_command(ssh, command, logger, vm)	

# commandチェックメソッド
def check_command(ssh,command,logger,vm):
	stdin, stdout, stderr = ssh.exec_command(command)

# どちらにもオブジェクトは入ってるので、テキスト内容で比較
	out = stdout.readlines()
	err = stderr.readlines() 
	if out != []:
		for out_info in out:
			logger.info('{:<15}'.format(vm.name) + out_info.strip('\n'))
		logger.info('-------------------------------------------')
	elif err != []:
		logger.info('コマンド入力でエラーが発生しました')
		for err_info in err:
			logger.info('{:<15}'.format('エラー内容') + err_info.strip('\n'))
		logger.info('-------------------------------------------')

if __name__ == '__main__':
	main()
