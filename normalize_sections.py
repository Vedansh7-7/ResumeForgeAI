from langchain_ollama import OllamaLLM

model = "llama3.2"

print("Connecting to local processor via LangChain and normalizing raw JD json...")

llm = OllamaLLM(model= model, temperature=0.3)

prompt = ""