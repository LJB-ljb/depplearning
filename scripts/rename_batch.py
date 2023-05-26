'''the input dir is img, the output dir is images'''
import os
import os.path as osp

imgdir = './img'
imgoutputdir = './images'
imgpths = os.listdir(imgdir)
imgs = [img.split('.') for img in imgpths]

for i in range(0, len(imgpths)):
    
    os.renames(osp.join(imgdir, imgpths[i]), osp.join(imgoutputdir, "{}.{}".format(i,imgs[i][-1])))

# os.rename(osp.join(imgdir,"1.jpg"), osp.join(imgdir,"6.jpg"))