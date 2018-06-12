#!/user/bin/env python3
#coding: utf-8
from pyVmomi import vim
from kadai6 import vm_module
from kadai13 import get_ip, connect_ssh
import time
import paramiko
from paramiko import SSHException
from paramiko_expect import SSHClientInteraction
import re
#import pexpect

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
	PROMPT = '[root@localhost:~] '
	password = 'Toku1456'
	
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
				logger.info('%sへのSSH接続処理をスキップします' % vm.name)
				logger.info('--------------------------------')
				continue
		
			HOST = vm.summary.guest.ipAddress
		
			ssh = connect_ssh(HOST,USER,PSWD,logger,vm)
			if ssh == False:
				pass
			else:
				result = check_command(ssh, command, logger, vm, PROMPT, password)	

# commandチェックメソッド
def check_command(ssh,command,logger,vm,PROMPT,password):
	
	# コマンドライン引数はtouch cpuinfo.txt & vim-cmd hostsvc/hosthardware & vim-cmd hostsvc/hosthardware > cpuinfo.txt 
	#192.168.144.136 esxcli network firewall set --enabled false

	interact = SSHClientInteraction(ssh, display=True)
#	interact.expect(PROMPT)
	interact.send(command)	
	interact.send('scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga')
	interact.send('yes')
	interact.expect('tokunaga@192.168.144.136\'s password:')#→ここで止まってしまう,これなくてパスワード実行してもできない
	interact.send('Toku1456')
	interact.expect()
	#if(re.search('[',))
#	interact.send('ls')
#		interact.expect(PROMPT)
#	output = interact.current_output_clean
#	ssh.close()
#	interact.send('scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga')
#	interact.expect('Toku1456')

#print(cmd_output_name)
#	interact.send('scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga')
#	interact.expect([PROMPT, 'tokunaga@192.168.144.136\'s password:'])
#	if interact.last_match == 'tokunaga@192.168.144.136\'s password:':
#		interact.send('aaaaaaa')
#		interact.expect(PROMPT)
		
#		interact.send('')
#		sentence = interact.expect(PROMPT)
#		if sentence:
#			interact.expect(yes)



















#	stdin, stdout, stderr = ssh.exec_command('scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga')
#	print(stdout.readlines())
#	print(stderr.readlines())
#	time.sleep(20)




	#stdin, stdout, stderr = ssh.exec_command(command)
	#   stdin, stdout, stderr = ssh.exec_command('scp cpuinfo.txt tokunaga@192.168.144.136:/home/tokunaga')
	#   stdin.write('Toku1456')
	#   stdin.flush()
	#   print(stdout.readlines())
	#   print(stderr.readlines())



	
	#shell = ssh.invoke_shell()
	#s = shell.recv(1000)
	#shell.send('ls')
	#a = s.decode('utf-8')
	#print(a)
	#output = s.decode('utf-8')
	#print(output)
	# if(re.search('The',output)):
		# a = shell.send('Toku1456')
		# print(a)
		#shell.sendall('Toku1456')
	


# どちらにもオブジェクトは入ってるので、テキスト内容で比較
#	out = stdout.readlines()
#	err = stderr.readlines() 
#	if out != []:
#		for out_info in out:
#			logger.info('{:<15}'.format(vm.name) + out_info.strip('\n'))
#		logger.info('-------------------------------------------')
#	elif err != []:
#		logger.info('コマンド入力でエラーが発生しました')
#		for err_info in err:
#			logger.info('{:<15}'.format('エラー内容') + err_info.strip('\n'))
#		logger.info('-------------------------------------------')

if __name__ == '__main__':
	main()
