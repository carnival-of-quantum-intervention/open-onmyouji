

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
    color = 128

    rects = []
    # 开始遍历
    if contours != None:
        for contour in contours:
            # 得到这个连通区域的外接矩形
            x, y, w, h = cv2.boundingRect(contour)

            # 如果高度不足，或者长宽比太小，认为是无效数据，否则把矩形画到原图上
            if EXPECT_RATIO - 0.1 < w / h < EXPECT_RATIO + 0.1:
                cv2.rectangle(bg, (x, y), (x+w, y+h), color)
                rects.append((x, y, w, h))
    cv2.imshow("test", bg)
    return rects

    extend_point0 = set()
    extend_point = []
    count = 0
    for i in range(expect_img.shape[0]):
        for j in range(expect_img.shape[1]):
            if expect_img[i][j] != 0:
                count += 1
    for i in range(bg_img.shape[0]-expect_img.shape[0]):
        if i < 0.15 * bg_img.shape[0] or i > 0.7 * bg_img.shape[0]:
            continue
        for j in range(bg_img.shape[1]-expect_img.shape[1]):
            if j < 0.15 * bg_img.shape[1] or j > 0.85 * bg_img.shape[1]:
                continue
            if bg_img[i][j] > 0:
                for I in range(-expect_img.shape[0]+1, expect_img.shape[0]):
                    if i+I < 0 or i+I >= bg_img.shape[0]:
                        continue
                    for J in range(-expect_img.shape[1]+1, expect_img.shape[1]):
                        if j+J < 0 or j+J >= bg_img.shape[1]:
                            continue
                        extend_point0.add((i+I)*bg_img.shape[1]+j+J)
    res = []
    pic_size = expect_img.shape[0] * expect_img.shape[1]
    for p in extend_point0:
        extend_point.append([int(p/bg_img.shape[1]), p % bg_img.shape[1]])
    for p in extend_point:
        similarity = 0
        zeronum = 0
        for i in range(expect_img.shape[0]):
            for j in range(expect_img.shape[1]):
                if bg_img[p[0]+i][p[1]+j] > 0 and expect_img[i][j] > 0:
                    similarity += 1
                if bg_img[p[0]+i][p[1]+j] == 0:
                    zeronum += 1
                    if zeronum > pic_size-count:
                        i = expect_img.shape[0] + 1
                        zeronum = -1
                        break
        if zeronum != -1 and similarity/count > 0.5:  # 0.5是我自己定的阈值，即相似度大于50%就选择
            res.append([p[0], p[1], similarity/count])
    return res


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
