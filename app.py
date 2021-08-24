from flask import Flask
from views import home, shopCart, shopBag, categories, login, register
from conf.config import DevelopmentConfig

ACTIVE_ENDPOINTS = [('/home', home), ('/shopcart', shopCart), ("/shopbag", shopBag), ("/categories", categories), ("/login", login), 
("/register", register)]

def create_app(config=DevelopmentConfig):
    app = Flask(__name__, static_url_path="/static", static_folder='static')
    app.config.from_object(config)
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
