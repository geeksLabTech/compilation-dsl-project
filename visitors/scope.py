
from parser.tzscript_types import *

class VariableInfo:
    def __init__(self, name: str, type: TzScriptType):
        self.name = name
        self.type = type

class FunctionInfo:
    def __init__(self, name: str, params_types: list[TzScriptType], return_type: TzScriptType):
        self.name = name
        self.params_types = params_types
        self.return_type = return_type

class EntryInfo:
    def __init__(self, name: str, params_types: list[TzScriptType]) -> None:
        self.name = name
        self.params_types = params_types

class Scope:
    def __init__(self, parent=None):
        self.local_vars: list[VariableInfo] = []
        self.local_funcs: list[FunctionInfo] = []
        self.entries: list[EntryInfo] = []
        self.parent: Self | None = parent
        self.children: list[Self] = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        self.main_level = False
        self.is_if_in_scope = False
        self.is_entry_in_scope = False

    # def main_scope(self):
    #     self.main_level = True
    
    # def is_if_in_scope(self):
    #     self.is_if_in_scope = True
    
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def create_child_scope_with_parent_info(self):
        child_scope = Scope(self)
        for f in self.local_funcs:
            child_scope.local_funcs.append(f)
        for v in self.local_vars:
            child_scope.local_vars.append(v)
        for e in self.entries:
            child_scope.entries.append(e)
        
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname: str, type: TzScriptType):
        self.local_vars.append(VariableInfo(vname, type))
    
    def define_function(self, fname, params, return_type: TzScriptType):
        self.local_funcs.append(FunctionInfo(fname, params, return_type))

    def define_entry(self, fname: str, params):
        self.entries.append(EntryInfo(fname, params))

    def is_var_defined(self, vname):
        for var in self.local_vars:
            if var.name == vname:
                return True

        if self.parent is None:
            return False
            
        return self.parent.is_var_defined(vname)
    
    
    def is_func_defined(self, fname: str, n: int):
        for f in self.local_funcs:
            if f.name == fname and f.params_types == n:
                return True
        
        if self.parent is None:
            return False

        return self.parent.is_func_defined(fname, n)

    def is_entry_defined(self, fname: str, n: int):
        for e in self.entries:
            if e.name == fname and e.params_types == n:
                return True
        
        if self.parent is None:
            return False

        return self.parent.is_entry_defined(fname, n)

    def is_local_var(self, vname: str):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname: str, n: int):
        return self.get_local_function_info(fname, n) is not None

    def get_local_variable_info(self, vname: str):
        var_info = None 
        for var in self.local_vars:
            if var.name == vname:
                var_info = var 
                break
        
        return var_info
    
    def get_local_function_info(self, fname: str, n: int):
        func_info = None 
        for func in self.local_funcs:
            if func.name == fname and func.params_types:
                func_info = func 
                break
        
        return func_info

