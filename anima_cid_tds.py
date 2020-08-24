# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:37:45 2020

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



r = requests.get('https://raw.githubusercontent.com/albertosaa/COVID/master/data/20200819.csv.zip')

zip_file = zipfile.ZipFile(io.BytesIO(r.content))


namelist=["Novos casos", "Casos acumulados", 'Novos óbitos','Óbitos acumulados']
cidlist = {"Aracaju":"SE","Belém":"PA","Belo Horizonte":"MG","Boa Vista":"RR","Campina Grande":"PB","Campinas":"SP","Campo Grande":"MS","Cuiabá":"MT","Curitiba":"PR","Diadema":"SP","Fortaleza":"CE","Florianópolis":"SC","Goiânia":"GO","Guarulhos":"SP","João Pessoa":"PB","Jundiaí":"SP","Macapá":"AP","Maceió":"AL","Manaus":"AM","Mauá":"SP","Natal":"RN","Osasco":"SP","Palmas":"TO","Piracicaba":"SP","Porto Alegre":"RS","Porto Velho":"RO","Recife":"PE","Ribeirão Preto":"SP","Rio Branco":"AC","Rio de Janeiro":"RJ","Salvador":"BA","Santo André":"SP","Santos":"SP","São Bernardo do Campo":"SP","São Caetano do Sul":"SP","São José dos Campos":"SP","São Luís":"MA","São Paulo":"SP","Sorocaba":"SP","Teresina":"PI","Vitória":"ES"}


#cria as pastas se elas não existirem
script_dir = os.path.dirname(__file__)
gifs_cid = os.path.join(script_dir,'gifs_cid/')
graf_cid = os.path.join(script_dir,'graf_cid/')
if not os.path.isdir(graf_cid):
    os.makedirs(graf_cid)
if not os.path.isdir(gifs_cid):
    os.makedirs(gifs_cid)
#3s

def smooth(Y,n):
# Retorna a média móvel com janela (2n+1), com as bordas tratadas como descrito no texto
     k = Y.size
     Y_smooth = np.zeros(k)
     Y_edge = np.concatenate( ( Y[0]*np.ones(n) , Y , Y[ k-n : k] + Y[k-1] - Y[k-n-1] )  )
     for i in range (0,k):
         Y_smooth[i]  =  np.sum(Y_edge[i:i+2*n+1])/(2*n+1)
    
     return Y_smooth


for a in cidlist:
    files = zip_file.namelist()
    with zip_file.open(files[0], 'r') as csvfile_byte:
        with io.TextIOWrapper(csvfile_byte, encoding='utf-8') as csv_file:
            cr = csv.reader(csv_file)
            linecsv = list(cr)
            
    
    for j in range(len(namelist)):
        k = 0 
        Y = []
        image=[]
        for row in linecsv:
            if (row[2] == a) and (row[1] == cidlist[a]):
                if k == 0:
                    First_Day = row[7]#data   
                if namelist[j] == "Casos acumulados" or namelist[j]=="Novos casos":
                    Y.append(int(row[10]))
                elif namelist[j]=="Óbitos acumulados" or namelist[j]=="Novos óbitos":
                    Y.append(int(row[11]))
                k += 1
            
        dados = np.array(Y)
        
        if namelist[j] =="Novos casos" or namelist[j] =="Novos óbitos":
            dados_0 = np.array(Y)
            dados = np.zeros(k)
            for b in range(1,k):
                dados[b]= dados_0[b]-dados_0[b-1]
        
        tipo= namelist[j]        
        for i in range(10,k):
            file_name = a + " - "+ tipo +" - "+ format(i,'03') +".jpg"
            if not os.path.isfile('graf_cid/'+file_name):
                date = datetime.strptime(First_Day, "%m/%d/%Y") + timedelta(days = i)
            
# Suavização: 4 iterações da média móvel   
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
                plt.title(namelist[j]+" - "+a+" - "+date.strftime("%d/%m/%Y"))
                plt.savefig(graf_cid + file_name,bbox_inches="tight") 
                plt.close()

            image.append(imageio.imread(graf_cid + file_name))
        imageio.mimsave('gifs_cid/'+tipo+" - "+a+'.gif',image)    
        
    
    
    
