import sys

import jsonpickle

from src.compiler.allocator.allocator import Allocator
from src.compiler.allocator.helpers import Layers
from src.compiler.allocator.types import ValueType
from src.compiler.code_generator.code_generator import CodeGenerator
from src.compiler.code_generator.expression import Operator
from src.compiler.code_generator.type import OperationType
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.lexer import lex, tokens
from src.compiler.ply import yacc
from .output import OutputFile
from .symbol_table import SymbolTable
from ..utils.observer import Subscriber, Event, Publisher


class Compiler(Publisher, Subscriber):
    def __init__(self):
        super().__init__()

        self._allocator = Allocator()
        self._symbol_table = SymbolTable()

        self.tokens = tokens
        self.lexer = lex
        self._parser = yacc.yacc(module=self, start="program", debug=True)
        self._code_generator = CodeGenerator(scheduler=self._allocator)

        # subscribe to expression code generator
        expressions = self._code_generator.expression_actions
        expressions.add_subscriber(self._symbol_table.function_table, {})
        expressions.add_subscriber(self._allocator, {})

        # subscribers for function table
        functions = self._symbol_table.function_table
        functions.add_subscriber(self._code_generator.function_actions, {})
        functions.add_subscriber(self._code_generator.expression_actions, {})
        functions.add_subscriber(self._allocator, {})

        # subscribe to compiler events
        self.add_subscriber(self._code_generator.function_actions, {})
        self.add_subscriber(self._symbol_table.function_table, {})

        # subscribe compiler to error messages
        self._allocator.add_subscriber(self, {CompilerEvent.STOP_COMPILE})
        self._code_generator.expression_actions.add_subscriber(self, {CompilerEvent.STOP_COMPILE})
        self._symbol_table.function_table.add_subscriber(self, {CompilerEvent.STOP_COMPILE})

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
            self.handle_event(Event(CompilerEvent.STOP_COMPILE, "Main function is required"))

        if debug:
            self._display_tables()
            self._display_quads()

        return self._make_json()

    def _make_json(self):
        """ Makes output json with all the necessary data for execution in the Virtual Machine"""
        constant_table = self._symbol_table.constant_table
        quads = self._code_generator.get_output_quads()
        function_data = self._symbol_table.function_table.get_output_function_data()

        output = OutputFile(constant_table, function_data, quads)
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
        class : CLASS ID class_block
              | CLASS ID COLON ID class_block
        """

    def p_function(self, p):
        """
        function : FUNC ID add_function params set_void init_block end_function
                 | FUNC ID add_function params ARROW primitive init_block end_function
        """

    def p_declaration(self, p):
        """
        declaration : VAR ID add_variable COLON type
        """

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
        type : ID
             | primitive
             | primitive array allocate_dimensions
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
        class_block3 : function
                     | declaration
        """

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
                  | input
                  | assign
                  | call return_type_warning
                  | return
        """

    def p_return_type_warning(self, p):
        """
        return_type_warning :
        """
        id_ = self._symbol_table.function_table.current_function_call_id_
        type_ = self._symbol_table.function_table.functions[id_].type_
        if type_ is not ValueType.VOID:
            print(f'Warning, function {id_} returns {type_.value}, but is not unused')

    def p_while(self, p):
        """
        while : WHILE LPAREN save_loop_start bool_expr set_loop_condition RPAREN block fill_and_reset_loop
        """

    def p_input(self, p):
        """
        input : INPUT LPAREN string RPAREN
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
        assign : assign1 ASSIGN input
               | assign1 assign2 bool_expr execute_priority_0
        """

    def p_assign1(self, p):
        """
        assign1 : ID push_variable
                | ID push_variable push_dimensions call_array
        """

    def p_assign2(self, p):  # TODO add rest to semantic cube
        """
        assign2 : ASSIGN push_operator
                | PASSIGN
                | LASSIGN
                | MASSIGN
                | DASSIGN
        """

    def p_call_array(self, p):
        """
        call_array : LBRACK expression verify_dimension RBRACK
                   | LBRACK expression verify_dimension RBRACK call_array
        """

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
        param_count = self._symbol_table.function_table.parameter_count + 1
        signature_len = len(self._symbol_table.function_table.function_data_table[
                                self._symbol_table.function_table.current_function_call_id_].parameter_signature)

        if param_count != signature_len:
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

    def p_relational_exp(self, p):  # TODO Changed to relation_exp to prevent compiler panic. fix this
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
                 |  call add_call_operator
                 | call_array
                 | constant2
        """

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
                  | ID PERIOD constant2
        """

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
        self._symbol_table.function_table.add(p[-1], self._code_generator.get_next_quad())

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
        (self._code_generator.push_constant(p[-1], self._symbol_table.constant_table))

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
        self._symbol_table.constant_table.add(p[-2], self._allocator)
        self._symbol_table.function_table.add_dimension(p[-2])

    def p_allocate_dimensions(self, p):
        """
        allocate_dimensions :
        """
        self._symbol_table.function_table.allocate_dimensions(self._allocator)

    def p_set_type(self, p):
        """
        set_type :
        """

        id_ = self._symbol_table.function_table.set_type(p[-1], self._allocator)
        if id_ is not None:
            # TODO refactor
            variable = self._symbol_table.function_table.get_variable(id_)
            self._code_generator.push_variable(id_, variable.type_, variable.address_)

    def p_execute_priority_0(self, p):  # used to check on stack and execute quad operations
        """
        execute_priority_0 :
        """
        (self._code_generator.execute_if_possible(0))

    def p_execute_builtin_call(self, p):  # used to check on stack and execute quad operations
        """
        execute_builtin_call :
        """
        (self._code_generator.execute_builtin_call())

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

        # TODO move all this garbage into a helper function
        type_ = OperationType(p[-1])
        priority = 0

        if type_ is {OperationType.ASSIGN}:
            priority = 0
        elif type_ in {OperationType.AND, OperationType.OR}:
            priority = 1
        elif type_ in {OperationType.GREAT_THAN,
                       OperationType.EQUAL,
                       OperationType.LESS_THAN,
                       OperationType.LESS_EQUAL,
                       OperationType.GREAT_EQUAL}:
            priority = 2
        elif type_ in {OperationType.ADD, OperationType.SUBTRACT}:
            priority = 3

        elif type_ in {OperationType.MULTIPLY, OperationType.DIVIDE}:
            priority = 4

        operator = Operator(priority, type_)
        (self._code_generator.push_operator(operator))

    def p_push_variable(self, p):
        """
        push_variable :
        """
        variable = self._symbol_table.function_table.get_variable(p[-1])
        self._code_generator.push_variable(p[-1], variable.type_, variable.address_)

    def p_push_dimensions(self, p):
        """
        push_dimensions :
        """
        operand = self._code_generator.peak_operand()
        id_ = self._symbol_table.function_table.get_id(operand.address)
        variable = self._symbol_table.function_table.get_variable(id_)
        # TODO: Code generator

    def p_verify_dimension(self, p):
        """
        verify_dimension :
        """
        # TODO: Code generator

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
