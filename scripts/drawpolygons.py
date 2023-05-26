import cv2
import os
import os.path as osp

def drawpolygons(imgname):
    name = imgname.split('.')[0]
    imgpth = './images'
    targetpth = './targets'
    classespth = './predefined_class.txt'

    with open(osp.join(targetpth, name)+'.txt') as f:
        datas = f.readline().split(' ')

    with open(classespth) as c:
        # classes = [cls.split('\n')[0] for cls in c.readlines()]
        classes = c.read().split('\n')

    assert datas[0]==imgname , 'open the wrong file!'
    img = cv2.imread(osp.join(imgpth, imgname))
    for data in datas[1:]:
        data = data.split(',')
        pt1 = tuple([int(data[0]), int(data[1])])
        pt2 = tuple([int(data[2]), int(data[3])])
        cv2.rectangle(img, pt1, pt2, color=(27,79,222), thickness=2)

        t_size = cv2.getTextSize(classes[int(data[4])], cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        cv2.putText(img, classes[int(data[4])], (pt1[0], pt1[1]+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 1,
                                    (27,79,222), 1)
        for j in range(5, len(data), 2):
            p1 = tuple([int(data[j]), int(data[j+1])])
            
            if (j+2 >= len(data)):
                p2 = tuple([int(data[5]), int(data[6])])
            else:
                p2 = tuple([int(data[j+2]), int(data[j+3])])
            cv2.line(img, p1, p2, color=(36,197,79), thickness=1)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()


