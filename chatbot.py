from dotenv import load_dotenv
load_dotenv()

# mistralai - Free
from langchain_mistralai import ChatMistralAI

from langchain_core.messages import AIMessage , SystemMessage , HumanMessage 

print('Choose AI Mode')
print('Press 1 for Data Science')
print('Press 2 for Full Stack with java')
print('Press 3 for Ethical Hacking')

choice = int(input('Whats Your Mood to Learn Today ?'))

if choice==1:
    mode = 'You are a Data Science AI help to teach , explain and clear the concepts'
elif choice==2:
    mode = 'You are a Full Stack Java AI help to teach , explain and clear the concepts'
elif choice==3:
    mode = 'You are a Ethical Hacking AI help to teach , explain and clear the concepts'

model = ChatMistralAI(model="mistral-small-2506",temperature=0.5)

history = [
    SystemMessage(content=mode)
]

print('---------------------------- Welcome ! , type 0 to exit ----------------------------')
while True:
    prompt = input('You :')
    history.append(HumanMessage(content=prompt))
    if prompt == '0':
        break

    response = model.invoke(history)
    history.append(AIMessage(content=response.content))
    print('Chat_Bot :',response.content)

print(history)