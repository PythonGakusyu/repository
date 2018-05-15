#!usr/bin/env python3
from pyVmomi import vim
from kadai6 import vm_module
import re

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
	for vm in vm_list.view:
		name = vm.name
		pattern = re.search('^centos-\d+-g1$', name)
		if pattern:
			logger.info(vm.name)

if __name__ == '__main__':
	main()
