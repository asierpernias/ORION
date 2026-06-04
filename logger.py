import logging


def log(*args):
        logging.info(" ".join(map(str, args)))
