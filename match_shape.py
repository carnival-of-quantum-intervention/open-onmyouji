#灰度图像，img1是原图，img2是待匹配的模板，返回值为外切矩形的[[左上点，右下点]]
def matchshape(img1, img2):
    import cv2
    import numpy as np
    h,w = img2.shape[:2]
    res = cv2.matchTemplate(img1,img2,cv2.TM_CCOEFF_NORMED)
    theshold = 0.5#阈值，到时候试试能不能用机器学习来定
    loc = np.where(res >= theshold)
    res=[]
    for pt in zip(*loc[::-1]):
        bottom_right = (pt[0]+w,pt[1]+h)
        cv2.rectangle(img1,pt,bottom_right,255,1)
        res.append([pt[0],bottom_right])
    cv2.imshow("res",img1)
    return res