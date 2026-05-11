import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler

#Configuracion de la pagina principal
st.set_page_config(page_title="Centro de Inteligencia Shinobi", layout="wide")



#Carga de datos y cache
@st.cache_data
def cargar_pergaminos():
    df = pd.read_csv("tarea_ud7_proyectofinal_AdrianBuenavida/players_data.csv")
    return df


df_base = cargar_pergaminos()



#Preprocesamiento y normalizacion
metricas_rendimiento = ['Goles', 'Asistencias', 'Pases_%', 'Regates', 'xG', 'Recuperaciones']



#Normalizamos los datos de 0 a 1 para el algoritmo
scaler = MinMaxScaler()
df_norm = df_base.copy()
df_norm[metricas_rendimiento] = scaler.fit_transform(df_base[metricas_rendimiento])



#Interfaz del sidebar
st.sidebar.title("Panel de Control")
st.sidebar.markdown("Define los parametros de la mision:")



#objetivo principal
objetivo_nombre = st.sidebar.selectbox("Selecciona Perfil Objetivo:", df_base['Nombre'].unique())


#Filtros de restriccion usando sliders
st.sidebar.markdown("### Restricciones del Sustituto")
max_valor = st.sidebar.slider("Limite de Coste (M):", 0, int(df_base['Valor_Mercado'].max()), 100)



#Especializacion1 
max_edad = st.sidebar.slider("Edad Maxima (Rastreo de Cantera):", 16, 40, 40)



#imilitud con distancia euclidiana de scipy
vector_objetivo = df_norm[df_norm['Nombre'] == objetivo_nombre][metricas_rendimiento].values[0]



#Filtramos la base de datos de candidatos
df_candidatos = df_norm[(df_norm['Nombre'] != objetivo_nombre) & 
                        (df_norm['Valor_Mercado'] <= max_valor) & 
                        (df_norm['Edad'] <= max_edad)].copy()




#Calculamos la distancia para cada fila
def calcular_similitud(row):
    vector_candidato = row[metricas_rendimiento].values
    return distance.euclidean(vector_objetivo, vector_candidato)



if not df_candidatos.empty:
    df_candidatos['Distancia'] = df_candidatos.apply(calcular_similitud, axis=1)
    
    
    #Ordenamos de menor a mayor distancia
    top_5 = df_candidatos.sort_values(by='Distancia').head(5)
    
    
    
    #Recuper datos originales sin normalizar
    top_5_reales = df_base.loc[top_5.index].copy()
    top_5_reales['Similitud (Distancia)'] = top_5['Distancia']


#Area principal ---->  st.columns
st.title("Centro de Mando: Analisis de Similitud")



#Mostramos KPIs del objetivo
st.markdown(f"### Analisis de Activo Principal: **{objetivo_nombre}**")
info_obj = df_base[df_base['Nombre'] == objetivo_nombre].iloc[0]



#organizamos los datos
col1, col2, col3, col4 = st.columns(4)
col1.metric("Equipo", info_obj['Equipo'])
col2.metric("Edad", f"{info_obj['Edad']} anos")
col3.metric("Valor de Mercado", f"{info_obj['Valor_Mercado']} M")
col4.metric("Potencial", info_obj['Potencial'])



st.divider()



if df_candidatos.empty:
    st.warning("No hay candidatos que cumplan con las restricciones establecidas.")
else:
    col_radar, col_tabla = st.columns([1, 1])

    with col_radar:
        st.markdown("#### Radar de Inteligencia")
        mejor_clon = top_5_reales.iloc[0]
        
        #Grafico de radar comparando objetivo y mejor clon
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=vector_objetivo,
            theta=metricas_rendimiento,
            fill='toself',
            name=objetivo_nombre
        ))
        
        vector_clon = top_5[top_5['Nombre'] == mejor_clon['Nombre']][metricas_rendimiento].values[0]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=vector_clon,
            theta=metricas_rendimiento,
            fill='toself',
            name=mejor_clon['Nombre']
        ))
        
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_tabla:
        st.markdown("#### Top 5 Clones Estadisticos")
        
        
        #Mostramos resultados 
        st.dataframe(top_5_reales[['Nombre', 'Edad', 'Valor_Mercado', 'Potencial', 'Similitud (Distancia)']], hide_index=True)


    st.divider()



    #Especializacion2 ---> Mapa de influencia
    st.markdown("#### Mapa de Influencia Tactico")
    st.markdown("Comparativa de las zonas de operacion (Coordenadas X, Y) entre el objetivo y los candidatos.")
    
    
    
    #Preparamos datos para el mapa
    df_mapa = pd.concat([df_base[df_base['Nombre'] == objetivo_nombre], top_5_reales])
    df_mapa['Tipo'] = ['Objetivo'] + ['Candidato'] * len(top_5_reales)
    
    

    
    #Grafico espacial
    fig_mapa = px.scatter(df_mapa, x='Coord_X_Media', y='Coord_Y_Media', 
                          color='Tipo', text='Nombre', size='Edad',
                          title="Distribucion en el Campo de Batalla")
    fig_mapa.update_traces(textposition='top center')
    
    st.plotly_chart(fig_mapa, use_container_width=True)
