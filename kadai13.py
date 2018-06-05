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

	USER = args.ssh_username
	PSWD = args.ssh_password
	command = args.command

	logger.info('開始します')
	logger.info('-------------------------------------------')
	for vm in vm_list.view:
		# IP取得メソッド
		ip_result = get_ip(vm,logger)
		# IP取得の結果判定
		if ip_result is True:
			logger.info('%sのIPアドレスの取得成功' % vm.name)
			logger.info('')
		else:
			logger.info('%sのIPアドレスの取得失敗' % vm.name)
			logger.info('')
			logger.info('%sへのSSH接続をスキップします' % vm.name)
			logger.info('-------------------------------------------')
			continue
		
		# 値を代入
		HOST = vm.summary.guest.ipAddress
		
		# SSH接続メソッド
		ssh  = connect_ssh(HOST,USER,PSWD,logger,vm)
		# 接続結果がFalseの場合passして終了
		if ssh is False:
			pass
		else:
			result = check_command(ssh,command,logger,vm)



# IP取得メソッド
def get_ip(vm,logger):
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
			return True
		else:
			return False


# ssh接続メソッド
def connect_ssh(HOST,USER,PSWD,logger,vm,):
	try:
		logger.info('SSH接続します...')
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(HOST, username=USER, password=PSWD)
	except SSHException as e:
		logger.info(e)
		logger.info('接続に失敗しました')
		logger.info('%sへのSSH接続でエラーが発生したのでスキップします' % vm.name)
		logger.info('-------------------------------------------')
		return False
	else:
		logger.info('接続に成功しました')
		return ssh


# commandチェックメソッド
def check_command(ssh,command,logger,vm):
	stdin, stdout, stderr = ssh.exec_command(command)
	
	# どちらにもオブジェクトは入ってるので、テキスト内容で比較
	out = stdout.readline()
	err = stderr.readline()

	if out != '':
		logger.info('{:<15}'.format(vm.name) + out.strip('\n'))
		logger.info('-------------------------------------------')
	elif err != '':
		logger.info('コマンド入力でエラーが発生しました')
		logger.info('{:<15}'.format('エラー内容') + err.strip('\n'))
		logger.info('-------------------------------------------')
	
if __name__ == '__main__':
	main()
