# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 18:05:54 2021

@author: nahuel lahoz
"""
"""interval_range, 
Funcion cut.group
"""


"""Importaciones"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #Librerias graficas

import plotly.express as px
from plotly.offline import plot 
import seaborn as sns

"""Carga de los datos"""

df=pd.read_csv("DataSet_TP2\DataSet-Edad-Talla-Peso-TA.csv", sep=';', decimal=",")
#df.info()
#df.head()
#df.describe(include="all")


'Arreglo de los datos'
df.isnull().sum() #Cuento cantidad de missing values 
df= df.dropna() #Dropeo valores faltantes
(df["Peso"] ==0).sum() #Tengo 29 datos en Peso que son igual a 0
df=df.drop(df[df.Peso ==0].index) #Elimino pesos en 0
#df.info()


'Rescato datos'

df.loc [df["Altura"]>10,'Altura']=df["Altura"]/100 #Valores pasados de centimetros a metros.
df.loc [df["Peso"]>500,'Peso']=df["Peso"]/1000 #Valores pasados de gramos a kilos
df.loc [df["PA_max"]>55,'PA_max']=df["PA_max"]/10 

#df["Altura"].describe()

#df["Peso"].describe()

#df["Peso"].max()

#df["PA_max"].describe()

#df.describe()


'Los datos ya tienen sentido, ahora genero nueva Columna de IMC (kg/m2)'

df["IMC"]= (df.Peso/(df.Altura**2))

df["IMC"].describe()




"""Ahora creo intervalos"""


'Intervalos de la edad'

df["Edad"].describe()
interv_edad=[0,19,30,40,55,70,110]

names = ["0-18", 
         "19-29", 
         "30-39",
         "40-54", 
         "55-70",
         "70-110"]



bins_edad=pd.cut(df["Edad"],interv_edad, labels= names)

#bins_edad.describe()
bins_edad.value_counts()



'Intervalos del IMC'

interv_imc= [0,18.5,25, 30, 40,50,100 ]

nombres= ["Insuficiente", "Normopeso","sobrepeso","Ob1","Ob_mor","Ob_ext"]

bins_imc=pd.cut(df["IMC"],interv_imc, labels= nombres)


#bins_imc.describe()
#bins_imc.value_counts(sort=False)
#bins_imc.value_counts()


'Intervalos presion'

interv_pres= [0,9,13,14,16,17,40]


etiquetas=["hipotenso","optima_normal","N_alta", "grado1","grado2","grado3"]

bins_presion=pd.cut(df["PA_max"],interv_pres, labels= etiquetas)

#bins_presion.describe()
#bins_presion.value_counts(sort=False)
#bins_presion.value_counts()



"""Una vez creados los intervalos y clasificados los datos, 
agrego una nueva columna al df donde lo especifica"""


df['Rango_edad']=bins_edad

df['Clas_pres']=bins_presion

df['Clas_imc']=bins_imc

#df.info()


'Realizo grafico de histograma y torta con cada uno de los cortes que hice'



"""
Edad --- en histograma
"""
plt.hist(x=bins_edad,color='#F2AB6D', rwidth=0.6, density=True, align='mid')
plt.title('Histograma de edades')
plt.xlabel('Edades')
plt.ylabel('Frecuencia')
plt.show()




"""
IMC
"""
sepa = [0.15,0.15,0.15,0.15,0.15,0.15]
plt.pie(bins_imc.value_counts(), labels=nombres, autopct='%1.2f%%', explode = sepa)
plt.title('Porcentajes de IMC')
plt.show()





"""
"PA_max"  -- en torta
"""
plt.pie(bins_presion.value_counts(), labels= etiquetas,autopct='%1.2f%%' )
plt.title('Porcentajes de Presiones')
plt.show()




"""Scater 2d"""


#Muestra una tendencia a subir la presion normal a medida que aumenta la edad
fig = px.scatter(df, x='Edad', y='PA_max' , color= bins_presion)
plot(fig)

# A mayor imc, tiende mas a la dispersion de los puntos hacia una presion mas alta, 
#por lo que se puede ver que a mayor imc, mayor probabiliadd de tener presion alta
fig0= px.scatter(df, x='PA_max', y='IMC' , color= bins_imc)
plot(fig0)


