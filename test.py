

if 0:
    import cv2
    import numpy as np
    from window import *
    from picture import *
    HWND = getHandle("阴阳师-网易游戏")
    # 读取图片
    captured = captureWindowAs(HWND, "cache/cache.png")

    src = captured
    cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("input", src)
    """
    提取图中的黄色部分
    """
    cv2.imshow(filterColor("test",
                           np.array([3, 220, 220]), np.array([50, 255, 255])))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if 0:
    import numpy as np
    import picture
    import cv2
    p1 = cv2.imread("picture/test/2.png")
    p2 = cv2.imread("picture/full.png")
    p2 = cv2.cvtColor(p2, cv2.COLOR_BGR2GRAY)
    res = picture.findColor(p1, p2, [10, 200, 16], [40, 255, 255])
    for i in res:
        cv2.rectangle(src, (i[0], i[1]), (i[0]+i[2], i[1]+i[3]), (0, 0, 255))
        # cv2.circle(src, (i[1], i[0]), ()/2, (0, 0, 255))
    print(res)
    cv2.imshow("Picture", src)
    cv2.imshow("Processed picture", p1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if 1:
    import cv2
    import numpy as np
    window_name = "filter2D Demo"

    # Load an image
    src = cv2.imread("picture/test/2.png")

    # Create window
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

   # Initialize arguments for the filter
    anchor = (-1, -1)
    delta = 0
    ddepth = -1

    # Loop - Will filter the image with different kernel sizes each 0.5 seconds
    ind = 0
    while True:

        c = cv2.waitKey(500)
        # Press 'ESC' to exit the program
        if c == 27:
            break

        # Update kernel size for a normalized box filter
        kernel_size = 3 + 2*(ind % 5)
        kernel = np.ones((kernel_size, kernel_size), np.float) / \
            (kernel_size*kernel_size)
        kernel = cv2.imread("picture/full.png")

        # Apply filter
        dst = cv2.filter2D(src, ddepth, kernel, anchor=anchor,
                           delta=delta, borderType=cv2.BORDER_DEFAULT)
        cv2.imshow(window_name, dst)
        ind += 1
