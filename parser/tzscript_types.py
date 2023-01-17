
from enum import Enum
from typing import Self



class TypesNames(Enum):
    Boolean = 'bool'
    Integer = 'int'
    Natural = 'nat'
    String = 'string'
    Address = 'address'
    IntOrNat = 'intOrNat'


class Operators(Enum):
    Add = '+'
    Sub = '-'
    Mul = '*'
    Div = '/'
    Eq = '=='
    Neq = '!='
    Lt = '<'
    Gt = '>'
    Leq = '<='
    Geq = '>='


class TzScriptType:
    def __init__(self, name: TypesNames) -> None:
        self.name = name

    def is_compatible(self, other) -> bool:
        return self.name == other.name

    def __eq__(self, other) -> bool:
        return self.name == other.name

class TzScriptBoolean(TzScriptType):
    def __init__(self) -> None:
        super().__init__(TypesNames.Boolean)


class TzScriptString(TzScriptType):
    def __init__(self) -> None:
        super().__init__(TypesNames.String)

class TzScriptAddress(TzScriptType):
    def __init__(self) -> None:
        super().__init__(TypesNames.Address)

class TzScriptNat(TzScriptType):
    def __init__(self) -> None:
        super().__init__(TypesNames.Natural)

    def is_compatible(self, other: TzScriptType) -> bool:
        return super().is_compatible(other) or other.name == TypesNames.Integer
        
class TzScriptInt(TzScriptType):
    def __init__(self) -> None:
        super().__init__(TypesNames.Integer)
    
    def is_compatible(self, other: TzScriptType) -> bool:
        return super().is_compatible(other) or other.name == TypesNames.Natural or other.name == TypesNames.IntOrNat

    
class TzScriptIntOrNat(TzScriptType):
    def __init__(self) -> None:
        super().__init__(TypesNames.IntOrNat)

    def is_compatible(self, other: TzScriptType) -> bool:            
        return super().is_compatible(other) or other.name == TypesNames.Natural or other.name == TypesNames.Integer or other.name == TypesNames.IntOrNat


types_dict_creator: dict[str, TzScriptType] = {'bool': TzScriptBoolean(), 'int': TzScriptInt(), 'nat': TzScriptNat(), 'string': TzScriptString(), 'address': TzScriptAddress(), 'intOrNat': TzScriptIntOrNat()}

