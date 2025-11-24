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

# --- Importar la biblioteca de Groq ---
from groq import Groq

# ====================================================================
# === 🚨 CONFIGURACIÓN - DEBES REEMPLAZAR ESTAS CLAVES MANUALMENTE 🚨 ===
# ====================================================================

# 1. Token de tu bot de Telegram
TOKEN = "REEMPLAZA_ESTO_CON_TU_TOKEN_DE_TELEGRAM" 

# 2. Clave API de Groq
GROQ_API_KEY = "REEMPLAZA_ESTO_CON_TU_CLAVE_API_DE_GROQ"

# Nombre del modelo de Groq (rápido y eficiente)
GROQ_MODEL = "llama3-8b-8192" 

# Inicializar el cliente de Groq
groq_client = None
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    # Esto atraparía un error de formato de clave si se asigna directamente
    print(f"Error al inicializar Groq client: {e}")
    print("Por favor, verifica que tu GROQ_API_KEY es correcta.")


# ====================================================================
# === CONFIGURACIÓN BASE Y PROMPT DE SISTEMA ===
# ====================================================================

SYSTEM_PROMPT = (
    "Eres una IA de acompañamiento físico y emocional para madres en etapas de embarazo, "
    "parto, posparto y crianza. Responde de forma cálida, empática y clara, con un tono "
    "cercano y de apoyo. Tu principal objetivo es brindar consuelo e información general. "
    "IMPORTANTE: Siempre prioriza la seguridad. Si el usuario pregunta sobre síntomas médicos "
    "urgentes o necesita un diagnóstico, debes responder con firmeza que NO eres un médico "
    "y que DEBEN consultar inmediatamente a un profesional de la salud o acudir a urgencias."
)

# Configuración de Logging
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
    if not groq_client:
        return "Error: El cliente de Groq no se inicializó. Revisa la clave API."
    
    try:
        # Llamada a la API de Groq
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            model=GROQ_MODEL,
            temperature=0.7, 
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error al conectar con Groq: {e}")
        # En caso de error de conexión o API, damos una respuesta de fallback
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
    
    # Mostrar el indicador de "escribiendo..."
    await update.message.reply_chat_action("typing") 
    
    # Generar la respuesta usando Groq
    respuesta_bot = generar_respuesta_con_groq(texto_usuario)
    
    # Enviar la respuesta de vuelta a Telegram
    await update.message.reply_text(respuesta_bot)

# Handler para errores
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Registra los errores causados por Updates."""
    logger.warning('Update "%s" causó error "%s"', update, context.error)
    if update.effective_message:
        await update.effective_message.reply_text("Lo siento, ocurrió un error inesperado al procesar tu solicitud.")

# ====================================================================
# === BUCLE PRINCIPAL (MAIN) ===
# ====================================================================

def main():
    """Ejecuta el bot."""
    
    # Verificación de claves críticas al inicio
    if TOKEN == "REEMPLAZA_ESTO_CON_TU_TOKEN_DE_TELEGRAM" or GROQ_API_KEY == "REEMPLAZA_ESTO_CON_TU_CLAVE_API_DE_GROQ":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: POR FAVOR, REEMPLAZA TOKEN Y GROQ_API_KEY EN EL CÓDIGO !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return

    # 1. Crear la aplicación y pasarle el token
    application = ApplicationBuilder().token(TOKEN).build()

    # 2. Definir y añadir los Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # 3. Iniciar el Polling (El bot escucha mensajes)
    print("Bot de Telegram iniciado.")
    print(f"Modelo Groq: {GROQ_MODEL}")
    print("El bot está ahora en modo Polling. No cierres esta ventana.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
