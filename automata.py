import pydot
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod

from utils import ContainerSet

class Automaton(ABC):
    @abstractmethod
    def __init__(self, states: int, finals: List[int], transitions: Dict[Tuple[int, str], List[int]], start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions: Dict[int, Dict[str, List[int]]] = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(str(start), shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(str(end), shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(str(start), str(end), label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', str(self.start), label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass
    


class NFA(Automaton):
    def __init__(self, states: int, finals: List[int], transitions: Dict[Tuple[int, str], List[int]], start=0):
        super().__init__(states, finals, transitions, start)
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

class DFA(Automaton):
    
    def __init__(self, states: int, finals: List[int], transitions: Dict[Tuple[int, str], int], start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
       
        processed_transitions = { key: [value] for key, value in transitions.items() }
        super().__init__(states, finals, processed_transitions, start)
        self.current = start
        
    def _move(self, symbol):
        if self.current in self.transitions:
            if symbol in self.transitions[self.current]:
                return self.transitions[self.current][symbol][0]
        return None
        
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        self._reset()
        last_char = -1
        for i, char in enumerate(string):
            last_char = i
            self.current = self._move(char)
            if self.current is None:
                return False
        
        return self.current in self.finals and last_char == len(string) - 1


def move(automaton: NFA, states: List[int], symbol: str):
    moves = set()
    for state in states:
        # Your code here
        transitions = automaton.transitions[state]
        if symbol in transitions:
            for x in transitions[symbol]:
                moves.add(x)
    
    return moves

def epsilon_closure(automaton: NFA, states: list[int]):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        # Your code here
        print('state', state)
        transitions = automaton.transitions[state]
        print('transitions', transitions)
        if '' in transitions:
            for x in transitions['']:
                closure.add(x)
                pending.append(x)

   
    return ContainerSet(*closure)

def nfa_to_dfa(automaton: NFA):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]
    pending = [ start ]
    while pending:
        state = pending.pop()
        for symbol in automaton.vocabulary:
                
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                moves = move(automaton, list(state), symbol)
                new_state = epsilon_closure(automaton, list(moves))
                
                if len(new_state) > 0:
                    if new_state != state:
                        viewed_status = None
                        try:
                            viewed_status = states.index(new_state)
                        except ValueError:
                            pass

                        if viewed_status is None:
                            new_state.id = len(states) 
                            new_state.is_final = any(s in automaton.finals for s in new_state)
                            pending = [new_state] + pending
                            states.append(new_state)
                        else:
                            new_state.id = states[viewed_status].id
                            
                        transitions[state.id, symbol] = new_state.id
                    else :
                        transitions[state.id, symbol] = state.id
        
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa