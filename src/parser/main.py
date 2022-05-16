import src
from src.ply import yacc
from src.lexer.main import lex, tokens
from src.directory.dir_func import DirFunc
from src.semantic.main import Cube
from src.virtual.memory import Memory


# maybe should be named compiler?
class Parser:
    def __init__(self):
        self.tokens = tokens
        self.cube = Cube()
        self.memory = Memory()
        self.lexer = lex
        self.dir_func = DirFunc()  # potentially = DirFunc(memory, cube)
        self.parser = yacc.yacc(module=self, start="program")

    def display_function_directory(self):
        self.dir_func.display(debug=True)

    def parse(self, file):
        self.parser.parse(file, self.lexer, debug=True)

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
        function : FUNC ID add_function params init_block
                 | FUNC ID add_function params ARROW will_set_type primitive init_block
        """

    def p_declaration(self, p):
        """
        declaration : variable ASSIGN expression
                    | variable ASSIGN array
                    | variable
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

    def p_params1(self, p):
        """
        params1 : param
                | param COMMA params1
        """

    def p_param(self, p):
        """
        param : ID add_var COLON will_set_type type
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
        while : WHILE LPAREN bool_expr RPAREN block
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
        assign : ID assign1 expression
        """

    def p_assign1(self, p):
        """
        assign1 : ASSIGN
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
        if : IF LPAREN bool_expr RPAREN block
           | IF LPAREN bool_expr RPAREN block if2
        """

    def p_if2(self, p):
        """
        if2 : ELSE if
            | ELSE block
        """

    # -- EXPRESSIONS -----------------------

    def p_bool_expr(self, p):
        """
        bool_expr : relational_exp
                  | relational_exp AND bool_expr
                  | relational_exp OR bool_expr
        """

    def p_relational_exp(self, p):
        """
        relational_exp : expression comp expression
                       | expression
        """

    def p_comp(self, p):
        """
        comp : LESS
             | MORE
             | EQUALS
             | NEQUALS
             | LEQUALS
             | MEQUALS
        """

    def p_expression(self, p):
        """
        expression : term
                   | term PLUS term
                   | term MINUS term
        """

    def p_term(self, p):
        """
        term : factor
             | factor TIMES factor
             | factor DIVIDE factor
        """

    def p_factor(sefl, p):
        """
        factor : constant
               | COLON LPAREN expression RPAREN
        """

    def p_call_array(self, p):
        """
        call_array : ID LBRACK expression RBRACK
        """

    def p_constant(self, p):
        """
        constant : constant2
                 | NUMBER
                 | FLOATLIT
                 | TRUE
                 | FALSE
                 | string
                 | call
                 | call_array
        """

    def p_constant2(self, p):
        """
        constant2 : ID
                  | ID PERIOD constant2
        """

    # Sorry Paco, I changed the 'DOT' Token to 'PERIOD' and commented out
    # this chunk of code. Maybe you are right, for now, let's just keep it simple :)
    #
    # def p_dots(p):
    #     # we might need this kind of syntax for easier semantic eval
    #     '''
    #     dots : ID
    #          | repeat_dots
    #     '''
    #
    #
    # def p_repeat_dots(p):
    #     ''' repeat_dots : ID DOT right_id'''
    #
    #
    # def p_right_id(p):
    #     ''' right_id : ID
    #         | repeat_dots'''

    # -- VARIABLES -----------------------

    def p_variable(self, p):
        """
        variable : VAR ID add_var
                 | VAR ID add_var COLON will_set_type type
        """

    def p_type(self, p):
        # TODO: might need to remove the array of custom types
        """
        type : ID
             | primitive
             | LBRACK primitive RBRACK
             | LBRACK ID RBRACK
        """

    def p_primitive(self, p):
        """
        primitive : INT     set_type
                  | FLOAT   set_type
                  | STRING  set_type
                  | BOOL    set_type
        """

    def p_string(self, p):
        """
        string : string_expr
               | string_expr string
        """

    def p_string_expr(self, p):
        """
        string_expr : STRINGLIT
                    | BSLASH LPAREN expression RPAREN
        """

    # -- SEMANTIC ACTIONS -----------------------

    def p_add_function(self, p):
        """
        add_function :
        """
        self.dir_func.add(p[-1])

    def p_add_var(self, p):
        """
        add_var :
        """
        self.dir_func.add_var(p[-1])

    def p_will_set_type(self, p):
        """
        will_set_type :
        """
        self.dir_func.will_set_type(p[-1])

    def p_set_type(self, p):
        """
        set_type :
        """
        self.dir_func.set_type(p[-1])

    # -- ERROR -----------------------

    def p_error(self, p):
        if p is None:
            token = "end of file"
        else:
            token = f"{p.type}({p.value}) on line {p.lineno}"

        print(f"Syntax error: Unexpected {token}")
