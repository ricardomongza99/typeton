import functools
from typing import List

from src.directory import FunctionTable
from src.directory.constants import ConstantTable
from src.lexer import lex, tokens
from src.parser.errors import CompilerError
from src.ply import yacc
from src.semantic.expression import Operator
from src.semantic.generator import QuadGenerator
from src.semantic.quadruple import OperationType
from src.virtual.compilation import Scheduler


def semantic_action(func):
    @functools.wraps(func)
    def wrapper(self, p):
        if len(self.compiler_errors) == 0:
            return func(self, p)
        return

    return wrapper


class Parser:
    def __init__(self):
        self.data = None
        self.tokens = tokens
        self.compiler_errors: List[CompilerError] = []
        self.memory = Scheduler()
        self.directory = FunctionTable()  # potentially = Directory(memory, cube)

        self.lexer = lex
        self.constant_table = ConstantTable()
        self.quadGenerator = QuadGenerator(scheduler=self.memory, directory=self.directory)
        self.tokens = tokens
        self.parser = yacc.yacc(module=self, start="program", debug=True)

    def should_run(self):
        return not len(self.compiler_errors) > 1

    def print_compiler_errors(self):
        for err in self.compiler_errors:
            err.print()

    def display_function_directory(self):
        self.directory.display(debug=True)

    def parse(self, data: str, debug=False):
        self.data = data
        self.parser.parse(data, self.lexer, debug=debug)

    # parser begin
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
        function : FUNC ID add_function params ARROW function_return_type init_block end_function
        """

    def p_declaration(self, p):
        """
        declaration : variable ASSIGN push_operator bool_expr execute_priority_0
                    | variable ASSIGN array
                    | variable
        """

    def p_declaration_error(self, p):
        """
        declaration : variable ASSIGN push_operator error execute_priority_0
        """
        self.compiler_errors[-1].message = f'Invalid expression near "{p[3].value}"'

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

    def p_params1(self, p):
        """
        params1 : param
                | param COMMA params1
        """

    def p_param(self, p):
        """
        param : ID add_var COLON type set_variable_type
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
        display : PRINT LPAREN expression RPAREN
        """

    def p_return(self, p):
        """
        return : RETURN
               | RETURN bool_expr
        """

    def p_assign(self, p):
        """
        assign : ID push_variable assign1 bool_expr execute_priority_0
        """

    def p_assign_error_1(self, p):
        """
        assign : ID push_variable error execute_priority_0
        """
        self.compiler_errors.append(CompilerError(f'Invalid assigment after "{p[1]}"'))

    def p_assign_error(self, p):
        """
        assign : ID push_variable assign1 error execute_priority_0
        """
        self.compiler_errors.append(CompilerError(f'Invalid Expression after "{p[1]} = "'))

    def recover(self, token_set=None):  # Future error handling
        while True:
            tok = self.parser.token()
            if tok is not None:
                print(tok)
            if not tok or (token_set is None or tok.type in token_set):
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

    def p_relational_exp(self, p):  # TODO Changed to relation_exp to prevent parser panic. fix this
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

    def p_term_error(self, p):
        """
        term : factor execute_priority_4 TIMES error push_operator term
             | factor execute_priority_4 DIVIDE error push_operator term

        """
        self.compiler_errors[-1].message = f'Expected valid expression after "{p[3]}"'

    def p_factor(self, p):
        """
            factor : constant
                   | LPAREN push_operator bool_expr RPAREN push_operator
            """

    def p_factor_error(self, p):
        """
        factor : LPAREN push_operator error RPAREN push_operator
        """
        self.compiler_errors[-1].message = f'Invalid expression near "{p[3].value}"'

    def p_execute_remaining(self, p):
        """
        execute_remaining :
        """
        self.quadGenerator.execute_remaining()

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
        self.compiler_errors[-1].message = f'Invalid expression near "{p[3].value}"'

    def p_variable_error_1(self, p):
        """
        variable : VAR ID add_var COLON error NLINE
        """
        self.compiler_errors[-1].message = f'Invalid expression near "{p[3].value}"'

    def p_type(self, p):
        # TODO: might need to remove the array of custom types
        """
            type : variable_primitive
                 | LBRACK variable_primitive RBRACK
                 | LBRACK ID RBRACK
            """

    def p_function_return_type(self, p):
        """
       function_return_type : INT set_function_type
                 | FLOAT   set_function_type
                 | STRING  set_function_type
                 | BOOL    set_function_type
                 | VOID    set_function_type
       """

    def p_variable_primitive(self, p):
        """
        variable_primitive : INT    set_variable_type
                  | FLOAT           set_variable_type
                  | STRING          set_variable_type
                  | BOOL            set_variable_type
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

    @semantic_action
    def p_add_function(self, p):
        """
        add_function :
        """
        self.directory.add(p[-1])

    def handle_error(self, possible_error):
        if type(possible_error) == list:
            for err in possible_error:
                if err is not None and type(err) is CompilerError:
                    err.trace = self.directory.current_trace()
                    self.compiler_errors.append(err)
        elif possible_error is not None and type(possible_error) is CompilerError:
            possible_error.trace = self.directory.current_trace()
            self.compiler_errors.append(possible_error)
        return possible_error

    @semantic_action
    def p_end_function(self, p):
        """
        end_function :
        """

        self.handle_error(self.quadGenerator.execute_remaining())
        self.handle_error(self.directory.end_function(memory=self.memory))

    @semantic_action
    def p_add_constant(self, p):
        """
        add_constant :
        """
        self.handle_error(self.constant_table.add(p[-1], self.memory))
        self.handle_error(self.quadGenerator.push_constant(p[-1], self.constant_table))

    @semantic_action
    def p_add_var(self, p):
        """
        add_var :
        """
        # if self.should_run():
        self.handle_error(self.directory.add_variable(p[-1]))

    @semantic_action
    def p_execute_priority_0(self, p):  # used to check on stack and execute quad operations
        """
        execute_priority_0 :
        """
        self.handle_error(self.quadGenerator.execute_remaining())

    @semantic_action
    def p_execute_priority_1(self, p):
        """
        execute_priority_1 :
        """

        self.handle_error(self.quadGenerator.execute_if_possible(1))

    @semantic_action
    def p_execute_priority_2(self, p):
        """
        execute_priority_2 :
        """

        self.handle_error(self.quadGenerator.execute_if_possible(2))

    @semantic_action
    def p_execute_priority_3(self, p):
        """
        execute_priority_3 :
        """
        self.handle_error(self.quadGenerator.execute_if_possible(4))

    @semantic_action
    def p_execute_priority_4(self, p):
        """
        execute_priority_4 :
        """

        self.handle_error(self.quadGenerator.execute_if_possible(4))

    @semantic_action
    def p_set_function_type(self, p):
        """
        set_function_type :
        """

        self.handle_error(self.directory.set_function_type(p[-1]))

    @semantic_action
    def p_get_conditional(self, p):
        """
        get_conditional :
        """
        self.quadGenerator.get_conditional()

    @semantic_action
    def p_fill_and_goto(self, p):
        """
        fill_and_goto :
        """
        self.quadGenerator.fill_and_goto()

    @semantic_action
    def p_fill_end(self, p):
        """
        fill_end :
        """
        self.quadGenerator.fill_end()

    @semantic_action
    def p_fill_end_single(self, p):
        """
        fill_end_single :
        """
        self.quadGenerator.fill_end_single()

    @semantic_action
    def p_save_loop_start(self, p):
        """
        save_loop_start :
        """
        self.quadGenerator.save_loop_start()

    @semantic_action
    def p_set_loop_condition(self, p):
        """
        set_loop_condition :
        """
        self.quadGenerator.set_loop_condition()

    @semantic_action
    def p_fill_and_reset_loop(self, p):
        """
        fill_and_reset_loop :
        """
        self.quadGenerator.fill_and_reset_loop()

    @semantic_action
    def p_push_operator(self, p):
        """
        push_operator :
        """

        # TODO move all this garbage into a helper function
        type_ = OperationType(p[-1])
        priority = 0

        if type_ is OperationType.ASSIGN:
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
        self.handle_error(self.quadGenerator.push_operator(operator))

    @semantic_action
    def p_push_variable(self, p):
        """
         push_variable :
        """
        self.handle_error(self.quadGenerator.push_variable(p[-1]))

    @semantic_action
    def p_set_variable_type(self, p):
        """
        set_variable_type :
        """

        id_ = self.handle_error(self.directory.set_variable_type(p[-1], memory=self.memory))
        if id_ is not None:
            self.handle_error(self.quadGenerator.push_variable(id_))

    # -- ERROR -----------------------

    def p_error(self, p):
        if p is None:
            token = "end of file"
            print("end of file")
        else:
            token = self.recover({"NLINE"})
            line_start = self.data.rfind('\n', 0, p.lexpos) + 1
            col = (p.lexpos - line_start) + 1

            self.handle_error(
                CompilerError("Unexpected " + str(p.value), f'({p.lineno}:{col})', self.directory.current_trace()))
            return token

    def display_debug(self):
        self.constant_table.display()
