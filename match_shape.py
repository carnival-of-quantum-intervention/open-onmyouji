import cv2


# 灰度图像，img1是原图，img2是待匹配的模板，返回值为外切矩形的[[左上点，右下点]]
def matchshape(img1, img2):
    h, w = img2.shape[:2]
    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)  # 返回值为二维矩阵，表示img1中每个点的匹配度
    return NMS_result(res, h, w)


def NMS_result(res, h, w, threshold=0.3):
    result = []
    for i in range(len(res) - 2):
        for j in range(len(res[0]) - 2):
            if res[i][j] > res[i - 1][j - 1] and res[i][j] > res[i - 1][j] and res[i][j] > res[i - 1][j + 1] and res[i][
                j] > res[i][j - 1] and res[i][j] > res[i][j + 1] and res[i][j] > res[i + 1][j - 1] and res[i][j] > \
                    res[i + 1][j] and res[i][j] > res[i + 1][j + 1] and res[i][j] > threshold:
                result.append([(j, i), (j + h, i + w)])
    return result


if __name__ == '__main__':
    img1 = cv2.imread('./picture/instance_zone.png')
    img2 = cv2.imread('./picture/explore.png')
    res = matchshape(img1, img2)
    for r in res:
        cv2.rectangle(img1, r[0], r[1], 255, 1)
    cv2.imshow("res", img1)
    cv2.waitKey()
