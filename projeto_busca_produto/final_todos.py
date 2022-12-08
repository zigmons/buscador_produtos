from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from projeto_google import busca_google_shopping
from projeto_buscape import busca_buscape

driver = webdriver.Chrome()

tabela_produtos = pd.read_excel(r'E:\Python Aulas\Projeto Selenium\Arquivos\buscas.xlsx')

tabela_ofertas = pd.DataFrame()
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

    print(tabela_google_shopping)
    print(tabela_buscape)
    break
