from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

#criar navegador
# driver = webdriver.Chrome()
#
# #importar BD
# # tabela_produtos = pd.read_excel(r'E:\Python Aulas\Projeto Selenium\Arquivos\buscas.xlsx')
#
# #entrar no google e pesquisar
# produto = 'iphone 12 64gb'
# termos_banidos = 'mini watch'
#
# preco_minimo = 3000
# preco_maximo = 8000

def busca_google_shopping(driver, produto, termos_banidos, preco_minimo, preco_maximo):
    driver.get('https://www.google.com/')
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_produto = produto.split(" ")
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)
    driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(produto)
    driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    elementos = driver.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for item in elementos:
        if 'Shopping' in item.text:
            item.click()
            break

    time.sleep(5)

    lista_resultados = driver.find_elements(By.CLASS_NAME, 'i0X6df')
    lista_ofertas = []

    for resultado in lista_resultados:

        nome = resultado.find_element(By.CLASS_NAME, 'Xjkr3b').text
        nome = nome.lower()
        link = resultado.find_element(By.CLASS_NAME, 'eaGTj').get_attribute('href')

        #verificação do nome
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True

        tem_todos_termos_produtos = True
        for palavra in lista_termos_produto:
            if palavra not in nome:
                tem_todos_termos_produtos = False

        if not tem_termos_banidos  and tem_todos_termos_produtos:
            preco = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
            preco = preco.replace('R$', "").replace(" ", "").replace('.',"").replace(',', ".")
            preco= float(preco)

            if preco_minimo <= preco <= preco_maximo:
                lista_ofertas.append((nome, preco, link))

    return lista_ofertas


