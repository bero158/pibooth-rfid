import time

class NtagReader:

    def __init__(self,pin_rst=7,debugLevel='WARNING'):
        """
        Initializes a SimpleMFRC522 instance.
        """
        
    def Close(self):
        """
        Close a SimpleMFRC522 instance.
        """

    def read_id_no_block(self):
        # Send request to RFID tag
        uids = ["04D92912FC7380","04FB3E12FC7380","0439E412FC7381","04F31E2AEB1490","04161F2AEB1491"]
        uid = uids[int(time.time())%len(uids)]
        uidb = list(bytes.fromhex(uid)) 
        return uidb
       
    
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

