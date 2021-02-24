

def find_full(bg_img, expect_img):
    import cv2
    EXPECT_RATIO = expect_img.shape[0]/expect_img.shape[1]

    kernel = np.ones(
        (expect_img.shape[0]//8+1, expect_img.shape[1]//8+1), np.uint8)

    bg = bg_img.copy()
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


if __name__ == '__main__':
    import numpy as np
    import picture
    import cv2
    src = cv2.imread("picture/test/2.png")
    p2 = cv2.imread("picture/full.png")
    p1 = picture.filterColor(src, np.array(
        [10, 200, 16]), np.array([40, 255, 255]))
    p2 = cv2.cvtColor(p2, cv2.COLOR_BGR2GRAY)
    res = find_full(p1, p2)
    for i in res:
        cv2.rectangle(src, (i[0], i[1]), (i[0]+i[2], i[1]+i[3]), (0, 0, 255))
        # cv2.circle(src, (i[1], i[0]), ()/2, (0, 0, 255))
    print(res)
    cv2.imshow("Picture", src)
    cv2.imshow("Processed picture", p1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
