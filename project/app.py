# encoding=utf-8
#
# Example of a cherrypy application that serves images.
#
# Adrego da Rocha - Abril de 2023
#
# To run: python3 app.py

import os.path, subprocess, glob
import cherrypy
import json
import hashlib
import sqlite3 as sql
import time, random
import imagem_modificador

# The absolute path to this file's base directory
baseDir = os.path.abspath(os.path.dirname(__file__))

# Dictionary with this application's static directories configuration
config = {
			"/":		{	"tools.staticdir.root": baseDir },
			#"/html":	{	"tools.staticdir.on": True, "tools.staticdir.dir": "html" },		#para que não se possa dar bypass à página do login inserindo um url com html/ficheiro.html
			"/js":		{	"tools.staticdir.on": True, "tools.staticdir.dir": "js" },
			"/css":		{	"tools.staticdir.on": True, "tools.staticdir.dir": "css" },
			"/images":	{	"tools.staticdir.on": True, "tools.staticdir.dir": "images" },
			"/uploads":	{	"tools.staticdir.on": True, "tools.staticdir.dir": "uploads" }, 
			"/bootstrap": 	{"tools.staticdir.on": True, "tools.staticdir.dir": "bootstrap"},         #adicionado para que possa utilizar os ficheiro na pasta boostrap, em vez de usar os links para servidores externos
			"/tmp": 	{"tools.staticdir.on": True, "tools.staticdir.dir": "tmp"}					#após muitas horas a perguntar-me porque é que as imagens processadas, mesmo depois de mudar os caminhos de absolutos para relativos, não apareciam (e se estavam afinal no cliente ou no serviDor), apercebi-me que o novo diretório tmp/ não era dinânmico

}

cherrypy.config.update({"server.socket_port": 10013,})

