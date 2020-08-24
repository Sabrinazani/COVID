# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:48:55 2020

@author: çaça
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import requests
import csv
import io
import zipfile
import imageio
from datetime import datetime , timedelta



r = requests.get('https://raw.githubusercontent.com/albertosaa/COVID/master/data/20200823.csv.zip')

zip_file = zipfile.ZipFile(io.BytesIO(r.content))


def smooth(Y,n):
# Retorna a média móvel com janela (2n+1), com as bordas tratadas como descrito no texto
     k = Y.size
     Y_smooth = np.zeros(k)
     Y_edge = np.concatenate( ( Y[0]*np.ones(n) , Y , Y[ k-n : k] + Y[k-1] - Y[k-n-1] )  )
     for i in range (0,k):
         Y_smooth[i]  =  np.sum(Y_edge[i:i+2*n+1])/(2*n+1)
    
     return Y_smooth


def animacid(reglistcid):
    
    script_dir = os.path.dirname(__file__)
    gifs_cid = os.path.join(script_dir,'gifs_cid/')
    graf_cid = os.path.join(script_dir,'graf_cid/')
    if not os.path.isdir(graf_cid):
        os.makedirs(graf_cid)
    if not os.path.isdir(gifs_cid):
        os.makedirs(gifs_cid)
        
    typelist=["Novos casos", "Casos acumulados", 'Novos óbitos','Óbitos acumulados']
        
    for a in reglistcid:
        files = zip_file.namelist()
    
        with zip_file.open(files[0], 'r') as csvfile_byte:
            with io.TextIOWrapper(csvfile_byte, encoding='utf-8') as csv_file:
                cr = csv.reader(csv_file)
                linecsv = list(cr) 
    
        for j in range(len(typelist)):
            k = 0 
            Y = []
            image=[]
            for row in linecsv:
                if (row[2] == a[1]) and (row[1] == a[0]):
                    if k == 0:
                        First_Day = row[7]#data   
                    if typelist[j] == "Casos acumulados": 
                        Y.append(int(row[10]))
                    elif typelist[j]=="Novos casos":
                        Y.append(int(row[11]))
                    elif typelist[j]=="Óbitos acumulados": 
                        Y.append(int(row[12]))
                    elif typelist[j]=="Novos óbitos":
                        Y.append(int(row[13]))
                    k += 1
            
            dados = np.array(Y)
            tipo= typelist[j]       
            city= a[1]
            for i in range(10,k):
                file_name = city + " - "+ tipo +" - "+ format(i,'03') +".jpg"
                
                if not os.path.isfile('graf_cid/'+file_name):
                    date = datetime.strptime(First_Day, "%m/%d/%Y") + timedelta(days = i)
                    R_smooth_k = dados[:i]#dados até o dia i
                    for r in range(0,3):
                        R_smooth_k = smooth(R_smooth_k,3)#suaviza os dados até dia i
                    dados_ar = np.concatenate((dados[:i],np.zeros(k-i))) #array com dados até i e 0s
                    
                    plt.grid(False)       
                    plt.ylim(0,np.amax(dados)) 
                    plt.bar(np.linspace(0,k-1,k),dados_ar,color='blue')
                    plt.plot(np.linspace(0,i-1,i), R_smooth_k,"r")
                    plt.xlabel("Dias")
                    plt.ylabel("Casos")
                    plt.title(city+" - "+tipo+" - "+date.strftime("%d/%m/%Y"))
                    plt.savefig(graf_cid + file_name,bbox_inches="tight") 
                    plt.close()

                image.append(imageio.imread(graf_cid + file_name))
            imageio.mimsave('gifs_cid/'+city+" - "+tipo+'.gif',image)    
    return()
        

################################################
# Exemplo de argumento:
# animacid(reglistcid = [["SP","São Paulo"],["SP","Campinas"],["SP","Guarulhos"],["SP","São Bernardo do Campo"],\
#              ["SP","São José dos Campos"],["SP","Santo André"],["SP","Ribeirão Preto"],\
#              ["SP","Osasco"],["SP","Sorocaba"], ["SP","Mauá"], ["SP","Santos"], ["SP","Diadema"],\
#              ["SP","São Caetano do Sul"],["SP","Jundiaí"],["SP","Piracicaba"],\
#              ["RJ","Rio de Janeiro"],["BA","Salvador"],["CE","Fortaleza"],["MG","Belo Horizonte"],\
#              ["AM","Manaus"],["PR","Curitiba"], ["PE","Recife"], ["RS","Porto Alegre"], ["PA","Belém"],["GO","Goiânia"],\
#              ["MA","São Luís"],["AL","Maceió"], ["PI","Teresina"],  ["RN","Natal"],\
#              ["MS","Campo Grande"], ["PB","João Pessoa"],["PB","Campina Grande"],\
#              ["SE","Aracaju"],["MT","Cuiabá"],["RO","Porto Velho"],["SC","Florianópolis"],\
#              ["AP","Macapá"],["AC","Rio Branco"],["ES","Vitória"], ["RR","Boa Vista"],["TO","Palmas"]])
    
