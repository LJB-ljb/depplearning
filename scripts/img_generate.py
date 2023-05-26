from PIL import ImageEnhance,ImageOps
import os
import cv2
import numpy as np
from PIL import Image

def labelgenerate(method, name):

    labelImg_old = "./Annotations_labelImg/{}.txt".format(name)
    labelImg_new = "./Annotations_labelImg/{}{}.txt".format(method, name)
    os.system("cp  {} {}".format(labelImg_old, labelImg_new))
    labelme_old = "./Annotations_labelme/{}.json".format(name)
    labelme_new = "./Annotations_labelme/{}{}.json".format(method, name)
    os.system("cp  {} {}".format(labelme_old, labelme_new))

def brightnessEnhancement(imageDir,imgpth, name):#亮度增强
    image = Image.open(os.path.join(imageDir,imgpth))
    image = ImageOps.exif_transpose(image)
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 1.1+0.4*np.random.random()#取值范围1.1-1.5
    # brightness = 1.5
    image_brightened = enh_bri.enhance(brightness)
    saveName = "brightnessE" + name + ".jpg"
    image_brightened.save(os.path.join(imageDir, saveName))

    labelgenerate("brightnessE", name)
    


def contrastEnhancement(imageDir,imgpth, name):  # 对比度增强
    image = Image.open(os.path.join(imageDir,imgpth))
    image = ImageOps.exif_transpose(image)
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.1+0.4*np.random.random()#取值范围1.1-1.5
    # contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    
    saveName="cesun"+name+".jpg"
    image_contrasted.save(os.path.join(imageDir,saveName))
    labelgenerate("cesun", name)

def rotation(imageDir,imgpth, name):
    img = Image.open(os.path.join(imageDir,imgpth))
    img = ImageOps.exif_transpose(img)
    random_angle = np.random.randint(-2, 2)*90
    if random_angle==0:
     rotation_img = img.rotate(-90) #旋转角度
    else:
        rotation_img = img.rotate( random_angle)  # 旋转角度
    saveName = "rotate" + name + ".jpg"
    rotation_img.save(os.path.join(imageDir, saveName))


def flip(imageDir,imgpth, name):   #翻转图像
    img = Image.open(os.path.join(imageDir,imgpth))
    img = ImageOps.exif_transpose(img)
    filp_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    saveName = "flip" +name + ".jpg"
    filp_img.save(os.path.join(imageDir, saveName))


def gaussian_noise(imageDir,imgpth, name, mean = 0, sigma = 0.1):  #给图片加一些噪声，高斯噪声
    image = cv2.imread(os.path.join(imageDir,imgpth))
    #设置高斯分布的均值和方差
    
    image = np.array(image / 255, dtype=float)
    noise = np.random.normal(mean, sigma, image.shape)
    noisy_img = image + noise
    if noisy_img.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    noisy_img = np.clip(noisy_img, low_clip, 1.0)
    noisy_img = np.uint8(noisy_img * 255)

    saveName = "gaussian_noise" +name + ".jpg"
    cv2.imwrite(os.path.join(imageDir, saveName), noisy_img)
    labelgenerate("gaussian_noise", name)

def gaussian_blur(imageDir,imgpth, name):
    image = cv2.imread(os.path.join(imageDir,imgpth))
    dst = cv2.GaussianBlur(image, (0, 0), 3)
    saveName = "gaussian_blur" +name + ".jpg"
    cv2.imwrite(os.path.join(imageDir, saveName), dst)
    labelgenerate("gaussian_blur", name)

def generate(imgdir, probabilitys=[0.8, 0.8, 0.8, 0.8, 0.5, 0.6]):
   
   imgpths = os.listdir(imgdir)
   
   for imgpth in imgpths:       
        name = imgpth.split('.')[0]
        probs = [np.random.random() for i in range(0, len(probabilitys))]
        excs = [probs[i]<=probabilitys[i] for i in range(0,len(probabilitys))]
        if excs[0]: brightnessEnhancement(imgdir, imgpth, name) 
        if excs[1]: contrastEnhancement(imgdir,imgpth, name)
        if excs[2]: rotation(imgdir, imgpth, name)
        if excs[3]: flip(imgdir,imgpth, name)
        if excs[4]: gaussian_noise(imgdir,imgpth, name, mean = 0, sigma = 0.1)
        if excs[5]: gaussian_blur(imgdir,imgpth, name)
        

def main():
    imgdir = './images'
    probabilitys=[0.9, 0.9, 0.4, 0.5, 0.7, 0.7]
    generate(imgdir, probabilitys)


if __name__ == "__main__":
    main()