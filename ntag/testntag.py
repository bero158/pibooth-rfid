from ntag import NtagReader
import logging

logging.basicConfig(filename='ntag.log', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

reader = NtagReader(pin_rst=7,debugLevel=logging.getLevelName(logger.level))
try:
    while True:
        print("Hold a tag near the reader")
        id = reader.read_id()
        print(f"ID: {bytes(id).hex()}")
except KeyboardInterrupt:
    reader.Close()
