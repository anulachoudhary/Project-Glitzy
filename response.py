class Response(object):
    """docstring for Response"""
    data = " "
    status = True
    error = " "
    error_code = 0


    def __init__(self, status, data = " ", error = " ", error_code = 0):
        
        self.status = status
        self.data = data
        self.error = error
        self.error_code = error_code

        

        