import cv2

img = cv2.imread("./images/2.jpg")
# print(img.shape)


cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow("img", img)
key = cv2.waitKey(0)
cv2.destroyAllWindows()

