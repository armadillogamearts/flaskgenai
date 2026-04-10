import os
import io
import base64
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# Configura a chave de API (Lembre-se de colocar GOOGLE_API_KEY na Vercel)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    prompt = request.form.get('descricao')
    
    try:
        # Usando o modelo que você testou no Playground
        model = genai.GenerativeModel('gemini-2.5-flash-image')
        
        # Solicitando explicitamente a geração da imagem
        response = model.generate_content(f"Gere uma imagem de: {prompt}")
        
        # Busca o arquivo de imagem (blob) dentro da resposta multimodal
        img_str = None
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                img_bytes = part.inline_data.data
                img_str = base64.b64encode(img_bytes).decode('utf-8')
                break
        
        if img_str:
            return render_template('index.html', imagem_b64=img_str, prompt=prompt)
        else:
            return render_template('index.html', erro="O modelo não retornou uma imagem. Tente ser mais descritivo.", prompt=prompt)

    except Exception as e:
        return render_template('index.html', erro=f"Erro técnico: {str(e)}", prompt=prompt)

if __name__ == "__main__":
    app.run()
