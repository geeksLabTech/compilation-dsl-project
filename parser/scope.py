class VariableInfo:
    def __init__(self, name):
        self.name = name

class FunctionInfo:
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Scope:
    def __init__(self, parent=None):
        self.local_vars: list[VariableInfo] = []
        self.local_funcs: list[FunctionInfo] = []
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname):
        self.local_vars.append(VariableInfo(vname))
    
    def define_function(self, fname, params):
        self.local_funcs.append(FunctionInfo(fname, params))

    def is_var_defined(self, vname):
        for var in self.local_vars:
            if var.name == vname:
                return True

        if self.parent is None:
            return False
            
        return self.parent.is_var_defined(vname)
    
    
    def is_func_defined(self, fname, n):
        for f in self.local_funcs:
            if f.name == fname and f.params == n:
                return True
        
        if self.parent is None:
            return False

        return self.parent.is_func_defined(fname, n)

    def is_local_var(self, vname):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname, n):
        return self.get_local_function_info(fname, n) is not None

    def get_local_variable_info(self, vname):
        var_info = None 
        for var in self.local_vars:
            if var.name == vname:
                var_info = var 
                break
        
        return var_info
    
    def get_local_function_info(self, fname, n):
        func_info = None 
        for func in self.local_funcs:
            if func.name == fname and func.params:
                func_info = func 
                break
        
        return func_info
    
    
scope = Scope()