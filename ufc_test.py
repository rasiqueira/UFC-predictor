# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:34:24 2020

@author: Rodrigo
"""

import pandas as pd
import sqlite3
import streamlit as st
import pickle
import numpy as np

conn = sqlite3.connect('ufc.db')
cursor = conn.cursor()
# lendo os dados
cursor.execute("""
                                   SELECT * FROM fighters order by name;"""
                                  )
df = pd.DataFrame(cursor.fetchall())
df.replace('', np.nan, inplace=True)
df.dropna(inplace=True)
cat = tuple(df[6].unique().tolist())
conn.close()
st.title('UFC MMA Predictor')
st.header('Acurácia do modelo atual: 71.2%')
st.subheader('Corner vermelho (Favorito)')
option_cat1 = st.selectbox('Qual a categoria do lutador do corner vermelho?',
   cat)

lut = tuple(df[0][df[6]==option_cat1].tolist())
option_lut1 = st.selectbox('Qual o lutador do corner vermelho?',
   lut)

st.subheader('Corner azul (Desafiante)')
cat2 = tuple(df[6].unique().tolist())
option_cat2 = st.selectbox('Qual a categoria do lutador do corner azul?',
   cat2)

lut2 = tuple(df[0][df[6]==option_cat2].tolist())

option_lut2 = st.selectbox('Qual o lutador do corner azul?',
   lut2)



st.write('Aperte o botão calcule para saber as probabilidade de cada lutador vencer a luta:')
if st.button('Calcule'):
    if option_lut1==option_lut2:
        st.write('Selecione lutadores diferentes')
    else:
        arr = []
        lut1 = df.loc[df[0].isin([option_lut1])]
        lut2 = df.loc[df[0].isin([option_lut2])]
        for i in range(1,6):
            if float(lut1[i])>float(lut2[i]):
                arr.append(1)
            else:
                arr.append(0)
        arr.append(1)
        filename = 'site_prob.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        resultado = loaded_model.predict_proba(np.array(arr).reshape(1, -1))
        st.write('A chance de '+option_lut1+' vencer a luta é de '+str(round(100*resultado[0][0],1))+'%')
        st.write('A chance de '+option_lut2+' vencer a luta é de '+str(round(100*resultado[0][1],1))+'%')

st.markdown('**Disclaimer**: use este aplicativo com responsabilidade e, ao usá-lo, não nos responsabilizamos por quaisquer perdas causadas pelas decisões decorrentes desse uso.')

st.subheader('Guia de usuario')
st.markdown('''Este aplicativo conta com vários crawlers que são executados *diariamente*.
Portanto, os dados são atualizados todos os dias e os dados mais recentes sobre 
lutadores e lutas estão disponíveis imediatamente.
O modelo de previsão é sempre treinado contando com todo o histórico do UFC, capturando, 
portanto, qualquer mudança de tendência nos dados.''')

st.subheader('Selecione a categoria e o lutador')
st.markdown('Se quiser fazer uma aposta **você assume o risco** mas espero que você ganhe algum dinheiro :sunglasses:')
