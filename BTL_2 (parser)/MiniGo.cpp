grammar MiniGo;

// ast 1

@lexer::header {
from lexererr import *
}


@lexer::members {
def __init__(self, input=None, output:TextIO = sys.stdout):
    super().__init__(input, output)
    self.checkVersion("4.9.2")
    self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
    self._actions = None
    self._predicates = None
    self.preType = None

def emit(self):
    tk = self.type
    self.preType = tk;
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}


options{
	language = Python3;
}

// task 1
// program: (CONST ID ASSIGN expression SEMICOLON) EOF;

program: dec_list EOF;
dec_list: declared dec_list | declared;


// ! ---------------- PARSER 1 ----------------------- */
// ! ---------------- PARSER 1 ----------------------- */
//TODO Literal 6.6 pdf
literal:
	INT_LIT
	| FLOAT_LIT
	| STRING_LIT
	| NIL
	| TRUE
	| FALSE
	| array_literal
	| struct_literal;

primitive_types: INT | FLOAT | BOOLEAN | STRING;
type_withID: primitive_types | type_array | ID;
// composite_types: STRUCT;
literal_primitive: INT_LIT | FLOAT_LIT | STRING_LIT | TRUE | FALSE | NIL;

sub_inside_array_lit: LB sub_inside_array_lit RB
				| sub_inside_array_lit COMMA sub_inside_array_lit
				| ID
				| literal_primitive
				| struct_literal;
inside_array_lit: LB sub_inside_array_lit RB inside_array_lit | sub_inside_array_lit;

// 6.6.1
sub_type_array: LSB (INT_LIT | ID) RSB sub_type_array | LSB (INT_LIT | ID) RSB;	// [1][2]
type_array: sub_type_array (primitive_types | STRUCT | ID);			// [1][2]string
array_literal: type_array LB inside_array_lit RB;				//[3]int{10, 20, 30}


// 6.6.2 
struct_literal: ID LB struct_list_element? RB;
struct_list_element: ID COLON expression (COMMA struct_list_element)?;

// part 4 tien pdf
// Newline có thể được dùng làm biểu thức kết thúc của một số đoạn code
endcode: SEMICOLON | NEWLINE;

// TODO 5.2 Expressions 6 pdf
list_expression: expression COMMA list_expression | expression;
expression: expression OR expression1 | expression1;                                                        // ||
expression1: expression1 ANDAND expression2 | expression2;                                                  // &&
expression2: expression2 (EQUALEQUAL | NOEQUAL | L | LEQUAL | R | REQUAL) expression3 | expression3;        // ==, !=, <, <=, >, >=
expression3: expression3 (ADD | SUB) expression4 | expression4;                                             // +, - (binary)
expression4: expression4 (MUL | DIV | DIVDIV) expression5 | expression5;                                    // *, /, % 
expression5: (NOSIG | SUB) expression5 | expression6;                                                       // !, - (unary)
expression6:
    expression6 LSB expression RSB
    | expression6 DOT ID
    | expression6 DOT ID LP list_expression? RP
    | expression7;
expression7: ID
			| literal
			| LP expression RP
			| ID LP list_expression? RP;
// ! ---------------- PARSER 1 ----------------------- */
// ! ---------------- PARSER 1 ----------------------- */


// ! ---------------- PARSER 2 ----------------------- */
// ! ---------------- PARSER 2 ----------------------- */
declared:
	variables_declared
	| constants_declared
	| function_declared
	| method_declared
	| struct_declared
	| interface_declared;

// variables_declared 5.1
variables_declared: (declared_init | declared_no_init) endcode;
declared_init: VAR ID type_withID? ASSIGN (expression | lhs) ;
declared_no_init: VAR ID type_withID;

// constants_declared 5.2
constants_declared: CONST ID ASSIGN expression endcode;

// function_declared 5.3
// (endcode | EOF)
function_declared: FUNC (a_func) type_withID? LB (inside_part_func)? RB endcode;
a_func: ID LP func_para_list? RP;
func_para_list: param COMMA func_para_list | param ;
param: list_ID type_withID COMMA param | list_ID type_withID;
list_ID: ID COMMA list_ID | ID;
inside_part_func: (statement endcode | declared) inside_part_func
				| (statement endcode | declared);

