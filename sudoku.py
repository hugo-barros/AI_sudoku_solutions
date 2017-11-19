from tabs import tabuleiro_easy_1, tabuleiro_easy_2, tabuleiro_med, tabuleiro_hard
import time

def desenharTabuleiroNaTela (T):
	strings = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
	for col in T:
		for j in range(9):
			if col[j] == 0:
				strings[j] += "   "
			else:
				strings[j] += " " + str(col[j]) + " "

	print
	for line in strings:
		print(line)
	print

	#time.sleep(0.15)


def naoAcabou(T):
	for i in range(9):
		for j in range(9):
			if (T[i][j] == 0):
				return True;

	return False;

def buscaEmProfundidade(T, dicionario, vertice=None):
	keyList = sorted(dicionario.keys())
	keyAtual = 0
	vertice = keyList[keyAtual]
	pilha_resultados = []
	pilha_aux = []
	pilha_resultados.append(vertice)

	atual = vertice
	while naoAcabou(T) == True:  # glo_stack.show_stack() != []:
		if atual in dicionario.keys():
			if dicionario[atual] != []:
				while dicionario[atual] != []:
					pilha_aux.append(atual) # coloco chave atual na minha pilha aux
					print ("pilha aux: " + str(pilha_aux))

					lin = int(atual.split(',')[0])
					col = int(atual.split(',')[1])
					print("Colocando o valor "+str(dicionario[atual][-1])+" na posicao "+pilha_aux[-1] )
					T[col][lin] = dicionario[atual].pop()

					desenharTabuleiroNaTela(T)
					#print ("key Atual eh " + keyList[keyAtual] + "("+str(keyAtual)+") - length keyList = "+str(len(keyList)))
					keyAtual = keyAtual + 1
					if (keyAtual < len(keyList)):						
						#print ("proximo key Atual eh " + keyList[keyAtual] + "("+str(keyAtual)+") - length keyList = "+str(len(keyList)))

						atual = keyList[keyAtual]

						lin = int(atual.split(',')[0])
						col = int(atual.split(',')[1])
						dicionario.update(descobrirPossibilidades(T, lin, col))
					else:
						print("\nacabou eh treta")
						desenharTabuleiroNaTela(T)
						return "Acabou"
			else:
				ind_nao_deu = atual
				
				print ("\nDeu BACKTRACK. na "+ind_nao_deu+"\n")
				print("\n"+ind_nao_deu+" nao deu (pelo primeiro else). Agora pilha_aux = "+str(pilha_aux))
				
				print
				keyAtual = keyAtual - 1 #backtracking
				if (len(pilha_aux) > 0):
					atual = pilha_aux.pop()

					lin = int(atual.split(',')[0])
					col = int(atual.split(',')[1])
					T[col][lin] = 0
					desenharTabuleiroNaTela(T)
		else:
			ind_nao_deu = atual
			print("\n"+ind_nao_deu+" nao deu (pelo segundo else). Agora pilha_aux = "+str(pilha_aux))
			
			print ("\ndeu backtrack. na "+ind_nao_deu+"\n")
			print
			keyAtual = keyAtual - 1 #backtracking
			if (len(pilha_aux) > 0):
				atual = pilha_aux.pop()

				lin = int(atual.split(',')[0])
				col = int(atual.split(',')[1])
				T[col][lin] = 0
				desenharTabuleiroNaTela(T)



