import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    ContextTypes, 
    filters
)

# 🚨 Importar la biblioteca de Groq
from groq import Groq
import os # Importar para una gestión más segura de claves (opcional)

# ====================================================================
# === 🚨 CONFIGURACIÓN - DEBES REEMPLAZAR ESTAS CLAVES ===
# ====================================================================

# Token de tu bot de Telegram
TOKEN = "8557944150:AAG7awDLV0sJlMABVq6o1RHMdVuZbbFPH04" 

# Clave API de Groq
# Recomendación: Si quieres más seguridad, puedes obtener la clave de una variable de entorno:
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_KEY = "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"

# Nombre del modelo de Groq que quieres usar (rápido y eficiente)
GROQ_MODEL = "llama-3.3-70b-versatile" 

# Inicializar el cliente de Groq
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Error al inicializar Groq client: {e}")
    # Puedes salir del programa si la clave es inválida
    # exit() 

# ====================================================================
# === CONFIGURACIÓN BASE Y PROMPT DE SISTEMA ===
# ====================================================================

# Definición del 'System Prompt' para darle contexto y personalidad al chatbot
SYSTEM_PROMPT = (
    "Eres una IA de acompañamiento físico y emocional para madres en etapas de embarazo, "
    "parto, posparto y crianza. Responde de forma cálida, empática y clara, con un tono "
    "cercano y de apoyo. Tu principal objetivo es brindar consuelo e información general. "
    "IMPORTANTE: Siempre prioriza la seguridad. Si el usuario pregunta sobre síntomas médicos "
    "urgentes o necesita un diagnóstico, debes responder con firmeza que NO eres un médico "
    "y que DEBEN consultar inmediatamente a un profesional de la salud o acudir a urgencias."
)

# Configuración de Logging para ver si algo falla
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====================================================================
# === LÓGICA DE GROQ ===
# ====================================================================

def generar_respuesta_con_groq(prompt: str) -> str:
    """
    Envía el mensaje del usuario a la API de Groq y devuelve la respuesta generada.
    """
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
            temperature=0.7, # Controla la creatividad (0.0 es más determinista)
        )
        # Extraer el contenido del mensaje de respuesta
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error al conectar con Groq: {e}")
        return "Disculpa, hubo un problema al conectar con el asistente de inteligencia artificial. Inténtalo de nuevo más tarde."

# ====================================================================
# === MANEJADORES DE TELEGRAM (HANDLERS) ===
# ====================================================================

# Handler para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start."""
    saludo_inicial = generar_respuesta_con_groq("Dame un saludo cálido y empático para una madre que inicia el chat, e indícale que estás aquí para apoyarla en su maternidad.")
    await update.message.reply_text(saludo_inicial)

# Handler principal para mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa el mensaje del usuario usando la IA de Groq."""
    
    texto_usuario = update.message.text
    
    # Mostrar el indicador de "escribiendo..." mientras Groq procesa
    await update.message.reply_chat_action("typing") 
    
    # Generar la respuesta usando Groq
    respuesta_bot = generar_respuesta_con_groq(texto_usuario)
    
    # Enviar la respuesta de vuelta a Telegram
    await update.message.reply_text(respuesta_bot)

# Handler para errores
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Registra los errores causados por Updates."""
    logger.warning('Update "%s" causó error "%s"', update, context.error)
    # Respuesta amigable en caso de error
    if update:
        await update.message.reply_text("Lo siento, ocurrió un error inesperado. Por favor, inténtalo de nuevo.")

# ====================================================================
# === BUCLE PRINCIPAL (MAIN) ===
# ====================================================================

def main():
    """Ejecuta el bot."""
    
    # 1. Crear la aplicación y pasarle el token
    application = ApplicationBuilder().token(TOKEN).build()

    # 2. Definir y añadir los Handlers (Manejadores)
    
    # Comando /start
    application.add_handler(CommandHandler("start", start))
    
    # Cualquier otro mensaje de texto (filtra comandos)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Manejo de errores
    application.add_error_handler(error_handler)

    # 3. Iniciar el Polling (El bot empieza a escuchar mensajes)
    print("Bot iniciado. Esperando mensajes en Telegram...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
