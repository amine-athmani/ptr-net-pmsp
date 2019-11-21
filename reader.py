# -*- coding: utf-8 -*-
import random
import os


class READ_BENCHMARK:

    
  def READ_INSTANCE(self,path):
    File=open(path,"r")
    content = File.read().split('\n')
    i=0 
    Instance=[]

    #Lire le nombre de machine et le nombre de travaux
    ligne0=content[0].split(' ')
    Instance.append(int(ligne0[0]))
    Instance.append(int(ligne0[2]))

    #Lire les temps d'exécutions des travaux sur les machines 
    i=2
    k=0
    ligne=[]
    Pjob=[] #Tableau des temps d'execution du job dans les machine 1....m
    P=[] #  Matrice des temps d'exécution des job j sur les machines i

    #Récuperer les temps d'exécutions des travaux sur les machines
    #La variable ligne contient à chaque itération contient les temps d'exécution du travail
    # "k" sur toutes les machines
    #La variable P contient la matrice des temps d'exécutions
    while k<Instance[0]:
      ligne=content[i].split('\t')
      for j in range (2,len(ligne),2):
        Pjob.append(int(ligne[j]))

      P.append(Pjob)
      ligne=[]
      Pjob=[]
      i+=1
      k+=1

    Instance.append(P)
    i=i+2
    k=0
    S=[] 
    Si=[] 
    Sij=[] 
    #Récuperer les Sijk 
    #La variable Sij(ligne) contient les Sijk relatifs au travail j au niveau d'une machine 
    #m
    #La variable Si (matrice) contient tous les Sijk entre les travaux au niveau d'une machine m
    #La variable S (tableau de matrice) contient les matrice Si dont chacune contient les
    #Sijk entre les travaux au niveau d'une machine donnée
    while content[i]!='':
      if (k!=Instance[0]):
        ligne=content[i].split('\t')
        for j in range(len(ligne)):
          Sij.append(int(ligne[j]))
        Si.append(Sij)
        Sij=[]
        k+=1
      else:
        k=0
        S.append(Si)
        Si=[]
      i+=1

    S.append(Si)
    Instance.append(S)
    File.close()
    return Instance


  def READ_AL_SALEM_INSTANCE(self,path):

    f=open(path,'r')
    content=f.readlines()
    Instance=list()
    Instance.append(int(content[2]))
    Instance.append(int(content[1]))

    #Read the processing time matrix

    P=list()
    i=4
    while content[i]!='\n':
      
      line=content[i].split(' ')
      line_job=list()
      for e in range(len(line)-1):
        line_job.append(int(line[e]))
      P.append(line_job)
      i+=1
    
    Instance.append(P)

    #Read the setup times matrix #############
    m=0
    i+=1
    S=list()
    while m <Instance[1]:

      #print("Creation of the setup time matrix of the ",m," machine.")
      Si=list()
      while content[i]!='\n':
        line=content[i].split(' ')
        line_job=list()
        
        for e in range(len(line)-1):
          line_job.append(int(line[e]))

        Si.append(line_job)
        i+=1
      S.append(Si)
      i+=1
      m+=1
    

    Instance.append(S)
    return Instance 
  