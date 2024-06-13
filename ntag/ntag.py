from .MFRC522 import MFRC522
import time


class NtagReader:
    debouncer = None
    """
    A class for reading and writing data using the MFRC522 RFID module.

    Attributes:
        MFRC522 (module): The MFRC522 module used for communication with the RFID reader.
        KEY (list): The default authentication key used for reading and writing data.
        TRAILER_BLOCK (int): The default trailer block to authenticate.
        BLOCK_ADDRS (list): The list of block addresses used for reading and writing data.
    """

    def __init__(self,pin_rst=4,debugLevel='WARNING'): #rst 4 for BCM mode
        """
        Initializes a SimpleMFRC522 instance.
        """
        
        self.MFRC522 = MFRC522(pin_rst=pin_rst,debugLevel=debugLevel)
    def Close(self):
        self.MFRC522.Close()

    def read_id_no_block(self):
        # Send request to RFID tag
        (status, TagType) = self.MFRC522.Request(self.MFRC522.PICC_REQIDL)
        if status != self.MFRC522.MI_OK:
            return None
        
        uid = self.MFRC522.SelectTagSN()
        return uid
       
    
    def read_id(self):
        """
        Reads the tag ID from the RFID tag.

        Returns:
            id (int): The tag ID as an integer.
        """
        id = None
        errorCount = 0
        while (not id) or (self.debouncer == id) :
            time.sleep(0.2)
            id = self.read_id_no_block()
            if self.debouncer:
                if id:
                    errorCount = 0
                else:
                    errorCount += 1
                    if errorCount > 2: #every second reading is an error so we're waiting for at least two invalid reading here.
                        self.debouncer = None
        self.debouncer = id
        return id

