import os, shutil, sys, time, datetime, tkinter
import tkinter.filedialog, tkinter.messagebox

startTime = datetime.datetime.now()

suffixs = ['.pdf','.dwg','.step','.stp']

#获取当前文件所在地址
currentPath = os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\','/')

#获取当前文件所在项目名
projectName = currentPath.split('/')[-1]

projectNameFather = currentPath.split('/')[-2]

#拼接该项目的工程图打包目录文件路径
drawingList = currentPath +'/' + projectName + projectNameFather + '件工程图打包目录.txt'
#判断该项目的工程图打包目录文件是否存在，不存在则新建一个
if(not os.path.exists(drawingList)):
	open(drawingList,'w')
	print('请在文件：' + projectName + projectNameFather + '件工程图打包目录.txt')
	print('中输入该项目需要从图纸库中提取的图纸名称，一行一个')
	print('后期更新图纸到图纸库以后，需将此目录文件进行修改更新')
else:
	#隐藏主对话框
	tkinter.Tk().withdraw()
	#判断用户是否确定了提示内容，决定选择文件夹，确定则继续操作，取消则退出
	if(tkinter.messagebox.askokcancel("提示",'请选择文件的存放位置')):
		#弹出选择文件夹对话框，获取用户选择的路径
		saveDir=tkinter.filedialog.askdirectory(title=u'选择',initialdir=(os.path.expanduser((currentPath))))
		
		#拼接该项目的工程图文件夹路径
		date = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
		drawingFolder=saveDir + '/' + projectName + projectNameFather + '件工程图纸包_' + date + '/'

		#判断工程图文件夹是否存在，存在则删除它
		# if(os.path.exists(drawingFolder)):
		# 	shutil.rmtree(drawingFolder,True)

		#新建工程图文件夹
		os.makedirs(drawingFolder)

		#打开目录文件
		file = open(drawingList)

		with open(drawingList) as file:
			#初始化复制的组数目
			groups = 0
			#初始化目标文件数目
			targetNum = 0
			#从目录文件获取每一行的目标文件名
			for targetName in file:
				targetNum += 1
				#初始化每组目标文件的复制次数
				num = 0
				#从后缀数组中获得每个要进行复制的后缀名
				for suffix in suffixs:
					#按照目录，拼接要复制的目标文件路径
					target = currentPath + '/../../' + projectNameFather + '/工程图纸库/' + targetName.rstrip() + suffix
					#print(target)
					#判断目标文件是否存在
					if(os.path.exists(target)):
						#打印复制提示
						if(num == 0):
							#按照目标文件名称长度，计算要补充的空格长度
							nameLen = len(targetName.rstrip()) 
							nameLen_utf8 = len(targetName.rstrip().encode('utf-8')) 
							size = int((nameLen_utf8 - nameLen)/2 + nameLen)
							spaceLen = ' '*(46-size)
							#打印复制了哪个目标文件
							print('√ ' + targetName.rstrip() + spaceLen + suffix, end='\t')
						else:
							print(suffix, end='\t')

						#复制目标文件到工程图文件夹
						shutil.copy(target,drawingFolder)
						#复制次数加1
						num += 1
				#如果目标文件没有找到，则打印提示
				if(num == 0):
					print('× ' + targetName.rstrip(),end='')
				#如果目标文件复制过，则复制的组数目加1
				else:
					groups += 1
				#完成一组文件的复制后进行换行
				print('')

		endTime = datetime.datetime.now()
		spendTime = str((endTime - startTime).seconds)

		#最后打印提示复制了总共多少组目标文件
		print('-----------------------------------------------------------------')
		print('共复制文件：'+ str(groups) + '组 ' + '未找到：' + str(targetNum-groups) + '组 耗时：'+ spendTime + '秒')
		file.close()
		print('-----------------------------------------------------------------')
		input('按回车键关闭窗口')

