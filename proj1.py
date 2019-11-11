# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 15:51:51 2019

@author: Roopesh
"""
#import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl



class ImgSeg:
    
    
    def fis(cons):
        Ix1=cons.Ix[:,:]/255
        Iy1=cons.Iy[:,:]/255
        I=np.zeros(Ix1.shape)
        #print(np.unique(Ix1))
        #print(np.unique(Iy1))
        IxMat=ctrl.Antecedent(np.arange(0,1,0.01), 'Ix')
        IyMat=ctrl.Antecedent(np.arange(0,1,0.01), 'Iy')
        Pic=ctrl.Consequent(np.arange(0,1,0.01), 'Picture')
        IxMat['B']=fuzz.trimf(IxMat.universe, [0, 0, 0.6])
        IxMat['W']=fuzz.trimf(IxMat.universe, [0.25, 1, 1])
        IyMat['B']=fuzz.trimf(IyMat.universe, [0, 0, 0.6])
        IyMat['W']=fuzz.trimf(IyMat.universe, [0.25, 1, 1])
        
        IxMat.view()
        IyMat.view()
        
        Pic['B']=fuzz.trimf(Pic.universe, [0, 0, 0.6])
        Pic['W']=fuzz.trimf(Pic.universe, [0.25, 1, 1])
        
        Pic.view()
        rule1 = ctrl.Rule(IxMat['B'] & IyMat['B'], Pic['B'])
        rule2 = ctrl.Rule(IxMat['W'], Pic['W'])
        rule3 = ctrl.Rule(IyMat['W'], Pic['W'])
        
        Edge_ctrl = ctrl.ControlSystem(rules=[rule1, rule2, rule3])
        Edging = ctrl.ControlSystemSimulation(Edge_ctrl)
        '''
        Edging.input['Ix'] = 0.2
        Edging.input['Iy'] = 0.8
        Edging.compute()
        print(Edging.output['Picture'])
        Pic.view(sim=Edging)
        
        cImg=Image.open(cons.addr)
        mainImgC=np.asarray(cImg).copy()
        '''
        mainImg=cons.imArr.copy()
        for i in range(Ix1.shape[0]):
            for j in range(Ix1.shape[1]):
                Edging.input['Ix'] = Ix1[i,j]
                Edging.input['Iy'] = Iy1[i,j]
                Edging.compute()
                I[i,j]=round(Edging.output['Picture'] * 255)
                if(I[i,j]>130):
                    if(mainImg[i,j]<128):
                        mainImg[i,j]=255
                        #for i in mainImgC[i,j]:
                            #i=255
                    else:
                        mainImg[i,j]=0
                        #for i in mainImgC[i,j]:
                            #i=0
                    
        print(np.unique(I))
        #plt.imshow(I,cmap = plt.get_cmap('gray'))
        Image.fromarray(I).show()
        Image.fromarray(mainImg).show()
        #Image.fromarray(mainImgC).show()
        
        


        

        
    def calcs(cons):
        cons.Ix=np.zeros(cons.imArr.shape)
        cons.Iy=np.zeros(cons.imArr.shape)
        '''
        for i in range(1,cons.imArr.shape[1]):
            cons.Ix[:,i]=abs(cons.imArr[:,i]-cons.imArr[:,i-1])
        for i in range(1,cons.imArr.shape[0]):
            cons.Iy[i,:]=abs(cons.imArr[i,:]-cons.imArr[i-1,:])
        '''
        for i in range(1,cons.imArr.shape[0]):
            for j in range(1,cons.imArr.shape[1]):
                cons.Ix[i,j]=abs(cons.imArr[i,j]-cons.imArr[i,j-1])
                cons.Iy[i,j]=abs(cons.imArr[i,j]-cons.imArr[i-1,j])
        '''
        for i in range(1,cons.imArr.shape[0]):
            for j in range(1,cons.imArr.shape[1]):
                if(abs(cons.imArr[i,j]-cons.imArr[i,j-1])>0):
                    cons.Ix[i,j]=255
                if(abs(cons.imArr[i,j]-cons.imArr[i-1,j])>0):
                    cons.Iy[i,j]=255
        '''
        print(np.unique(cons.imArr))
        print(np.unique(cons.Ix))
        print(np.unique(cons.Iy))
        
        '''
        plt.subplot(1,2,1)
        plt.imshow(cons.Ix,cmap = plt.get_cmap('gray'))
        plt.subplot(1,2,2)
        plt.imshow(cons.Iy,cmap = plt.get_cmap('gray'))
        '''
        imx=Image.fromarray(cons.Ix)
        imy=Image.fromarray(cons.Iy)
        imx.show()
        imy.show()
        
    
    def Convert2Gmat(cons):
        #print(cons.addr)
        img=Image.open(cons.addr).convert('L')
        imArr=np.asarray(img)
        #print(imArr.shape)
        img.show()
        #plt.imshow(imArr,cmap = plt.get_cmap('gray'))
        cons.imArr=imArr
        
        
            
    def __init__(cons,addr):
        cons.addr=addr
        cons.Convert2Gmat()
        cons.calcs()
        cons.fis()
        #print(cons.ImAdd)
        
        
        
        
x=ImgSeg('Drawing.png')
