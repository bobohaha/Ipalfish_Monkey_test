class LogUtil:

    def __init__(self):
        pass

    @staticmethod
    def log(log):
        print(log)

    @staticmethod
    def log_start(tag):
        print(tag + '(): >>')

    @staticmethod
    def log_end(tag):
        print(tag + '(): <<')
