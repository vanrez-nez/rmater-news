import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%y/%m/%d %H:%M:%S')

def log(msg: str) -> None:
    logging.info(msg)

def warn(msg: str) -> None:
    logging.warning(msg)