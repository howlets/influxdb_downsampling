from cmreslogging.handlers import CMRESHandler
import logging.config
import rp_generator.settings as settings


def configure_logger(name='default', log_path=settings.LOG_PATH):
    logging.config.dictConfig({'version': 1, 'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'
        }},
        'handlers': {
            'console': {
                'level': settings.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'}
        },
        'loggers': {
            'default': {
                'level': settings.LOG_LEVEL,
                'handlers': ['console']
            }
        },
        'disable_existing_loggers': False
    })

    return logging.getLogger(name)


def service_logger():
    return configure_logger()