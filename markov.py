import numpy as np
import sqlite3

# dicionário que irá armazenar o léxico
lexico = {}

def atualiza_lexico(atual: str, proxima: str) -> None:
	
	if atual not in lexico:
		lexico.update({atual: {proxima: 1}})
		return

	opcoes = lexico[atual]

	if proxima not in opcoes:
		opcoes.update({proxima: 1})
	else:
		opcoes.update({proxima: opcoes[proxima]+1})

	lexico[atual] = opcoes

# recebe lista de mensagens do db
conn = sqlite3.connect("mensagens.db")
dados = conn.execute("""SELECT message from mensagens WHERE canal=?""", [''])

# lista com as mensagens
mensagens = [_[0] for _ in dados.fetchall()]

for mensagem in mensagens:
	# lista com as palavras da mensagem
	palavras = mensagem.split()

	for i in range(len(palavras)-1):
		atualiza_lexico(palavras[i], palavras[i+1])

for palavra, freq in lexico.items():
	# atualiza a frequencia que uma palavra aparece para porcetagem
	# palavra  -> lista de palavras seguidas: % chance
	nova_freq = dict((chave, valor/sum(freq.values())) for chave, valor in freq.items())
	lexico[palavra] = nova_freq

while True:
	palavra = input('\n> ')
	if palavra not in lexico:
		print('Essa palavra não existe no lexico!')
	else:
		
		print(f'\n{palavra}', end='')
		c = 0
		anterior = str('ninguemdiriaissoQWQ')
		predicao = str()
		while c < 9:
			opcoes = lexico[palavra]
			predicao = np.random.choice(list(opcoes.keys()), p=list(opcoes.values()))
			if predicao == anterior:
				break
			print(f' {predicao}', end='')
			anterior = predicao
			c += 1
