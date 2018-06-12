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
    #接続メソッド
    si = vm_module.si_connect(args.host, args.username, args.password)
    #CreateContainerViewメソッド
    vm_list = vm_module.CreateContainerView(si, vim.VirtualMachine)


    USER = args.ssh_username
    PSWD = args.ssh_password

    centos_name = 'centos-1-g2'
    ESXi_name = 'ESXi'
	
    logger.info('開始します')
    logger.info('--------------------------------')

    # 転送先のVM電源ON、IPアドレス取得
    centos = [vm for vm in vm_list.view if vm.name == centos_name]
    if centos:
        centos_vm = centos[0]
    else:
        logger.error('対象のCentosが見つかりませんでした')
        sys.exit(1)
    ip_result = get_ip(centos_vm, logger)
    if ip_result == True:
        logger.info('転送先の%sのIPアドレスの取得成功' % centos_vm.name)
        logger.info('')
    else:
        logger.error('転送先の%sのIPアドレスの取得失敗' % centos_vm.name)
        logger.info('')
        logger.error('転送することができないため、終了します')
        sys.exit(1)

    # 転送元のVM電源ON、IPアドレス取得
    esxi = [vm for vm in vm_list.view if vm.name == ESXi_name]
    if esxi:
        esxi_vm = esxi[0]
    else:
        logger.error("対象のESXiが見つかりませんでした")
        sys.exit(1)
    ip_result = get_ip(esxi_vm, logger)
    if ip_result == True:
        logger.info('%sのIPアドレスの取得成功' % esxi_vm.name)
        logger.info('')
    else:
        logger.error('%sのIPアドレスの取得失敗' % esxi_vm.name)
        logger.info('')
        logger.error('%sへのSSH接続処理が実行不可のため終了します' % esxi_vm.name)
        sys.exit(1)

    HOST = esxi_vm.summary.guest.ipAddress

    try:
        ssh = connect_ssh(HOST, USER, PSWD)

    except pxssh.ExceptionPxssh as e:
        logger.error('ssh接続できませんでした。終了します。')
        logger.error(str(e))
        sys.exit(1)
			
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

    input_message = ssh.before.decode('utf-8')

#    message_list = ['tokunaga@192.168.144.136\'s password:','Are you sure you want to continue connecting (yes/no)?']
#
#   if re.search(message_list[0], input_message):
#        command = 'Toku1456'
#        ssh_execution(ssh, command, logger)
#    elif re.search(message_list[1], input_message):
#        command = 'yes'
#        ssh_execution(ssh, command, logger)
#        command = 'Toku1456'
#        ssh_execution(ssh, command, logger)

    message = 'Are you sure you want to continue connecting (yes/no)?'
    if re.search(message, input_message):
        command = 'yes'
        ssh_execution(ssh, command, logger)
	
    command = 'Toku1456'
    ssh_execution(ssh, command, logger)

    logger.info('--------------------------------')
    logger.info('出力結果')	
    logger.info(ssh.before.decode('utf-8'))
    logger.info('--------------------------------')
    ssh.logout()



# ssh接続
def connect_ssh(HOST, USER, PSWD):
    ssh = pxssh.pxssh()
    hostname = HOST
    username = USER
    password = PSWD
    ssh.login(hostname, username, password, auto_prompt_reset=False)
    return ssh

# コマンド実行
def ssh_execution(ssh, command, logger):
    logger.info('コマンド実行中です')
    ssh.sendline(command)
    ssh.prompt()

if __name__ == '__main__':
    main()
