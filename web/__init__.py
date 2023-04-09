from flask import Flask
import os
import threading


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'jra.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.ini', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册控制器
    from web.app.controllers import alert_controller, application_controller, server_controller,vad_controller
    app.register_blueprint(alert_controller.ac)
    app.register_blueprint(application_controller.appc)
    app.register_blueprint(server_controller.sc)
    app.register_blueprint(vad_controller.vad)
    # 注册数据库
    from web.database import db
    db.init_app(app)
    # app.run(host="0.0.0.0",port=5000,debug=True)
    return app