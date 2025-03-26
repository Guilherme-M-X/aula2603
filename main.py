from flask import Flask, request
import cv2
import os
import numpy as np

app = Flask(__name__)

PASTA_UPLOADS = 'static/uploads'
os.makedirs(PASTA_UPLOADS, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def principal():
    if request.method == 'POST':
        arquivo = request.files.get('imagem')

        if arquivo and arquivo.filename != '':
            # imagem original
            caminho_original = os.path.join(PASTA_UPLOADS, 'original.jpg')
            arquivo.save(caminho_original)

            # Processar imagem
            imagem = cv2.imread(caminho_original)
            efeito = request.form.get('efeito', '')

            if efeito == 'cinza':
                imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)
            elif efeito == 'blur':
                imagem = cv2.blur(imagem, (5, 5))
            elif efeito == 'limiar':
                cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
                _, imagem = cv2.threshold(cinza, 127, 255, cv2.THRESH_BINARY)
                imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)
            elif efeito == 'erosao':
                kernel = np.ones((5, 5), np.uint8)
                imagem = cv2.erode(imagem, kernel, iterations=1)
            elif efeito == 'opening':
                kernel = np.ones((5, 5), np.uint8)
                imagem = cv2.morphologyEx(imagem, cv2.MORPH_OPEN, kernel)


            # Salvar image
            caminho_processada = os.path.join(PASTA_UPLOADS, 'processada.jpg')
            cv2.imwrite(caminho_processada, imagem)

            return f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Resultado</title>
                    <style>
                        body {{font-family: Arial, sans-serif; margin: 20px;}}
                        img {{max-width: 500px; margin: 10px; border: 1px solid #ddd;}}
                        .container {{display: flex; flex-wrap: wrap;}}
                        .image-box {{margin: 10px;}}
                    </style>
                </head>
                <body>
                    <h1>Imagem Processada</h1>
                    <div class="container">
                        <div class="image-box">
                            <h2>Original</h2>
                            <img src="/static/uploads/original.jpg">
                        </div>
                        <div class="image-box">
                            <h2>Processada</h2>
                            <img src="/static/uploads/processada.jpg">
                        </div>
                    </div>
                    <br><br>
                    <a href="/">Voltar</a>
                </body>
                </html>
            '''

    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inicial</title>
            <style>
                body {font-family: Arial, sans-serif; margin: 20px;}
                form {display: flex; flex-direction: column; max-width: 400px;}
                input, select, button {margin: 10px 0; padding: 8px;}
                button {background-color: #ff0000; color: white; border: none; cursor: pointer;}
            </style>
        </head>
        <body>
            <h1>Inicio</h1>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="imagem" required>
                <select name="efeito">
                    <option value="cinza">Cinza</option>
                    <option value="blur">Blur</option>
                    <option value="limiar">Binarização</option>
                    <option value="erosao">Erosão</option>
                    <option value="opening">Opening</option>
                </select>
                <button type="submit">Processar</button>
            </form>
        </body>
        </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)