import os
import os.path as osp
import cv2
import json
import argparse

def arg_parse():
    """Parse arguements"""

    parser = argparse.ArgumentParser(description='translate labels to yolo-poly formation')
    parser.add_argument("--txtpath", dest='txtpath', help="path to labelImg labels", 
                                                    default="./Annotations_labelImg", type=str)
    parser.add_argument("--jsonpath", dest='jsonpath', help="path to labelme labels", 
                                                    default="./Annotations_labelme", type=str)
    parser.add_argument("--targetpath", dest='targetpath', help="path to target path", 
                                                    default="./targets", type=str)
    parser.add_argument("--imgpath", dest="imagepath", help="path to image path", 
                                                    default="./images", type=str)
    parser.add_argument("--classpath", dest="classpath", help="classes of detect", 
                                                    default="./predefined_class.txt", type=str)
    parser.add_argument("--devidepercent", dest="devidepercent", help="percentage of train validation test dataset", 
                                                    default=[0.7, 0.2, 0.1], type=list)
    parser.add_argument("--outputpath", dest='outputpath', help="path to output path", 
                                                    default="./data4use", type=str)


    return parser.parse_args()


def load_classnames(class_path):
    '''load predefined class names from disk'''
    with open(class_path) as f:
        class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
    return class_names

def load_labelImg(labelImg_path):
    '''
        load labelImg labels
        labels_data looks like this:
        {'3': [['2', '0.426563', '0.619792', '0.571875', '0.547917']], 
        ' 2': [['1', '0.546094', '0.588542', '0.342187', '0.235417'], ['1', '0.688281', '0.840625', '0.298438', '0.318750']]}
        it is the "key-value" shape, key is the name of file, value is the data of labels, the first element of 
        value represents class, others are coordinates of center of box and width and height of box, they are all in 
        normalization form   
    '''
    label_paths = [osp.join(labelImg_path, label_path) for label_path in os.listdir(labelImg_path)]
    labels_data = {}

    for i in range(0, len(label_paths)):
        filename = osp.basename(label_paths[i]).split('.')[0]
        with open(label_paths[i]) as f:
            data = f.readlines()
        # labels_data.extend(data[i].split() for i in range(0, len(data)))
            data = [data[i].split() for i in range(0, len(data))]
        label_data ={filename:data}
        labels_data.update(label_data)
    
    return labels_data

def load_labelme(labelme_path):
    '''
    load labelme polygons
    polygons_data looks like this:
    {'2': [ [640,480], ['car', [358.66995073891627, 382.11822660098517], [404.9753694581281, 360.935960591133], 
    [403.0049261083744, 352.06896551724134], [408.42364532019707, 344.679802955665]]}
    it is the "key-value" shape, key is the name of file, value is the data of  polygons, the first element of
    value represents width and height of image, others are classes and coordinates of  polygon's apexs

    '''
    polygon_paths = [osp.join(labelme_path, polygon_path) for polygon_path in os.listdir(labelme_path)]
    polygons_data = {}

    for i in range(0, len(polygon_paths)):
        filename = osp.basename(polygon_paths[i]).split('.')[0]
        with open(polygon_paths[i]) as f:
            data = json.load(f)
        # polygons_data.extend(data["shapes"][i]["points"] for i in range(0,len(data["shapes"])))
        polygon = []
        polygon.append([data["imageWidth"],data["imageHeight"]])
        for j in range(0, len(data["shapes"])):

            datas = [ data["shapes"][j]["label"]]
            # datas.extend([data["imageWidth"], data["imageHeight"]])
            datas.extend(data["shapes"][j]["points"] )  
            polygon.append(datas)
        polygon_data ={filename:polygon}
        polygons_data.update(polygon_data)
    
    return polygons_data

