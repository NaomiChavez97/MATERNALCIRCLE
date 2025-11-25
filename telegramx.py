name: 🤖 Ejecutar Chatbot Groq

# 1. Define cuándo se ejecutará este workflow
on:
  # Permite ejecutar manualmente el workflow desde la interfaz de GitHub
  workflow_dispatch:
  
  # Ejecuta el bot en un horario programado
  # NOTA: El bot se reiniciará cada 5 minutos.
  schedule:
    # Ejecutar cada 5 minutos
    - cron: '*/5 * * * *' 

# Define los trabajos (jobs) que se ejecutarán
jobs:
  run_telegram_bot:
    runs-on: ubuntu-latest # Ejecutar en una máquina virtual Linux

    steps:
      # 1. Checkout del código
      - name: Checkout del repositorio
        uses: actions/checkout@v4

      # 2. Configurar Python
      - name: Configurar Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # 3. Instalar dependencias
      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install python-telegram-bot groq

      # 4. Ejecutar el script
      # Usamos variables de entorno (Secrets) para las claves
      - name: Ejecutar el script del Bot
        env:
          # Estas variables se leen desde GitHub Secrets
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        run: |
          # Asegúrate de que el nombre del archivo de tu bot sea 'maternidad_bot.py'
          python maternidad_bot.py
