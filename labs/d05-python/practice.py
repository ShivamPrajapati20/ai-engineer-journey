class LLMClient:
    def __init__(self, model:str,max_retries: int=3 ):
        self.model = model
        self.max_retries = max_retries

    def complete(self, prompt):
        return f"{self.model}: {prompt}"



    