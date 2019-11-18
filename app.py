from flask import Flask, render_template, request, make_response, redirect, url_for, g, escape
from pymongo import MongoClient
from flask import session

MONGO_URI='mongodb://localhost'
client=MongoClient(MONGO_URI)

db=client['EFI_Programacion_2']
collection=db['usuario']
Jugador=db['jugador']



app = Flask(__name__)
app.secret_key="sladasd"
nom='sesion'

@app.route('/', methods=['GET', 'POST'])
def home():
        return render_template("index.html", usuario=nom)


@app.route('/mercado', methods=['GET', 'POST'])
def mercado():
    usuario=request.args.get('usuario')
    listaJ=[]
    price=[]
    imagen=[]
    idj=[]
    while True:        
        jugadoresM1=Jugador.find()
        for a in jugadoresM1:
            print (a)
            price.insert(0,a['valor'])
            listaJ.insert(0,a['nombre'])
            imagen.insert(0,a['imagen'])
            idj.insert(0,a['_id'])
            numJ=len(listaJ)
        if jugadoresM1== False:
            break

    
        return render_template("mercado.html", jugador=listaJ, numJ=numJ, price=price, imagen=imagen, usuario=usuario, idj=idj)

@app.route('/login', methods=['GET', 'POST'])
def loginU():
    return render_template('login.html')

@app.route('/loginU', methods=['GET','POST'])
def login():
    mail = request.form.get("email")
    contra = request.form.get("contrasena")
    resultados=collection.find({"mail":mail, "password":contra})
    for r in resultados:
        idusuario=r['_id']  
    usuarioLogin=collection.find({"_id":idusuario})
    for y in usuarioLogin:
        session['username']= y["nom_usuario"]
        print (usuarioLogin)
        if y['tipo_usuario'] == True :
            return redirect('/'+y["nom_usuario"]), render_template("index.html", usuario=y["nom_usuario"],coins="C "+str(y['coins']), admin="admin")
        else:
            return redirect('/'+y["nom_usuario"]), render_template("index.html", usuario=y["nom_usuario"],coins="C "+str(y['coins']))
        
    

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html')


@app.route('/new_user', methods=['GET','POST'])
def new_user():
    mail = request.form.get("email")
    contra = request.form.get("contrasena")
    user = request.form.get("user")

    collection.insert_one({"nom_usuario":user, "mail":mail, "password":contra, "tipo_usuario": False, "equipo":[], "coins":0  })
    

    return redirect('/')

@app.route('/compra', methods=['GET', 'POST'])
def compra():
    usuario=request.args.get('usuario')
    price=request.args.get('price')
    idjugador=request.args.get('idj')
    res=collection.find({"nom_usuario":usuario})
    price=int(price)
    for a in res:
        idusuario=a['_id']
    
    usuarioLogin=collection.find({"_id":idusuario})  #solo me trae usuario

    for b in usuarioLogin:
        print (b)
        if b['coins'] < price:
            print ("no podes comprar al jugador")
            
        else:
            print ("si podes comprar al jugador")
            resta=b['coins']-price
            listaJ=b['equipo']
            listaJ.insert(0,idjugador)
            collection.update_one({"nom_usuario":usuario,},{"$set":{"coins":resta, "equipo":listaJ, "password":b['password'], "mail":b["mail"], "tipo_usuario":b["tipo_usuario"]}})
    
    return redirect('/mercado?usuario='+usuario)


@app.route('/logout')
def logout():
    if 'username' in session:
        print (session)
        session.pop('username')
    return redirect('/')






if __name__=='__main__':
    app.run(debug=True, port=8000)
