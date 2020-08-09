#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 10:23:44 2020

@author: asaa
"""

import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
import io
import zipfile
import imageio

from datetime import datetime , timedelta



r = requests.get('https://raw.githubusercontent.com/albertosaa/COVID/master/data/20200620.csv.zip')

zip_file = zipfile.ZipFile(io.BytesIO(r.content))

reglist = ["SP","MG","RJ","BA","PR","RS","PE","CE","PA","SC","MA","GO","AM","ES","PB","RN","MT","AL","PI","DF","MS","SE","RO","TO","AC","AP","RR"]

for a in range(len(reglist)):
    files = zip_file.namelist()
    with zip_file.open(files[0], 'r') as csvfile_byte:
        with io.TextIOWrapper(csvfile_byte, encoding='utf-8') as csv_file:
            cr = csv.reader(csv_file)
            linecsv = list(cr)


    Y = []
    k = 0 
    im=[]
    
    for row in linecsv:
        if (row[1] == reglist[a]) and (row[2] == "") and ( row[9] != "" ):

            if k == 0:
                First_Day = row[7]
            
            Y.append(int(row[10]))
            k += 1
            pop = int(row[9])
    R_raw = np.array(Y)
    dR_raw = np.zeros(k)
    for i in range (1,k):
        dR_raw[i] = R_raw[i] - R_raw[i-1] 
    
    
    def smooth(Y,n):
#
#
# Retorna a média móvel com janela (2n+1), com as bordas tratadas como descrito no texto
#
#    
        k = Y.size
        Y_smooth = np.zeros(k)
    
        Y_edge = np.concatenate( ( Y[0]*np.ones(n) , Y , Y[ k-n : k] + Y[k-1] - Y[k-n-1] )  )
    
        for i in range (0,k):
            Y_smooth[i]  =  np.sum(Y_edge[i:i+2*n+1])/(2*n+1)
        
        
        return Y_smooth

    pop= pop//2000
    
    for i in range (10,k):
        file_name = reglist[a]+format(i,'03')+".jpg"
    
        date = datetime.strptime(First_Day, "%m/%d/%Y") + timedelta(days = i)
    
        R_raw_k = R_raw[:i]
    
#
# Suavização: 4 iterações da média móvel   
#
        R_smooth_k = smooth(R_raw_k,3)
        for j in range (0,3):
            R_smooth_k = smooth(R_smooth_k,3)
        
        dR_smooth_k = np.zeros(i)
        for j in range (1,i):
            dR_smooth_k[j] = R_smooth_k[j] - R_smooth_k[j-1]
        
        dR_smooth = np.concatenate((dR_smooth_k,np.zeros(k-i)))
        dR_raw_p = np.concatenate((dR_raw[:i],np.zeros(k-i)))
    
    
        plt.grid(False)       
        plt.ylim(0,pop) 
        plt.bar(np.linspace(0,k-1,k),dR_raw_p)
        plt.plot(np.linspace(0,i-1,i) , dR_smooth_k,"r")
        plt.xlabel("Dias")
        plt.ylabel("Casos")
        plt.title("Novos casos - "+reglist[a]+" - "+date.strftime("%d/%m/%Y"))
#        plt.savefig(file_name,bbox_inches="tight") 
        plt.figure(num=i)
        im.append(plt.figure(num=i))
    
    imageio.mimsave(relist[a]+".gif",im) 
    
    plt.close()
        

    
