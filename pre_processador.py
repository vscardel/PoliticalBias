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
	rep_tokenizada = []
	aux = []
	for i in reportagem:
		if i in string.punctuation:
			aux.append(' ')
		elif i in i== '\xa0' or i == '\n':
			aux.append('')
		else:
			aux.append(i)
	string_reportagem = ''.join(aux)
	for palavra in string_reportagem.split(' '):
		if palavra not in stopwords and palavra not in string.punctuation:
			rep_tokenizada.append(palavra.lower())
	# rep_processada = [stemmer.stem(word) for word in reportagem
	# 				  if word not in string.punctuation 
	# 				  and word not in stopwords
	# 				  and word != 'veja.com'
	# 				  and word != 'Veja.com/VEJA.com'
	# 				  and word != 'Veja.com'
	# 				  and word != '–']
	# aux = ''.join(rep_processada)
	# rep_tokenizada = tokenize.word_tokenize(aux,language = 'portuguese')
	return rep_tokenizada

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
	treino = np.empty([len(treino_texto),len(vocab)], dtype=np.float32)
	teste = np.empty([len(teste_texto),len(vocab)], dtype=np.float32)
	treino = converte_em_vetor(treino_texto,treino,vocab,posicoes)
	teste = converte_em_vetor(teste_texto,teste,vocab,posicoes)
	return treino,teste

def calcula_pos_palavra(palavras):
	posicoes = {}
	for cont,palavra in enumerate(palavras):
		posicoes[palavra] = cont
	return posicoes

#pega 20% do treino e usa como validacao
def constroi_validacao(treino,label,proporcao):
	tam_validacao = int(proporcao*len(treino))
	num_instancias_por_classe = int(tam_validacao / 2)
	validacao = np.empty([tam_validacao,len(vocab)], dtype=np.float32)
	label_validacao = np.empty([tam_validacao], dtype=np.uint8)
	novo_treino = np.empty([len(treino)-tam_validacao,len(vocab)], dtype=np.float32)
	label_treino = np.empty([len(treino)-tam_validacao], dtype=np.uint8)
	classe_atual = label[0]
	cont_validacao = 0
	cont_classe_atual = 0
	cont_treino = 0
	for i,instancia in enumerate(treino):
		if (label[i] == classe_atual) and (cont_classe_atual < num_instancias_por_classe):
			validacao[cont_validacao] = instancia
			label_validacao[cont_validacao] = label[i]
			cont_validacao += 1
			cont_classe_atual += 1
		elif (label[i] == classe_atual) and (cont_classe_atual >= num_instancias_por_classe):
			novo_treino[cont_treino] = instancia
			label_treino[cont_treino] = label[cont_treino]
			cont_treino += 1
		elif label[i] != classe_atual:
			classe_atual = label[i]
			validacao[cont_validacao] = instancia
			label_validacao[cont_validacao] = label[i]
			cont_validacao += 1
			cont_classe_atual = 1
	return novo_treino,label_treino,validacao,label_validacao

num_rep_treino = 2
proporcao = 0.2

print('carregando base')
treino,teste,label = carrega_base(num_rep_treino)
print('construindo vocabulario')
vocab = constroi_vocabulario(treino,teste)
palavras = list(vocab.keys())
posicoes_palavras = calcula_pos_palavra(palavras)
print('convertendo corpus em vetores')
treino,teste = converte_base_em_vetor(treino,teste,vocab,posicoes_palavras)
print('calculando a validacao')
treino,label,validacao,label_validacao = constroi_validacao(treino,label,proporcao)
print(treino)
print('salvando a base')
np.save('base_processada/base_treino',treino)
np.save('base_processada/base_teste',teste)
np.save('base_processada/base_labels_treino',label)
np.save('base_processada/base_validacao',validacao)
np.save('base_processada/base_labels_validacao',label_validacao)