import logging

logging.basicConfig(
        filename="orion.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
def log(*args):
        logging.info(" ".join(map(str, args)))
