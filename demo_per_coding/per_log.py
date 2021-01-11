import logging
import traceback


def func():
    try:
        a = 10
        a = a / 0
        return a
    except Exception as err_msg:
        print(err_msg)
        msg = traceback.format_exc()
        new_msg = '\n' + msg
        logging.error(new_msg)


file_handler = logging.FileHandler(filename='test.log', mode='a', encoding='utf-8')
stream_handler = logging.StreamHandler()

log_format = '[%(asctime)s-%(name)s【%(levelname)s】%(module)s]: %(message)s'
date_format = '%Y-%m-%d %H:%M:%S %p'

logging.basicConfig(
    format=log_format,
    datefmt=date_format,
    handlers=[file_handler, stream_handler],
    level=logging.DEBUG
)
logging.info('starting...')
func()
