from base_agent import *
from useful_step import *

class MyAgent(BaseAgent,UsefulStep):
    def __init__(self):
        super().__init__()
        print(self.cols_n)

MyAgent()
        