#Lo mismo pero considerando tambien las edades
fig01= px.scatter(df, x='IMC', y='PA_max' , color= bins_edad)
plot(fig01)





"""Armo un scatter 3d para ver correlacion de variables"""

fig02 = px.scatter_3d(df, x='Edad', y='IMC', z='PA_max' , color= bins_edad)
plot(fig02)
#Obtengo un grafico que muestra los rangos de edades
#Poner bordes y achicar bolitas

fig03 = px.scatter_3d(df, x='Edad', y='IMC', z='PA_max' , color= bins_imc)
plot(fig03)
#Con el imc -- A medida que sube la edad y el imc vemos una mayor tendencia a la presion alta


"""Agrupo"""


#Me devuelve cuantos hombres y cuantas mujeres hay en la columna PA_max
df.groupby(['Sexo'])["PA_max"].count() 


#Me los agrupa por categoria de presion y me dice cuantos son hombres y cuantos mujeres

df.groupby([bins_presion])['Sexo'].value_counts()


#Aqui puedo ver como cuales son los valores estadisticos de la columna altura 
#separada por las categorias de presion
df.groupby(df.Clas_pres)['Altura'].describe()

#Aqui puedo ver como cuales son los valores estadisticos de la columna IMC 
#separada por las categorias de presion
df.groupby(df.Clas_pres)['IMC'].describe().round(2)


#Aqui puedo ver como cuales son los valores estadisticos de la columna Edad
#separada por las categorias de presion

df.groupby(df.Clas_pres)['Edad'].describe().round(2)

#Aqui puedo ver como cuales son los valores estadisticos de la columna PA_max
#separada por las categorias de la edad
df.groupby(df.Rango_edad)['PA_max'].describe().round(2)


#Aqui puedo ver como cuales son los valores estadisticos de la columna PA_max
#separada por las categorias de imc
df.groupby(df.Clas_imc)['PA_max'].describe().round(2)



"""
Deteccion de outliers
"""

'PYOD'

'https://www.analyticsvidhya.com/blog/2019/02/outlier-detection-python-pyod/'

#A traves de esta funcion intento detectar utilizando los intecuartiles.
#To aquello que este 3 desviaciones standar mas, o menos, de la media.Es el 99%
#Por fuera de esto se lo podria considerar una anomalia


# Function to Detection Outlier on one-dimentional datasets.
def find_anomalies(df):
    #define a list to accumlate anomalies
    anomalies = []
    
    # Set upper and lower limit to 3 standard deviation
    data_std = np.std(df.PA_max)
    data_mean = np.mean(df.PA_max)
    anomaly_cut_off = data_std * 3
    
    lower_limit  = data_mean - anomaly_cut_off 
    upper_limit = data_mean + anomaly_cut_off
    #print(lower_limit)
    # Generate outliers
    for outlier in df.PA_max:
        if outlier > upper_limit or outlier < lower_limit:
            anomalies.append(outlier)
    return anomalies

r=find_anomalies(df)

#Obtengo como resultado 69 outliers

#Grafico con un box plot que presenta la misma idea 
sns.boxplot(data=df.PA_max)


#En esta grafica puedo encontrar lo que ya venia viendo y es que la media normal de presion
#aumenta a medida que sube la edad  y que hay varios outliers para cada edad
sns.boxplot(x=df.Rango_edad,y=df.PA_max)

"""
Grafica de violines - boxplots- scater - 
matriz de correlacion
"""



#Me permite ver graficamente donde estan distribuidas las edades en las presiones
sns.boxplot(x=df. Clas_pres,y=df.Edad )


#Puedo ver los outliers de presion segun la clasificacion de imc
sns.boxplot(x=df.Clas_imc,y=df.PA_max)


#Grafica de violines
sns.catplot(x = bins_edad, y =   df['PA_max'] , data =df, kind = "violin",  bw = 0.25, hue =df['Sexo'],split = True,  inner = "quartile") 



"""Matriz de correlacion de variables"""


correlation_mat = df.corr()

sns.heatmap(correlation_mat, annot = True)

plt.show()








