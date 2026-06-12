from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

llm = HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V4-Pro"
)

model = ChatHuggingFace(llm=llm)

response = model.invoke('What is Artificial Intelligence?')

print(response.content)
