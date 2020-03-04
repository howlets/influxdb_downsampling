from pytz import utc
import logging
from flask import Blueprint
import rp_generator.settings as settings
from rp_generator.api.endpoints import ns as influx
from apscheduler.schedulers.background import BackgroundScheduler
from rp_generator.influx_worker.rp_handler import generate_rps
from rp_generator.api.restplus import api
from logger.logging import service_logger
from rp_generator.influx_worker.env_verifier import check_env_variables
import os
from flask import Flask

log = service_logger()


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    return flask_app


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='')
    api.init_app(blueprint)
    api.namespaces.clear()
    api.add_namespace(influx)
    flask_app.register_blueprint(blueprint)

    return flask_app


def create_app():
    new_app = Flask(__name__)
    new_app = initialize_app(new_app)
    new_app.secret_key = os.urandom(12)

    return new_app


def schedule_jobs():
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=utc)
    scheduler.start()
    scheduler.add_job(generate_rps, trigger='interval', seconds=int(settings.RP_CHECK_TIME))
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)


def main():
    log.info(msg=f"Starting Influx RP Generator service on port: {settings.SERVER_PORT}")
    app = create_app()
    check_env_variables()
    schedule_jobs()
    app.run(
        debug=settings.FLASK_DEBUG,
        port=settings.SERVER_PORT,
        host=settings.SERVER_NAME,
        threaded=settings.FLASK_THREADED
    )


if __name__ == "__main__":
    main()


