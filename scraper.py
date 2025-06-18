# import requests
# from bs4 import BeautifulSoup
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
# }
#
# # Missing closing parenthesis here:
# page = requests.get('https://tienda.c41.com.ar/categoria-producto/film-y-laboratorio/film-35mm/negativo-color-35mm/', headers=headers)
# soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.title.text)
#
# rollos = []
# productos = soup.find_all('li', class_= 'product')
# for producto in productos:
#     h2 = producto.find('h2', class_= 'woocommerce-loop-product__title')
#     precio_tag = producto.find('span', class_= 'woocommerce-Price-amount')
#     link_tag = producto.find('a',class_= 'woocommerce-LoopProduct-link')
#
#     nombre = h2.text.strip() if h2 else 'Sin nombre'
#     precio = precio_tag.text.strip() if precio_tag else 'Sin precio'
#     link = link_tag['href'] if link_tag else 'Sin link'
#
#     rollos.append({'nombre': nombre, 'precio': precio, 'link': link})
#
# print(f"Se encontraron {len(rollos)} rollos 35 mm a color \n")
# for rollo in rollos:
#     print(f"Nombre: {rollo['nombre']}")
#     print(f"Precio: {rollo['precio']}")
#     print(f"Link: {rollo['link']}")
#     print('-' * 40)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # activá si no querés que se abra el navegador
driver = webdriver.Chrome(service=Service(), options=options)

base_url = 'https://tienda.c41.com.ar/categoria-producto/film-y-laboratorio/film-35mm/negativo-color-35mm/'
page_number = 1
rollos = []

while True:
    url = base_url + f'page/{page_number}/' if page_number > 1 else base_url
    print(f"Cargando página {page_number}: {url}")
    driver.get(url)
    time.sleep(2)

    # Scroll para cargar contenido dinámico
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    productos = soup.find_all('li', class_='product')

    if not productos:
        print("No se encontraron productos. Fin.")
        break

    for producto in productos:
        h2 = producto.find('h2', class_='woocommerce-loop-product__title')
        precio_tag = producto.find('span', class_='woocommerce-Price-amount')
        link_tag = producto.find('a', class_='woocommerce-LoopProduct-link')

        nombre = h2.text.strip() if h2 else 'Sin nombre'
        precio = precio_tag.text.strip() if precio_tag else 'Sin precio'
        link = link_tag['href'] if link_tag else 'Sin link'

        rollos.append({'nombre': nombre, 'precio': precio, 'link': link})

    # Verificamos si existe link a la próxima página
    next_page_url = f'/page/{page_number + 1}/'
    if not soup.find('a', href=lambda href: href and next_page_url in href):
        print("No hay más páginas.")
        break

    page_number += 1

driver.quit()

# Mostrar resultados
print(f"\nSe encontraron {len(rollos)} rollos negativos color 35mm:\n")
for rollo in rollos:
    print(f"Nombre: {rollo['nombre']}")
    print(f"Precio: {rollo['precio']}")
    print(f"Link: {rollo['link']}")
    print('-' * 40)