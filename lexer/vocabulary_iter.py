

class VocabularyIter():
    def __init__(self, type_vocabulary : str):
        if type_vocabulary.isnumeric():
            self.vocabulary = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':7,'7':8,'8':9}
        elif type_vocabulary.isupper():
            self.vocabulary = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16,'Q':17,'R':18,'S':19,'T':20,'U':21,'V':22,'W':23,'X':24,'Y':25,'Z':26}
        elif type_vocabulary.islower():
            self.vocabulary = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
        
    
    def create_iter(self,start: int, end: int):
        list_all_vocabulary  = list(self.vocabulary.keys())
        iter_reduce_vocabulary = VocabularyIterator(iter(list_all_vocabulary[start:end]))
        return iter_reduce_vocabulary
    
class VocabularyIterator:
    def __init__(self, elements ) -> None:
        self.elements = elements
        self.current = None

    def next(self):
        self.current = next(self.elements)
        return self.current
    
    
