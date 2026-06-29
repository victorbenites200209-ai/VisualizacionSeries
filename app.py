import streamlit as st
import pandas as pd
import numpy as np

st.title("Evolución y Tendencia de Ventas")

# 1. Entrada de datos
entrada = st.text_input("Ingrese la serie histórica, separada por comas:", value="10,15,18,26,31")

if entrada.strip():
    try:
        # Limpieza y conversión de datos históricos
        elementos = [i.strip() for i in entrada.split(",") if i.strip()]
        historico = [float(i) for i in elementos]
        n_historico = len(historico)
        
        if n_historico < 2:
            st.warning("⚠️ Por favor, ingresa al menos 2 datos para poder calcular una tendencia.")
        else:
            # 2. Configuración de los períodos (X)
            horizonte_futuro = 6
            total_periodos = n_historico + horizonte_futuro
            
            x_historico = np.arange(n_historico)
            x_total = np.arange(total_periodos)
            
            # 3. Cálculo de la Línea de Tendencia (Regresión Lineal: y = mx + b)
            m, b = np.polyfit(x_historico, historico, 1)
            
            # Calculamos la tendencia para todo el horizonte, pero luego la segmentaremos
            tendencia_completa = m * x_total + b
            
            # 4. Segmentación para que la tendencia SOLO se vea en el futuro
            # Rellenamos el histórico con None, excepto el ÚLTIMO punto histórico 
            # para que la línea de tendencia se conecte visualmente con las ventas reales.
            tendencia_futura = [None] * (n_historico - 1) + list(tendencia_completa[n_historico - 1:])
            
            # Las ventas reales llevan None en los 6 períodos futuros
            ventas_reales = list(historico) + [None] * horizonte_futuro
            
            # 5. Aplicando tu cambio en los índices (1, 2, 3...)
            indices = [i+1 for i in x_total]
            
            # 6. Construcción del DataFrame para graficar
            df_grafico = pd.DataFrame({
                "Ventas Reales": ventas_reales,
                "Proyección Tendencia": tendencia_futura
            }, index=indices)
            
            # 7. Renderizado del gráfico y resultados
            st.line_chart(df_grafico)
            
            # Extra: Mostrar la predicción del último período futuro
            st.info(f"📈 Según la tendencia, la venta estimada para el período **{indices[-1]}** es de **{tendencia_completa[-1]:.2f}**")
            
    except ValueError:
        st.error("❌ Por favor, asegúrate de ingresar solo números separados por comas.")
else:
    st.warning("⚠️ El campo no puede estar vacío.")



