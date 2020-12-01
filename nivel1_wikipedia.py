import requests
from lxml import html


# Encabezados : Quien hace los requerimientos o como se está haciendo el requerimiento
# "user-agent" con esta variable se identefica el navegador y el sistema operativo del cliente.
encabezados = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

}
# La semilla  por donde voy a empezar.

url = "https://www.wikipedia.org/"

# Hacer mi requerimiento.

respuesta = requests.get(url, headers=encabezados)

# Transforma la información en string.

parseador = html.fromstring(respuesta.text)

idiomas = parseador.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
for idioma in idiomas:
    print(idioma)


idiomas = parseador.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())
