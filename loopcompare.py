# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:24:39 2020

@author: mi19356
"""
import numpy as np
import pandas as pd 
import os
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy.polynomial.polynomial as P
import math


class load_elinfo:
   
    def __init__(self,cname):
        loc=os.path.join(os.path.dirname(__file__),'data')
        
        #import data
        exp=pd.read_excel(os.path.join(loc, cname + '.xlsx'),header=None,sheet_name='Exp').to_numpy()
        sim=pd.read_excel(os.path.join(loc, cname + '.xlsx'),header=None,sheet_name='Sim').to_numpy()
    
        self.exp=exp
        self.sim=sim
        
    def fitcurves(self):
        
        exp=self.exp
        sim=self.sim
        
        #determine if increasing values or decreasing ###need to have this for exp and sim
        decreas=[]
        decreassim=[]
        ppp=0
        pp=0
        for i in range(0,len(exp[0,0::2])):
            
            if (exp[0,pp]>exp[1,pp]):
                decreas.append(True)
            else:
                decreas.append(False)
            pp+=2
            
            if (sim[0,ppp]>sim[1,ppp]):
                decreassim.append(True)
            else:
                decreassim.append(False)
            ppp+=2
            
        #find indeces of loading and unloading interchange###need to have this for both exp and sim
        pp=0
        turnpointexp=[]
        turnpointsim=[]
        for i in range(0,len(exp[0,0::2])):
            if (decreas[i]==False):
                turnpointexp.append(np.argmax(exp[:,pp]))
            if(decreassim[i]==False):
                turnpointsim.append(np.argmax(sim[:,pp]))
                #turnpointexp=np.asarray([x.index(max(x)) for x in zip(*exp[:,0::2])])
                #turnpointsim=np.asarray([x.index(max(x)) for x in zip(*sim[:,0::2])])
            if(decreas[i]==True):
                turnpointexp.append(np.argmin(exp[:,pp]))
            if(decreassim[i]==True):
                turnpointsim.append(np.argmin(sim[:,pp]))
            pp+=2
       # else:
        #    turnpointexp=np.asarray([x.index(min(x)) for x in zip(*exp[:,0::2])])
         #   turnpointsim=np.asarray([x.index(min(x)) for x in zip(*sim[:,0::2])])
             
        #find maximum and minimum strains
       # for i in range(0,len(exp[0,0::2])):
        #    maxv
        maxvalsexp=np.asarray([max(x) for x in zip(*exp[:,0::2])])
        minvalsexp=np.asarray([min(x) for x in zip(*exp[:,0::2])])

        
        #polyfit
        zexp1=[]
        zexp2=[]
        zsim1=[]
        zsim2=[]
        n=0
        t=1
        p=2
        for i in range(0,len(exp[0,:])):
            if i % p == 0:
               # zexp.append(P.polyfit(exp[:,i],exp[:,t],30))
                zexp1.append(P.polyfit(exp[0:turnpointexp[n],i],exp[0:turnpointexp[n],t],4))
                zexp2.append(P.polyfit(exp[turnpointexp[n]:,i],exp[turnpointexp[n]:,t],4))
                zsim1.append(P.polyfit(sim[0:turnpointsim[n],i],sim[0:turnpointsim[n],t],4))
                zsim2.append(P.polyfit(sim[turnpointsim[n]:,i],sim[turnpointsim[n]:,t],4))
            else:
                t+=2
                n+=1
   
        #new values and extra x-values
   
        xpoints1=np.linspace(minvalsexp,maxvalsexp,100)
        xpoints2=np.linspace(maxvalsexp,minvalsexp,100)
        
       # plt.plot(exp[0:turnpointexp[1],0],exp[0:turnpointexp[1],1])
        #plt.plot(exp[turnpointexp[1]:,0],exp[turnpointexp[1]:,1]) 
        
       # plt.plot(sim[0:turnpointexp[1],0],sim[0:turnpointexp[1],1])
       # plt.plot(sim[turnpointexp[1]:,0],sim[turnpointexp[1]:,1])
        
        ffitexp1=[]
        ffitexp2=[]
        ffitsim1=[]
        ffitsim2=[]
        
        for i in range(0,len(exp[0,0::2])):
            ffitexp1.append(P.polyval(xpoints1[:,i], zexp1[i]))
            ffitexp2.append(P.polyval(xpoints2[:,i], zexp2[i]))
            ffitsim1.append(P.polyval(xpoints1[:,i], zsim1[i]))
            ffitsim2.append(P.polyval(xpoints2[:,i], zsim2[i]))
            
        
        
        plt.plot(xpoints1[:,0],ffitexp1[0],'r')
        plt.plot(xpoints2[:,0],ffitexp2[0],'g')
        
        plt.plot(xpoints1[:,0],ffitsim1[0],'r')
        plt.plot(xpoints2[:,0],ffitsim2[0],'g')
        
        plt.show()
        
     
        
        self.ffitexp1=np.asarray(ffitexp1)
        self.ffitsim1=np.asarray(ffitsim1)
        self.ffitexp2=np.asarray(ffitexp2)
        self.ffitsim2=np.asarray(ffitsim2)
        self.decreas=decreas
        self.decreassim=decreassim
        
    def errorcal(self):
        ffitexp1=self.ffitexp1
        ffitsim1=self.ffitsim1
        ffitexp2=self.ffitexp2
        ffitsim2=self.ffitsim2
        decreas=self.decreas
        decreassim=self.decreassim
              
        
                
        
        ffitsim=[[]]*len(ffitexp1[:,0])
        ffitexp=[[]]*len(ffitexp1[:,0])
        for i in range(0,len(ffitexp1[:,0])):
            ffitexp[i]=np.append(ffitexp1[i,:],ffitexp2[i,:])
            ffitsim[i]=np.append(ffitsim1[i,:],ffitsim2[i,:])
            
        #need to check if false and true, must be the same
        for i in range(0,len(decreas)):
            if (decreas[i]!=decreassim[i]):
                ffitsim[i]=ffitsim[i][::-1]
        
        #combine exp and sim data
        totalffitmax=[]
        totalffitmin=[]
        for i in range(0,len(ffitexp1[:,0])):
            totalffitmax.append(np.maximum(ffitexp[i],ffitsim[i]))
            totalffitmin.append(np.minimum(ffitexp[i],ffitsim[i]))

        #divide predicted with experiment
        ratio=[]
        for i in range(0,len(ffitexp1[:,0])):
            ratio.append(np.log(abs(np.asarray(ffitsim[i]))/abs(np.asarray(ffitexp[i]))))
            
        #calculate the unsigned relative error
        diff=(np.asarray(totalffitmax)-np.asarray(totalffitmin))/np.asarray(totalffitmin)
        
        
        
        #find the median unsigned percantage error
    
        MAPE=np.asarray([np.exp(np.median(np.abs(x)))-1 for x in zip(*np.transpose(ratio))])*100
        
        return MAPE

       
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx       
        
load=load_elinfo('hysteresis')
load.fitcurves()
load.errorcal()