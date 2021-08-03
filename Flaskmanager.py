from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inversiones'
mysql= MySQL(app)
mysql.names="utf8"

print('init')
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM PLATAFORMAS')
    data= cur.fetchall()
    print (data)
    return render_template('index.html', plataformas=data)

@app.route('/scraphyipzazone')
def scrap1():
    from bs4 import BeautifulSoup
    from urllib.request import Request, urlopen
    #site= input("introduce pagina de hyip-zazona para scrapear")
    site= "https://hyip-zanoza.me/es/program/arbirate.com"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    etiqueta = soup('td')
    columna=0
    for x in etiqueta:  
        if columna==1:
            #valor1= x.find('div').find('div').find('div')
            valor1= x.select('div')[3].text
            print('Estado:', valor1)
            valor2= x.select('div')[6].text
            print('creacion:', valor2) 
        elif columna==5:    
            valor3= x.select('div')[1].text
            print('Beneficio diario:', valor3)  
        elif columna==9:
            valor4= x.select('div')[0]
            print('Deposito mínimo:',valor4.text)
        elif columna==11:
            valor5= x.select('div')[0]
            print('Pagos:',valor5.text)  
        columna+=1
        if columna==20:    
            break
    cur = mysql.connection.cursor()
    sql= "INSERT INTO plataformas (nombre, beneficio,min,inicio) VALUES (%s,%s,%s,%s)"
    data= ('nueva plataforma', valor3, valor4,valor2)
    cur.execute(sql,data)
    mysql.connection.commit()
    texto= (valor3+' ingresado')
    return(texto)


@app.route('/scrappupolarhyip')
def scrap2():
    import urllib
    from bs4 import BeautifulSoup
    #pagina_web = input('Enter - ')
    pagina_web = 'http://popularhyip.com/es.html'
    codigo = urllib.request.urlopen(pagina_web)
    bea = BeautifulSoup(codigo)
    print (bea)
    print ('putoo')
    #for x in bea.select(".mytable td:nth-child(1) "):
    #x = bea.select(".mytable")
    for x in bea.select(".mytable"):
        y= x.select("td:nth-child(4)")
        for i in y:
            print('Contenido:', i.text)
            print('\n')
    return ('delete')


@app.route('/add_plataform', methods=['POST'])
def add_contact():
    if request.method=='POST':
        nombre=request.form['nombre']
        print(nombre)
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO plataformas (beneficio) VALUES (%s)',[nombre])
        mysql.connection.commit()
        return(nombre)

@app.route('/edit')
def edit_plataform():
    return render_template('index.html')    
  
'''  
@app.route('/delete')
def delete_contact():
    return ('delete')
'''

if __name__ == '__main__':
    app.run(port=3000, debug= 'true')