class Root(object):
	@cherrypy.expose
	def __init__(self):
		self.acios = Actions()
		#self.html = Page_inicio()


	@cherrypy.expose
	def index(self):
		return open("html/index.html")

	# UpLoad image
	@cherrypy.expose
	def upload(self, myFile, nameImg, authorImg):		#adicionados parâmetros nameImg, authorImg
		h = hashlib.sha256()

		filename = baseDir + "/uploads/" + myFile.filename
		fileout = open(filename, "wb")
		while True:
			data = myFile.file.read(8192)
			if not data: break
			fileout.write(data)
			h.update(data)
		fileout.close()

		ext = myFile.filename.split(".")[-1]
		# final path of the image and changing the filename
		path = "uploads/" + h.hexdigest() + "." + ext
		os.rename(filename, path)
		
		# nameImg and authorImg are input parameters of this method
		# obtain the date and time of loading
		datetime = time.strftime('date:%d-%m-%Y time:%H:%M:%S')

		# insert the file information in the images table
		# eventually initialize the votes tables

		db = sql.connect('database.db')
		# db.execute(query of type INSERT (nameImg, authorImg, path, datetime))
		db.execute("INSERT INTO images(name, author, path, datetime) VALUES (?, ?, ?, ?)", (nameImg, authorImg, path, datetime))
		db.commit()
		db.close()

	# List requested images
	@cherrypy.expose
	def list(self, id):
		db = sql.connect('database.db')
		if (id == "all"):
			# result = db.execute(query of type SELECT for all images)
			result = db.execute("SELECT * FROM images")
		else:
			# result = db.execute(query of type SELECT for all images of the author id)
			result = db.execute("SELECT * FROM images WHERE author LIKE ? ", (id,))		#usar '%' no campo do autor para fazer pesquisas que incluam a palavra escrita e outra parte, antes ou depois, dependendo de onde se mete o '%'
		rows = result.fetchall()
		db.close()

		# Generate result (list of dictionaries) from rows (list of tuples)
		result = []
		for linha in rows:
			dicioImagem={"id": linha[0], "name": linha[1], "author":linha[2], "path":linha[3], "datetime": linha[4]}
			result.append(dicioImagem)
		
		
		# eventually sort result by image name before return
		result.sort(key=lambda x: x["name"].lower())

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"images": result}).encode("utf-8")

	# List comments
	@cherrypy.expose
	def comments(self, idimg):
		db = sql.connect('database.db')
		# result = db.execute(query of type SELECT for image of the id idimg)
		result = db.execute("SELECT * FROM images WHERE id=?", (idimg,))
		linha = result.fetchone()
		
		# Generate output dictionary with image information
		imageinfo = dict()
		imageinfo={"id": linha[0], "name": linha[1], "author":linha[2], "path":linha[3], "datetime": linha[4]}
		

		# result = db.execute(query of type SELECT for all comments of the id idimg)
		result = db.execute("SELECT * FROM comments WHERE idimg = ?", (idimg,))
		rows = result.fetchall()


		# Generate output dictionary with image comments list
		comments = []
		for linha in rows:
			dicioComment={"id": linha[0], "idimg": linha[1], "user":linha[2], "comment":linha[3], "datetime": linha[4]}
			comments.append(dicioComment)

		# result = db.execute(query of type SELECT for votes of the id idimg)
		result = db.execute("SELECT * FROM votes WHERE idimg = ?", (idimg,))
		linhas = result.fetchall()
		db.close()

		# Generate output dictionary with image votes
		imagevotes = dict()

		if linhas == []:
			imagevotes={"ups":0, "downs":0}
		else:
			gostos = 0
			desgostos = 0
			for linha in linhas:
				if linha[3]==1:
					gostos+=1
				if linha[4]==1:
					desgostos+=1
			imagevotes={"ups":gostos, "downs":desgostos}






		""" for line in linhas:
			linha=line			#só a última entrada interessa, visto que é a que tem o id mais alto, e é a mais recente
		if linhas == []: 
			linha=None
		if linha != None:
			imagevotes={"id": linha[0], "idimg": linha[1], "ups":linha[2], "downs":linha[3]}
	#	print(imagevotes)
		else:	
			imagevotes={"ups":0, "downs":0}		#não é preciso o id, nem verificar se o idimg é int ou string ou outra coisa; esta informação não vai ser enviada para a base de dados, 
			#mas sim para a função showimageandinfo() do image.js, que usa apenas as chaves ups e downs, pelo que não haverá erro em não haver um id como é suposto. 
			#Neste caso, os ups e downs servem para que os votos na página html tenham o valor 0, e não o valor undefined """

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"image": imageinfo, "comments": comments, "votes": imagevotes}).encode("utf-8")
	





	@cherrypy.expose
	def newcomment(self, idimg, username, newcomment):
		datetime = time.strftime('date:%d-%m-%Y time:%H:%M:%S')
		
		db=sql.connect('database.db')
		db.execute("INSERT INTO comments(idimg, user, comment, datetime) VALUES (?, ?, ?, ?)", (idimg, username, newcomment, datetime))
		db.commit()
		db.close()



	@cherrypy.expose
	def upvote(self, idimg, userID):
		db=sql.connect('database.db')
		authorID = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,)).fetchone()[0]
		result = db.execute("SELECT * FROM votes WHERE idimg = ? and idauthor = ?", (idimg,authorID))
		linhas = result.fetchone()
		db.close()

		db=sql.connect('database.db')
		if linhas == None:
			db.execute("INSERT INTO votes(idimg, idauthor, ups, downs) VALUES (?, ?, ?, ?)", (idimg, authorID, 1, 0))
			db.commit()
			db.close()
			return json.dumps({"result": 1}).encode("utf-8")
		else:
			db.execute("DELETE FROM votes WHERE idimg = ? and idauthor = ?", (idimg, authorID))
			if linhas[3]==1:																								
				db.execute("INSERT INTO votes(idimg, idauthor, ups, downs) VALUES (?, ?, ?, ?)", (idimg, authorID, 0, linhas[4]))	#retirar gosto
				db.commit()
				db.close()
				return json.dumps({"result": -1}).encode("utf-8")
			else:
				db.execute("INSERT INTO votes(idimg, idauthor, ups, downs) VALUES (?, ?, ?, ?)", (idimg, authorID, 1, linhas[4]))	#meter gosto
				db.commit()
				return json.dumps({"result": 1}).encode("utf-8")
			

		



	@cherrypy.expose
	def downvote(self, idimg, userID):
		db=sql.connect('database.db')
		authorID = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,)).fetchone()[0]
		result = db.execute("SELECT * FROM votes WHERE idimg = ? and idauthor = ?", (idimg,authorID))
		linhas = result.fetchone()
		db.close()

		db=sql.connect('database.db')
		if linhas == None:
			db.execute("INSERT INTO votes(idimg, idauthor, ups, downs) VALUES (?, ?, ?, ?)", (idimg, authorID, 0, 1))
			db.commit()
			db.close()
			return json.dumps({"result": 1}).encode("utf-8")
		else:
			db.execute("DELETE FROM votes WHERE idimg = ? and idauthor = ?", (idimg, authorID))
			if linhas[4]==1:																									
				db.execute("INSERT INTO votes(idimg, idauthor, ups, downs) VALUES (?, ?, ?, ?)", (idimg, authorID, linhas[3], 0))	#retirar desgosto
				db.commit()
				db.close()
				return json.dumps({"result": -1}).encode("utf-8")
			else:
				db.execute("INSERT INTO votes(idimg, idauthor, ups, downs) VALUES (?, ?, ?, ?)", (idimg, authorID, linhas[3], 1))	#meter desgosto
				db.commit()
				db.close()
				return json.dumps({"result": 1}).encode("utf-8")
			

		
		


	# UpLoad comment
	# Increment Up votes
	# Increment Down votes






	#imagem modificador
	# watermark
	@cherrypy.expose
	def watermark(self, file1, file2, f):
		#verificar se f é válido
		try:
			f=float(f)
			assert(f>=0 and f<=1)
		except:
			print("Valor de f inválido")
			result = "watermark_falhou"
			return json.dumps({"result" : result}).encode("utf-8") 
	

		#guardar imagem 1 na pasta tmp do servidor
		filename1 = baseDir + "/tmp/" + file1.filename
		fileout = open(filename1, "wb")
		while True:
			data = file1.file.read(8192)
			if not data: break
			fileout.write(data)
		fileout.close()


		#guardar imagem 2
		filename2 = baseDir + "/tmp/" + file2.filename
		fileout = open(filename2, "wb")
		while True:
			data = file2.file.read(8192)
			if not data: break
			fileout.write(data)
		fileout.close()


		#obter coordenadas da imagem1 de modo a pôr toda a imagem2 no canto inferior direito da primeira (é retornado (None, None) se tal não for exequível)
		start_x, start_y = imagem_modificador.watermark_positions(filename1, filename2)


		#criar nova imagem a partir das 2 guardadas no servidor e guardar esta nova imagem com watermark na pasta tmp, para posterior GET no image_manipulation.js
		cherrypy.response.headers["Content-Type"] = "application/json"
		if start_x != None and start_y != None:
			nome_imagem_servidor=imagem_modificador.watermark(filename1, filename2, f, start_x, start_y)
			result = nome_imagem_servidor
		else:
			result = "watermark_falhou"
		return json.dumps({"result" : result}).encode("utf-8") 
	

	@cherrypy.expose
	def vignette(self, file):
		#ler imagem e guardá-la na tmp
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)

		#aplicar vignette
		try:
			xref, yref = imagem_modificador.vignette_positions(filename)
			caminho_imagem = imagem_modificador.vignette(filename, xref, yref)
		except:
			caminho_imagem = "vignette_falhou"

		#devolver resultado (dizer apenas o caminho da nova imagem, se esta foi feita com sucesso, ou indicar que o método falhou)
		return json.dumps({"result" : caminho_imagem}).encode("utf-8")
	


	@cherrypy.expose
	def bordador(self, file, diff, bw):
		#ler imagem e guardá-la na tmp
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)

		#verificar o valor da checkbox do bw
		if bw == "true":
			bw = True
		else:
			bw = False

		#aplicar bordador
		try:
			diff=int(diff)
			caminho_imagem = imagem_modificador.im_handler(filename, diff, bw)
		except:
			caminho_imagem = "bordador_falhou"

		#devolver resultado (dizer apenas o caminho da nova imagem, se esta foi feita com sucesso, ou indicar que o método falhou)
		return json.dumps({"result" : caminho_imagem}).encode("utf-8")
	

	@cherrypy.expose
	def sepsis_lomography(self, file, sepia_lomografia):
		#ler imagem e guardá-la na tmp
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)

		#verificar o valor da checkbox do bw e aplicar sepia/lomografia
		if sepia_lomografia == "true":
			try:
				caminho_imagem = imagem_modificador.lomografia(filename)
			except:
				caminho_imagem = "sepia_lomografia_falhou"
		else:
			try:
				caminho_imagem = imagem_modificador.sepia(filename)
			except:
				caminho_imagem = "sepia_lomografia_falhou"
				
		return json.dumps({"result" : caminho_imagem}).encode("utf-8")


	

	@cherrypy.expose
	def saturador(self, file, f):
		
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)
	
		try:
			f=float(f)
			caminho_imagem = imagem_modificador.saturation(filename, f)
		except:
			caminho_imagem = "saturador_falhou"

		return json.dumps({"result" : caminho_imagem}).encode("utf-8")
	


	@cherrypy.expose
	def gamma(self, file, f):
		
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)
		
		try:
			f=float(f)
			caminho_imagem = imagem_modificador.gamma_modificaDor(filename, f)
		except:
			caminho_imagem = "gamma_falhou"

		return json.dumps({"result" : caminho_imagem}).encode("utf-8")
	

	@cherrypy.expose
	def intensificador(self, file, f):
		
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)
		 
		try:
			f=float(f)
			caminho_imagem = imagem_modificador.image_modifier_intensifier(filename, f)
		except:
			caminho_imagem = "intensificador_falhou"

		return json.dumps({"result" : caminho_imagem}).encode("utf-8")
	


	@cherrypy.expose
	def resizer(self, file, f, mode):
		
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)
		 
		try:
			f=float(f)
			caminho_imagem = imagem_modificador.resizer(filename, f, mode)
		except:
			caminho_imagem = "resizer_falhou"

		return json.dumps({"result" : caminho_imagem}).encode("utf-8")
	

	@cherrypy.expose
	def unknown(self, file):
		
		filename = baseDir + "/tmp/" + file.filename
		with open(filename, "wb") as stream:
			while True:
				data = file.file.read(29)
				if not data:
					break
				stream.write(data)


		acaso = random.randrange(1, 4)
		if acaso == 1:
			try:
				caminho_imagem = imagem_modificador.trocar_canais_red_green(filename)
			except:
				caminho_imagem = "unknown_falhou"
		elif acaso == 2:
			try:
				caminho_imagem = imagem_modificador.image_modifier_cinza(filename)
			except:
				caminho_imagem = "unknown_falhou"
		else:
			try:
				caminho_imagem = imagem_modificador.imagem_negativa(filename)
			except:
				caminho_imagem = "unknown_falhou"


		return json.dumps({"result" : caminho_imagem}).encode("utf-8")



	@cherrypy.expose
	def tmp_cleaner(self):
		print()
		imagens_tmp = glob.glob(baseDir+"/tmp/*")
		for imagem in imagens_tmp:
			print("Ficheiro removido: "+imagem)
			os.remove(imagem)					#demasiado arriscado para mim; preferir testar com um cp do shell, e se tudo aparentar estar bem, usar mv para uma pasta de deleção
		#print(os.getcwd())
		#subprocess.Popen("mv tmp/* DELETE_BACKUP/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		#return True #para efeitos de limpar a pasta /tmp e fechar a página ao mesmo tempo
















	#Estas funcionalidades servem para proteger as páginas html de agentes não autenticados (sem elas, a página de Login seria como uma porta que podia ser contornada, ao inserir o URL das páginas html estáticas)
	@cherrypy.expose
	def page_inicio(self, userID="None"):	

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,))
		linha = result.fetchone()
		db.close()

		if linha != None:
			return open("html/inicio.html")
		else:
			raise cherrypy.HTTPRedirect("http://127.0.0.1:10013")
		

	@cherrypy.expose
	def page_gallery(self, userID="None"):

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,))
		linha = result.fetchone()
		db.close()

		if linha != None:
			return open("html/gallery.html")
		else:
			raise cherrypy.HTTPRedirect("http://127.0.0.1:10013")


	@cherrypy.expose
	def page_upload(self, userID="None"):

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,))
		linha = result.fetchone()
		db.close()

		if linha != None:
			return open("html/upload.html")
		else:
			raise cherrypy.HTTPRedirect("http://127.0.0.1:10013")
		

	@cherrypy.expose
	def page_image(self, id="None", userID="None"):

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,))
		linha = result.fetchone()
		db.close()

		if linha != None:
			return open("html/image.html")
		else:
			raise cherrypy.HTTPRedirect("http://127.0.0.1:10013")
		

	@cherrypy.expose
	def page_image_manipulation(self, userID="None"):

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,))
		linha = result.fetchone()
		db.close()

		if linha != None:
			return open("html/image_manipulation.html")
		else:
			raise cherrypy.HTTPRedirect("http://127.0.0.1:10013")
		

	@cherrypy.expose
	def page_about(self):
		return open("html/about.html")



	@cherrypy.expose
	def getUsername(self, userID):

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE user_id = ?", (userID,))
		linha = result.fetchone()
		db.close()

		if linha != None:
			return json.dumps({"result" : linha[1]}).encode("utf-8")
		#return json.dumps({"result" : "erro"}).encode("utf-8")
		raise cherrypy.HTTPRedirect("http://127.0.0.1:10013")









		



			 


