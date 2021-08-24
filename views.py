from http import HTTPStatus
from flask import Blueprint, Response, request, render_template, url_for
from werkzeug.wrappers import response
from connect_db import connect

home = Blueprint("home", __name__, url_prefix="/home")
shopCart = Blueprint("shopcart", __name__, url_prefix="/shopcart")
shopBag = Blueprint("shopbag", __name__, url_prefix="/shopbag")
categories = Blueprint("categories", __name__, url_prefix="/categories")
login = Blueprint("login", __name__, url_prefix="/login")
register = Blueprint("register", __name__, url_prefix="/register")

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}

@home.route("/", methods=["GET"])
def show_product():
    conexion = connect()
    for datos in conexion.sentenciaCompuesta("select * from producto"):
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
    conexion = connect()
    for datos in conexion.sentenciaCompuesta("select N_NOMCATEGORIA from categoria"):
        RESPONSE_BODY["data"] += datos
    conexion.close()
    return render_template('categories.html')

@login.route("/", methods=["GET"])
def show_product():
    return render_template('login.html')

@register.route("/", methods=["GET"])
def show_product():
    return render_template('register.html')