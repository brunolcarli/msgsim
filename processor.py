import redis
from time import sleep

########################################
# Processa as mensagens do Redis
# Enquanto houverem mensagens em
# uma fila no redis, o processador
# atende a primeira mensagem da fila
# e escreve ela em forma de json/dict
# em um arquivo de log
#########################################


def transform(msg):

	try:
		msg = eval(msg.decode())
	
		construct = msg[1][3:-1]

		new_shape = {
			'tag':msg[0],
			'id':msg[1][0],
			'mac':msg[1][1],
			'ts':msg[1][2],
			'opt': construct,
			'ts_a':msg[1][-1],
		}
	except:
		new_shape = {}

	return new_shape

# conecta ao Redis
try:
	red = redis.StrictRedis(db=9) #nosso default db será 9
except:
	print("conexão indisponível")

# loop principal
while True:
	print("Waiting for messages in the queue...")
	sleep(1)

	# verifica o númerod e mensagens na fila
	queue = red.llen('list_messages')
	print(queue, " messages in the list_messages queue")

	# atende o primeiro da fila
	pop_to_log = red.lpop('list_messages')

	#transforma de tupla pra dict
	processed_message = transform(pop_to_log)

	# registra no log
	with open("log.txt", 'a') as f:
		f.write(str(processed_message))
		f.write("\n")

print("Encenrrando processamento!")