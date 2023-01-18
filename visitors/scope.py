
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
    
    def define_function(self, fname: str, params: list[TzScriptType], return_type: TzScriptType):
        self.local_funcs.append(FunctionInfo(fname, params, return_type))

    def define_entry(self, entry_name: str, params: list[TzScriptType]):
        self.entries.append(EntryInfo(entry_name, params))

    def is_var_defined(self, vname):
        for var in self.local_vars:
            if var.name == vname:
                return True

        if self.parent is None:
            return False
            
        return self.parent.is_var_defined(vname)
    
    
    def is_func_defined(self, fname: str):
        for f in self.local_funcs:
            if f.name == fname:
                return True
        
        if self.parent is None:
            return False

        return self.parent.is_func_defined(fname)

    def is_entry_defined(self, fname: str):
        for e in self.entries:
            if e.name == fname:
                return True
        
        if self.parent is None:
            return False

        return self.parent.is_entry_defined(fname)

    def is_local_var(self, vname: str):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname: str):
        return self.get_function_info(fname) is not None

    def get_local_variable_info(self, vname: str):
        var_info = None 
        for var in self.local_vars:
            if var.name == vname:
                var_info = var 
                break
        
    
        return var_info
    
    def get_function_info(self, fname: str):
        func_info = None 
        for func in self.local_funcs:
            if func.name == fname:
                func_info = func 
                break
        
        if func_info is None and self.parent is not None:
            func_info = self.parent.get_function_info(fname)

        return func_info

