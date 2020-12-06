import requests
from bs4 import BeautifulSoup


encabezados = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

url = "https://stackoverflow.com/questions"

respuesta = requests.get(url, headers=encabezados)

soup = BeautifulSoup(respuesta.text)

contenedor_de_preguntas = soup.find( id="questions")
lista_de_preguntas = contenedor_de_preguntas.find_all('div', class_="question-summary")

for pregunta in lista_de_preguntas:
    texto_pregunta = pregunta.find('h3').text
    descripcion_pregunta = pregunta.find(class_='excerpt').text
    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r', '').strip()
    print(texto_pregunta)
    print(descripcion_pregunta)

    print()
