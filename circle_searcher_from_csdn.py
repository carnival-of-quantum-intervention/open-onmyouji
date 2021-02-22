#加载环境包
import cv2
import numpy as np

def getScreenSize():
	import win32api,win32con
	width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得X轴屏幕分辨率
	height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得Y轴屏幕分辨率
	return width,height
def getHandle(titlename):
	import win32gui
	#获取句柄
	return win32gui.FindWindow(0, titlename)
# 确定圆大小
def getRadius(hwnd):
	import win32gui
	width,height=getScreenSize()
	#获取窗口左上角和右下角坐标
	left, top, right, bottom = win32gui.GetWindowRect(hwnd)
	# 结果
	Radius = 70 * (right - left) / width
	return Radius

def findCircles(img, r):
	#图片简单处理
	GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#灰度化
	GrayImage = cv2.equalizeHist(GrayImage)
	GrayImage= cv2.medianBlur(GrayImage,5)#中值模糊
 
	#阈值处理，输入图片默认为单通道灰度图片
	ret,th1 = cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)#固定阈值二值化
	#threshold为固定阈值二值化
	#第二参数为阈值
	#第三参数为当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值（一般情况下，都是256色，所以默认最大为255）
	#thresh_binary是基于直方图的二值化操作类型，配合threshold一起使用。此外还有cv2.THRESH_BINARY； cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；	cv2.THRESH_TOZERO_INV
	th2 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,  cv2.THRESH_BINARY,3,5)  
	#adaptiveThreshold自适应阈值二值化，自适应阈值二值化函数根据图片一小块区域的值来计算对应区域的阈值，从而得到也许更为合适的图片。
	#第二参数为当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值（一般情况下，都是256色，所以默认最大为255）
	#第三参数为阈值计算方法，类型有cv2.ADAPTIVE_THRESH_MEAN_C，cv2.ADAPTIVE_THRESH_GAUSSIAN_C
	#第四参数是基于直方图的二值化操作类型，配合threshold一起使用。此外还有cv2.THRESH_BINARY； cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；cv2.THRESH_TOZERO_INV
	#第五参数是图片中分块的大小
	#第六参数是阈值计算方法中的常数项
	th3 = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,3,5)
	#同上
	kernel = np.ones((5,5),np.uint8)#创建全一矩阵，数值类型设置为uint8 
	erosion = cv2.erode(th3,kernel,iterations=1)#腐蚀处理
	dilation = cv2.dilate(erosion,kernel,iterations=1)#膨胀处理
 
	imgray=cv2.Canny(dilation,30,100)#Canny边缘检测算子

	circles = cv2.HoughCircles(imgray,method=cv2.HOUGH_GRADIENT,dp=1,minDist=80,param1=100,param2=20,minRadius=r-5,maxRadius=r+5)#霍夫圆变换
	if circles == None:
		print("No circles found.")
		return [[]]
	#第3参数默认为1
	#第4参数表示圆心与圆心之间的距离（太大的话，会很多圆被认为是一个圆）
	#第5参数默认为100
	#第6参数根据圆大小设置(圆越小设置越小，检测的圆越多，但检测大圆会有噪点)
	#第7圆最小半径
	#第8圆最大半径
	circles = np.uint16(np.around(circles))
	#np.uint16数组转换为16位，0-65535
	#np.around返回四舍五入后的值
	return circles

# hwnd为窗口的编号，0号表示当前活跃窗口
def captureWindowsAs(hwnd, filename):
	import time
	import win32gui, win32ui, win32con, win32api
	# 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
	hwndDC = win32gui.GetWindowDC(hwnd)
	# 根据窗口的DC获取mfcDC
	mfcDC = win32ui.CreateDCFromHandle(hwndDC)
	# mfcDC创建可兼容的DC
	saveDC = mfcDC.CreateCompatibleDC()
	# 创建bigmap准备保存图片
	saveBitMap = win32ui.CreateBitmap()
	# 获取监控器信息
	MoniterDev = win32api.EnumDisplayMonitors(None, None)
	w = MoniterDev[0][2][2]
	h = MoniterDev[0][2][3]
	# print w,h　　　#图片大小
	# 为bitmap开辟空间
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
	# 高度saveDC，将截图保存到saveBitmap中
	saveDC.SelectObject(saveBitMap)
	# 截取从左上角（0，0）长宽为（w，h）的图片
	saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
	saveBitMap.SaveBitmapFile(saveDC, filename)

hwnd=getHandle("阴阳师-网易游戏")
captureWindowsAs(hwnd,"cache.png")
img=cv2.imread('cache.png')#读取图片
r=int(getRadius(hwnd))
P=findCircles(img, r)[0]#去掉circles数组一层外括号

count = 0
for i in P:
	if i[1]-i[2] < 0 or i[0]-i[2]<0 or i[1]+i[2] > (img.shape)[1] or i[0]+i[2] > (img.shape)[0]:
		continue
	cropImg = img[i[1]-i[2]:i[1]+i[2],i[0]-i[2]:i[0]+i[2]]
	cv2.imwrite(str(count)+".jpg",cropImg)
	count+=1
	for j in [imgray, img]:
		# 画出外圆
		cv2.circle(j,(i[0],i[1]),i[2],(255, 255, 255),2)#第二参数（）内是圆心坐标，第三参数是半径，第四参数（）内是颜色，第五参数是线条粗细
		# 画出圆心
		# cv2.circle(j,(i[0],i[1]),2,(0,0,0),3)
print("圆的个数是：")
print(len(P))
for i in P:
	r=int(i[2])
	x=int(i[0])
	y=int(i[1])
	print("圆心坐标为：",(x,y))
	print("圆的半径是：",r)
   
#cv2.imshow('Step 1',th3)#第一参数为窗口名称
#cv2.imshow('Step 2',erosion)#第一参数为窗口名称
#cv2.imshow('Step 3',imgray)#第一参数为窗口名称
cv2.imshow('Detected circles',img)#第一参数为窗口名称
 
cv2.waitKey(0)#无穷大等待时间
cv2.destroyAllWindows()