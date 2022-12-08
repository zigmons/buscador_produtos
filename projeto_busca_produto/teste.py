from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time




# #entrar no google e pesquisar
# produto = 'iphone 12 64gb'
# termos_banidos = 'mini watch'
#
# preco_minimo = 3000
# preco_maximo = 8000
driver = webdriver.Chrome()

tabela_produtos = pd.read_excel(r'E:\Python Aulas\Projeto Selenium\Arquivos\buscas.xlsx')

tabela_ofertas = pd.DataFrame()



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

lista_ofertas_google = busca_google_shopping(driver, produto, termos_banidos, preco_minimo, preco_maximo)

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


lista_ofertas_buscape = busca_buscape(driver, produto, termos_banidos, preco_minimo, preco_maximo)

for linha in tabela_produtos.index:
    produto = tabela_produtos.loc[:,'Nome']
    termos_banidos = tabela_produtos.loc[:,'Termos banidos']
    preco_minimo = tabela_produtos.loc[:,'Preço mínimo']
    preco_maximo = tabela_produtos.loc[:,'Preço máximo']

    lista_ofertas_google_shopping = busca_google_shopping(driver, produto, termos_banidos, preco_minimo, preco_maximo)
    if lista_ofertas_google_shopping:
        tabela_google_shopping = pd.DataFrame(lista_ofertas_google_shopping, columns=['produto', 'preço', 'link'])
    else:
        tabela_google_shopping = None

    lista_ofertas_buscape = busca_buscape(driver, produto, termos_banidos, preco_minimo, preco_maximo)
    if lista_ofertas_buscape:
        tabela_buscape = pd.DataFrame(lista_ofertas_buscape, columns=['produto', 'preço', 'link'])
    else:
        tabela_buscape = None