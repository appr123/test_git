import numpy as np
import cv2


def rgb_to_grayscale(image):
    # 获取图像的宽度和高度
    height, width, _ = image.shape

    # 创建一个与原图像相同尺寸的灰度图像矩阵
    grayscale_image = np.zeros((height, width), dtype=np.uint8)

    # 遍历图像的每个像素点，计算灰度值
    for i in range(height):
        for j in range(width):
            # 获取RGB值
            r, g, b = image[i, j]

            # 计算灰度值
            gray_value = 0.299 * r + 0.587 * g + 0.114 * b

            # 将灰度值写入灰度图像矩阵
            grayscale_image[i, j] = int(gray_value)

    return grayscale_image


# 读取彩色图像
color_image = cv2.imread('asd1.jpg')

# 转换为灰度图像
gray_image = rgb_to_grayscale(color_image)
cv2.imwrite('asd_gray.jpg', gray_image)
# 显示灰度图像
cv2.imshow('Grayscale Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()