# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 16:45:34 2021

@author: nahuel lahoz
"""

"""
Importaciones
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

"""
codigo
"""
# Cargo los datos
df=pd.read_csv("WPP2019_TotalPopulationBySex.csv")
df.head()
df.info()



#VarID y Variant
#La pregunta que surge es: ¿Son "Sinónimos"? 
#Esto quiere decir que, cada vez que aparece un determinado valor para VarID aparece un único valor para Variant? 
#¿O es que existen combinaciones?? ¿Qué conclusiones podemos sacar de lo que observemos?

unicos_Variant = len(df['Variant'].unique())
unicos_VarID = len(df['VarID'].unique())
combinacion = len((df['VarID'].apply(str) + df['Variant']).unique())
if unicos_Variant == combinacion and unicos_VarID == combinacion:
    print('Los dos campos se relacionans.')
    

# genero una matriz de correlacion y puedo ver que tan relacionadas estan

correlation_mat = df.corr()

sns.heatmap(correlation_mat, annot = True)

plt.show()

    
"""
Si la longitud en terminos de valores únicos en la columna Variant es igual a la de Variant concatenada con VarID 
y la longitud de Variant concatenada a VarID es igual a la de VarID,
por propiedad de transitividad, 
los valores de Variant tienen la misma longitud que los de VarID por lo que confirmamos que están relacionados.
"""





#¿Cuáles son los países que aparecen en el DataSet? ¿Son sólo países?

df[(df.LocID < 900)].Location.unique()


"""
Al revisar la columna Location vemos que hay otra que la "acompaña", es su indicador,
esta es la columna de LocID, la cual va en forma ascendente hasta el 900 indicando todos nombres de paises.
Luego ya no.
Ergo, filtramos por la columna LocID menor a 900, y le pedimos las Locaciones de forma única.
"""






#¿Qué Locaciones no tienen discriminada su población (total o parcialmente) entre varones y mujeres?

df[(df[["PopFemale","PopMale"]]).isnull().any(1)].Location.unique()

"""
Agarro el df, tómo las columnas de PopMale y PopFemale; le pido que me dé todas las filas vacias de estas col.
Y ahora le digo que de estas filas vacias me diga a que paises pertenecen sin repetirmelos
"""
 


   
# ¿Los datos de población total son coherentes con el desagregado de masculinos y femeninos?

#¿Qué países tienen datos faltantes?

df[df.isnull().any(1)].Location.unique()

"""
Pido los nulos en el df a traves del metodo y le digo que de la fila que encuentre
me devuelva las locaciones sin repetirlas
"""




#¿Cuál es la tasa de crecimiento poblacional anual media para todos los países en el intervalo 2000-2020? (*) 
#Entendemos como "Tasa de crecimiento poblacional" al porcentaje en que crece (o decrece) la población de un año respecto del anterior.

df["TasaCrecimiento"]=(df.PopTotal/df.PopTotal.shift(1)) 
'Nueva col. donde calculo la tasa de crecimiento p todo el dataset'

df_tasa=df[(df.Variant == "Medium")&(df.LocID < 900)&(df.Time >=2000)&(df.Time <= 2020)].reset_index().drop("index", axis=1)[["Location", "Time","PopTotal","TasaCrecimiento"]]
'Creo un nuevo df donde Filtro segun los intereses de lo que busco. Muestro segun pais y año la polacion total y su tasa de crecimiento'

df_tasa_group=df_tasa.groupby("Location", as_index=False)["TasaCrecimiento"].mean()
'Agrupo el anterior df por su Location y me devuelve el promedio de su tasa de crecimiento en los años establecidos'


#¿Cuáles son los 10 países que tienen mayor tasa de crecimiento poblacional anual media en ese periodo? 
df_tasa_group.sort_values(by="TasaCrecimiento", ascending=False).head(10)


#¿Y los que tienen la menor? 
df_tasa_group.sort_values(by="TasaCrecimiento", ascending=False).tail(10)



#Tener en cuenta algunos controles de integridad, 
#Si la suma de población actual (2020) para todos los países y una misma categoría les da algo parecido a lo que todos sabemos es la población mundial actual.

# La población mundial en la actualidad 2020 es de 7.8 billones

df_poblacion_total= df.loc[df["Location"]== "World"]# Buscamos la variable world 
df_poblacion_total= df_poblacion_total.loc[df_poblacion_total["Time"]== 2020] # En el año 2020
df_poblacion_total.loc[df_poblacion_total["Variant"] == "Medium"].PopTotal*1000 # Tomamos el valor  a partir de la varaible medium y multiplicamos por mil














