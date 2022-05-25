import sys

from src.compiler.allocator.allocator import Allocator
from src.compiler.code_generator.code_generator import CodeGenerator
from src.compiler.code_generator.expression import Operator
from src.compiler.code_generator.type import OperationType
from src.compiler.errors import CompilerError, CompilerEvent
from src.compiler.lexer import lex, tokens
from src.compiler.ply import yacc
from .symbol_table import SymbolTable
from ..utils.observer import Subscriber


class Compiler(Subscriber):
    def __init__(self):
        self._allocator = Allocator()
        self._symbol_table = SymbolTable()

        self.tokens = tokens
        self.lexer = lex
        self._parser = yacc.yacc(module=self, start="program", debug=True)
        self._code_generator = CodeGenerator(scheduler=self._allocator)

        # subscribe symbol table to expression generator events
        self._code_generator.expression_actions.subscribe(self._symbol_table.function_table, {})

        # subscribe compiler receive semantic errors
        self._allocator.subscribe(self, {CompilerEvent.STOP_COMPILE})
        self._code_generator.expression_actions.subscribe(self, {CompilerEvent.STOP_COMPILE})
        self._symbol_table.function_table.subscribe(self, {CompilerEvent.STOP_COMPILE})
        self._symbol_table.function_table.current_function.get_variable_table.subscribe(
            self,
            {CompilerEvent.STOP_COMPILE})

        self.syntax_error = None

    # handle subscribed events (semantic errors)
    def handle_event(self, event):
        if event.type_ is CompilerEvent.STOP_COMPILE:
            self.p_error(event.payload)
            sys.exit()

    def compile(self, data: str, debug=False):
        return self._parser.parse(data, self.lexer, debug=False)

    def display_tables(self):
        self._code_generator.display()
        self._symbol_table.function_table.display(debug=True)
        self._symbol_table.constant_table.display()

    def display_quads(self):
        self._code_generator.display()

    # -- START -----------------------
    def p_program(self, p):
        """
        program : program1 program
                | program1
        """

    def p_program1(self, p):
        """
        program1 : body NLINE
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

    def p_function_error(self, p):
        """
        function : FUNC ID error init_block
        """

    def p_declaration(self, p):
        """
        declaration : variable ASSIGN push_operator bool_expr execute_priority_0
                    | variable ASSIGN array
                    | variable
        """

    def p_declaration_error(self, p):
        """
        declaration : variable error NLINE
        """

    def p_array(self, p):
        """
            array : LBRACK array1 RBRACK
            """

    def p_array1(self, p):
        """
        array1 : expression COMMA array1
               | expression
        """

    # -- PARAMS -----------------------

    def p_params(self, p):
        """
        params : LPAREN params1 RPAREN
               | LPAREN RPAREN
        """

    def p_params_error(self, p):
        """
        params : LPAREN error RPAREN
        """
        self._compiler_errors[
            -1].message = f'Expected valid parameres such as: "some_func( an_id: Int, other_id: Bool...)" or "some_func()"'

    def p_params1(self, p):
        """
        params1 : param
                | param COMMA params1
        """

    def p_params1_error(self, p):
        """
        params1 : error COMMA params1
        """

    def p_param(self, p):
        """
        param : ID add_param COLON primitive
        """

    # def p_param_error(self, p):
    #     """
    #     param : ID error primitive
    #           | error COLON primitive
    #           | error primitive
    #     """
    #     if p[2] == ':':
    #         self.compiler_errors[-1].message = f'Missing identifier before colon "{p[1]}"'
    #     elif type(p[1]) is str:
    #         self.compiler_errors[-1].message = f'Missing Colon:  {p[1]} : <-- add here'
    #     else:
    #         self.compiler_errors[-1].message = f'Invalid param declaration: "{p[1]}"'
    #

    # self.compiler.restart()

    #     print('received ', p[1], p[2], p[3])
    #     print(self.compiler.token())
    #     if p[2] != ':':
    #         print(f' Missing type separator, add semicolon "{p[1]} {p[2].value}" --> "{p[1]} : {p[2].value}"')
    #         self.recover("COMMA")
    #     elif type(p[1]) is not str and p[1].value == ':':
    #         print('error here')
    #         # self.compiler_errors[
    #         #     1].message = f' Missing identifier: Add id before colon " empty :" --> variable_name : ..."',
    #

    def p_param_error(self, p):
        """
        param : ID error primitive
              | error COLON primitive
        """

        if p[2] != ':':
            print(f' Missing type separator, add semicolon "{p[1]} {p[2].value}" --> "{p[1]} : {p[2].value}"')
            self.recover("RCURLY")
        elif type(p[1]) is not str and p[1].value == ':':
            print(f' Missing identifier: Add id before colon " empty :" --> variable_name : ..."')
            self.recover({"RCURLY"})

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
                  | call
                  | return
        """

    def p_while(self, p):
        """
        while : WHILE LPAREN save_loop_start bool_expr set_loop_condition RPAREN block fill_and_reset_loop
        """

    def p_input(self, p):
        """
        input : variable ASSIGN INPUT LPAREN string RPAREN
        """

    def p_display(self, p):
        """
        display : PRINT push_operator LPAREN bool_expr RPAREN execute_builtin_call
        """

    def p_return(self, p):
        """
        return : RETURN
               | RETURN push_operator bool_expr execute_priority_function
        """

    def p_assign(self, p):
        """
        assign : ID push_variable assign1 bool_expr execute_priority_0
        """

    def recover(self, token_set=None):  # Future error handling
        while True:
            tok = self._parser.token()
            if not tok or tok.type in token_set:
                break
        return tok

    def p_assign1(self, p):  # TODO add rest to semantic cube
        """
            assign1 : ASSIGN push_operator
                    | PASSIGN
                    | LASSIGN
                    | MASSIGN
                    | DASSIGN
            """

    def p_call(self, p):
        """
        call : ID LPAREN call1 RPAREN
        """

    def p_call1(self, p):
        """
        call1 : expression
              | expression COMMA call1
        """

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

    def p_call_array(self, p):
        """
            call_array : ID LBRACK expression RBRACK
            """

    def p_constant(self, p):
        """
        constant : INTLIT    add_constant
                 | FLOATLIT  add_constant
                 | BOOLLIT   add_constant
                 | string
                 | call
                 | call_array
                 | constant2
        """

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

    # -- VARIABLES -----------------------

    def p_variable(self, p):
        """
        variable : VAR ID add_var COLON type
        """

    def p_variable_error(self, p):
        """
        variable : VAR ID error type
        """
        self._compiler_errors[-1].message = f'Invalid expression near "{p[3].value}"'

    def p_variable_error_1(self, p):
        """
        variable : VAR ID add_var COLON error NLINE
        """
        self._compiler_errors[-1].message = f'Invalid expression near "{p[3].value}"'

    def p_type(self, p):
        # TODO: might need to remove the array of custom types
        """
            type : primitive
                 | LBRACK primitive RBRACK
                 | LBRACK ID RBRACK
            """

    def p_primitive(self, p):
        """
        primitive : INT     set_variable_type
                  | FLOAT   set_variable_type
                  | STRING  set_variable_type
                  | BOOL    set_variable_type
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

    def p_end_function(self, p):
        """
        end_function :
        """
        (self._code_generator.execute_remaining())
        (self._symbol_table.function_table.end_function(memory=self._allocator))

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
        (self._symbol_table.function_table.add_variable(p[-1], True))

    def p_add_var(self, p):
        """
        add_var :
        """
        (self._symbol_table.function_table.add_variable(p[-1], False))

    def p_execute_priority_function(self, p):  # used to check on stack and execute quad operations
        """
        execute_priority_function :
        """
        return_address = self._code_generator.peek_operands().address
        return_type = self._allocator.get_type(address=return_address)
        print(return_address)
        # print(return_type)
        self._symbol_table.function_table.check_return(return_type)
        self._code_generator.execute_if_possible(-1)

    def p_execute_priority_0(self, p):  # used to check on stack and execute quad operations
        """
        execute_priority_0 :
        """
        self._code_generator.execute_if_possible(0)

    def p_execute_builtin_call(self, p):  # used to check on stack and execute quad operations
        """
        execute_builtin_call :
        """
        self._code_generator.execute_builtin_call()

    def p_execute_priority_1(self, p):
        """
        execute_priority_1 :
        """
        self._code_generator.execute_if_possible(1)

    def p_execute_priority_2(self, p):
        """
        execute_priority_2 :
        """

        self._code_generator.execute_if_possible(2)

    def p_execute_priority_3(self, p):
        """
        execute_priority_3 :
        """
        self._code_generator.execute_if_possible(3)

    def p_execute_priority_4(self, p):
        """
        execute_priority_4 :
        """
        self._code_generator.execute_if_possible(4)

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
        priority = -1

        if type_ in {OperationType.ASSIGN}:
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
        self._code_generator.push_operator(operator)

    def p_push_variable(self, p):
        """
         push_variable :
        """
        address, type_ = self._symbol_table.function_table.find(p[-1])
        self._code_generator.push_variable(p[-1], type_, address)

    def p_set_variable_type(self, p):
        """
        set_variable_type :
        """

        id_ = self._symbol_table.function_table.set_variable_type(p[-1], self._allocator)
        if id_ is not None:
            address, type_ = self._symbol_table.function_table.find(id_)
            self._code_generator.push_variable(id_, type_, address)

    # -- ERROR -----------------------

    def p_error(self, p):
        self.display_tables()
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

    def display_debug(self):
        self.display_tables()
    #
    # def p_error(self, p):
    #     if p is None:
    #         token = "end of file"
    #         print("end of file")
    #         return token
    #     else:
    #         line_start = self.data.rfind('\n', 0, p.lexpos) + 1
    #         col = (p.lexpos - line_start) + 1
    #         # (
    #         # self.recover({"RCURLY"})
    #         self.compiler_errors.append(CompilerError(
    #             "Unexpected " + str(p.value),
    #             f'({p.lineno}:{col})',
    #             self.symbol_table.current_trace()
    #         ))
    #
    #         self.recover({"}"})
    #         self.compiler.errok()
