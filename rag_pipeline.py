from langchain_community.llms import Ollama

def generate_answer(context, query):
    llm = Ollama(model="mistral")

    prompt = f"""
    Answer based only on context:

    Context:
    {context}

    Question:
    {query}
    """

    return llm.invoke(prompt)