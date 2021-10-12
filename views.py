from http import HTTPStatus
from flask import Blueprint, Response, request, render_template, url_for, redirect, flash, abort
from werkzeug.wrappers import response
from connect_db import connect
import connect_db

home = Blueprint("home", __name__, url_prefix="/home")
shopCart = Blueprint("shopcart", __name__, url_prefix="/shopcart")
shopBag = Blueprint("shopbag", __name__, url_prefix="/shopbag")
categories = Blueprint("categories", __name__, url_prefix="/categories")
login = Blueprint("login", __name__, url_prefix="/login")
register = Blueprint("register", __name__, url_prefix="/register")

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
conexion = None

@home.route("/", methods=["GET"])
def show_product():
    if USER_DATA["rol"]=="ROL_CLIENTE":
        abort(403)
    for datos in conexion.sentenciaCompuesta("select * from natame.producto"):
        RESPONSE_BODY["data"] += datos
    conexion.close()
    return render_template('home.html')

@shopBag.route("/", methods=["GET"])
def show_product():
    return render_template('shopbag.html')

@shopCart.route("/", methods=["GET"])
def show_product():
    return render_template('shopcart.html')

@shopCart.route("/drop/<int:product_id>", methods=["GET"])
def delete_from_cart(product_id):
    pass

@categories.route("/", methods=["GET"])
def show_product():
    #conexion = connect()
    for datos in conexion.sentenciaCompuesta("select N_NOMCATEGORIA from categoria"):
        RESPONSE_BODY["data"] += datos
    conexion.close()
    return render_template('categories.html')

#Errores

@home.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@home.errorhandler(403)
def forbidden(error):
    return render_template('403.html'),403

@home.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'),500

#Login 

@login.route("/", methods=["GET"])
def show_product():
    return render_template('login.html')

USER_DATA = {"k_tipoid":"","k_identificacion":-1,"n_usuario":"","k_region":-1,"rol":""}

@login.route("/", methods=["POST"])
def login_post():
    usuario = request.form.get('email')
    password = request.form.get('pass')
    
    if usuario == "" or password == "":
        flash('Please check your login details and try again.')
        return redirect(url_for('login.show_product')) # if the user doesn't exist or password is wrong, reload the page
    #user = get_user(usuario)
    global conexion
    conexion = connect(usuario,password)
    connected = conexion.getConnectionState()
    if not connected:
        flash('Please check your login details and try again.')
        return redirect(url_for('login.show_product')) # if the user doesn't exist or password is wrong, reload the page
    #login_user(user, remember=False)
    user_role = ""
    query_rol = "select distinct granted_role from USER_ROLE_PRIVS where upper(username)=upper('"+usuario+"')"
    user_role = conexion.sentenciaCompuesta(query_rol)[0][0]
    query = """select u.k_tipoid, u.k_identificacion, r.k_region 
        from natame.representante_para_cliente r, natame.representante_cliente rp, natame.cliente c, natame.usuario u 
        where r.k_identificacion=rp.k_identificacion_rep 
        and c.k_identificacion = rp.k_identificacion_cli 
        and c.k_tipoid = rp.k_tipoid_cli
        and rp.f_fin_rep is null 
        and c.k_identificacion = u.k_identificacion 
        and c.k_tipoid = u.k_tipoid 
        and u.n_usuario='""" + usuario + "'"
    datos_cookie=[]
    for dato in conexion.sentenciaCompuesta(query):
        datos_cookie.append(dato[0])
        datos_cookie.append(dato[1])
        datos_cookie.append(dato[2])
    USER_DATA["k_tipoid"] = datos_cookie[0]
    USER_DATA["k_identificacion"] = datos_cookie[1]
    USER_DATA["n_usuario"] = usuario
    USER_DATA["rol"]= user_role
    if len(datos_cookie)==2:
        USER_DATA["k_region"] = datos_cookie[2]
    print(USER_DATA)
    return redirect(url_for('home.show_product'))


#End Login

@register.route("/", methods=["GET"])
def show_product():
    return render_template('register.html')