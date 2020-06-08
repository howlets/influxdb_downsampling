from cmreslogging.handlers import CMRESHandler
import logging.config
import rp_generator.settings as settings


def configure_logger(name='default'):
    logging.config.dictConfig({'version': 1, 'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'
        }},
        'handlers': {
            'console': {
                'level': settings.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': settings.LOG_LEVEL,
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'mode': 'a',
                'filename': f'{settings.LOG_PATH}/{settings.SERVICE_NAME}.log'
            }
        },
        'loggers': {
            'default': {
                'level': settings.LOG_LEVEL,
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })

    return logging.getLogger(name)


def service_logger():
    return configure_logger()
