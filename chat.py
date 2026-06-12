from dotenv import load_dotenv
load_dotenv()
# ChatGPT - Need paid API Token
# from langchain.chat_models import init_chat_model 
# model = init_chat_model('gpt-4.1')

# Gemini 2.5 Flash Lite - Free
# from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
# response = model.invoke('what is GenAI?')

# groq - Free
# from langchain.chat_models import init_chat_model
# model = init_chat_model('groq:openai/gpt-oss-120b')
# response = model.invoke('what is GenAI?')

# mistralai - Free
from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(model="mistral-small-2506",temperature=0.5,max_tokens=20)
response = model.invoke('tell me a joke about AI')

print(response.content)
