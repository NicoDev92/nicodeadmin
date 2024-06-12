import random
from datetime import datetime

def user_info(request):
    
    if request.user.is_authenticated:
        nombre = request.user.first_name
        apellido = request.user.last_name
        
        
        return {
            'usuario_nombre': nombre,
            'usuario_apellido': apellido,
        }
    else:
        return {}

def saludo_aleatorio(request):
    if request.user.is_authenticated:
        
        saludos = {
            "morning": "Buenos días",
            "afternoon": "Buenas tardes",
            "evening": "Buenas noches",
        }
        
        quotes = [
            "Espero que estés bien.",
            "¿Cómo estás?",
            "Espero que estés bien y tengas un gran día.",
            "Me alegra que estés aquí.",
            "Espero que disfrutes tu dia.",
            "Es un placer recibirte nuevamente.",
            "Estoy feliz de tenerte aquí.",
            "¿Cómo te encuentras?",
            "Qué alegría verte por aquí.",
            "Estoy aquí para ayudarte en lo que necesites.",
            "¿Cómo puedo ayudarte hoy?",
            "Estoy para servirte!",
            "Si necesitas algo, aquí estoy.",
            "Eestoy encantado de verte.",
            "Estoy contento de ser de ayuda.",
            "Estoy aquí para ayudarte.",
            "Qué gusto tenerte por aquí.",
            "Es un placer trabajar juntos.",
            "Estoy aquí para hacer tu trabajo más agradable."
        ]
        quote = random.choice(quotes)
        
        anio = datetime.now().year
        
        current_hour = datetime.now().hour
        if current_hour < 12:
            saludo = saludos["morning"]
        elif 12 <= current_hour < 18:
            saludo = saludos["afternoon"]
        else:
            saludo = saludos["evening"]
        
        return {
            'frase': quote,
            'saludo' : saludo,
            'anio' : anio
        }
    else:
        return {}
