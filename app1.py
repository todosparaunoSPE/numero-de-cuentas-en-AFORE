# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:42:53 2024

@author: jperezr
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Función para generar los datos iniciales
def generar_datos_iniciales():
    '''
    Genera un DataFrame inicial con nombres de estados mexicanos y cuentas iniciales aleatorias.
    '''
    nombres_estados = [
        "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", 
        "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", 
        "Colima", "Durango", "Guanajuato", "Guerrero", 
        "Hidalgo", "Jalisco", "México", "Michoacán", 
        "Morelos", "Nayarit", "Nuevo León", "Oaxaca", 
        "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", 
        "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", 
        "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
    ]
    
    cuentas_iniciales = np.random.randint(50000, 500000, size=len(nombres_estados))
    
    df = pd.DataFrame({
        "Estado": nombres_estados,
        "Cuentas Iniciales": cuentas_iniciales
    })
    
    return df

# Función para simular el crecimiento de las cuentas
def simular_crecimiento(df):
    '''
    Simula el crecimiento exponencial de las cuentas de AFORE por estado a lo largo de varios años.
    '''
    anios = 5
    tasas_crecimiento = np.random.uniform(0.01, 0.05, size=len(df))
    
    datos_simulacion = []
    
    for i in range(anios):
        cuentas_anio = df["Cuentas Iniciales"] * (1 + tasas_crecimiento) ** (i + 1)
        datos_simulacion.append(cuentas_anio)
    
    df_simulacion = pd.DataFrame(datos_simulacion).transpose()
    df_simulacion.columns = ["Año {}".format(i + 1) for i in range(anios)]
    df_simulacion.index = df["Estado"]
    
    return df_simulacion

# Función para graficar el crecimiento de las cuentas
def graficar_crecimiento(df_simulacion):
    '''
    Grafica el crecimiento proyectado de las cuentas de AFORE por estado a lo largo de varios años.
    '''
    plt.figure(figsize=(12, 8))
    for estado in df_simulacion.index[:5]:  # Graficamos solo los primeros 5 estados para mayor claridad
        plt.plot(df_simulacion.columns, df_simulacion.loc[estado], label=estado)
    
    plt.xlabel('Año')
    plt.ylabel('Número de Cuentas')
    plt.title('Simulación de Crecimiento del Número de Cuentas en los Estados')
    plt.legend()
    
    return plt

# Función para mostrar el mapa de Google Maps
def mostrar_mapa():
    '''
    Muestra un mapa de Google Maps incrustado en la aplicación.
    '''
    iframe_html = '''
        <div style="display: flex; justify-content: center;">
        <iframe width="800" height="550" src="https://www.google.com/maps/d/embed?mid=1ga6pN3K6aBmrT9Bt37TkjoKERP5PI8E" frameborder="0" allowfullscreen></iframe>
        </div>
    '''
    
    st.markdown(iframe_html, unsafe_allow_html=True)

# Función para mostrar la ayuda en el sidebar
def mostrar_ayuda():
    '''
    Muestra la explicación sobre el tipo de crecimiento utilizado en la simulación en el sidebar.
    '''
    st.sidebar.title('Ayuda')
    st.sidebar.markdown('En esta aplicación, simulamos el crecimiento de cuentas de AFORE por estado utilizando un modelo de crecimiento exponencial.')
    st.sidebar.markdown('### Detalles de la Simulación:')
    st.sidebar.markdown('- **Generación de Datos Iniciales:** Se generan nombres de estados y cuentas iniciales aleatorias para representar la situación inicial.')
    st.sidebar.markdown('- **Simulación de Crecimiento:** Utilizamos tasas de crecimiento aleatorias para proyectar cómo podría evolucionar el número de cuentas a lo largo de varios años.')
    st.sidebar.markdown('- **Representación Gráfica:** Mostramos gráficamente el crecimiento proyectado de las cuentas para los primeros 5 estados.')
    st.sidebar.markdown('- **Mapa de Google Maps:** Se incluye un mapa interactivo de Google Maps para visualizar la ubicación geográfica de interés.')
    #st.sidebar.markdown('Para más detalles, contáctenos.')

# Ejecución principal en Streamlit
def main():
    st.title("Simulación de Crecimiento de Cuentas de AFORE por Estado")
    
    # Mostrar ayuda en el sidebar
    mostrar_ayuda()
    
    # Generar y mostrar datos iniciales
    df_inicial = generar_datos_iniciales()
    st.subheader("Datos iniciales:")
    st.write(df_inicial)
    
    # Simular y graficar el crecimiento de las cuentas
    df_simulacion = simular_crecimiento(df_inicial)
    st.subheader("Simulación de crecimiento del número de cuentas (en miles):")
    st.write(df_simulacion.reset_index().rename(columns={'index': 'Estado'}))  # Mostrar DataFrame con nombres de estados
    
    # Graficar el crecimiento
    st.subheader("Gráfico de Crecimiento:")
    plt = graficar_crecimiento(df_simulacion)
    st.pyplot(plt)
    
    # Mostrar el mapa de Google Maps
    st.subheader("Mapa de Google Maps:")
    mostrar_mapa()

if __name__ == "__main__":
    main()