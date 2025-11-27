import os
import tweepy
from datetime import date

# 1. Configuración de Autenticación
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_secret = os.environ.get("ACCESS_SECRET")

def obtener_proximo_evento():
    hoy = date.today()
    anio = hoy.year

    # LISTA DE EVENTOS
    lista_eventos = [
        {"mes": 1, "dia": 1, "nombre": "AnoNuevo"},
        {"mes": 1, "dia": 6, "nombre": "Reyes"},
        {"mes": 2, "dia": 14, "nombre": "SanValentin"},
        {"mes": 6, "dia": 21, "nombre": "Verano"},
        {"mes": 10, "dia": 31, "nombre": "Halloween"},
        {"mes": 12, "dia": 25, "nombre": "Navidad"}
    ]

    evento_mas_cercano = None
    dias_minimos = 9999

    for evento in lista_eventos:
        # Fecha del evento en el año actual
        fecha_evento = date(anio, evento["mes"], evento["dia"])
        
        # Si ya pasó hoy, miramos la fecha del año siguiente
        if fecha_evento < hoy:
            fecha_evento = date(anio + 1, evento["mes"], evento["dia"])
        
        dias_faltantes = (fecha_evento - hoy).days
        
        # Nos quedamos con el evento que esté más cerca
        if dias_faltantes < dias_minimos:
            dias_minimos = dias_faltantes
            evento_mas_cercano = evento

    return evento_mas_cercano, dias_minimos

def construir_mensaje(evento, dias):
    nombre = evento["nombre"]
    
    # --- MENSAJES PERSONALIZADOS ---
    
    # 1. DÍA DE REYES 👑 (6 Enero)
    if nombre == "Reyes":
        if dias == 0: return "¡ES HOY! ¡FELIZ DIA DE REYES A TODOS! 👑"
        elif dias == 1: return "¡Mañana es día de Reyes! 🫅🏻"
        else: return f"¡Faltan {dias} días para el Día de Reyes! 👑"

    # 2. SAN VALENTÍN 💘 (14 Febrero)
    elif nombre == "SanValentin":
        if dias == 0: return "¡ES HOY! ¡FELIZ SAN VALENTIN! 💘"
        elif dias == 1: return "¡Falta 1 para San Valentín! ¡ES MAÑANA! 💘"
        else: return f"¡Faltan {dias} días para San Valentín! 💘"

    # 3. VERANO 🏖️ (21 Junio)
    elif nombre == "Verano":
        if dias == 0: return "¡ES HOY! ¡OFICIALMENTE ES VERANO! ¿Que planes tienes para este VERANO? 👀"
        elif dias == 1: return "¡Falta 1 para el Verano! 👀 YA ES MAÑANA 🌊"
        else: return f"¡Faltan {dias} días para Verano! 🏖️"

    # 4. HALLOWEEN 🎃 (31 Octubre)
    elif nombre == "Halloween":
        if dias == 0: return "¡ES HOY! ¡FELIZ HALLOWEEN! 🎃🕷️"
        elif dias == 1: return "¡Falta 1 para Halloween! ¡ES MAÑANA! ¿De que te vas a disfrazar?"
        else: return f"¡Faltan {dias} días para Halloween! 🎃"

    # 5. NAVIDAD 🎄 (25 Diciembre)
    elif nombre == "Navidad":
        if dias == 0: return "¡ES HOY! ¡FELIZ NAVIDAD! 🍾🎉🎁"
        elif dias == 1: return "¡Falta 1 para NAVIDAD! ¡MAÑANA ES NAVIDAD!"
        else: return f"¡Faltan {dias} días para Navidad! 🎄"

    # 6. AÑO NUEVO 🍾 (1 Enero)
    elif nombre == "AnoNuevo":
        if dias == 0: return "¡FELIZ AÑO NUEVO! 🍇🍾"
        elif dias == 1: return "¡Falta 1 día para Año Nuevo! ¡ES MAÑANA! 🍾"
        else: return f"¡Faltan {dias} días para Año Nuevo! 🍾🍇"

    return None

def publicar_tweet():
    hoy = date.today()
    
    # --- FRENO DE MANO ---
    # El bot no tuiteará nada hasta llegar a esta fecha.
    # Configurado para: 2 de Enero de 2026
    fecha_inicio = date(2026, 1, 2)
    
    if hoy < fecha_inicio:
        print(f"Hoy es {hoy}. El bot está en espera hasta el {fecha_inicio}. A mimir 😴.")
        return
    # ---------------------

    evento, dias = obtener_proximo_evento()
    mensaje = construir_mensaje(evento, dias)
    
    print(f"Evento detectado: {evento['nombre']}")
    print(f"Mensaje: {mensaje}")

    # Verificar llaves
    if not api_key:
        print("No se encontraron las llaves (Secrets).")
        return

    # Conectar a Twitter
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )
    
    try:
        client.create_tweet(text=mensaje)
        print("¡Tweet enviado con éxito!")
    except Exception as e:
        print(f"Error al publicar: {e}")
        raise e

if __name__ == "__main__":
    publicar_tweet()


