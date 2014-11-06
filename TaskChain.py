class TaskChain:
    def __init__(self):
        self._tasks=[]
        
    def addTask(self,task):
        self._tasks.append(task)
        
    def process():
        for task in self._tasks:
            task.begin()
            task.process()
            task.end()
            
