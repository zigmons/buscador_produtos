import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

# driver = webdriver.Chrome()
#
# produto = 'iphone 12 64gb'
# termos_banidos = 'mini watch'
#
# preco_minimo = 3000
# preco_maximo = 7000

def busca_buscape(driver, produto, termos_banidos, preco_minimo, preco_maximo):
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_produto = produto.split(" ")
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)

    driver.get('https://www.buscape.com.br/')
    driver.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div/div/div[1]/input').send_keys(produto)
    driver.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div/div/div[1]/input').send_keys(Keys.ENTER)

    time.sleep(5)
    lista_resultados = driver.find_elements(By.CLASS_NAME, 'Cell_Content__fT5st')

    lista_ofertas = []

    for resultado in lista_resultados:
        preco = resultado.find_element(By.CLASS_NAME, 'CellPrice_MainValue__JXsj_').text
        nome = resultado.get_attribute('title')
        nome = nome.lower()
        link = resultado.get_attribute('href')

        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True

        tem_todos_termos_produtos = True
        for palavra in lista_termos_produto:
            if palavra not in nome:
                tem_todos_termos_produtos = False

        if not tem_termos_banidos  and tem_todos_termos_produtos:
            preco = preco.replace('R$', "").replace(" ", "").replace('.',"").replace(',', ".")
            preco= float(preco)
            if preco_minimo <= preco <= preco_maximo:
                lista_ofertas.append((nome, preco, link))

    return lista_ofertas
