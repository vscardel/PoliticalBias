from bs4 import BeautifulSoup
import time
from selenium import webdriver
from random import seed
from random import randint
import sys
import re

def get_cartaCapital(driver,soup_pag_principal,fp,iteracoes):
	artigos = soup_pag_principal.find_all('article')
	iteracoes = iteracoes + len(artigos)
	for artigo in artigos:
		try:
			link_artigo = artigo.find('a')
			print('carregando artigo ' + str(link_artigo.get('href')))
			driver.get(str(link_artigo.get('href')))
			html_artigo = driver.page_source
			soup_artigo = BeautifulSoup(html_artigo,'html.parser')
			content = soup_artigo.find('div',class_ = 'eltdf-post-text')
			text = ''
			for i in content.find_all('p'):
				text = text + str(i.get_text())
			print('escrevendo artigo')
			fp.write('{ ' + text + '}\n' )
		except:
			print('erro ao tentar escrever artigo')
	return iteracoes

def get_forum(driver,soup_pag_principal,fp,iteracoes):
	artigos = soup_pag_principal.find_all('h4',class_='media-heading')
	iteracoes = iteracoes + len(artigos)
	for artigo in artigos:
		try:
			link_artigo = artigo.find('a')
			print('carregando artigo ' + str(link_artigo.get('href')))
			driver.get(str(link_artigo.get('href')))
			html_artigo = driver.page_source
			soup_artigo = BeautifulSoup(html_artigo,'html.parser')
			content = soup_artigo.find('div',class_='text')
			text = ''
			for i in content.find_all('p'):
				text = text + str(i.get_text())
			print('escrevendo artigo')
			fp.write('{ ' + text + '}\n' )
		except:
			print('erro ao tentar escrever artigo')
	return iteracoes

def get_247(driver,soup_pag_principal,fp,iteracoes):
	artigos = soup_pag_principal.find_all('h3',class_="articleGrid__headline")
	iteracoes = iteracoes + len(artigos)
	for artigo in artigos:
		try:
			link_artigo = artigo.find('a')
			print('carregando artigo ' + str(link_artigo.get('href')))
			driver.get(str(link_artigo.get('href')))
			html_artigo = driver.page_source
			soup_artigo = BeautifulSoup(html_artigo,'html.parser')
			content = soup_artigo.find('article')
			text = ''
			for i in content.find_all('p'):
				text = text + str(i.get_text())
			print('escrevendo artigo')
			fp.write('{ ' + text + '}\n' )
		except:
			print('erro ao tentar escrever artigo')
	return iteracoes

def get_antagonista(driver,soup_pag_principal,fp,iteracoes):
	artigos = soup_pag_principal.find_all('article')
	iteracoes = iteracoes + len(artigos)
	for artigo in artigos:
		try:
			link_artigo = artigo.find('a',class_='article_link')
			print('carregando artigo ' + str(link_artigo.get('href')))
			driver.get(str(link_artigo.get('href')))
			html_artigo = driver.page_source
			soup_artigo = BeautifulSoup(html_artigo,'html.parser')
			content = soup_artigo.find('div',class_='entry-content')
			text = ''
			for i in content.find_all('p'):
				text = text + str(i.get_text())
			print('escrevendo artigo')
			fp.write('{ ' + text + '}\n' )
		except:
			print('erro ao tentar escrever artigo')
	return iteracoes

def get_istoe(driver,soup_pag_principal,fp,iteracoes):
	artigos = soup_pag_principal.find_all('article',class_='thumb')
	iteracoes = iteracoes + len(artigos)
	for artigo in artigos:
		try:
			link_artigo = artigo.find('a')
			print('carregando artigo ' + str(link_artigo.get('href')))
			driver.get(str(link_artigo.get('href')))
			html_artigo = driver.page_source
			soup_artigo = BeautifulSoup(html_artigo,'html.parser')
			content = soup_artigo.find('div',class_='content-section content')
			text = ''
			for i in content.find_all('p'):
				text = text + str(i.get_text())
			print('escrevendo artigo')
			fp.write('{ ' + text + '}\n' )
		except:
			print('erro ao tentar escrever artigo')
	return iteracoes


def atualizaLinkCCFVcrus(link,cont):
	novo_link = []
	l = link.split('/')
	for index,text in enumerate(l):
		if text == str(cont + 1):
			novo_link.append(str(cont+2) + '/')
		elif text == 'https:':
			novo_link.append("https://")
		else:
			if index == len(l) - 1:
				novo_link.append(text)
			else:
				novo_link.append(text + '/')
	return ''.join(novo_link)


def atualizaLink247(link,cont):
	novo_link = []
	l = link.split('/')
	l[len(l)-1] = "poder?page="+str(cont+2)
	for index,text in enumerate(l):
		if text == 'https:':
			novo_link.append("https://")
		else:
			if index == len(l) - 1:
				novo_link.append(text)
			else:
				novo_link.append(text + '/')
	return ''.join(novo_link)


driver = webdriver.Chrome('chromedriver')
fp = open('base/direita/istoe.txt','a')

cont = 39
num_iteracoes = 600
iteracao = 0

link_atual = "https://istoe.com.br/busca/page/40/?busca=pol%C3%ADtica"

while True:

	print("Iteracao " + str(cont + 1))

	if iteracao >= num_iteracoes:
		break
	print("carregando pagina " + str(cont+1))
	driver.get(link_atual)
	html = driver.page_source
	soup_pag_principal = BeautifulSoup(html,'html.parser')
	iteracao = get_istoe(driver,soup_pag_principal,fp,iteracao)
	link_atual = atualizaLinkCCFVcrus(link_atual,cont)
	cont = cont + 1
	print(iteracao)

fp.close()
print('fim')
	