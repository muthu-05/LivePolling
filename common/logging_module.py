import logging

def get_logger(name):
    log_format = '%(asctime)s %(name)%8s %(levelname)5s %(message)s'
    logging.basicConfig(level=logging.ERROR, format=log_format, filename='/tmp/connectme_error.log',filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
