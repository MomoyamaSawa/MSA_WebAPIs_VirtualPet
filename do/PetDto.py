

class GptLogItem():
    def __init__(self,q,a,t):
        self.question = q
        self.answer = a
        self.time = t

class GptLogsDto():
    def __init__(self,logs:list[GptLogItem]):
        self.logs = logs
