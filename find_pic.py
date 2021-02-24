import cv2


def find_full(bg_img, expect_img):
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
    p1 = cv2.imread("test.png")
    p2 = cv2.imread("picture/full.png")
    p1 = cv2.cvtColor(p1, cv2.COLOR_BGR2GRAY)
    p2 = cv2.cvtColor(p2, cv2.COLOR_BGR2GRAY)
    res = find_full(p1, p2)
    print(res)
