import cv2
import numpy as np


def findCircles(img, r):
    # 图片简单处理
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
    GrayImage = cv2.equalizeHist(GrayImage)
    GrayImage = cv2.medianBlur(GrayImage, 5)  # 中值模糊

    # 阈值处理，输入图片默认为单通道灰度图片
    ret, th1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)  # 固定阈值二值化
    # threshold为固定阈值二值化
    # 第二参数为阈值
    # 第三参数为当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值（一般情况下，都是256色，所以默认最大为255）
    # thresh_binary是基于直方图的二值化操作类型，配合threshold一起使用。此外还有cv2.THRESH_BINARY； cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；	cv2.THRESH_TOZERO_INV
    th2 = cv2.adaptiveThreshold(
        GrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C,  cv2.THRESH_BINARY, 3, 5)
    # adaptiveThreshold自适应阈值二值化，自适应阈值二值化函数根据图片一小块区域的值来计算对应区域的阈值，从而得到也许更为合适的图片。
    # 第二参数为当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值（一般情况下，都是256色，所以默认最大为255）
    # 第三参数为阈值计算方法，类型有cv2.ADAPTIVE_THRESH_MEAN_C，cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    # 第四参数是基于直方图的二值化操作类型，配合threshold一起使用。此外还有cv2.THRESH_BINARY； cv2.THRESH_BINARY_INV； cv2.THRESH_TRUNC； cv2.THRESH_TOZERO；cv2.THRESH_TOZERO_INV
    # 第五参数是图片中分块的大小
    # 第六参数是阈值计算方法中的常数项
    th3 = cv2.adaptiveThreshold(
        GrayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 5)
    # 同上
    kernel = np.ones((5, 5), np.uint8)  # 创建全一矩阵，数值类型设置为uint8
    erosion = cv2.erode(th3, kernel, iterations=1)  # 腐蚀处理
    dilation = cv2.dilate(erosion, kernel, iterations=1)  # 膨胀处理

    imgray = cv2.Canny(dilation, 30, 100)  # Canny边缘检测算子

    circles = cv2.HoughCircles(imgray, method=cv2.HOUGH_GRADIENT, dp=1,
                               minDist=80, param1=100, param2=20, minRadius=r-5, maxRadius=r+5)  # 霍夫圆变换
    if circles is None:
        return []
    # 第3参数默认为1
    # 第4参数表示圆心与圆心之间的距离（太大的话，会很多圆被认为是一个圆）
    # 第5参数默认为100
    # 第6参数根据圆大小设置(圆越小设置越小，检测的圆越多，但检测大圆会有噪点)
    # 第7圆最小半径
    # 第8圆最大半径

    circles = np.uint16(np.around(circles))
    # np.uint16数组转换为16位，0-65535
    # np.around返回四舍五入后的值
    return circles[0]


def findColor(src_img, expect_img, min_hsv, max_hsv):
    import cv2
    EXPECT_RATIO = expect_img.shape[0]/expect_img.shape[1]

    kernel = np.ones(
        (expect_img.shape[0]//8+1, expect_img.shape[1]//8+1), np.uint8)

    bg = filterColor(src_img, min_hsv, max_hsv)
    bg = cv2.dilate(bg, kernel, iterations=1)
    # cv2.bitwise_not(bg, bg)  # 颜色反转
    bg = cv2.erode(bg, kernel, iterations=1)
    # cv2.bitwise_not(bg, bg)  # 颜色反转

    # 检测连通域，每一个连通域以一系列的点表示，FindContours方法只能得到第一个域
    contours, hierarchy = cv2.findContours(
        bg, method=cv2.CHAIN_APPROX_SIMPLE, mode=cv2.RETR_EXTERNAL)

    # 开始遍历
    if contours != None:
        return [cv2.boundingRect(contour) for contour in contours]
    else:
        return []


def compareCircle(img1, img2):
    res = 0
    all_sum = 0
    width = img1.shape[0]
    height = img1.shape[1]
    rx = width/2
    ry = height/2
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            all_sum += int(img1[i, j])+int(img2[i, j])
            #print(pow(rx-i,2),"+",pow(ry-j,2) ,"?", pow(width/2,2))
            if pow(rx-i, 2)+pow(ry-j, 2) > pow(width/2, 2):
                # print(i,",",j)
                continue
            res += abs(int(img1[i, j])-int(img2[i, j]))
    return res/(all_sum/2)


def findSimilarestPictureWith(subImageParams, images, expectImage, compareFunc):
    import os.path
    import os
    count = 0

    potentialPoints = []

    for i in subImageParams:
        if i[1]-i[2] < 0 or i[0]-i[2] < 0 or i[1]+i[2] > (images.shape)[1] or i[0]+i[2] > (images.shape)[0]:
            continue
        cropImage = images[i[1]-i[2]:i[1]+i[2], i[0]-i[2]:i[0]+i[2]]
        cv2.imwrite("cache/"+str(count)+".jpg", cropImage)
        cropImage = cv2.resize(cropImage, (100, 100),
                               interpolation=cv2.INTER_CUBIC)
        cropImage = cv2.cvtColor(cropImage, cv2.COLOR_BGR2GRAY)
        ret = compareFunc(cropImage, expectImage)
        if ret <= 0.35:
            potentialPoints.append([i[0], i[1], ret])
        count += 1
    # 移除多余的文件
    while os.path.exists("cache/"+str(count)+".jpg"):
        os.remove("cache/"+str(count)+".jpg")
        count += 1
    count = None

    # potentialPoints.sort(key=operator.itemgetter(2), reverse=True)
    potentialPoints.sort(key=lambda _tuple: _tuple[2])
    # print(potentialPoints)
    if len(potentialPoints) == 0:
        return 0, 0
    else:
        ChosenPoint = potentialPoints[0]
        return ChosenPoint[0], ChosenPoint[1]


def filterColor(src, low_hsv, high_hsv):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    return mask  # cv2.bitwise_and(mask, src)


def processImage(image):
    image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image