def caculate(label_data, polygon_data):
    '''caculate the coordinates of boxes and corrdinates of polygons'''
    img_width = int(polygon_data[0][0])
    img_height = int(polygon_data[0][1])

    dots = []
    polygons = []
    labels = []
    for i in range(0, len(label_data)):
        label = label_data[i][0]
        labels.append(label) 

        center = label_data[i][1:3]
        center = [float(c) for c in center]
        width =float(label_data[i][3])
        height = float(label_data[i][4])
        dot = [(center[0] - width/2)*img_width , (center[1] - height/2)*img_height ,
                        (center[0] + width/2)*img_width , (center[1] + height/2)*img_height]
        dot = [round(d) for d in dot]
        dots.append(dot)
        
        polygon_apexs = polygon_data[i+1]
        polygon = []
        for j in range(1, len(polygon_apexs)):
            polygon_apex_x = round(int(polygon_apexs[j][0]))
            polygon_apex_y = round(int(polygon_apexs[j][1]))
            polygon.extend([polygon_apex_x,polygon_apex_y])
        polygons.append(polygon)

    return dots , polygons , labels

def write(labels_data, polygons_data,  imagepath, outputpath):
    '''write labelImg and labelme information to target files'''
    images = os.listdir(imagepath)
    names = []
    outputs = []
    for i in range(0, len(images)):
        
        names.append(images[i].split('.')[0])
        outputs.append(osp.join(outputpath, names[i])+'.txt')
        if  (names[i] in labels_data) & (names[i] in polygons_data)  :
            with open(outputs[i], 'w') as f:
                f.writelines(images[i]+' ')
                dots, polygons, labels = caculate(label_data=labels_data[names[i]], polygon_data=polygons_data[names[i]])
                for j in range(len(labels)):
                    [f.writelines(str(dot) + ',') for dot in dots[j]]
                    f.writelines(labels[j] + ',')
                    [f.writelines(str(polygons[j][k])+',') for k in range(0, len(polygons[j])-1)]
                    f.writelines(str(polygons[j][-1]))
                    if (j==len(labels)-1):
                        continue
                    else:
                        f.writelines(' ')
                     
                # f.writelines()
        else:
            print("Image {}  do not have labelImg or labelme files, please check!".format(names[i]))
            continue

def devide(targetpath, outputpath, devidepercent):
    '''devide all targets into train validation test parts according to devide percentage'''
    targets = [osp.join(targetpath , target) for target in os.listdir(targetpath)]
    number_of_targets = len(targets)
    # targets2devide = number_of_targets
    train_number = int(devidepercent[0]*number_of_targets)
    val_number = int(devidepercent[1]*number_of_targets)
    test_number = number_of_targets - train_number - val_number
    
    alldata = open(osp.join(outputpath , "alldata.txt"),'w')
    for target in targets:
        with open(target) as f:
            contains = f.readlines()
        alldata.writelines(contains)
        alldata.writelines('\n')   

    alldata.close()
    with open(osp.join(outputpath , "alldata.txt")) as alldata: 
        datas = alldata.readlines()
    
    train = open(osp.join(outputpath,"train.txt"),'w')
    val = open(osp.join(outputpath ,"val.txt"), 'w')
    test = open(osp.join(outputpath , "test.txt"), 'w')
    train.writelines(datas[0:train_number])
    # train.writelines('\n')
    val.writelines(datas[train_number:(train_number+val_number)])
    # val.writelines('\n')
    test.writelines(datas[(train_number+val_number):])
    # test.writelines('\n')
    
    train.close()
    val.close()
    test.close()
    

def main():
    args = arg_parse()

#  load class names
    class_path = args.classpath
    class_names = load_classnames(class_path)


#  load labelImg labels
    labelImg_path = args.txtpath
    labels_data = load_labelImg(labelImg_path)


#  load labelme polygons
    labelme_path = args.jsonpath
    polygons_data = load_labelme(labelme_path)


#  prepare data for training
    targetpath = args.targetpath
    imagepath = args.imagepath
    write(labels_data, polygons_data, imagepath, targetpath)

#   devide all targets into train validation test parts
    outputpath = args.outputpath
    devidepercent = args.devidepercent
    devide(targetpath, outputpath, devidepercent)
    
if __name__ == "__main__":
    main()
