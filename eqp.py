from random import randint
from time import time, sleep
from sklearn.naive_bayes import GaussianNB
from collections import namedtuple
import redis


class Eqp:
	"""Classe para um equipamento"""

	def __init__(self, tipo=""):

		self.tipo = tipo

		if not self.tipo:
			self_define = self.define()
			self.tag = self_define[0]
			self.LAYOUTS = self_define[1]
		else:
			self_define = self.define(True)
			self.tag = self_define[0]
			self.LAYOUTS = self_define[1]


		self.id = self.gen_id()
		self.mac = self.gen_mac()
		self.ts = int(time())

	def gen_bool(self):
		"""gera um booleano aleatorio"""
		return bool(randint(0, 1))
		

	def define(self, manual_shift=False):
		"""define as caracteristicas do equipamento em sua inicialização"""

		tipos = {
			'a1':('ax89', 'ax91', 'v1'),
			'a2':('ax2.0', 'ax2.1', 'v1'),
			'b1':('bx67', 'v1'),
			'c1':('cx99', 'v1'),
		}


		if manual_shift:
			this = self.tipo
			return ([this, tipos[this]])
		else:
			keys = [k for k, v in tipos.items()]
			draw = randint(0, len(keys) - 1)
			this = keys[draw]
			return ([this, tipos[this]])

	def gen_message(self, model):
		"""Gera uma mensagem"""

		if model not in self.LAYOUTS:
			return (())
		else:
			#opções de modelos
			opts = {
				'ax89': 1,
				'ax91': 2,
				'ax2.0': 3,
				'ax2.1': 4,
				'bx67': 5,
				'cx99': 6,
				'v1': 7,
			}

			#treinar o algoritmo com esses dados
			#os dados em train representam valor para a chave no modelo
			train = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],]

			#os dados em result representam o valor final que o algoritmo deve apresentar
			#elas devem ser o numero de campos que nossa estrutura tera
			result = [4,6,3,2,9,5,4]

			#o algoritmo de aprendizado utilizado sera o naive bayes
			clf = GaussianNB()
			clf.fit(train, result)

			#o algoritmo preve o numero de campos que devera ter o modelo fornecido
			pred = clf.predict(opts[model])

			#montamos uma string com os campos da estrutura baseado na previsao do algoritmo
			string = ""
			for i in range(1, int(pred)):
				sn = "o" + str(i) + " "
				string += sn

			#montamos a estrutura com os devidos campos para a mensagem
			Struct = namedtuple("Struct", "id, mac, ts " + string + "st")

			#cada campo rpevisto pelo algortimo sera um booleano aleatorio
			o = [self.gen_bool() for i in string.split()]

			#Finalmente monta-se o registro
			msg = Struct(self.id, self.mac, int(time()), *o, self.ts)
			
			#retornando em forma de tupla
			return((model ,tuple(msg)))

	def gen_mac(self):
		"""Gera um mac aleatorio para este equipamento"""
		a = str(randint(10, 99))
		b = str(randint(100, 999))
		c = str(randint(0, 9))
		return int(a + b + b)

	def gen_id(self):
		"""Gera um id aleatorio para este equipamento"""
		return abs(hash(self.tag))

	def draw_random_model(self):
		"""retorna um modelo aleatorio baseado nos possiveis modelos definidos no
		layout deste equipamento"""
		draw = randint(0, len(self.LAYOUTS) - 1)
		return self.LAYOUTS[draw]


	def auto_gen_msg(self, min_delay=5, max_delay=12):
		"""Envia emnsagens aleatoriamente entre os tempos de delay estabelecidos"""
		while True:
			msg = self.gen_message(self.draw_random_model())
			print(self.tag, " delivered a message ...")
			self.save_to_redis(msg)
			
			wait = randint(min_delay, max_delay)
			sleep(wait)

	def save_to_redis(self, msg):
		'''registra uma mensagem no redis'''
		red = redis.StrictRedis(db = 9)
		red.rpush('list_messages', msg)
		




