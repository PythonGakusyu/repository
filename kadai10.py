#!/user/bin/env python3
#coding: UTF-8
from pyVmomi import vim
from kadai6 import vm_module
import csv

def main():
	# loggerフォーマットメソッド
	logger = vm_module.logger_format()
	# parserメソッド
	args = vm_module.set_args()
	# インスタンス作成
	si_info = vm_module(args.host, args.username, args.password)
	# 接続メソッド
	si = si_info.si_connect()

	vm_list = si.content.viewManager.CreateContainerView(si.content.rootFolder,
														 [vim.VirtualMachine],
														 True)
	# csvファイル出力のヘッダーリストと空のセット
	header = [('VM名', '搭載ESXi名')]
	rows = set()
	
	# csvファイルへの出力
	csv_file = open('./python.csv', 'w', newline = '')
	writer = csv.writer(csv_file)
	writer.writerows(header)
	for vm in vm_list.view:
		for device in vm.config.hardware.device:
			# デバイスの判定
			class_name = vim.vm.device.VirtualVmxnet3
			if isinstance(device, class_name) and device.connectable.connected == False:
				rows.add((vm.name, vm.runtime.host.name))
	# 書き込み
	writer.writerows(rows)

if __name__ == '__main__':
	main()
