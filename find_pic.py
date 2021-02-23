import cv2

def compare(img1,img2):
    res = 0
    all_sum = 0
    width = img1.shape[0]
    height = img1.shape[1]
    rx=width/2
    ry=height/2
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            all_sum += int(img1[i,j])+int(img2[i,j])
            #print(pow(rx-i,2),"+",pow(ry-j,2) ,"?", pow(width/2,2))
            if pow(rx-i,2)+pow(ry-j,2) > pow(width/2,2):
                #print(i,",",j)
                continue
            res += abs(int(img1[i,j])-int(img2[i,j]))
            
    print(res,all_sum/2)
    return res/(all_sum/2)

# img1=cv2.imread("1.png")
# img2=cv2.imread("2.png")
# img1=cv2.resize(img1,(100,100),interpolation=cv2.INTER_CUBIC)
# img2=cv2.resize(img2,(100,100),interpolation=cv2.INTER_CUBIC)
# img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# img2=cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# print(compare(img1,img2))

def find_full(bg_img,expect_img):
    extend_point = set()
    for i in range(bg_img.shape[0]-expect_img.shape[0]):
        for j in range(bg_img.shape[1]-expect_img.shape[1]):
            if bg_img[i][j] > 0:
                for I in range(-expect_img.shape[0]+1,expect_img.shape[0]):
                    if i+I < 0 or i+I >= bg_img.shape[0]:
                        continue
                    for J in range(-expect_img.shape[1]+1,expect_img.shape[1]):
                        if j+J < 0 or j+J >= bg_img.shape[1]:
                            continue
                        extend_point.add([i,j])
    #print(extend_point)
    res = []
    pic_size = expect_img.shape[0] * expect_img.shape[1]
    for p in extend_point:
        similarity = 0
        zeronum = 0
        for i in range(expect_img.shape[0]):
            for j in range(expect_img.shape[1]):
                if bg_img[p[0]+i][p[1]+j] > 0 and expect_img[i][j]:
                    similarity += 1
                if bg_img[p[0]+i][p[1]+j] == 0:
                    zeronum += 1
                    if zeronum > pic_size/1.25:
                        i = expect_img.shape[0] + 1
                        zeronum = -1
                        break
        if zeronum != -1 and similarity/pic_size > 0.5: #0.5是我自己定的阈值，即相似度大于50%就选择
            res.append([p[0],p[1],similarity/pic_size])
    return res
                
    