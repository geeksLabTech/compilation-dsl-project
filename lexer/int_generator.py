
class IntGenerator():
    def __init__(self) -> None:
        self.current_number = -1
    
    def generate_number(self):
        self.current_number+=1
        return self.current_number
    
generator = IntGenerator()

        
