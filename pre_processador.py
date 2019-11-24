import sys
import nltk
from nltk import tokenize
import string
import numpy as np
import os

path = 'base'

def preprocessa_reportagem(reportagem):
	stopwords = nltk.corpus.stopwords.words('portuguese')
	stemmer = nltk.stem.RSLPStemmer()
	rep_tokenizada = tokenize.word_tokenize(reportagem,language = 'portuguese')
	rep_processada = [stemmer.stem(word) for word in rep_tokenizada 
					  if word not in string.punctuation 
					  and word not in stopwords
					  and word != 'veja.com'
					  and word != 'Veja.com/VEJA.com'
					  and word != 'Veja.com'
					  and word != '–']
	return rep_processada

def read_file(path):
	f = open(path,'r')
	text = f.read()
	return text

def fill_train_and_test(tag,num_rep_treino,list_of_files,treino,teste,label,lado):
	for num in range(len(list_of_files)):
		if num < num_rep_treino:
			text = read_file(path + '/' + lado + '/' + list_of_files[num])
			reportagens = text.split('}')
			for r in reportagens:
				if r != '' and r != '\n':
					rep_processada = preprocessa_reportagem(r)
					treino.append(rep_processada)
					label.append(tag)
		else:
			text = read_file(path + '/' + lado + '/' + list_of_files[num])
			reportagens = text.split('}')
			for r in reportagens:
				rep_processada = preprocessa_reportagem(r)
				teste.append(rep_processada)
	return treino,teste,label

def carrega_base(num_rep_treino):
	treino = []
	label = []
	teste = []
	for lado in sorted(os.listdir(path)):
		list_of_files = os.listdir(path + '/' + lado)
		if lado == 'esquerda':
			#pega apenas o numero de repostagens especificado para treino
			treino,teste,label = fill_train_and_test(0,num_rep_treino,list_of_files,treino,teste,label,lado)
		else:
			treino,teste,label = fill_train_and_test(1,num_rep_treino,list_of_files,treino,teste,label,lado)
	return treino,teste,label

def constroi_vocabulario(treino,teste):
	vocab = {}
	corpus = treino + teste
	for list_of_words in corpus:
		for word in list_of_words:
			if word in vocab:
				vocab[word] += 1
			else:
				vocab[word] = 1
	return vocab

def converte_em_vetor(vetor_texto,vetor_resultante,vocab,posicoes):
	for cont_t,reportagem in enumerate(vetor_texto):
		vet_rep = np.zeros([len(vocab)], dtype=np.uint8)
		for word in reportagem:
			vet_rep[posicoes[word]] = vocab[word]
		vetor_resultante[cont_t] = vet_rep
	return vetor_resultante

def converte_base_em_vetor(treino_texto,teste_texto,vocab,posicoes):
	treino = np.empty([len(treino_texto),len(vocab)], dtype=np.uint8)
	teste = np.empty([len(teste_texto),len(vocab)], dtype=np.uint8)
	treino = converte_em_vetor(treino_texto,treino,vocab,posicoes)
	teste = converte_em_vetor(teste_texto,teste,vocab,posicoes)
	return treino,teste

def calcula_pos_palavra(palavras):
	posicoes = {}
	for cont,palavra in enumerate(palavras):
		posicoes[palavra] = cont
	return posicoes

num_rep_treino = 2
print('carregando base')
treino,teste,label = carrega_base(num_rep_treino)
print('construindo vocabulario')
vocab = constroi_vocabulario(treino,teste)
palavras = list(vocab.keys())
posicoes_palavras = calcula_pos_palavra(palavras)
print('convertendo corpus em vetores')
treino,teste = converte_base_em_vetor(treino,teste,vocab,posicoes_palavras)
print('salvando a base')
np.save('base_processada/base_treino',treino)
np.save('base_processada/base_teste',teste)
np.save('base_processada/base_labels',label)