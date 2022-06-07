from distutils.errors import CompileError
import sys

import jsonpickle

from src.compiler.code_generator.code_generator import CodeGenerator
from src.compiler.code_generator.type import Dimension, Operand, OperationType
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.lexer import lex, tokens
from src.compiler.ply import yacc
from src.compiler.stack_allocator.helpers import Layers
from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.types import ValueType
from .output import OutputFile
from .symbol_table import SymbolTable
from .symbol_table.class_table import ClassTable
from ..utils.observer import Subscriber, Event, Publisher


class Compiler(Publisher, Subscriber):
    def __init__(self):
        super().__init__()

        self._allocator = StackAllocator()
        self._symbol_table = SymbolTable()

        self.tokens = tokens
        self.lexer = lex
        self._parser = yacc.yacc(module=self, start="program", debug=True)
        self._code_generator = CodeGenerator(
            self._allocator, self._symbol_table.class_table.classes)

        object_actions = self._code_generator.object_actions
        object_actions.add_subscriber(self._symbol_table.function_table, {})

        # subscribe to expression code generator
        expressions = self._code_generator.expression_actions
        expressions.add_subscriber(self._symbol_table.function_table, {})
        expressions.add_subscriber(self._allocator, {})

        # subscribe to array actions
        array_actions = self._code_generator.array_actions
        array_actions.add_subscriber(self._symbol_table.function_table, {})
        array_actions.add_subscriber(self, {})

        # subscribe to builtin actions
        built_in_actions = self._code_generator.builtin_actions
        built_in_actions.add_subscriber(self._symbol_table.function_table, {})
        built_in_actions.add_subscriber(self, {})

        # subscribers for function table
        functions = self._symbol_table.function_table
        functions.add_subscriber(self._code_generator.function_actions, {})
        functions.add_subscriber(self._code_generator.expression_actions, {})
        functions.add_subscriber(self._allocator, {})

        # subscribe to compiler events
        self.add_subscriber(self._code_generator.function_actions, {})
        self.add_subscriber(self._symbol_table.function_table, {})

        # subscribe compiler to error messages
        self._allocator.add_subscriber(self._symbol_table.function_table, {})
        self._allocator.add_subscriber(self, {CompilerEvent.STOP_COMPILE})

        self._code_generator.expression_actions.add_subscriber(
            self, {CompilerEvent.STOP_COMPILE})
        self._symbol_table.function_table.add_subscriber(
            self, {CompilerEvent.STOP_COMPILE})
        self._code_generator.object_actions.add_subscriber(
            self, {CompilerEvent.STOP_COMPILE})

        self.syntax_error = None

    # handle subscribed events (semantic errors)
    def handle_event(self, event):
        if event.type_ is CompilerEvent.STOP_COMPILE:
            self.p_error(event.payload)

    def compile(self, data: str, debug=False):
        """
        Compiles a program.

        :param data: program to be compiled
        :param debug: shows compiled programs inner workings if true
        :return: output json file (ready to be executed by the Virtual Machine)
        """

        self._parser.parse(data, self.lexer, debug=False)

        if self._symbol_table.function_table.function_data_table.get("main") is None:
            self.handle_event(Event(CompilerEvent.STOP_COMPILE,
                              CompilerError("Main function is required")))

        if debug:
            self._display_tables()
            self._display_quads()
            self._symbol_table.class_table.display()

        return self._make_json()

    def _make_json(self):
        """ Makes output json with all the necessary data for execution in the Virtual Machine"""
        constant_table = self._symbol_table.constant_table
        quads = self._code_generator.get_output_quads()
        function_data = self._symbol_table.function_table.get_output_function_data()

        output = OutputFile(constant_table, function_data,
                            quads, self._allocator._segments[Layers.CONSTANT.value].end+1)
        return jsonpickle.encode(output)

    def _display_tables(self):
        self._symbol_table.function_table.display(debug=True)
        self._symbol_table.constant_table.display()

    def _display_quads(self):
        self._code_generator.display()

    # -- START -----------------------

    def p_program(self, p):
        """
        program : program1 program
                | program1
        """

    def p_program1(self, p):
        """
        program1 : body more_lines
                 | body
        """

    def p_more_lines(self, p):
        """
        more_lines : NLINE more_lines
                 | NLINE
        """

    def p_body(self, p):
        """
        body : class
             | function
             | declaration
        """

    # -- TOP LEVEL -----------------------

    def p_class(self, p):
        """
        class : CLASS ID add_class class_block end_class

        """
        #         | CLASS ID COLON ID class_block

    def p_add_class(self, p):
        """
        add_class :
        """
        self._symbol_table.class_table.add_class(p[-1])

    def p_end_class(self, p):
        """
        end_class :
        """
        self._symbol_table.class_table.end_class()

    def p_function(self, p):
        """
        function : FUNC ID add_function params set_void init_block end_function
                 | FUNC ID add_function params ARROW primitive init_block end_function
        """

    def p_declaration(self, p):
        """
        declaration : VAR ID add_variable COLON type
        """

    def p_class_declaration(self, p):
        """
        class_declaration : ID add_class_variable COLON class_type
        """

    def p_class_type(self, p):
        """
        class_type : INT set_class_variable_type
                   | BOOL set_class_variable_type
                   | FLOAT set_class_variable_type
                   | STRING set_class_variable_type
                   | ID set_class_object_type
        """

    def p_add_class_variable(self, p):
        """
        add_class_variable :
        """
        self._symbol_table.class_table.current_class.add_variable(p[-1])

    def p_set_class_object_type(self, p):
        """
        set_class_object_type :
        """
        class_data = self._symbol_table.class_table.classes[p[-1]]
        if class_data is None:
            self.handle_event(Event(CompilerEvent.STOP_COMPILE,
                              CompilerError("Class '" + p[-1] + "' not found")))

        self._symbol_table.class_table.current_class.set_type(
            ValueType.POINTER, p[-1])

    def p_set_class_variable_type(self, p):
        """
        set_class_variable_type :
        """
        type_ = ValueType(p[-1])
        self._symbol_table.class_table.current_class.set_type(type_, None)

    # -- PARAMS -----------------------

    def p_params(self, p):
        """
        params : LPAREN params1 RPAREN
               | LPAREN RPAREN
        """

    def p_params1(self, p):
        """
        params1 : param
                | param COMMA params1
        """

    def p_param(self, p):
        """
        param : ID add_param COLON primitive
        """

    # -- TYPE -----------------------

    def p_type(self, p):
        """
        type :  primitive
             | primitive array allocate_dimensions
             | ID set_type
        """

    def p_primitive(self, p):
        """
        primitive : INT     set_type
                  | FLOAT   set_type
                  | STRING  set_type
                  | BOOL    set_type
        """

    def p_array(self, p):
        """
        array : LBRACK INTLIT RBRACK add_dimension
              | LBRACK INTLIT RBRACK add_dimension array
        """

    # -- BLOCKS -----------------------

    def p_class_block(self, p):
        """
        class_block : LCURLY class_block1 RCURLY
        """

    def p_class_block1(self, p):
        """
        class_block1 : class_block2
                     | class_block3 class_block2
        """

    def p_class_block2(self, p):
        """
        class_block2 : NLINE class_block1
                     | NLINE
        """

    def p_class_block3(self, p):
        """
        class_block3 :  class_declaration
        """

        # removed function for now

    def p_init_block(self, p):
        """
        init_block : LCURLY init_block1 RCURLY
        """

    def p_init_block1(self, p):
        """
        init_block1 : init_block2
                    | init_block3 init_block2
        """

    def p_init_block2(self, p):
        """
        init_block2 : NLINE init_block1
                    | NLINE
        """

    def p_init_block3(self, p):
        """
        init_block3 : statement
                    | declaration
        """

    def p_block(self, p):
        """
        block : LCURLY block1 RCURLY
        """

    def p_block1(self, p):
        """
        block1 : block2
               | statement block2
        """

    def p_block2(self, p):
        """
        block2 : NLINE block1
               | NLINE
        """

    # -- STATEMENTS -----------------------

    def p_statement(self, p):
        """
        statement : display
                  | if
                  | while
                  | assign
                  | call return_type_warning
                  | return
                  | delete_heap_memory
        """

    def p_delete_heap_memory(self, p):
        """
        delete_heap_memory : DELETE ID 
        """
        var = self._symbol_table.function_table.get_variable(p[2])
        self._code_generator.object_actions.free_heap_memory(var)

    def p_return_type_warning(self, p):
        """
        return_type_warning :
        """
        id_ = self._symbol_table.function_table.current_function_call_id_
        type_ = self._symbol_table.function_table.functions[id_].type_
        if type_ is not ValueType.VOID:
            print(
                f'Warning, function {id_} returns {type_.value}, but is not unused')

    def p_while(self, p):
        """
        while : WHILE LPAREN save_loop_start bool_expr set_loop_condition RPAREN block fill_and_reset_loop
        """

    def p_input(self, p):
        """
        input : INPUT push_operator LPAREN STRINGLIT add_constant print_prompt RPAREN execute_builtin_call
        """

    def p_display(self, p):
        """
        display : PRINT push_operator LPAREN bool_expr RPAREN execute_builtin_call
        """

    def p_return(self, p):
        """
        return : RETURN
               | RETURN push_operator bool_expr set_return
        """

    def p_assign(self, p):
        """
        assign : assign1 ASSIGN other_assign
               | assign1 assign2 bool_expr execute_priority_0
               | assign1 assign2 input execute_priority_0
        """

    def p_resolve_object_(self, p):
        """
        resolve_object :
        """
        self._code_generator.object_actions.resolve()

    def p_other_assing(self, p):
        """
        other_assign : push_variable_class new_object verify_and_allocate_object

        """

    def p_new_object(self, p):
        """
        new_object : NEW ID verify_class_exists LPAREN RPAREN
        """

    def p_verify_and_allocate_object(self, p):
        """
        verify_and_allocate_object :
        """

        self._code_generator.object_actions.allocate_heap()

    def p_push_variable_class(self, p):
        """
        push_variable_class :
        """
        operand: Operand = self._code_generator.peak_operand()
        print(operand.address)

        var = self._symbol_table.function_table.get_id(address=operand.address)

        if var.class_id is None:
            self.handle_event(
                Event(CompileError, f'Cannot assign object {p[-1]} to primitive variable'))

        class_data = self._symbol_table.class_table.get_class(var.class_id)
        self._code_generator.object_actions.push_class_data(class_data)
        self._code_generator.object_actions.push_variable(var)

    def p_verify_class_exists(self, p):
        """
        verify_class_exists :
        """
        class_data = self._symbol_table.class_table.get_class(p[-1])
        if class_data is None:
            print(f'Class {p[-1]} does not exist')
            print('Error, class does not exist')
            self.handle_event(
                Event(CompileError, f'Class {p[-1]} does not exist'))

        self._code_generator.object_actions.push_class_data(class_data)

    #
    # def p_push_class_variable(self, p):
    #     """
    #     push_class_variable :
    #     """
    #     self._code_generator.object_actions.push_variable(p[-1])

    # def p_push_class_id(self, p):
    #     """
    #     push_class_id :
    #     """
    #
    #     # verify
    #     data = self._symbol_table.class_table.classes[p[-1]]
    #     if data is None:
    #         print('error')
    #         return
    #
    #     self._code_generator.object_actions.push_class_data(data)

    def p_assign1(self, p):
        """
        assign1 : ID push_variable
                | call_array
                | constant_object resolve_object

        """

    def p_constant_object(self, p):
        """
        constant_object : ID push_object PERIOD object_property
        """

    def p_push_object(self, p):
        """
        push_object :
        """
        self._code_generator.object_actions.set_parse_type(0)

        variable = self._symbol_table.function_table.get_variable(p[-1])
        if variable.class_id is None:
            self.handle_event(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'Variable {p[-1]} is not an object')))

        self._code_generator.object_actions.property_parent = variable
        self._code_generator.object_actions.push_object(variable)

    def p_assign2(self, p):  # TODO add rest to semantic cube
        """
        assign2 : ASSIGN push_operator
                | PASSIGN push_operator
                | LASSIGN push_operator
                | MASSIGN push_operator
                | DASSIGN push_operator
        """

    def p_call_array(self, p):
        """
        call_array : ID push_variable push_dimensions call_array1 get_array_pointer
        """

    def p_call_array1(self, p):
        """
        call_array1 : LBRACK expression verify_dimension RBRACK
                    | LBRACK expression verify_dimension RBRACK calculate_dimension call_array1
        """

    def p_calculate_dimension(self, p):
        """
        calculate_dimension :
        """
        self._code_generator.calculate_dimension()

    # Function Call ----------------------------------------------------------------------------------------------------

    # TODO update grammar diagram (added call_body, renamed call1 -> call_parameters
    def p_call(self, p):
        """
        call : ID verify_function_existence LPAREN gen_are_memory call_parameters RPAREN verify_param_count generate_go_sub
             | ID verify_function_existence LPAREN gen_are_memory RPAREN verify_param_count generate_go_sub
        """

    def p_call_parameters(self, p):
        """
        call_parameters : bool_expr verify_parameter_signature
              | bool_expr verify_parameter_signature COMMA increment_parameter_count call_parameters
        """

    # Call Actions ----------------------------------------------------------------

    def p_verify_function_existence(self, p):
        """
        verify_function_existence :
        """
        self._symbol_table.function_table.verify_function_exists(p[-1])

    def p_verify_param_count(self, p):
        """
        verify_param_count :
        """

        param_count = self._symbol_table.function_table.parameter_count
        signature_len = len(self._symbol_table.function_table.function_data_table[
            self._symbol_table.function_table.current_function_call_id_].parameter_signature)

        if param_count + 1 != signature_len and (signature_len != 0 and param_count == 0):
            print(param_count, signature_len)
            self.handle_event(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'Function Call Parameter Mistmatch {param_count} != {signature_len}')))

    def p_generate_go_sub(self, p):
        """
        generate_go_sub :
        """
        # TODO move to function table
        id_ = self._symbol_table.function_table.current_function_call_id_
        self._code_generator.function_actions.generate_go_sub(id_)

        # reset

    def p_gen_are_memory(self, p):
        """
        gen_are_memory :
        """
        self._symbol_table.function_table.generate_are_memory()
        self.p_push_operator('(')

    def p_verify_parameter_signature(self, p):
        """
        verify_parameter_signature :
        """
        # Todo add this into function directory
        func_table = self._symbol_table.function_table
        current_func = func_table.function_data_table[func_table.current_function_call_id_]

        if func_table.parameter_count >= len(current_func.parameter_signature):
            self.handle_event(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'Too many parameters for function {func_table.current_function_call_id_}')))

        param_type_ = current_func.parameter_signature[func_table.parameter_count]
        self._code_generator.function_actions.verify_parameter_type(param_type_, func_table.parameter_count)

    def p_increment_parameter_count(self, p):
        """
        increment_parameter_count :
        """
        func_table = self._symbol_table.function_table
        func_table.parameter_count += 1

    # --------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------------------------

    def p_if(self, p):
        """
        if : if_single
           | if_multiple
        """

    def p_if_single(self, p):  # allow single
        """
        if_single : IF LPAREN bool_expr RPAREN get_conditional block fill_end_single
        """

    def p_if_multiple(self, p):
        """
        if_multiple : IF LPAREN bool_expr RPAREN get_conditional block if_multiple_2
        """

    def p_if_multiple_2(self, p):  # force else at the end, less loop-holes, safer code
        """
        if_multiple_2 : fill_and_goto ELSE if_multiple
                      | fill_and_goto ELSE  block fill_end
        """

    # -- EXPRESSIONS -----------------------

    def p_bool_expr(self, p):
        """
        bool_expr : relational_exp execute_priority_1
                  | relational_exp execute_priority_1 AND push_operator bool_expr
                  | relational_exp execute_priority_1 OR push_operator bool_expr
        """

    # TODO Changed to relation_exp to prevent compiler panic. fix this
    def p_relational_exp(self, p):
        """
        relational_exp : expression execute_priority_2 comp relational_exp
                       | expression execute_priority_2
        """

    def p_expression(self, p):
        """
        expression : term execute_priority_3
                   | term execute_priority_3 PLUS push_operator expression
                   | term execute_priority_3 MINUS push_operator  expression
        """

    def p_term(self, p):
        """
        term : factor execute_priority_4
             | factor execute_priority_4 TIMES push_operator term
             | factor execute_priority_4 DIVIDE push_operator term
        """

    def p_factor(self, p):
        """
        factor : constant 
               | LPAREN push_operator bool_expr RPAREN push_operator
        """

    def p_constant(self, p):
        """
        constant : INTLIT    add_constant
                 | FLOATLIT  add_constant
                 | BOOLLIT   add_constant
                 | string
                 | call add_call_operator
                 | call_array
                 | constant2
                 | constant_object resolve_object
        """
        self._code_generator.object_actions.set_parse_type(1)

    def p_add_call_operator(self, p):
        """
        add_call_operator :
        """

        id_ = self._symbol_table.function_table.current_function_call_id_
        type_ = self._symbol_table.function_table.functions[id_].type_
        address = self._allocator.allocate_address(type_, Layers.TEMPORARY)

        self._code_generator.expression_actions.add_call_assign(address, type_)
        self.p_push_operator(')')

    def p_constant2(self, p):
        """
        constant2 : ID push_variable
        """

    def p_object_property(self, p):
        """
        object_property : ID push_object_property PERIOD object_property
                        | ID push_object_property
        """

    def p_push_object_property(self, p):
        """
        push_object_property :
        """

        self._code_generator.object_actions.push_object_property(p[-1])

    def p_comp(self, p):
        """
        comp : LESS push_operator
             | MORE push_operator
             | EQUALS push_operator
             | NEQUALS push_operator
             | LEQUALS push_operator
             | MEQUALS push_operator
        """

    def p_string(self, p):
        """
        string : string_expr
               | string_expr string
        """

    def p_string_expr(self, p):
        """
        string_expr : STRINGLIT add_constant
                    | BSLASH LPAREN expression RPAREN
        """

    # -- SEMANTIC ACTIONS -----------------------

    def p_add_function(self, p):
        """
        add_function :
        """
        self._symbol_table.function_table.add(
            p[-1], self._code_generator.get_next_quad())

    def p_set_void(self, p):
        """
        set_void :
        """
        self._symbol_table.function_table.current_function.set_type("Void")

    def p_validate_return(self, p):
        """
        set_return :
        """
        (self._symbol_table.function_table.set_return())

    def p_end_function(self, p):
        """
        end_function :
        """
        self._code_generator.execute_remaining()
        self._symbol_table.function_table.end_function()

    def p_add_constant(self, p):
        """
        add_constant :
        """
        (self._symbol_table.constant_table.add(p[-1], self._allocator))
        (self._code_generator.push_constant(
            p[-1], self._symbol_table.constant_table))

    def p_add_param(self, p):
        """
        add_param :
        """
        (self._symbol_table.function_table.add_variable(p[-1], is_param=True))

    def p_add_variable(self, p):
        """
        add_variable :
        """
        self._symbol_table.function_table.add_variable(p[-1], is_param=False)

    def p_add_dimension(self, p):
        """
        add_dimension :
        """
        print(p[-2])
        self._symbol_table.constant_table.add(p[-2], self._allocator)
        self._symbol_table.function_table.add_dimension(p[-2])

    def p_allocate_dimensions(self, p):
        """
        allocate_dimensions :
        """
        size = self._symbol_table.function_table.allocate_dimensions(self._allocator, self._symbol_table.constant_table)
        # self._code_generator.array_actions.initialize_array(size)

    def p_set_type(self, p):
        """
        set_type :
        """

        id_ = self._symbol_table.function_table.set_type(
            p[-1], self._allocator)
        # if id_ is not None:
        #    # TODO refactor
        #     variable = self._symbol_table.function_table.get_variable(id_)
        #     self._code_generator.push_variable(id_, variable.type_, variable.address_)

    # used to check on stack and execute quad operations
    def p_execute_priority_0(self, p):
        """
        execute_priority_0 :
        """
        (self._code_generator.execute_if_possible(0))

    # used to check on stack and execute quad operations
    def p_execute_builtin_call(self, p):
        """
        execute_builtin_call :
        """
        (self._code_generator.execute_builtin_call())

    def p_print_prompt(self, p):
        """
        print_prompt :
        """
        self._code_generator.push_operator(OperationType.PRINT)
        self._code_generator.execute_builtin_call()

    def p_execute_priority_1(self, p):
        """
        execute_priority_1 :
        """
        (self._code_generator.execute_if_possible(1))

    def p_execute_priority_2(self, p):
        """
        execute_priority_2 :
        """

        (self._code_generator.execute_if_possible(2))

    def p_execute_priority_3(self, p):
        """
        execute_priority_3 :
        """
        (self._code_generator.execute_if_possible(3))

    def p_execute_priority_4(self, p):
        """
        execute_priority_4 :
        """
        (self._code_generator.execute_if_possible(4))

    def p_get_conditional(self, p):
        """
        get_conditional :
        """
        self._code_generator.get_conditional()

    def p_fill_and_goto(self, p):
        """
        fill_and_goto :
        """
        self._code_generator.fill_and_goto()

    def p_fill_end(self, p):
        """
        fill_end :
        """
        self._code_generator.fill_end()

    def p_fill_end_single(self, p):
        """
        fill_end_single :
        """
        self._code_generator.fill_end_single()

    def p_save_loop_start(self, p):
        """
        save_loop_start :
        """
        self._code_generator.save_loop_start()

    def p_set_loop_condition(self, p):
        """
        set_loop_condition :
        """
        self._code_generator.set_loop_condition()

    def p_fill_and_reset_loop(self, p):
        """
        fill_and_reset_loop :
        """
        self._code_generator.fill_and_reset_loop()

    def p_push_operator(self, p):
        """
        push_operator :
        """
        self._code_generator.push_operator(p[-1])

    def p_push_variable(self, p):
        """
        push_variable :
        """
        variable = self._symbol_table.function_table.get_variable(p[-1])
        self._code_generator.push_variable(
            p[-1], variable.type_, variable.address_, variable.class_id)

    def p_push_dimensions(self, p):
        """
        push_dimensions :
        """
        # TODO: Clean this mess
        operand = self._code_generator.peak_operand()
        variable = self._symbol_table.function_table.get_id(operand.address)

        dimensions = []
        for dim_data in reversed(variable.dim_data_list):
            size = self._symbol_table.constant_table.get_from_value(dim_data.size)
            m = self._symbol_table.constant_table.get_from_value(dim_data.m)

            if m is None:
                dimension = Dimension(size_address=size.address)
            else:
                dimension = Dimension(size_address=size.address, m_address=m.address)

            dimensions.append(dimension)

        self._code_generator.push_dimensions(dimensions)

    def p_verify_dimension(self, p):
        """
        verify_dimension :
        """
        self._code_generator.verify_dimension()

    def p_get_array_pointer(self, p):
        """
        get_array_pointer :
        """
        self._code_generator.get_array_pointer()

    # -- ERROR -----------------------

    def p_error(self, p):
        # self.display_debug()

        error_message = 'Syntax error'
        if p:

            if type(p) is CompilerError:
                p.trace = self._symbol_table.function_table.current_trace()
                p.print()
            else:
                error_message += f': at token {p.type} ({p.value}) on line {p.lineno}'
                print(error_message)
        else:
            error_message += f': end of file'
            self.syntax_error = error_message
        sys.exit()

    def display_debug(self):
        self._symbol_table.constant_table.display()
        self._code_generator.display()