def guloso(T):
	# 1 - trazer dicionario
	if naoAcabou(T) == True:
		dic_final = descobrirDicionario(T)
		print("Dicionario = " + str(dic_final))
		qts_adicionou = 0;
		# 2 - ver quantos tem tamanho = 1
		# 3 - colocar no T todos que tem tamanho = 1
		for key,value in dic_final.items():
			if (len(value) == 1):
				qts_adicionou = qts_adicionou + 1
				lin = int(key.split(',')[0])
				col = int(key.split(',')[1])
				T[col][lin] = value[0]
				print("Novo numero encontrado com soh um valor possivel: valor "+ str(value[0]) + " na posicao " + key )
				#desenharTabuleiroNaTela(T)
		if qts_adicionou > 0:
			print ("acabou os numeros encontrados com certeza nessa rodada, vamos gerar o novo dicionario agora.")
			print("O tabuleiro ficou assim:")
			desenharTabuleiroNaTela(T)
			time.sleep(2)
			guloso(T) # 4 - trazer novo dicionario (passo 1) volta passo 2 ateh chegar no stuck. (ou completar)
		else: # se stuck
			new_dics = {} # key = lin,col,valor | value = dicionarios que sao gerados a partir dela 
			
			menorValue = min(len(lista) for lista in dic_final.values())

			print("Min = "+ str(menorValue))
			if menorValue != 0:
				for key,value in dic_final.items():
					#print ("entrei nesse forzinho. Key: " + key + ". Value: " + str(value))
					if len(value) == menorValue:
						lin = int(key.split(',')[0])
						col = int(key.split(',')[1])
						# 5 - pegar a chave(posicao) que tem menor numero(X) de valores possiveis e trazer X novos dicionarios
						
						for i in range(len(value)): # iterando nos diferentes valores do "value" de menor length
							T[col][lin] = value[i]

							new_key = key+","+str(value[i])
							new_dics[new_key] = []

							print ("New key = " + new_key)
							print("tabela que seria caso essa key seja escolhida")
							desenharTabuleiroNaTela(T)

							time.sleep(0.8)
							novo_dicionario = descobrirDicionario(T)
							if min(len(v) for v in novo_dicionario.values()) != 0:
								new_dics[new_key].append( descobrirDicionario(T) ) #ATENCAO
							else:
								print ("Esta key ("+new_key+") iria fazer com que o tabuleiro chegasse num impasse sem solucao (escolha errada) entao nao foi considerada")
								

							T[col][lin] = 0
				# 6 - desses X novos dicionarios (em new_dics), descobrir qual tem o menor numero de possibilidades e seguir com ele.
				maior_soma_possibilidades = 0
				key_escolhido = ''
				for key,value in new_dics.items():
					soma_possibilidades = sum (len(v.values()) for v in value)
					print("(Key "+key+") - Soma possibilidades = " + str(soma_possibilidades))
					time.sleep(0.5)
					#for v in value:
					#	soma_possibilidades = soma_possibilidades + v.length
					
					if soma_possibilidades > maior_soma_possibilidades:
						print("(Key "+key+") - Soma possibilidades("+str(soma_possibilidades)+") > maior soma atual("+str(maior_soma_possibilidades)+")")
						key_escolhido = key
						maior_soma_possibilidades = soma_possibilidades
						print("maior soma atual = "+str(soma_possibilidades))
						print("Key escolhido = "+key_escolhido)
						#time.sleep(2)

				print("Key escolhida!!! foi a "+key_escolhido)
				time.sleep(1)
				# ao final do FOR, usar o T conforme o novo key
				print ("key q deu problema " + key_escolhido)
				lin = int(key_escolhido.split(',')[0])
				col = int(key_escolhido.split(',')[1])
				val = int(key_escolhido.split(',')[2])
				T[col][lin] = val
				guloso(T)
			else: # if minValue == 0
				print("Infelizmente o algoritmo guloso escolheu um caminho errado e nao sera possivel terminar o problema")
				return

	else:
		print ("Fim do algoritmo Guloso com sucesso!!!")
		desenharTabuleiroNaTela(T)
	
	
	# 7 - voltar para passo 1 utilizando esse novo dicionario





def descobrirDicionario(T):
	dic_final = {}
	for i in range(9):
		for j in range(9):
			if T[i][j] == 0:
				dic_final.update(descobrirPossibilidades(T, j, i))

	return dic_final


# cria um dicionario com possibilidades da lin,col pedida.
def descobrirPossibilidades(T, lin, col):
	key = str(lin)+','+str(col)
	dic = {key: [1,2,3,4,5,6,7,8,9]}

	
	# se ja tem na mesma coluna, remove do dic.
	for i in T[col]:
		if i in dic[key]:
			dic[key].remove(i)

	#print dic

	# se ja tem na mesma linha, remove do dic.
	for i in range(9):
		if T[i][lin] in dic[key]:
			dic[key].remove(T[i][lin])

	#print# dic

	lin_atual = lin - (lin % 3) # pega sempre a primeira linha de um quadrado
	#print (str(lin_atual) + " linha atual")
	col_atual = col - (col % 3) # pega sempre a primeira coluna de um quadrado
	#print (str(col_atual) + " coluna atual")

	# se esta dentro do quadrado, remove do dic.
	for i in range(lin_atual, lin_atual+3):
		for j in range(col_atual, col_atual+3):
			#print("i = " + str(i) + " ; j = " + str(j))
			if T[j][i] in dic[key]: # ATENCAO ! ver se esta certo
				#print("T[j][i] = " + str(T[j][i]) + ". Estou removendo da lista." )
				dic[key].remove(T[j][i])

	print ("Descobrindo Possibilidades na linha " + str(lin) + " e coluna " + str(col) + ":")
	print (dic)
	return dic

def main():

	desenharTabuleiroNaTela(tabuleiro_easy_1)
	guloso(tabuleiro_easy_1)
	desenharTabuleiroNaTela(tabuleiro_easy_2)
	guloso(tabuleiro_easy_2)


	desenharTabuleiroNaTela(tabuleiro_med)
	guloso(tabuleiro_med)
	desenharTabuleiroNaTela(tabuleiro_hard)
	guloso(tabuleiro_hard)
'''
	print ("##################################################################")
	desenharTabuleiroNaTela(tabuleiro_easy_1)
	descobrirDicionario(tabuleiro_easy_1)
	print
	print
	print

	#buscaEmProfundidade(tabuleiro_easy_1, descobrirDicionario(tabuleiro_easy_1))



	print ("##################################################################")
	desenharTabuleiroNaTela(tabuleiro_easy_2)
	descobrirDicionario(tabuleiro_easy_2)
	print
	print
	print

	#buscaEmProfundidade(tabuleiro_easy_2, descobrirDicionario(tabuleiro_easy_2))



	print ("##################################################################")
	desenharTabuleiroNaTela(tabuleiro_med)
	descobrirDicionario(tabuleiro_med)
	print
	print
	print

	#buscaEmProfundidade(tabuleiro_med, descobrirDicionario(tabuleiro_med))

	print ("##################################################################")
	desenharTabuleiroNaTela(tabuleiro_hard)
	descobrirDicionario(tabuleiro_hard)
	print
	print
	print

	#buscaEmProfundidade(tabuleiro_hard, descobrirDicionario(tabuleiro_hard))
'''

if __name__ == '__main__':
	main()