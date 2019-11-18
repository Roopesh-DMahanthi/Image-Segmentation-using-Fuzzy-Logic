#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 20:14:10 2019

@author: roopesh
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 15:51:51 2019

@author: Group-45,46,47,48
"""
import cv2
from PIL import Image
import numpy as np
np.seterr(over='ignore')
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

class ImgSeg:
    
    def disp(cons):
        cImg=Image.open('temp.png')
        for i in range(cons.edgeImg.shape[0]):
            for j in range(cons.edgeImg.shape[1]):
                if(cons.edgeImg[i,j]>70):
                    cImg.putpixel((j,i),(0,0,0,255))
        cImg.show()
        cImg.save("finalimg.png")
    
    def fis(cons):
        Ix1=cons.Ix[:,:]/255
        Iy1=cons.Iy[:,:]/255
        I=np.zeros(Ix1.shape)
        #print(np.unique(Ix1))
        #print(np.unique(Iy1))
        IxMat=ctrl.Antecedent(np.arange(0,1,0.01), 'Ix')
        IyMat=ctrl.Antecedent(np.arange(0,1,0.01), 'Iy')
        Pic=ctrl.Consequent(np.arange(0,1,0.01), 'Picture')
        IxMat['B']=fuzz.trimf(IxMat.universe, [0, 0, 0.4])
        IxMat['W']=fuzz.trapmf(IxMat.universe, [0.2,0.5, 1, 1])
        IyMat['B']=fuzz.trimf(IyMat.universe, [0, 0, 0.4])
        IyMat['W']=fuzz.trapmf(IyMat.universe, [0.2,0.5, 1, 1])
        '''
        IxMat.view()
        IyMat.view()
        '''
        Pic['B']=fuzz.trimf(Pic.universe, [0, 0, 0.4])
        Pic['W']=fuzz.trapmf(Pic.universe, [0.2,0.5, 1, 1])
        
        #Pic.view()
        rule1 = ctrl.Rule(IxMat['B'] & IyMat['B'], Pic['B'])
        rule2 = ctrl.Rule(IxMat['W'], Pic['W'])
        rule3 = ctrl.Rule(IyMat['W'], Pic['W'])
        
        Edge_ctrl = ctrl.ControlSystem(rules=[rule1, rule2, rule3])
        Edging = ctrl.ControlSystemSimulation(Edge_ctrl)
        
        ind=0
        l=Ix1.shape[0]*Ix1.shape[1]
        for i in range(Ix1.shape[0]):
            for j in range(Ix1.shape[1]):
                printProgressBar(ind+1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
                ind+=1
                Edging.input['Ix'] = Ix1[i,j]
                Edging.input['Iy'] = Iy1[i,j]
                Edging.compute()
                I[i,j]=round(Edging.output['Picture'] * 255)
                
                    
        #print(np.unique(I))
        #plt.imshow(I,cmap = plt.get_cmap('gray'))
        edgImg=Image.fromarray(I).convert('RGB')
        edgImg.show()
        edgImg.save('edgedout.png')
        cons.edgeImg=I
        
        #Image.fromarray(mainImg).show()
        #Image.fromarray(mainImgC).show()
        
        


        
    def calcs(cons):
        kernelx1 = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        kernelx2 = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
        kernely1 = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        kernely2 = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
        img_prewittx1 = cv2.filter2D(cons.imArr, -1, kernelx1)
        img_prewittx2 = cv2.filter2D(cons.imArr, -1, kernelx2)
        img_prewitty1 = cv2.filter2D(cons.imArr, -1, kernely1)
        img_prewitty2 = cv2.filter2D(cons.imArr, -1, kernely2)
        cons.Ix = img_prewittx1 + img_prewittx2
        cons.Iy = img_prewitty1 + img_prewitty2
        '''
        imx=Image.fromarray(cons.Ix)
        imy=Image.fromarray(cons.Iy)
        imx.show()
        imy.show()
        '''
        
      
    def calcs2(cons):
        cons.IxRL=np.zeros(cons.imArr.shape)
        cons.IyDU=np.zeros(cons.imArr.shape)
        cons.IxLR=np.zeros(cons.imArr.shape)
        cons.IyUD=np.zeros(cons.imArr.shape)
        cons.Ix=np.zeros(cons.imArr.shape)
        cons.Iy=np.zeros(cons.imArr.shape)
        
        for i in range(0,cons.imArr.shape[0]):
            for j in range(0,cons.imArr.shape[1]):
                if(j!=0):
                    cons.IxRL[i,j]=abs((cons.imArr[i,j])-(cons.imArr[i,j-1]))
                if(i!=0):
                    cons.IyUD[i,j]=abs((cons.imArr[i,j])-(cons.imArr[i-1,j]))
                if(j+1!=cons.imArr.shape[1]):
                    cons.IxLR[i,j]=abs((cons.imArr[i,j])-(cons.imArr[i,j+1]))
                if(i+1!=cons.imArr.shape[0]):
                    cons.IyDU[i,j]=abs((cons.imArr[i,j])-(cons.imArr[i+1,j]))
                    
        for i in range(0,cons.imArr.shape[0]):
            for j in range(0,cons.imArr.shape[1]):
                if(cons.IxRL[i,j]>cons.IxLR[i,j]):
                    cons.Ix[i,j]=cons.IxRL[i,j]
                else:
                    cons.Ix[i,j]=cons.IxLR[i,j]
                if(cons.IyUD[i,j]>cons.IyDU[i,j]):
                    cons.Iy[i,j]=cons.IyUD[i,j]
                else:
                    cons.Iy[i,j]=cons.IyDU[i,j]
        '''
        print(np.unique(cons.imArr))
        print(np.unique(cons.Ix))
        print(np.unique(cons.Iy))
        
        
        plt.subplot(1,2,1)
        plt.imshow(cons.Ix,cmap = plt.get_cmap('gray'))
        plt.subplot(1,2,2)
        plt.imshow(cons.Iy,cmap = plt.get_cmap('gray'))
        
            imx=Image.fromarray(cons.Ix)
        imy=Image.fromarray(cons.Iy)
        imx.show()
        imy.show()
        '''
    
    def Convert2Gmat(cons):
        #print(cons.addr)
        img=Image.open(cons.addr)
        width, height = img.size
        while(width*height>90000) :
            width//=2
            height//=2
            img = img.resize((width, height)) 
        print(width,height)
        img.save('temp.png')
        img.show()
        img=img.convert('L')
        imArr=np.asarray(img)
        #print(imArr.shape)
        
        #plt.imshow(imArr,cmap = plt.get_cmap('gray'))
        cons.imArr=imArr
        
        
            
    def __init__(cons,addr):
        cons.addr=addr
        cons.Convert2Gmat()
        print("Primary Image Resizing & Gray-Scale Conversion Successful.....")
        cons.calcs()
        print("Gradient Details Extracted Successfully.....")
        print("Applying Fuzzy Interface System on Gradients......(Wait For a While)")
        cons.fis()
        print("Applying Fuzzy Interface System on Gradients Successful......")
        print("Displaying Pictures with only Detected Edges as well as Overlaped Edge Detected Primary Color Image....")
        cons.disp()
        #print(cons.ImAdd)
        
        
        
file=input("Enter a valid image name - ")
x=ImgSeg(file)
