from pydarknet import Detector, Image
import cv2
import os
import numpy as  np
import math


now = 550
if __name__ == "__main__":
    # import argparse

    # parser = argparse.ArgumentParser(description='Process an image.')
    # parser.add_argument('path', metavar='image_path', type=str,
    #                     help='Path to source image')

    # args = parser.parse_args()
    # print("Source Path:", args.path)
    
    
    # net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

    net = Detector(bytes("cfg/bfc_v3tiny.cfg", encoding="utf-8"), bytes("weights/bfc_v3tiny_last.weights", encoding="utf-8"), 0, bytes("cfg/obj.data",encoding="utf-8"))
    frame_id = 20
    
    data_svball = []
    data_svgoal = []

    try:
        if not os.path.exists('Hasil/image_'+str(now)):
            os.makedirs('Hasil/image_'+str(now))
    except OSError:
        print ('Error: Creating directory of data')
    try:
        if not os.path.exists('Hasil/data'+str(now)):
            os.makedirs('Hasil/data'+str(now))
    except OSError:
        print ('Error: Creating directory of data')


    for i in range (200):
        dir_images = '../../Data/image_'+str(now)+'/'
        img = cv2.imread(dir_images+str(frame_id)+'.png')
        print(dir_images+str(frame_id)+'.png')
        
        print(img.shape)
        # grayR = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_left = img[:,0:img.shape[1]//2,:].copy()
        img_right = img[:,img.shape[1]//2:img.shape[1],:].copy()
        print(img_left.shape)
        print(img_right.shape)
        pil_img_left = Image(img_left)
        pil_img_right = Image(img_right)

        x = 0
        y = 0
        Xl_Ball= 0
        Xr_Ball = 0 
        Yl_Ball= 0
        Yr_Ball = 0
        
        Xl_Goal1=0
        Xl_Goal2=0
        Xr_Goal1=0
        Xr_Goal2=0
        
        Yl_Goal1=0
        Yl_Goal2=0
        Yr_Goal1 = 0
        Yr_Goal2 = 0

        for i in range(2):
            if i == 0:
                results = net.detect(pil_img_left)
            else:   
                results = net.detect(pil_img_right)
            # print(results)

            for cat, score, bounds in results:

                # print(cat)
                if cat == 'Ball':
                    x, y, w, h = bounds
                    if i == 0:  
                        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
                        cv2.putText(img, cat, (int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
                        cv2.circle(img, (int(x), int(y)), 2, (0, 255, 0),thickness=2 )
                        Xl_Ball = x
                        Yl_Ball = y
                        print ('Xleft:', Xl_Ball, 'Yleft:', Yl_Ball)
                    else:
                        cv2.rectangle(img, (int(x - w / 2)+img.shape[1]//2, int(y - h / 2)), (int(x + w / 2)+img.shape[1]//2, int(y + h / 2)), (255, 0, 0), thickness=2)
                        cv2.putText(img, cat, (int(x)+img.shape[1]//2,int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
                        cv2.circle(img, (int(x)+img.shape[1]//2, int(y)), 2, (0, 255, 0),thickness=2 )
                        Xr_Ball = x
                        Yr_Ball = y
                        print ('Xright:', Xr_Ball, 'Yright:', Yr_Ball)
                if cat == 'Goal':
                    x, y, w, h = bounds
                    if i == 0:  
                        cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
                        cv2.putText(img, cat, (int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
                        cv2.circle(img, (int(x), int(y)), 2, (0, 255, 0),thickness=2 )
                        if x < 640 :
                            Xl_Goal1 = x
                            Yl_Goal1 = y
                            print ('Xleft1:', Xl_Goal1, 'Yleft1:', Yl_Goal1)
                        else :
                            Xl_Goal2 = x
                            Yl_Goal2 = y
                            print ('Xleft2:', Xl_Goal2, 'Yleft2:', Yl_Goal2)
                    
                    else:
                        cv2.rectangle(img, (int(x - w / 2)+img.shape[1]//2, int(y - h / 2)), (int(x + w / 2)+img.shape[1]//2, int(y + h / 2)), (255, 0, 0), thickness=2)
                        cv2.putText(img, cat, (int(x)+img.shape[1]//2,int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
                        cv2.circle(img, (int(x)+img.shape[1]//2, int(y)), 2, (0, 255, 0),thickness=2 )
                        if x < 640 :
                            Xr_Goal1 = x
                            Yr_Goal1 = y
                            print ('Xright1:', Xr_Goal1, 'Yright1:', Yr_Goal1)
                        else :
                            Xr_Goal2 = x
                            Yr_Goal2= y
                            print ('Xright2:', Xr_Goal2, 'Yright2:', Yr_Goal2) 
                        
        f = 699.475 
        B = 6.29477 
        try:
            print('Xl_Ball :', Xl_Ball, 'Xr_Ball :', Xr_Ball)
            print('Xl_Goal1 :', Xl_Goal1, 'Xr_Goal1 :', Xr_Goal1)
            print('Xl_Goal2 :', Xl_Goal2, 'Xr_Goal2 :', Xr_Goal2)
            
            if Xl_Ball != 0:
                if Xr_Ball != 0:
                    stereovision_ball = (B*f)/(Xl_Ball-Xr_Ball)

                    print("+++++++++++++++")
                    print('stereovision ball :', stereovision_ball)
                    data_svball.append(stereovision_ball)
                    np.savetxt('Hasil/data'+str(now)+'/sv_ball.txt', (data_svball),fmt = '%.7f', newline='\n')
                    print("+++++++++++++++")
            
            if Xl_Goal1 != 0 :
                if  Xr_Goal1 != 0:
                    stereovision_goal1 = (B*f)/(Xl_Goal1-Xr_Goal1)
                    Pangkat1 = -0.0008*stereovision_goal1**2 + 1.3766*stereovision_goal1 - 49.698
            if Xl_Goal2 != 0 : 
                if Xr_Goal2 != 0 :
                    stereovision_goal2 = (B*f)/(Xl_Goal2-Xr_Goal2)
                    Pangkat2 = -0.0008*stereovision_goal2**2 + 1.3766*stereovision_goal2 - 49.698
            
            print("+++++++++++++++")

            print('stereovision goal1 :', stereovision_goal1)
            print('regresi goal1 :', Pangkat1)
            print('stereovision goal2 :', stereovision_goal2)
            print('regresi goal2 :', Pangkat2)
            data_svgoal.append(stereovision_goal1)
            data_svgoal.append(stereovision_goal2)
            np.savetxt('Hasil/data'+str(now)+'/sv_goal.txt', (data_svgoal),fmt = '%.7f', newline='\n')

            print("+++++++++++++++")
        
        except ZeroDivisionError:
            pass

        cv2.imwrite('Hasil/image_'+str(now)+'/'+str(frame_id)+'.png',img)
        frame_id += 1
    
        print(img.shape)