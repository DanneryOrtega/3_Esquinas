from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = '3_esquinas'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

@app.route('/client/new')
def new_client():
    return render_template('client/new_client.html')


@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
       cedula_nit = request.form['cedula_nit']
       nombre_completo = request.form['nombre_completo']
       dirección = request.form['dirección']
       celular = request.form['celular']
       cur = mysql.connection.cursor()
       cur.execute("INSERT INTO client (cedula_nit, nombre_completo, dirección, celular) VALUES (%s,%s,%s,%s)", (cedula_nit, nombre_completo, dirección, celular))
       mysql.connection.commit()
       flash('Cliente añadido con éxito')
       return redirect(url_for('new_client'))
    #    print(cedula_nit)
    #    print(nombre_completo)
    #    print(dirección)
    #    print(celular)
    #    return 'received'
    # return render_template('client/new_client.html')

@app.route('/client/lista')
def lista_client():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM client')
    data = cur.fetchall()
    #print(data)

    return render_template('client/lista_client.html', clients = data)

@app.route('/edit_client/<id>')
def get_client(id):
    cur = mysql.connection.cursor()  
    cur.execute('SELECT * FROM client WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('client/edit_client.html', client = data[0])

@app.route('/update_client/<id>', methods = ['POST'])
def update_client(id):
    if request.method == 'POST':
        cedula_nit = request.form['cedula_nit']
        nombre_completo = request.form['nombre_completo']
        dirección = request.form['dirección']
        celular = request.form['celular']

        cur = mysql.connection.cursor()  
        cur.execute("""
            UPDATE client
            SET cedula_nit = %s,
                nombre_completo = %s,
                dirección = %s,
                celular = %s
            WHERE id = %s
        """, (cedula_nit, nombre_completo, dirección, celular, id))
        mysql.connection.commit()
        flash('Cliente editado con exito')
        return redirect(url_for('lista_client'))




@app.route('/delete_client/<string:id>')
def delete_client(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM client WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Cliente eliminado con exito')
    return redirect(url_for('lista_client'))

LISTAR_PRODUCTOS = 'SELECT * FROM productos'
LISTAR_CLIENT = 'SELECT * FROM client'
LISTAR_VENTA = 'SELECT * FROM ventas'

@app.route('/')
def inicio():
    return render_template('sitio/login.html')

@app.route('/menu')
def menu():
    return render_template('sitio/menu.html')

@app.route('/nosotros')
def usuario():
    return render_template('sitio/nosotros.html')

@app.route('/productos/editar')
def editar():
    # CREAR_PRODUCTO = 'INSERT INTO productos()'-
    return render_template('product/editar_prod.html')

@app.route('/productos/lista')
def lista():
    # cur = mysql.new_cursor(dictionary=True)
    # cur.execute(LISTAR_PRODUCTOS)
    # productos = cur.fetchall()  , productos=productos
    return render_template('product/lista.html')
    
@app.route('/productos/inventario')
def inventario():
    return render_template('productos/inventario.html')





@app.route('/ventas/lista')
def lista_ventas():
    # cur = mysql.new_cursor(dictionary=True)
    # cur.execute(LISTAR_VENTA)
    # ventas = cur.fetchall() ventas=ventas
    return render_template('ventas/lista_ventas.html')

@app.route('/ventas/new')
def new_ventas():
    return render_template('ventas/facturacion.html')

if __name__ == '__main__':
    app.run(debug=True)