class Actions(object):
	@cherrypy.expose
	def doLogin(self, username, password):

		h = hashlib.sha256()
		h.update(password.encode())
		password = h.hexdigest()

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE username = ?", (username,))
		linha = result.fetchone()
		db.close()


		if linha == None:
			return json.dumps({"result" : "Nome de utilizador ou palavra-passe incorretos."}).encode("utf-8")

		account_info = dict()
		account_info={"id": linha[0], "username": linha[1], "password":linha[2], "userID": linha[3]}


		if account_info["username"].lower() == username.lower() and account_info["password"]==password:
			#cherrypy.response.headers["Content-Type"] = "application/json"			#com isto, estava a dar erro
			return json.dumps({"result" : "html/inicio.html", "userID": account_info["userID"]}).encode("utf-8")
		
		return json.dumps({"result" : "Nome de utilizador ou palavra-passe incorretos."}).encode("utf-8")
	

	@cherrypy.expose
	def doRegister(self, username, password):

		db=sql.connect('database.db')
		result = db.execute("SELECT * FROM accounts WHERE username = ?", (username,))
		linha = result.fetchone()
		db.close()

		if linha == None:

			h = hashlib.sha256()
			h.update(password.encode())
			password = h.hexdigest()

			s = hashlib.sha256()
			s.update(password.encode())
			s.update(username.encode())
			userID = username+s.hexdigest()

			db = sql.connect('database.db')
			db.execute("INSERT INTO accounts(username, password, user_id) VALUES (?, ?, ?)", (username, password, userID))
			db.commit()
			db.close()
			return json.dumps({"result" : "Conta criada."}).encode("utf-8")
		
		else:
			return json.dumps({"result" : "Erro: a conta já existe."}).encode("utf-8")
		






			




cherrypy.quickstart(Root(), "/", config)
