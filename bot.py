import os
import google.generativeai as genai
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy KurtGol IA ⚽ Pregúntame lo que quieras de fútbol")

async def buscar_google(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SEARCH_API_KEY}"
    res = requests.get(url).json()
    return res.get("organic_results", [])[:3]

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text
    resultados = await buscar_google(pregunta)
    contexto = "\n".join([r["snippet"] for r in resultados])
    prompt = f"Con esta info: {contexto}. Responde como KurtGol IA experto en fútbol: {pregunta}"
    respuesta = model.generate_content(prompt)
    await update.message.reply_text(respuesta.text)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
print("KurtGol IA encendido...")
app.run_polling()
