# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:55:17 2024

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

# Función para simular el crecimiento de las cuentas y predecir el futuro
def simular_crecimiento(df):
    '''
    Simula y predice el crecimiento de las cuentas de AFORE por estado a lo largo de varios años.
    '''
    anios_pasados = 5  # Años de datos pasados disponibles
    anios_futuros = 3  # Años a proyectar hacia el futuro
    tasas_crecimiento_pasadas = np.random.uniform(0.01, 0.05, size=len(df))
    tasas_crecimiento_futuras = np.random.uniform(0.01, 0.05, size=len(df))  # Tasas de crecimiento futuro
    
    datos_simulacion = []
    
    # Simular crecimiento pasado
    for i in range(anios_pasados):
        cuentas_anio = df["Cuentas Iniciales"] * (1 + tasas_crecimiento_pasadas) ** (i + 1)
        datos_simulacion.append(cuentas_anio)
    
    # Predecir crecimiento futuro
    for i in range(anios_futuros):
        cuentas_anio = datos_simulacion[-1] * (1 + tasas_crecimiento_futuras)  # Usamos la última tasa de crecimiento simulada
        datos_simulacion.append(cuentas_anio)
    
    df_simulacion = pd.DataFrame(datos_simulacion).transpose()
    df_simulacion.columns = ["Año {}".format(i + 1) for i in range(anios_pasados + anios_futuros)]
    df_simulacion.index = df["Estado"]
    
    return df_simulacion

# Función para graficar el crecimiento de las cuentas con interactividad
def graficar_crecimiento_interactivo(df_simulacion, estados_seleccionados):
    '''
    Grafica el crecimiento proyectado de las cuentas de AFORE por estado a lo largo de varios años.
    Permite seleccionar qué estados graficar de manera interactiva.
    '''
    plt.figure(figsize=(12, 8))
    for estado in estados_seleccionados:
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
    st.sidebar.markdown('En esta aplicación, simulamos y proyectamos el crecimiento de cuentas de AFORE por estado utilizando un modelo de crecimiento exponencial.')
    st.sidebar.markdown('### Detalles de la Simulación:')
    st.sidebar.markdown('- **Generación de Datos Iniciales:** Se generan nombres de estados y cuentas iniciales aleatorias para representar la situación inicial.')
    st.sidebar.markdown('- **Simulación de Crecimiento:** Utilizamos tasas de crecimiento aleatorias para simular el crecimiento pasado y predecir el crecimiento futuro de las cuentas.')
    st.sidebar.markdown('- **Representación Gráfica:** Mostramos gráficamente el crecimiento proyectado de las cuentas para los estados seleccionados por el usuario.')
    st.sidebar.markdown('- **Mapa de Google Maps:** Se incluye un mapa interactivo de Google Maps para visualizar la ubicación geográfica de interés.')

# Ejecución principal en Streamlit
def main():
    st.title("Simulación y Proyección de Crecimiento de Cuentas de AFORE por Estado")
    
    # Mostrar ayuda en el sidebar
    mostrar_ayuda()
    
    # Generar y mostrar datos iniciales
    df_inicial = generar_datos_iniciales()
    st.subheader("Datos iniciales:")
    st.write(df_inicial)
    
    # Simular y graficar el crecimiento de las cuentas
    df_simulacion = simular_crecimiento(df_inicial)
    st.subheader("Simulación y Proyección de crecimiento del número de cuentas (en miles):")
    st.write(df_simulacion.reset_index().rename(columns={'index': 'Estado'}))  # Mostrar DataFrame con nombres de estados
    
    # Obtener la lista de estados para la interactividad
    estados_disponibles = df_simulacion.index.tolist()
    
    # Permitir al usuario seleccionar los estados a graficar
    estados_seleccionados = st.multiselect('Selecciona estados para graficar:', estados_disponibles, default=estados_disponibles[:5])
    
    # Graficar el crecimiento de los estados seleccionados
    st.subheader("Gráfico de Crecimiento:")
    if estados_seleccionados:
        plt = graficar_crecimiento_interactivo(df_simulacion, estados_seleccionados)
        st.pyplot(plt)
    else:
        st.warning('Por favor selecciona al menos un estado para graficar.')
    
    # Mostrar el mapa de Google Maps
    st.subheader("Mapa de Google Maps:")
    mostrar_mapa()

if __name__ == "__main__":
    main()