import cv2
import os
import numpy as np
import sys
import matplotlib.pyplot as plt



def main():
    # first  step : find the hsv color green  and lower and upper green

    img= cv2.imread(sys.argv[1]+ "/studio1.jpg")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    green = np.uint8([[[0, 255, 0]]])
    hsv_green = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)

    #print(hsv_green)
    # [[[ 60 255 255]]]

    lowerb = np.array([50,100,100])
    upperb = np.array([100,255,255])
    dst = cv2.inRange(hsv, lowerb, upperb)
    newdst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)

    #here i created a help folder with pictures i need to use for the output (the mask..)
    os.mkdir("images")
    cv2.imwrite("images/mask.jpg", newdst)


    # second step :

    #1. Create a background image


    bg = cv2.imread(sys.argv[1]+"/background1.jpg")
    front = cv2.imread("images/mask.jpg")

    h, w = front.shape[0], front.shape[1]
    bg = cv2.resize(bg, (w, h))

    img_back = cv2.bitwise_and(front, bg)
    cv2.imwrite(sys.argv[2]+"/ImageBack.jpg",img_back)

    # 2. put off the color green of the orginial picture
    # je fais l inverse de mon mask pour pouvoir mettre du moir a la place du fond vert

    img_front0 = cv2.bitwise_not(front, front)
    cv2.imwrite("images/Front0.jpg", img_front0)
    img_front1 = cv2.imread("images/Front0.jpg")

    #je resize mon mask inverse pour quil soit a la meme taille que mon  img

    h, w = img.shape[0], img.shape[1]
    img_front1 = cv2.resize( img_front1, (w, h))
    img_frontf= cv2.bitwise_and( img_front1, img)
    cv2.imwrite("images/WithoutG.jpg", img_frontf)


    # 3. Combine the pictures  i  received in  (1) and (2)
    # je fais or entre limage sans le vert et limage  noir avec mon fond

    h, w = img_back.shape[0], img_back.shape[1]
    img_frontf = cv2.resize( img_frontf, (w, h))

    imgfinal = cv2.bitwise_or( img_frontf, img_back)
    imgfinal = cv2.cvtColor(imgfinal, cv2.COLOR_BGR2RGB)

    cv2.imwrite(sys.argv[3]+"/Output.jpg", imgfinal)

    #plt.imshow( imgfinal)
    #plt.show()


if __name__ == "__main__":
    main()
