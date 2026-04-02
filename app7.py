import streamlit as st
import pandas as pd
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime


st.title("Evaluación Rápida de Vulnerabilidad Sísmica")

# -------------------------------------------------
# CARGAR CSV VS30
# -------------------------------------------------

@st.cache_data
def cargar_csv():
    return pd.read_csv("vs30_reducido.csv")

vs30_data = cargar_csv()

clasificacion_suelo = {
    0: "D", 1: "E", 2: "C", 3: "C",
    4: "D", 5: "D", 6: "B", 7: "C",
    8: "D", 9: "D", 10: "C", 11: "D",
    12: "D", 13: "D"
}

def obtener_suelo(lat, lon):
    try:
        vs30_data["dist"] = (vs30_data["lat"] - lat)**2 + (vs30_data["lon"] - lon)**2
        punto = vs30_data.loc[vs30_data["dist"].idxmin()]
        valor = int(punto["valor"])
        return clasificacion_suelo.get(valor, None)
    except:
        return None

# -------------------------------------------------
# TABLAS
# -------------------------------------------------

tablas = {

    # AUTOMÁTICAS
    "Cercha de acero AC/CE": {
        "DES": {"So": 2.9,"Suelo": {"B":0.8,"C":0.0,"D":-0.3,"E":-0.5},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
        "DMO": {"So": 3.1,"Suelo": {"B":0.5,"C":0.0,"D":-0.6,"E":-1.6},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
        "DMI": {"So": 1.7,"Suelo": {"B":1.2,"C":0.0,"D":-0.7,"E":-2.0},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
    },
        
    "Pórtico arristrado de acero AC/PA": {
        "DES": {"So": 1.8,"Suelo": {"B":0.8,"C":0.0,"D":-0.3,"E":-0.5},"Pisos": {"1-3":0.0,"+4":-0.5},"Smin": 0.8},
        "DMO": {"So": 1.6,"Suelo": {"B":0.4,"C":0.0,"D":-0.6,"E":-1.4},"Pisos": {"1-3":0.0,"+4":-0.6},"Smin": 0.8},
        "DMI": {"So": 0.8,"Suelo": {"B":1.2,"C":0.0,"D":-0.8,"E":-2.0},"Pisos": {"1-3":0.0,"+4":0.4},"Smin": 0.8}
    },
    
    "Pórtico resistente a momento de acero AC/PRM": {
        "DES": {"So": 2.3,"Suelo": {"B":0.7,"C":0.0,"D":-0.3,"E":-0.5},"Pisos": {"1-3":0.0,"+4":-0.3},"Smin": 0.8},
        "DMO": {"So": 2.7,"Suelo": {"B":0.4,"C":0.0,"D":-0.5,"E":-1.3},"Pisos": {"1-3":0.0,"+4":-0.9},"Smin": 0.8},
        "DMI": {"So": 2.6,"Suelo": {"B":1,"C":0.0,"D":-0.6,"E":-1.6},"Pisos": {"1-3":0.0,"+4":-0.4},"Smin": 0.8}
    },
    
    "Muros reforzados de concreto CR/MR": {
        "DES": {"So": 1.6,"Suelo": {"B":0.2,"C":0.0,"D":-0.2,"E":-0.3},"Pisos": {"1-3":0.0,"+4":-0.2},"Smin": 0.8},
        "DMO": {"So": 1.6,"Suelo": {"B":0.3,"C":0.0,"D":-0.3,"E":-0.8},"Pisos": {"1-3":0.0,"+4":0},"Smin": 0.8},
        "DMI": {"So": 1.4,"Suelo": {"B":0.2,"C":0.0,"D":-0.4,"E":-0.9},"Pisos": {"1-3":0.0,"+4":0},"Smin": 0.8}
    },
    
    "Pórtico resistente a momento de concreto CR/PMR": {
        "DES": {"So": 1.9,"Suelo": {"B":0.8,"C":0.0,"D":-0.4,"E":-1.3},"Pisos": {"1-3":0.0,"+4":0.2},"Smin": 0.8},
        "DMO": {"So": 1.9,"Suelo": {"B":1,"C":0.0,"D":-0.5,"E":-1.7},"Pisos": {"1-3":0.0,"+4":-0.3},"Smin": 0.8},
        "DMI": {"So": 2.7,"Suelo": {"B":1.2,"C":0.0,"D":-0.9,"E":-1.8},"Pisos": {"1-3":0.0,"+4":-0.3},"Smin": 0.8},
        "ND": {
            "Alta":{"So": -0.6,"Suelo": {"B":0.5,"C":0.0,"D":-0.8,"E":-0.4},"Pisos": {"1-3":0.0,"+4":0.54},"Smin": 0.8},
            "Intermedia":{"So": -0.3,"Suelo": {"B":0.6,"C":0.0,"D":-0.3,"E":-0.8},"Pisos": {"1-3":0.0,"+4":0.57},"Smin": 0.8},
            "Baja":{"So": 0.4,"Suelo": {"B":0.6,"C":0.0,"D":-0.4,"E":-0.9},"Pisos": {"1-3":0.0,"+4":0.8},"Smin": 0.8}
        }
    },
    
    # NO AUTOMÁTICAS
   "Muro confinado de masposteria de arcilla cocida MA/MC": {
        "DMO": {"Alta":{"So": 0.1,"Suelo": {"B":0.2,"C":0.0,"D":-0.2,"E":-0.4},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
                "Intermedia":{"So": 0.9,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-0.9},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
                "Baja":{"So": 1.5,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-1.2},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
             },
        
                      
    },
    
     "Muro reforzado de masposteria de arcilla cocida MA/MR": {
        "DMO": {"Alta":{"So": 1.3,"Suelo": {"B":0.2,"C":0.0,"D":-0.2,"E":-0.4},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
                "Intermedia":{"So": 2.1,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-1.0},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
                "Baja":{"So": 2.8,"Suelo": {"B":0.3,"C":0.0,"D":-0.5,"E":-1.3},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
             },
                            
    },
     
     "Muro reforzado de madera MD/MR": {
        "DU": {"Alta":{"So": 1.4,"Suelo": {"B":0.3,"C":0.0,"D":-0.3,"E":-0.5},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Intermedia":{"So": 2.4,"Suelo": {"B":0.4,"C":0.0,"D":-0.5,"E":-1.2},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Baja":{"So": 3.2,"Suelo": {"B":0.4,"C":0.0,"D":-0.6,"E":-1.6},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
               
             },
        
                      
    },
     
     "Portico resistente a momento + mampostería de concreto CR/PRMM": {
        "DU": {"Alta":{"So": 0.4,"Suelo": {"B":0.6,"C":0.0,"D":-0.2,"E":-0.4},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Intermedia":{"So": 1.1,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-0.9},"Pisos": {"1-3":0.0,"+4":-0.3},"Smin": 0.8},
               "Baja":{"So": 1.8,"Suelo": {"B":0.7,"C":0.0,"D":-0.5,"E":-1.2},"Pisos": {"1-3":0.0,"+4":0.2},"Smin": 0.8}
             },
        
        "ND": {"Alta":{"So": -0.4,"Suelo": {"B":0.7,"C":0.0,"D":-0.2,"E":-0.4},"Pisos": {"1-3":0.0,"+4":-0.1},"Smin": 0.8},
               "Intermedia":{"So": 0.4,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-1.0},"Pisos": {"1-3":0.0,"+4":-0.6},"Smin": 0.8},
               "Baja":{"So": 1.2,"Suelo": {"B":0.8,"C":0.0,"D":-0.5,"E":-1.3},"Pisos": {"1-3":0.0,"+4":-0.1},"Smin": 0.8}
             },
        
      
        
                   
    },
     
     "Muro no reforzado de madera MD/MNR": {
               
        "ND": {"Alta":{"So": 0.3,"Suelo": {"B":0.3,"C":0.0,"D":-0.3,"E":-0.6},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Intermedia":{"So": 1.4,"Suelo": {"B":0.4,"C":0.0,"D":-0.5,"E":-1.3},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Baja":{"So": 2.3,"Suelo": {"B":0.4,"C":0.0,"D":-0.6,"E":-1.7},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
             },
        
                     
    },
     
      "Muro no reforzado de mamposteria de arcilla cocida MA/MNR": {
               
        "ND": {"Alta":{"So": -0.5,"Suelo": {"B":0.2,"C":0.0,"D":-0.2,"E":-0.4},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Intermedia":{"So": 0.3,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-1.0},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Baja":{"So": 1.0,"Suelo": {"B":0.3,"C":0.0,"D":-0.5,"E":-1.3},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
               
             },
        
                      
    },
      
      "Muro no reforzado de adobe AD/MNR": {
               
        "ND": {"Alta":{"So": -0.5,"Suelo": {"B":0.2,"C":0.0,"D":-0.2,"E":-0.4},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Intermedia":{"So": 0.3,"Suelo": {"B":0.3,"C":0.0,"D":-0.4,"E":-1.0},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Baja":{"So": 1.0,"Suelo": {"B":0.3,"C":0.0,"D":-0.5,"E":-1.3},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
             },
        
                      
    },
      
      "Muro no reforzado de bareque BQ/MNR": {
               
        "ND": {"Alta":{"So": 0.1,"Suelo": {"B":0.3,"C":0.0,"D":-0.3,"E":-0.5},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Intermedia":{"So": 1.2,"Suelo": {"B":0.4,"C":0.0,"D":-0.5,"E":-1.2},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8},
               "Baja":{"So": 2.0,"Suelo": {"B":0.4,"C":0.0,"D":-0.6,"E":-1.6},"Pisos": {"1-3":0.0,"+4":0.0},"Smin": 0.8}
             },
                
    },

  
}

# -------------------------------------------------
# TIPOS AUTOMÁTICOS
# -------------------------------------------------

tipologias_automaticas = [
    "Cercha de acero AC/CE",
    "Pórtico arristrado de acero AC/PA",
    "Pórtico resistente a momento de acero AC/PRM",
    "Muros reforzados de concreto CR/MR",
    "Pórtico resistente a momento de concreto CR/PMR",
    "Sistema combinado de concreto CR/SC"
]

# -------------------------------------------------
# GEOLOCALIZACIÓN
# -------------------------------------------------

st.subheader("Geolocalización")

location = streamlit_geolocation()

suelo_detectado = None
lat = None
lon = None

if location and location["latitude"] is not None:
    lat = location["latitude"]
    lon = location["longitude"]

    st.success(f"Ubicación detectada: {lat:.5f}, {lon:.5f}")

    suelo_detectado = obtener_suelo(lat, lon)

    if suelo_detectado:
        st.info(f"Tipo de suelo detectado: {suelo_detectado}")
    else:
        st.warning("No se pudo determinar el tipo de suelo.")

# -------------------------------------------------
# ENTRADAS
# -------------------------------------------------

tipologia = st.selectbox("Tipología estructural", list(tablas.keys()))
zona = st.selectbox("Nivel de amenaza sísmica", ["Alta", "Intermedia", "Baja"])

niveles_disponibles = list(tablas[tipologia].keys())

# -------------------------------------------------
# LÓGICA MODIFICADA
# -------------------------------------------------

if tipologia in tipologias_automaticas:

    if "ND" in niveles_disponibles:
        modo = st.selectbox("Modo de evaluación", ["Automático (DES/DMO/DMI)", "No dúctil (ND)"])

        if modo == "Automático (DES/DMO/DMI)":
            if zona == "Alta":
                nivel = "DES"
            elif zona == "Intermedia":
                nivel = "DMO"
            else:
                nivel = "DMI"

            st.info(f"Nivel asignado automáticamente: {nivel}")

        else:
            nivel = "ND"
            st.warning("Modo ND activado: se usará la zona seleccionada")

    else:
        if zona == "Alta":
            nivel = "DES"
        elif zona == "Intermedia":
            nivel = "DMO"
        else:
            nivel = "DMI"

        st.info(f"Nivel asignado automáticamente: {nivel}")

else:
    nivel = st.selectbox("Nivel de disipación", niveles_disponibles)

# -------------------------------------------------
# SUELO Y PISOS
# -------------------------------------------------

if suelo_detectado:
    suelo = suelo_detectado
else:
    suelo = st.selectbox("Tipo de suelo", ["B", "C", "D", "E"])

pisos = st.number_input("Número de pisos", 1, 50, 1)

# -------------------------------------------------
# SESIÓN
# -------------------------------------------------

if "evaluaciones" not in st.session_state:
    st.session_state.evaluaciones = []

# -------------------------------------------------
# CÁLCULO
# -------------------------------------------------

if st.button("Calcular y Guardar Evaluación"):

    if nivel == "ND":
        datos = tablas[tipologia][nivel][zona]
    elif tipologia in tipologias_automaticas:
        datos = tablas[tipologia][nivel]
    else:
        datos = tablas[tipologia][nivel][zona]

    So = datos["So"]
    Ms = datos["Suelo"][suelo]

    if pisos <= 3:
        Mp = datos["Pisos"]["1-3"]
    else:
        Mp = datos["Pisos"]["+4"]

    Smin = datos["Smin"]

    Score = So + Ms + Mp

    st.subheader("Resultados")

    st.write("So:", So)
    st.write("Ms:", Ms)
    st.write("Mp:", Mp)

    st.success(f"Score: {round(Score,2)}")
    st.write("Smin:", Smin)

    if Score < Smin:
        estado = "Requiere evaluación detallada"
        st.error(estado)
    else:
        estado = "No requiere evaluación detallada"
        st.success(estado)

    st.session_state.evaluaciones.append({
        "Fecha": datetime.now().strftime("%Y-%m-%d"),
        "Latitud": lat,
        "Longitud": lon,
        "Tipología": tipologia,
        "Zona": zona,
        "Nivel": nivel,
        "Suelo": suelo,
        "Pisos": pisos,
        "So": So,
        "Ms": Ms,
        "Mp": Mp,
        "Score": round(Score,2),
        "Smin": Smin,
        "Resultado": estado
    })

# -------------------------------------------------
# HISTORIAL
# -------------------------------------------------

if len(st.session_state.evaluaciones) > 0:

    st.subheader("📋 Historial de Evaluaciones")

    df = pd.DataFrame(st.session_state.evaluaciones)
    st.dataframe(df)

    archivo = "evaluaciones_vulnerabilidad.xlsx"
    df.to_excel(archivo, index=False)

    with open(archivo, "rb") as f:
        st.download_button(
            "📥 Descargar Excel",
            f,
            file_name="evaluaciones_vulnerabilidad.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )