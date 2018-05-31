#!/usr/bin/env python3
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import argparse
import ssl
import atexit
import time
import logging


class vm_module:

    # loggerフォーマットメソッド
    @staticmethod
    def logger_format():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    # parserメソッド
    @staticmethod
    def set_args():
        parser = argparse.ArgumentParser(
            prog='kadai3.py',
            usage='～.py IPアドレス, username, password',
            description='Please sign in',
            epilog='end',
            add_help=True)
        parser.add_argument('-hn', '--host', help='hostのIPを入力してください', required=True)
        parser.add_argument('-u', '--username', help='usernameを入力してください', required=True)
        parser.add_argument('-p', '--password', help='passwordを入力してください', required=True)
        return parser.parse_args()
    
    def set_args_paramiko():
        parser = argparse.ArgumentParser(
            prog='kadai3.py',
            usage='～.py IPアドレス, username, password',
            description='Please sign in',
            epilog='end',
            add_help=True)
        parser.add_argument('-hn', '--host', help='hostのIPを入力してください', required=True)
        parser.add_argument('-u', '--username', help='usernameを入力してください', required=True)
        parser.add_argument('-p', '--password', help='passwordを入力してください', required=True)
        parser.add_argument('-su', '--ssh_username', help='ssh接続のusernameを入力してください', required=True)
        parser.add_argument('-sp', '--ssh_password', help='ssh接続のpasswordを入力してください', required=True)
        return parser.parse_args()

        # コンストラクタ
#   def __init__(self, host, username, password):
#       self.host = host
#       self.username = username
#       self.password = password

    # 接続メソッド
#   def si_connect(self):
#       host = self.host
#       username = self.username
#       password = self.password

#       context = None
#       if hasattr(ssl, '_create_unverified_context'):
#           context = ssl._create_unverified_context()

#       si = SmartConnect(host=host,
#                         user=username,
#                         pwd=password,
#                         sslContext=context)
#
#       atexit.register(Disconnect, si)
#       return si


    # 接続メソッド
    @staticmethod
    def si_connect(host, username, password):
        context = None
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()

        si = SmartConnect(host=host,
                          user=username,
                          pwd=password,
                          sslContext=context)

        atexit.register(Disconnect, si)
        return si

    # オブジェクト取得メソッド
    def search_object(si, objecttype, objectname):
        obj_list = si.content.viewManager.CreateContainerView(si.content.rootFolder,
                                                              [objecttype],
                                                              True)
        for search_result in obj_list.view:
            if search_result.name == objectname:
                return search_result
            else:
                return '存在しないオブジェクト名です'

    # タスク監視メソッド
    def task_monitor(task):
        while task.info.state == 'running':
            time.sleep(2)
            print('処理中です...')
        if task.info.state == 'success':
            return True
        else:
            return False
