# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 10:29:48 2021

@author: nahue
"""


"""Importaciones"""

import numpy as np
import pandas as pd
import re #modulo regex

#Librerias graficas
import matplotlib.pyplot as plt 
import plotly.express as px
from plotly.offline import plot 


import seaborn as sns


'Recuperacion de informacion'

Tabla_info_completa=pd.read_csv("HNP\HNP_StatsSeries.csv") #Levanto el archivo con la informacion de los datos
#Tabla_info_completa.info()


#Expresion regular para buscar los indices correctos ya que 'SP.HCI.OVRL','SP.GNP.PCAP.CD' no devuelven nada
regex1 = "GNP.PCAP.CD$"
for linea in df_Completo["Indicator Code"]:
    res = re.findall(regex1, linea)
    if res:
        print(linea)

# 'NY.GNP.PCAP.CD' resultado



regex2 = "HCI.OVRL$"
for linea in df_Completo["Indicator Code"]:
    res = re.findall(regex2, linea)
    if res:
        print(linea)

# "HD.HCI.OVRL"  resultado 


'Imprimo informacion de que significa cada uno de los indices'


#Creo el filtro en el que le pido que me considere solo esos 4 indicadores para todo el df
filtro=Tabla_info_completa["Series Code"] .isin(['SP.DYN.CBRT.IN','SP.DYN.LE00.IN','HD.HCI.OVRL','NY.GNP.PCAP.CD'])


#Genero el df filtrado con los indicadores
Tabla_info= Tabla_info_completa[filtro]
Tabla_info.info()

with open('info_indicadores.txt', 'w') as archivo:
    
        
    for linea in Tabla_info['Series Code' ]:          
            archivo.write( ' # Codigo:' + linea )
            archivo.write('\n')

    
    for linea in Tabla_info['Indicator Name' ]:          
            archivo.write( ' - Nombre:' + linea )
            archivo.write('\n')

    
    for linea in Tabla_info['Long definition']:
            archivo.write('* DEF: ' + linea )
            archivo.write('\n')

    for linea in Tabla_info['Topic']:
            archivo.write('+ Topico: ' + linea )
            archivo.write('\n')




"""Carga de los datos"""

df_Completo=pd.read_csv("HNP\HNP_StatsData.csv") #Levanto el archivo con los datos a usar
#df_Completo.info()
#df.head()
#df.describe(include="all")


'Arreglo de los datos completos'

df_Completo=df_Completo.drop(['Unnamed: 65'], axis=1) #Elimino la ultima columna que se crea debido a la ultima coma en los datos. 



'Filtrado de datos completos por paises e indicadores'


#Filro para indicadores 

filtro= df_Completo["Indicator Code"] .isin(['SP.DYN.CBRT.IN','SP.DYN.LE00.IN','HD.HCI.OVRL','NY.GNP.PCAP.CD'])
                    
df_Ind = df_Completo [filtro]




'Aplico un melt para hacer un reshape del df'

#Creo una variable donde tomo las columnas dadas como fechas 

x=df_Ind.columns[4:]

#Realizo el melt

df_Ind= pd.melt(df_Ind, id_vars =['Country Name','Country Code' ,'Indicator Code'], value_vars =x,var_name ='Año', value_name ='Indicator Value')
#Los datos quedador organizados por nombre, luego cada uno de los indicadores, acomodados por la secuencia de años





#Paso la columna año a dato del tipo numerico

df_Ind['Año'] = df_Ind['Año'].astype(str).astype(int)


                    

#Creo el filtro en el que le pido que me considere solo estos 3 paises para todo el df
filtro=df_Ind["Country Code"] .isin(['VEN', 'ARG', 'CUB'] )

#Genero el df filtrado
df_VAC = df_Ind[filtro] 
df_VAC.reset_index(drop=True, inplace=True)




#Creo el filtro en el que le pido que me considere solo estos paises para todo el df
filtro=df_Ind["Country Code"] .isin(['IRN','IRQ','SYR', 'AFG','PAK','SAU'] )


#Genero el df filtrado 
df_Med_Or = df_Ind[filtro]
df_Med_Or.reset_index(drop=True, inplace=True)


#Creo el filtro en el que le pido que me considere solo estos 3 paises para todo el df
filtro=df_Ind["Country Code"] .isin(['USA','CAN','DEU','CHE','CHN','JPN','ZAF','EGY','AUS','NZL'] )


#Genero el df filtrado 
df_Potencias = df_Ind[filtro]
df_Potencias.reset_index(drop=True, inplace=True)



#Elimino el df completo para que no quede ocupando RAM y utilizo el filtrado
del df_Completo 

del df_Ind #tambien el de los indices


'DF para graficar'

#Indicador GNI

filtro= df_Potencias["Indicator Code"] .isin(['NY.GNP.PCAP.CD'])
df_Potencias2 = df_Potencias[filtro]


filtro= df_VAC["Indicator Code"] .isin(['NY.GNP.PCAP.CD'])
df_VAC2 = df_VAC[filtro]


filtro= df_Med_Or["Indicator Code"] .isin(['NY.GNP.PCAP.CD'])
df_Med_Or2 = df_Med_Or[filtro]



#Indicador de TASA DE NACIMIENTO PER CAPITA'

filtro= df_Med_Or["Indicator Code"] .isin(['SP.DYN.CBRT.IN'])
df_Med_Or3 = df_Med_Or[filtro]


filtro= df_Potencias["Indicator Code"] .isin(['SP.DYN.CBRT.IN'])
df_Potencias3 = df_Potencias[filtro]


filtro= df_VAC["Indicator Code"] .isin(['SP.DYN.CBRT.IN'])
df_VAC3 = df_VAC[filtro]


#Indicador de expectativa de vida


filtro= df_VAC["Indicator Code"] .isin(['SP.DYN.LE00.IN'])
df_VAC4 = df_VAC[filtro]



filtro= df_Med_Or["Indicator Code"] .isin(['SP.DYN.LE00.IN'])
df_Med_Or4 = df_Med_Or[filtro]



filtro= df_Potencias["Indicator Code"] .isin(['SP.DYN.LE00.IN'])
df_Potencias4 = df_Potencias[filtro]


#dfs concatenados

df_concat=pd.concat([df_Potencias2,df_VAC2,df_Med_Or2],ignore_index=True, sort = False, axis=0)


df_concat2=pd.concat([df_Potencias4,df_VAC4,df_Med_Or4],ignore_index=True, sort = False, axis=0)






"""   Graficos   """



'Evoluciones del gni'


#Grafico de evolucion del GNI en las diferentes potencias

fig01=px.line(df_Potencias2, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Evolucion del GNI")

plot(fig01)
    

'Podemos ver en estos paises una estabilidad constante, ademas de una tendencia al crecimiento'
'Tambien es interesante ver como todos los paises tuvieron en la epoca del 2000 una caida en sus GNI y luego un fuerte repunte'






####





fig02=px.line(df_VAC2, 
        x="Año", 
        y="Indicator Value", 
        color="Country Code", 
        title="Evolucion del GNI")

plot(fig02)

'Claramente vemos una inestabilidad, hay grandes oscilaciones'
'Podemos ver la misma caida y repunte que en los otros paises'
'Si analizamos la historia podemos ver como la bonanza de ciertos paises ademas se correlaciono con ciertas medidas politicas del socialismo'




#####





fig03=px.line(df_Med_Or2, 
        x="Año", 
        y="Indicator Value", 
        color="Country Code", 
        title="Evolucion del GNI")

plot(fig03)

'A partir del año 2002, como en los otros podemos ver un aumento en Arabia, esto debido al precio del petroleo. Es algo que se repite en el resto'
'Podemos ver como luego'





######


'Indicador de tasa de nacimiento per capita'

#######


fig04=px.line(df_Med_Or3, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Tasa de nacimiento")

plot(fig04)






#####







fig05=px.line(df_Potencias3, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Tasa de nacimiento")
plot(fig05)



####






fig06=px.line(df_VAC3, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Tasa de nacimiento")
plot(fig06)







'Con la expectativa de vida'
#####





fig07=px.line(df_VAC4, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Expectativa de vida")
plot(fig07)







####





fig08=px.line(df_Med_Or4, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Expectativa de vida")
plot(fig08)




#####


fig09=px.line(df_Potencias4, 
        x="Año", 
        y="Indicator Value", 
        color="Country Name", 
        title="Expectativa de vida")
plot(fig09)




######

'Subplot'

#Creo un subplot entre el gni y la expectativa de vida



fig, axes = plt.subplots(2, 1)
sns.lineplot(ax=axes[0],  x="Año",  y="Indicator Value" ,data= df_Potencias4,hue='Country Code')
sns.lineplot(ax=axes[1],  x="Año",  y="Indicator Value" ,data= df_Potencias2,hue='Country Code')
axes[0].set_title('GNI')
axes[1].set_title('Exp de vida')
fig.suptitle('GNI vs Expectativa de vida') #Acomodar esto


#####


fig, axes = plt.subplots(2, 1)
sns.lineplot(ax=axes[0],  x="Año",  y="Indicator Value" ,data= df_VAC4,hue='Country Code')
sns.lineplot(ax=axes[1],  x="Año",  y="Indicator Value" ,data= df_VAC2,hue='Country Code')
axes[0].set_title('GNI')
axes[1].set_title('Exp de vida')
fig.suptitle('GNI vs Expectativa de vida')




######


fig, axes = plt.subplots(2, 1)
sns.lineplot(ax=axes[0],  x="Año",  y="Indicator Value" ,data= df_Med_Or4,hue='Country Code')
sns.lineplot(ax=axes[1],  x="Año",  y="Indicator Value" ,data= df_Med_Or2,hue='Country Code')
axes[0].set_title('GNI')
axes[1].set_title('Exp de vida')
fig.suptitle('GNI vs Expectativa de vida')



#####
"Mapa del gni en los paises desarrollados de cada continente"

fig1=px.choropleth(df_Potencias2, locations= 'Country Code', color= "Indicator Value", hover_name= 'Country Name',
                  color_continuous_scale=px.colors.sequential.Plasma,
                  animation_frame='Año',
                  labels= 'Country Name',
                  scope = 'world')
      
fig1.update_layout(
    height=700,
    title_text='GNI per capita')
plot(fig1)



#######

'Mapa del mundo con la exp de vida en medio oriente'

fig2=px.choropleth(df_Med_Or4, locations= 'Country Code', color= "Indicator Value", hover_name= 'Country Name',
                  color_continuous_scale=px.colors.sequential.Plasma,
                  animation_frame='Año',
                  labels= {'Indicator value': 'Años de vida' },
                  scope = 'world',
                  template="plotly_dark")

fig2.update_layout(
    height=700,
    title_text='Expectativa de vida en Medio Oriente')
plot(fig2)





######

'Mapa mundial que muestra en todos los paises la evolucion del gni'


fig3=px.choropleth(df_concat, locations= 'Country Code', color= "Indicator Value", hover_name= 'Country Name',
                  color_continuous_scale=px.colors.sequential.Plasma,
                  animation_frame='Año',
                  labels= {'Indicator value': 'Años de vida' },
                  scope = 'world',
                  template="plotly_dark")

fig3.update_layout(
    height=700,
    title_text='GNI en el mundo')
plot(fig3)





#######


'Mapa mundial donde podemos ver la exp de vida de todos'



fig4=px.choropleth(df_concat2, locations= 'Country Code', color= "Indicator Value", hover_name= 'Country Name',
                  color_continuous_scale=px.colors.sequential.Plasma,
                  animation_frame='Año',
                  labels= {'Indicator value': 'Años de vida' },
                  scope = 'world',
                  template="plotly_dark")

fig4.update_layout(
    height=700,
    title_text='Esperanza de vida')
plot(fig4) 