// method_declared 5.3
method_declared: FUNC (LP ID ID RP) (a_func) type_withID? LB (inside_part_func)? RB endcode;
// struct_type 4.6
struct_declared: TYPE ID STRUCT LB inside_part_struct_type RB endcode;
inside_part_struct_type: (ID type_withID endcode) inside_part_struct_type
						| (ID type_withID endcode);

// interface_type 4.7
// type Votien interface {
//      Add(x, y int) int; 
// }
interface_declared: TYPE ID INTERFACE LB inside_part_interface RB endcode;
inside_part_interface: (sub_inside_part_interface) inside_part_interface
					| (sub_inside_part_interface);
// Add(x, y int) int; 
sub_inside_part_interface: ID LP (interface_para_list)? RP type_withID? endcode;
interface_para_list: param_interface COMMA interface_para_list | param_interface;
param_interface: list_ID_interface type_withID COMMA param_interface | list_ID_interface type_withID;
list_ID_interface: ID COMMA list_ID_interface | ID;

// part 5 tien: a scalar variables_declared
// scalar_variable: ID;

//TODO Statement 5 and 4 pdf
list_statement: statement list_statement | statement;
statement:
	(
		declared_statement
		| assign_statement
		| if_statement
		| for_statement
		| break_statement
		| continue_statement
		| call_statement
		| return_statement
	);
// pdf thay 7.1 Variable and Constant Declaration Statement
declared_statement: variables_declared | constants_declared;

// pdf thay 7.2 Assignment Statement
assign_op: COLONEQUAL | ADDEQUAL | SUBEQUAL | MULEQUAL | DIVEQUAL | DIVDIVEQUAL;
assign_statement: lhs assign_op rhs;

index: LSB expression RSB;
lhs: lhs (DOT ID index)
		| lhs (DOT ID)
		| lhs index
		| ID;					//a[2].b.c[2]

rhs: expression;


// pdf thay 7.3 If Statement
if_statement: IF expression LB (inside_part_func)? RB (elif_part)? (else_part)?;
elif_part: ELSE IF expression LB (inside_part_func)? RB elif_part
		| ELSE IF expression LB (inside_part_func)? RB;
else_part: ELSE LB (inside_part_func)? RB;

// pdf thay 7.4 For Statement in MiniGo
for_assign: ID assign_op expression;		// x := 1
for_statement: for_basic | for_init_cond | for_range;
for_basic: FOR (expression) LB (inside_part_func)? RB;
for_init_cond: FOR ((for_assign | declared_init) SEMICOLON (expression) SEMICOLON for_assign) LB (inside_part_func)? RB;
for_range: FOR (ID COMMA ID COLONEQUAL RANGE expression) LB (inside_part_func)? RB;



// pdf thay 7.5 Break Statement
break_statement: BREAK;

// pdf thay 7.6 Continue Statement
continue_statement: CONTINUE;

// pdf thay 7.7 Call statement
call_statement: function_call | method_call;

function_call: ID LP list_expression? RP;
method_call: lhs DOT (ID LP list_expression? RP);

// pdf thay 7.8 Return statement
return_statement: RETURN expression?;
// ! ---------------- PARSER 2 ----------------------- */
// ! ---------------- PARSER 2 ----------------------- */



// ! ---------------- LEXER DEADLINE PASS 13 TEST CASE 23:59 16/1 ----------------------- */ todo
//TODO Keywords 3.3.2 pdf
IF: 'if';
ELSE: 'else';
FOR: 'for';
RETURN: 'return';
FUNC: 'func';
TYPE: 'type';
STRUCT: 'struct';
INTERFACE: 'interface';
STRING: 'string';
INT: 'int';
FLOAT: 'float';
BOOLEAN: 'boolean';
CONST: 'const';
VAR: 'var';
CONTINUE: 'continue';
BREAK: 'break';
RANGE: 'range';
NIL: 'nil';
TRUE: 'true';
FALSE: 'false';

//TODO Operators 3.3.3 pdf
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
DIVDIV: '%';

