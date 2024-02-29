import pytest                                       #NOTA IMPORTANTE: em alguns computadores, executar o comando "py.test-3 test_web_server_requests.py" fica preso no "Collecting...". Fazer CTRC^C desencrava o processo e faz-o continuar normalmente
import sqlite3 as sql
from app import Root
from subprocess import Popen
import time, requests
import cherrypy, json, hashlib
from cherrypy.test import helper


#testes persistência

def test_database_select_votes():
    db = sql.connect("database.db")
    result = db.execute("SELECT * FROM votes")
    linhas = result.fetchall()
    db.close()      

    assert(linhas[0])==(79, 8, 2, 1, 0)                 #o primeiro registo na tabela votos da base de dados é: 79|8|2|1|0 (id, imgid, author, ups, downs)


def test_database_select_comments():
    db = sql.connect("database.db")
    result = db.execute("SELECT * FROM comments")
    linhas = result.fetchall()
    db.close()      

    assert(linhas[1][3])=="Que imagem linda"             #o segundo registo na tabela dos comentários tem o comentário "Que imagem linda"


def test_database_select_first_account():
    db = sql.connect("database.db")
    result = db.execute("SELECT * FROM accounts WHERE id=?", (1,))
    linhas = result.fetchone()
    db.close()      

    assert(linhas[1])=="Alcatrão"                         #a primeira conta registada na tabela de dados é a minha


def test_database_select_images():
    db = sql.connect("database.db")
    result = db.execute("SELECT * FROM images WHERE author=?", ('João Alcatrão',))
    linhas = result.fetchall()
    db.close()      

    assert(len(linhas))==5                                #dei upload a 5 imagens com este nome de autor



def test_database_insert_existent_account():
    with pytest.raises(sql.IntegrityError) as e:
        db = sql.connect("database.db")
        db.execute("INSERT INTO accounts(username, password, user_id) VALUES (?, ?, ?)", ("João", "password", "hash do nome mais a password encriptada"))
    assert str(e.value) == 'UNIQUE constraint failed: accounts.username'        #a conta já existe, pelo que este erro deve ocorrer

    


#teste funcional com uso de requests para aceder à página inicial
def test_pagina_index():
    proc = Popen("exec python3 app.py", shell=True)           #sem o exec, o Popen spawna outro processo com o comando "python3 app.py" em sim, que não é terminado pelo proc.terminate(). Assim, o processo que se quer iniciar substitui o processo inicial do Popen   
    time.sleep(3)

    servurl = "http://127.0.0.1:10013/"
    r = requests.get(servurl)
    time.sleep(1.5)
   

 
    proc.terminate()                                          #terminal o processo que lançou o servidor, para que o teste não corra indefinidamente

    paginaEsperada = ''
    with open("html/index.html" ,'r') as stream:
        paginaEsperada = stream.read()


    assert(r.text == paginaEsperada)


#teste funcional para registar conta, dar login no webserver com ela
def test_register_and_login():
    proc = Popen("exec python3 app.py", shell=True)           #sem o exec, o Popen spawna outro processo com o comando "python3 app.py" em sim, que não é terminado pelo proc.terminate(). Assim, o processo que se quer iniciar substitui o processo inicial do Popen   
    time.sleep(3)

    servurl = 'http://127.0.0.1:10013/acios/doRegister?username=test&password=test'
    r_register = requests.get(servurl)
    time.sleep(1.5)

    servurl = 'http://127.0.0.1:10013/acios/doLogin?username=test&password=test'
    r_login = requests.get(servurl)
    time.sleep(1.5)
   

 
    proc.terminate()                                          #terminal o processo que lançou o servidor, para que o teste não corra indefinidamente



    db = sql.connect("database.db")
    db.execute("DELETE FROM accounts WHERE username = ?", ("test",))
    db.commit()
    db.close()




    h = hashlib.sha256()                                        #calcular o userID
    h.update("test".encode())
    password = h.hexdigest()

    s = hashlib.sha256()
    s.update(password.encode())
    s.update("test".encode())
    userID = "test"+s.hexdigest()

    assert(r_register.json() == {"result" : "Conta criada."})
    assert(r_login.json() == {"result" : "html/inicio.html", "userID": userID})

   



#teste com registo, login e acesso à pagina da gallery
def test__register_login_and_access_gallery():
    proc = Popen("exec python3 app.py", shell=True)           #sem o exec, o Popen spawna outro processo com o comando "python3 app.py" em sim, que não é terminado pelo proc.terminate(). Assim, o processo que se quer iniciar substitui o processo inicial do Popen   
    time.sleep(3)

    servurl = 'http://127.0.0.1:10013/acios/doRegister?username=test&password=test'
    r_register = requests.get(servurl)
    time.sleep(1.5)

    servurl = 'http://127.0.0.1:10013/acios/doLogin?username=test&password=test'
    r_login = requests.get(servurl)
    time.sleep(1.5)

    servurl = 'http://127.0.0.1:10013/acios/doLogin?username=test&password=test'
    r_login = requests.get(servurl)
    time.sleep(1.5)
   

 
    
    h = hashlib.sha256()                                        #calcular o userID
    h.update("test".encode())
    password = h.hexdigest()

    s = hashlib.sha256()
    s.update(password.encode())
    s.update("test".encode())
    userID = "test"+s.hexdigest()


    servurl = 'http://127.0.0.1:10013/page_gallery?userID='+userID
    r_gallery = requests.get(servurl)
    time.sleep(1.5)



    proc.terminate()   

    db = sql.connect("database.db")
    db.execute("DELETE FROM accounts WHERE username = ?", ("test",))
    db.commit()
    db.close()




    assert(r_register.json() == {"result" : "Conta criada."})
    assert(r_login.json() == {"result" : "html/inicio.html", "userID": userID})

    pagina_galeria=''
    with open("html/gallery.html", 'r') as stream:
        pagina_galeria = stream.read()

    assert(r_gallery.text == pagina_galeria)






#testar métodos do servidor, sem uso dos requests
class test_pagina_index_e_about(helper.CPWebCase):
    @staticmethod
    def setup_server():
        cherrypy.tree.mount(Root(), '/', {})

    def test_index(self):
        self.getPage("/")
        self.assertStatus('200 OK')
    def test_about(self):
        self.getPage("/page_about")
        self.assertStatus('200 OK')
    

    