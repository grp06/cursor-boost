import os
import openai

def generate_cursorrules(snapshot):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that injects a user's system information and parses out the most important details. Only respond with the complete file contents, without any additional explanation or commentary."},
            {"role": "user", "content": f"You are a coding assistant optimizing text files for LLM-based applications. Using the following system snapshot, generate a text file that highlights the most relevant details for coding context. Only output the complete file contents, without explanations or extra text:\n\n{snapshot}"}
        ],
        temperature=1,
    )
    return response.choices[0].message.content