EQUALEQUAL: '==';
NOEQUAL: '!=';
L: '<';
LEQUAL: '<=';
R: '>';
REQUAL: '>=';

ANDAND: '&&';
OR: '||';
NOSIG: '!';

ASSIGN: '=';
ADDEQUAL: '+=';
SUBEQUAL: '-=';
MULEQUAL: '*=';
DIVEQUAL: '/=';
DIVDIVEQUAL: '%=';
COLONEQUAL: ':=';

//TODO Separators 3.3.4 pdf
LP: '(';
RP: ')';
LB: '{';
RB: '}';
LSB: '[';
RSB: ']';
DOT: '.';
COMMA: ',';
COLON: ':';
SEMICOLON: ';';

//TODO Identifiers 3.3.1 pdf
ID: [a-zA-Z_][a-zA-Z0-9_]*;

//TODO Literals 3.3.5 pdf
// integer literals                                 // change to decimal
INT_LIT: (DEC_INT | BIN_INT | OCT_INT | HEX_INT); 	// {self.text=str(int(self.text, 0))};
fragment DEC_INT: '0' | ([1-9][0-9]*);       		// decimal integer
fragment BIN_INT: '0' [bB] [01]+;            		// binary integer
fragment OCT_INT: '0' [oO] [0-7]+;           		// octal integer
fragment HEX_INT: '0' [xX] [0-9a-fA-F]+;      		// heximal integer

// float literals
// testcase float sua lai thi thay part1 o cuoi thanh part2
// FLOAT_LIT: DEC_INT E_PART1? '.' [0-9]* E_PART1?;
FLOAT_LIT: [0-9]+ E_PART1? '.' [0-9]* E_PART1?;
fragment E_PART1: ([Ee] [+-]? [0-9]+);
// fragment E_PART2: ([0-9]+ [Ee] [+-]? [0-9]+);

// boolean, nil o keyword

// String Literal
STRING_LIT: '"' STR_CHAR* '"';

fragment STR_CHAR: ~[\n\\"] | ESC_SEQ;
fragment ESC_SEQ: '\\' [ntr"\\]; // | '\'"';                 // escapse seq

fragment ESC_ILLEGAL: '\\' ~[ntr"\\]; // | [\r];

// Dấu xuống hàng sẽ được chuyển sang thành ; nếu nó nằm ở cuối p
// phát biểu  hoặc khai báo
// nghĩa là khi token đi trước nó là
// ID, các hằng nguyên, thực, luận lý, chuỗi,
// các từ khoá ứng với các kiểu nguyên, thực, luận lý, chuỗi, các từ khoá return, continue, break và các dấu ), ], }.
// Trong các trường hợp khác, thì dấu xuống hàng bị loại bỏ.
NEWLINE: '\r'? '\n' {
	change_list=[
		self.ID,
		self.INT_LIT,
		self.FLOAT_LIT,
		self.TRUE,
		self.FALSE,
		self.STRING_LIT,

		self.INT,
		self.FLOAT,
		self.BOOLEAN,
		self.STRING,

		self.RETURN,
		self.CONTINUE,
		self.BREAK,

		self.RP,
		self.RB,
		self.RSB,

		self.NIL
	]
	if (self.preType in change_list) :
		self.text=';'
		self.type=self.SEMICOLON
	else:
		self.skip()	
};

//TODO skip 3.1 and 3.2 pdf
COMMENT: '/*' (COMMENT|.)*? '*/' -> skip ;
LINE_COMMENT: '//' ~[\n]* -> skip ;

WS: [ \t\r\f\b]+ -> skip; // skip spaces, tabs     

//TODO ERROR pdf BTL1 + lexererr.py
ERROR_CHAR: . {raise ErrorToken(self.text)};

UNCLOSE_STRING: '"' STR_CHAR* ('\r\n' | '\n' | EOF) {
    if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
        raise UncloseString(self.text[0:-2])
    elif (self.text[-1] == '\n'):
        raise UncloseString(self.text[0:-1])
    else:
        raise UncloseString(self.text)
};

ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    raise IllegalEscape(self.text)
};
//! ---------------- LEXER ----------------------- */