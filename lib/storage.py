class Storage:
    def __init__(self,
                 file="storage.bin",
                 maxDataCount = 50
                 ):
        self.file = file
        self.maxDataCount = maxDataCount

    def saveData(self, data):
        f = open(self.file, "a")
        f.write("Now the file has more content!")
        f.close()