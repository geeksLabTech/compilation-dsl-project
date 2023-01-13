# from parser.tzscript_ast import *
from inspect import stack
from math import fabs
from intermediate_ast.high_level_ir_ast import *
from visitor import when
from visitors.reference_counter_visitor import ReferenceCounterVisitor
import visitors.visitor_d as visitor


class StackValue:
    def __init__(self, value, type, id, belongs_to_storage=False):
        self.value = value
        self.type = type
        self.id = id
        self.belongs_to_storage = belongs_to_storage


class MichelsonGenerator(object):
    def __init__(self):
        self.code = ''
        self.stack: list[StackValue] = []
        self.storage_type = '', ''
        entry = None
        # Track how many times a variable will be used
        self.reference_counter: dict[str, int] = {}

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ContractNode)
    def visit(self, node: ContractNode):
        self.code = ""
        self.code += f"parameter "
        # for i, entry_node in enumerate(node.entrypoints.entrypoint_list):
        #     # self.code += ""
        #     # handle parameters
        #     # self.code += "( "
        #     if len(entry_node.params) >= 1:

        #         close = []
        #         for i, param in enumerate(entry_node.params):
        #             if len(entry_node.params) > 1 and i != len(entry_node.params)-1:
        #                 self.code += f"( or {param}"
        #                 close.append(")")
        #         for c in close:
        #             self.code += c

        #         self.code += ";\n"
        #     else:
        #         self.code += f"unit;\n"

        # We will asume only one entry and storage for simplicity
        # Entry with only one param
        entry = node.entrypoints.entrypoint_list[0]
        self.code += f"{entry.params[0].type} %{entry.id};\n"

        # process storage
        self.code += "storage"
        storage = node.storage.storage_list[0]
        self.code += f' {storage.type};\n'

        # Add initial values to stack
        # We will add the values separated and for this later include an unpair instruction at the beggining
        # The value of an entry depends of the smart contract call
        value = 0 if 'int' else '0'
        self.stack.append(StackValue(value, storage.type, storage.id, True))
        self.stack.append(StackValue(value, entry.params[0].type, entry.id))

        # Figure this out later
        # if len(node.storage.storage_list) > 0:
        #     close = []
        #     for i, s in enumerate(node.storage.storage_list):
        #         if i != len(node.storage[i].storage_list)-1:
        #             self.code += f"( or {s} "
        #             close.append(")")
        #     for c in close:
        #         self.code += c
        #     self.code += ";\n"
        # else:
        #     self.code += "unit;\n"
        
        ref_visitor = ReferenceCounterVisitor()
        ref_visitor.visit(node.code)
        self.reference_counter = ref_visitor.reference_counter
        print('reference counter: ', self.reference_counter)

        self.code += "code {\n"
        self.code += "UNPAIR;\n"
        
        generate_branches_for_entries = True
        if len(node.entrypoints.entrypoint_list) == 1:
            generate_branches_for_entries = False
        for st in node.code.statements:
            self.visit(st)

        # Next section is because every michelson program needs to end with a PAIR of list of OPERATIONS, value
        # This way needs improvement

        # Remove unused variables
        remains, stack_idx, michelson_idx = self.remains_non_storage_var()
        while remains:
            self.put_value_to_top_in_stack(stack_idx)
            self.code += f'DIG {michelson_idx};\n'
            self.code += f'DROP\n'
            self.stack.pop()
            remains, stack_idx, michelson_idx = self.remains_non_storage_var()

        for v in self.stack:
            print('node in stack: value, type, id', v.value, v.type, v.id, v.belongs_to_storage)
        print('current code: ', self.code)
        print()
        assert len(self.stack) == 1

        self.code += 'NIL operation;\n'
        self.code += 'PAIR;\n'

        self.code += "}\n"
        print('final code: ')
        print(self.code)
        # self.code += "}\n"

    @visitor.when(IfEntryNode)
    def visit(self, node: IfEntryNode):
        for s in node.statements:
            self.visit(s)

    @visitor.when(PushValueNode)
    def visit(self, node: PushValueNode):
        print('push value node: ', type(node.value), type(node.type))
        if str(node.type) == 'num':
            node.value = int(node.value)
            if node.value > 0:
                tp = 'nat'
            else: tp = 'int'
        else:
            tp = node.type

        self.code += f"PUSH {tp} {node.value};\n"
        self.stack.append(StackValue(node.value, node.type, None))

    @visitor.when(PushVariableNode)
    def visit(self, node: PushVariableNode):
        value = self.stack.pop()
        self.stack.append(StackValue(value.value, value.type, node.id))

    @visitor.when(ReplaceVariableNode)
    def visit(self, node: ReplaceVariableNode):
        michelson_index = 0
        index_in_stack = 0
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i].id == node.id:
                # self.code += f'DIG {michelson_index};\n'
                index_in_stack = i
                break
            michelson_index += 1

        self.put_value_to_top_in_stack(index_in_stack)
        previous_value = self.stack.pop()
        # self.code += 'DROP;\n'
        print('current stack, ', self.stack)
        print('current-code: ', self.code)
        next_value = self.stack.pop()
        self.reference_counter[node.id] -= 1
        self.stack.append(StackValue(next_value.value, next_value.type,
                          previous_value.id, previous_value.belongs_to_storage))

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        first, second = self.prepare_for_binary_op()
        self.code += "ADD;\n"
        self.stack.append(StackValue(
            first.value + second.value, first.type, None))

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        first, second = self.prepare_for_binary_op()
        self.code += "MUL;\n"
        self.stack.append(StackValue(
            first.value * second.value, first.type, None))

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        first, second = self.prepare_for_binary_op()
        self.code += "SUB;\n"
        self.stack.append(StackValue(
            first.value - second.value, first.type, None))

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        first, second = self.prepare_for_binary_op()
        self.code += "EDIV;\n"
        self.stack.append(StackValue(
            first.value / second.value, first.type, None))

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        first, second = self.prepare_for_binary_op()
        self.code += "EQ;\n"
        self.stack.append(StackValue(
            first.value == second.value, 'bool', None))

    @visitor.when(InequalityNode)
    def visit(self, node: InequalityNode):
        first, second = self.prepare_for_binary_op()
        self.code += "NEQ;\n"
        self.stack.append(StackValue(
            first.value != second.value, 'bool', None))

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        first, second = self.prepare_for_binary_op()
        self.code += "GT;\n"
        self.stack.append(StackValue(first.value > second.value, 'bool', None))

    @visitor.when(GreaterThanEqualNode)
    def visit(self, node: GreaterThanEqualNode):
        first, second = self.prepare_for_binary_op()
        self.code += "GE;\n"
        self.stack.append(StackValue(
            first.value >= second.value, 'bool', None))

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        first, second = self.prepare_for_binary_op()
        self.code += "LT;\n"
        self.stack.append(StackValue(first.value < second.value, 'bool', None))

    @visitor.when(LessThanEqualNode)
    def visit(self, node: LessThanEqualNode):
        first, second = self.prepare_for_binary_op()
        self.code += "LE;\n"
        self.stack.append(StackValue(
            first.value <= second.value, 'bool', None))

    @visitor.when(GetToTopNode)
    def visit(self, node: GetToTopNode):
        michelson_index = 0
        index_in_stack = 0
        # Loop in reverse in self.stack
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i].id == node.id:
                self.code += f'DIG {michelson_index};\n'
                index_in_stack = i
                break
            michelson_index+=1
        
        print('estado de counnter', self.reference_counter)
        self.reference_counter[node.id] -= 1
        self.put_value_to_top_in_stack(index_in_stack)

    @visitor.when(IfStatementNode)
    def visit(self, node: IfStatementNode):
        for st in node.expr:
            self.visit(st)
        
        self.code += "IF\n"
        
        condition = self.stack.pop()
        assert condition.type == 'bool'
        copied_stack = self.stack.copy()
        
        self.code += 'then {\n'
        for st in node.then_clause:
            self.visit(st)
        self.code += '}\n'

        self.stack = copied_stack.copy()
        self.code += 'else {\n'
        for st in node.else_clause:
            self.visit(st)
        self.code += '}\n'

        self.stack = copied_stack.copy()


    # this is wrong
    @visitor.when(WhileDeclarationNode)
    def visit(self, node: WhileDeclarationNode):
        self.code += "LOOP {"
        self.visit(node.expr)
        self.code += "} DO\n"

        for st in node.body:
            self.visit(st)

        self.code += "END\n"

    def prepare_for_binary_op(self) -> tuple[StackValue, StackValue]:
        assert len(self.stack) >= 2
        first_still_needed = False
        second_still_needed = False
        first = self.stack.pop()
        second = self.stack.pop()

        if first.id in self.reference_counter:
            first_still_needed = self.reference_counter[first.id] > 0
        
        if second_still_needed in self.reference_counter:
            second_still_needed = self.reference_counter[second.id] > 0

        if first_still_needed:
            self.stack.append(first)
            self.code += f'DUP;\n'

            self.put_value_to_top_in_stack(-2)
            self.code += f'DIG 2;\n'

            if second_still_needed:
                self.stack.append(second)
                self.code += f'DUP;\n'

                self.stack.insert(-4, second)
                self.code += f'DUG 3;\n'
            
            self.swap_values_in_top_stack()
            self.code += f'SWAP;\n'

        
        elif second_still_needed:
            self.swap_values_in_top_stack()
            self.code += f'SWAP;\n'

            self.stack.append(second)
            self.code += f'DUP;\n'

            self.put_value_to_top_in_stack(-2)
            self.code += f'DIG 2;\n'

            self.swap_values_in_top_stack()
            self.code += f'SWAP;\n'
        
        print('code', self.code)
        print('first', first.value, first.type)
        print('second', second.value, second.type)
        # assert first.type == second.type
        return first, second

    def put_value_to_top_in_stack(self, index: int):
        value = self.stack.pop(index)
        self.stack.append(value)

    def remains_non_storage_var(self):
        michelson_index = 0
        index_in_stack = 0
        for i in range(len(self.stack)-1, -1, -1):
            if not self.stack[i].belongs_to_storage:
                index_in_stack = i
                return True, index_in_stack, michelson_index

            michelson_index += 1

        return False, False, False

    def swap_values_in_top_stack(self):
        temp1 = self.stack.pop()
        temp2 = self.stack.pop()
        self.stack.append(temp1)
        self.stack.append(temp2)
