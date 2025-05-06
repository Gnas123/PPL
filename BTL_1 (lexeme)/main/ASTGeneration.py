"""
 * Initial code for Assignment 1, 2
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/Shiba.Vo.Tien
 * Link Group : https://www.facebook.com/groups/khmt.ktmt.cse.bku
 * Date: 20.01.2025
"""
from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *
from functools import reduce

##! continue update
class ASTGeneration(MiniGoVisitor):
    #copy function target/main/MiniGoVisitor.py
    pass

    
#     # program: NEWLINE? dec_list NEWLINE?;
#     def visitProgram(self, ctx: MiniGoParser.ProgramContext):
#         print("di qua visitProgram")
#         return Program(self.visit(ctx.dec_list()))

#     # dec_list: declared NEWLINE? dec_list | declared;
#     def visitDec_list(self, ctx:MiniGoParser.Dec_listContext):
#         print("di qua visitDec_list")
#         if ctx.dec_list():
#             return [self.visit(ctx.declared())] + self.visit(ctx.dec_list())
#         return [self.visit(ctx.declared())] 

#     # literal:
#     #     INT_LIT
#     #     | FLOAT_LIT
#     #     | STRING_LIT
#     #     | NIL
#     #     | TRUE
#     #     | FALSE
#     #     | array_literal
#     #     | struct_literal;
#     def visitLiteral(self, ctx:MiniGoParser.LiteralContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitliteral")
#         if ctx.INT_LIT():
#             # print("di qua visitliteral: INT_LIT")
#             return IntLiteral(int(ctx.INT_LIT().getText()))
#         if ctx.FLOAT_LIT():
#             # print("di qua visitliteral: FLOAT_LIT")
#             return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
#         if ctx.STRING_LIT():
#             # print("di qua visitliteral: STRING_LIT")
#             return StringLiteral(ctx.STRING_LIT().getText())
#         if ctx.NIL():
#             # print("di qua visitliteral: NIL")
#             return NilLiteral()
#         if ctx.TRUE():
#             # print("di qua visitliteral: true")
#             return BooleanLiteral(True)
#             # return BooleanLiteral(ctx.TRUE().getText())
#         if ctx.FALSE():
#             # print("di qua visitliteral: false")
#             return BooleanLiteral(False)
#             # return BooleanLiteral(ctx.FALSE().getText())
#         if ctx.array_literal():
#             # print("di qua visitliteral: ARRAY_LITERAL")
#             return self.visit(ctx.array_literal())
#         if ctx.struct_literal():
#             # print("di qua visitliteral: STRUCT_LITERAL")
#             return self.visit(ctx.struct_literal())


#     # Visit a parse tree produced by MiniGoParser#primitive_types.
#     # primitive_types: INT | FLOAT | BOOLEAN | STRING;
#     def visitPrimitive_types(self, ctx:MiniGoParser.Primitive_typesContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitPrimitive_types")
#         if ctx.INT():
#             return IntType()
#         if ctx.FLOAT():
#             return FloatType()
#         if ctx.BOOLEAN():
#             return BooleanType()
#         if ctx.STRING():
#             return StringType()


#     # array_literal: type_array LB list_expression RB;
#     # note check lai phan dimention neu sai
#     def visitArray_literal(self, ctx: MiniGoParser.Array_literalContext):
#         print("di qua visitArray_literal")
#         typ = self.visit(ctx.type_array().getChild(1))
#         if ctx.type_array().ID():
#             typ = ClassType(Id(ctx.type_array().ID().getText()))
#         dimensions = self.visit(ctx.type_array().getChild(0))
#         value = self.visit(ctx.list_expression())
#         print("end visitArray_literal")
#         return ArrayLiteral(typ, dimensions, value)

#     # [1][1]int
#     # type_array: sub_type_array (primitive_types | STRUCT | ID);
#     def visitType_array(self, ctx: MiniGoParser.Type_arrayContext):
#         print("di qua visitType_array")
#         typ = ''
#         if ctx.STRUCT():
#             typ = ctx.STRUCT().getText()
#         elif ctx.ID():
#             typ = ClassType(Id(ctx.ID().getText()))
#         else:
#             typ = self.visit(ctx.primitive_types())  # Ensure this is a function call
#         return ArrayType(typ, self.visit(ctx.sub_type_array()))

#     # [1][1]
#     # sub_type_array: LSB INT_LIT RSB sub_type_array | LSB INT_LIT RSB;
#     def visitSub_type_array(self, ctx: MiniGoParser.Sub_type_arrayContext):
#         print("di qua visitSub_type_array")
#         if ctx.sub_type_array():
#             return [int(ctx.INT_LIT().getText())] + self.visit(ctx.sub_type_array())
#         return [int(ctx.INT_LIT().getText())]
    

#     # struct_literal: ID LB struct_list_element? RB;
#     def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
#         # return self.visitChildren(ctx)
#         id=Id(ctx.ID().getText())
#         if ctx.struct_list_element():
#             # print("co struct_list_element")
#             return StructLiteral(id, self.visit(ctx.struct_list_element()))
#         # print("khong co struct_list_element")    
#         return StructLiteral(id, [])


#     # struct_list_element: ID COLON expression (COMMA struct_list_element)?;
#     def visitStruct_list_element(self, ctx:MiniGoParser.Struct_list_elementContext):
#         # print("da di qua visitStruct_list_element")
#         id = Id(ctx.ID().getText())
#         if ctx.struct_list_element():
#             # print("trong if")
#             return [(id, self.visit(ctx.expression()))] + self.visit(ctx.struct_list_element())
#         # print("ngoai if")
#         return [(id, self.visit(ctx.expression()))]

    

#     # list_expression: expression COMMA list_expression | expression;
#     def visitList_expression(self, ctx:MiniGoParser.List_expressionContext):
#         # return self.visitChildren(ctx)
#         exp=self.visit(ctx.getChild(0))
#         if ctx.getChildCount() == 1:
#             return [exp]
#         return [exp] + self.visit(ctx.list_expression())


#     # expression: expression OR expression1 | expression1;     
#     def visitExpression(self, ctx:MiniGoParser.ExpressionContext):
#         # return self.visitChildren(ctx)
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression1())
        
#         op=ctx.OR().getText()
#         left=self.visit(ctx.expression())
#         right=self.visit(ctx.expression1())
#         return BinaryOp(op, left, right)

#     # expression1: expression1 ANDAND expression2 | expression2;
#     def visitExpression1(self, ctx:MiniGoParser.Expression1Context):
#         # return self.visitChildren(ctx)
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression2())
        
#         op=ctx.ANDAND().getText()
#         left=self.visit(ctx.expression1())
#         right=self.visit(ctx.expression2())
#         return BinaryOp(op, left, right)
    

#     # expression2: expression2 (EQUALEQUAL | NOEQUAL | L | LEQUAL | R | REQUAL) expression3 | expression3;
#     def visitExpression2(self, ctx:MiniGoParser.Expression2Context):
#         # return self.visitChildren(ctx)
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression3())
        
#         # (EQUALEQUAL | NOEQUAL | L | LEQUAL | R | REQUAL)
#         op=''
#         if ctx.EQUALEQUAL():
#             op=ctx.EQUALEQUAL().getText()
#         elif ctx.NOEQUAL():
#             op=ctx.NOEQUAL().getText()
#         elif ctx.L():
#             op=ctx.L().getText()
#         elif ctx.LEQUAL():
#             op=ctx.LEQUAL().getText()
#         elif ctx.R():
#             op=ctx.R().getText()
#         elif ctx.REQUAL():
#             op=ctx.REQUAL().getText()

#         left=self.visit(ctx.expression2())
#         right=self.visit(ctx.expression3())
#         return BinaryOp(op, left, right)
        


#     # expression3: expression3 (ADD | SUB) expression4 | expression4;
#     def visitExpression3(self, ctx:MiniGoParser.Expression3Context):
#         # return self.visitChildren(ctx)
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression4())
        
#         op=''
#         if ctx.ADD():
#             op=ctx.ADD().getText()
#         elif ctx.SUB():
#             op=ctx.SUB().getText()

#         left=self.visit(ctx.expression3())
#         right=self.visit(ctx.expression4())
#         return BinaryOp(op, left, right)


#     # expression4: expression4 (MUL | DIV | DIVDIV) expression5 | expression5;
#     def visitExpression4(self, ctx:MiniGoParser.Expression4Context):
#         # return self.visitChildren(ctx)
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression5())
        
#         op=''
#         if ctx.MUL():
#             op=ctx.MUL().getText()
#         elif ctx.DIV():
#             op=ctx.DIV().getText()
#         elif ctx.DIVDIV():
#             op=ctx.DIVDIV().getText()

#         left=self.visit(ctx.expression4())
#         right=self.visit(ctx.expression5())
#         return BinaryOp(op, left, right)


#     # expression5: (NOSIG | SUB) expression5 | expression6
#     def visitExpression5(self, ctx:MiniGoParser.Expression5Context):
#         # return self.visitChildren(ctx)
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression6())
        
#         op=''
#         if ctx.NOSIG():
#             op=ctx.NOSIG().getText()
#         elif ctx.SUB():
#             op=ctx.SUB().getText()

#         right=self.visit(ctx.expression5())
#         return UnaryOp(op, right)    

#     # expression6:
#     #     expression6 LSB expression RSB
#     #     | expression6 DOT ID
#     #     | expression6 DOT ID LP list_expression? RP
#     #     | expression7;
#     def visitExpression6(self, ctx:MiniGoParser.Expression6Context):
#         if ctx.getChildCount()==1:
#             return self.visit(ctx.expression7())
#     #     | expression6 DOT ID        
#         elif ctx.getChildCount()==3:
#             return FieldAccess(self.visit(ctx.expression6()), Id(ctx.ID().getText()))
#     #     expression6 LSB expression RSB
#         elif ctx.getChildCount()==4:
#             arr = self.visit(ctx.expression6())
#             idx = self.visit(ctx.expression())
#             print("di qua visitExpression6: arraycell")
#             return ArrayCell(arr, idx)
#     #     | expression6 DOT ID LP list_expression? RP
#         obj=self.visit(ctx.expression6())
#         method=Id(ctx.ID().getText())
#         param=[]
#         if ctx.list_expression():
#             param=self.visit(ctx.list_expression())
#         print("di qua visitExpression6: callexp")    
#         return CallExpr(obj, method, param)
        

#     # expression7: ID
# 	# 		| literal
# 	# 		| LP expression RP
# 	# 		| LB list_expression RB ;
# 	# 		| ID LP list_expression? RP
#     def visitExpression7(self, ctx:MiniGoParser.Expression7Context):
#         # print("da di qua expresion7")
#         if ctx.getChildCount() == 1:
#     #        ID
#             if ctx.ID():
#                 return Id(ctx.ID().getText())
# 	# 		| literal
#             return self.visit(ctx.literal())
#         elif ctx.getChildCount() == 3:
#             if ctx.LP() and ctx.RP():
# 	# 		| ID LP list_expression? RP
#                 if ctx.ID():
#                     print("di qua visitExpression7: callexp ID")    
#                     return CallExpr(None, Id(ctx.ID().getText()), [])
# 	# 		| LP expression RP
#                 return self.visit(ctx.expression())
# 	# 		| LB list_expression RB ;
#             return [self.visit(ctx.list_expression())]

# 	# 		| ID LP list_expression? RP
#         print("di qua visitExpression7: callexp none")    
#         return CallExpr(None, Id(ctx.ID().getText()), self.visit(ctx.list_expression()))
    
#     # type_withID: primitive_types | type_array | ID;
#     def visitType_withID(self, ctx:MiniGoParser.Type_withIDContext):
#         if ctx.ID():
#             return ClassType(Id(ctx.ID().getText()))
#         if ctx.primitive_types():
#             return self.visit(ctx.primitive_types())
#         # if ctx.type_array():
#         return self.visit(ctx.type_array())
        

#     # endcode: SEMICOLON NEWLINE* | NEWLINE+;
#     def visitEndcode(self, ctx: MiniGoParser.EndcodeContext):
#         print("di qua visitEndcode--------------------------")
#         # if ctx.SEMICOLON():
#         #     return [ctx.SEMICOLON().getText()]+[i.getText() for i in ctx.NEWLINE()]
#         # else:
#         #     return [i.getText() for i in ctx.NEWLINE()]
        
#         return self.visitChildren(ctx)
        
        

#     # struct_declared: TYPE ID STRUCT LB inside_part_struct_type? RB endcode;
#     # type Votien struct {
#     #             a int;
#     #         }
#     def visitStruct_declared(self, ctx:MiniGoParser.Struct_declaredContext):
#         name = Id(ctx.ID().getText())
#         fields = []
#         if ctx.inside_part_struct_type():
#             fields = self.visit(ctx.inside_part_struct_type())
#         print("di qua visitliteral: visitStruct_declared")
#         return StructDecl(name, fields)        
    

#     # inside_part_struct_type: (NEWLINE | ID type_withID endcode) inside_part_struct_type | (NEWLINE | ID type_withID endcode);
#     # a int;
#     def visitInside_part_struct_type(self, ctx:MiniGoParser.Inside_part_struct_typeContext):
#         variable = None
#         varType = None 
#         if ctx.inside_part_struct_type():
#             if ctx.NEWLINE():
#                 return [] + self.visit(ctx.inside_part_struct_type())
#             else:
#                 variable=Id(ctx.ID().getText())
#                 varType=self.visit(ctx.type_withID())
#                 return [VariablesDecl(variable, varType, None)] + self.visit(ctx.inside_part_struct_type())

#         if ctx.NEWLINE():
#             return []
#         else:
#             variable=Id(ctx.ID().getText())
#             varType=self.visit(ctx.type_withID())
#             return VariablesDecl(variable, varType, None)

                
                
    
#     # declared:
#     #     variables_declared
#     #     | constants_declared
#     #     | function_declared
#     #     | method_declared
#     #     | struct_declared
#     #     | interface_declared;
#     def visitDeclared(self, ctx:MiniGoParser.DeclaredContext):
#         print("di qua visitDeclared")
#         return self.visit(ctx.getChild(0))

#     # variables_declared: (declared_init | declared_no_init) SEMICOLON;
#     def visitVariables_declared(self, ctx:MiniGoParser.Variables_declaredContext):
#         print("di qua visitVariables_declared")
#         return self.visit(ctx.getChild(0))

#     # declared_init: VAR ID type_withID? ASSIGN (expression | lhs) ;
#     def visitDeclared_init(self, ctx:MiniGoParser.Declared_initContext):
#         print("di qua visitDeclared_init")
#         variable=Id(ctx.ID().getText())
#         varType=None
#         if ctx.type_withID():
#             varType=self.visit(ctx.type_withID())
#         varInit = None
#         if ctx.expression():
#             varInit = self.visit(ctx.expression())
#         else:
#             varInit = self.visit(ctx.lhs())

#         return VariablesDecl(variable, varType, varInit)


#     # declared_no_init: VAR ID type_withID;
#     def visitDeclared_no_init(self, ctx:MiniGoParser.Declared_no_initContext):
#         print("di qua visitDeclared_no_init")
#         variable = Id(ctx.ID().getText())
#         varType  = self.visit(ctx.type_withID())
#         varInit  = None
#         return VariablesDecl(variable, varType, varInit)

# # sub_struct: ID | array_element_access;
#     def visitSub_struct(self, ctx:MiniGoParser.Sub_structContext):
#         print("di qua visitSub_struct")
#         if ctx.ID():
#             return Id(ctx.ID().getText())
#         return self.visit(ctx.array_element_access())

    
# # struct_field_access: struct_field_access DOT sub_struct | sub_struct;
#     def visitStruct_field_access(self, ctx:MiniGoParser.Struct_field_accessContext):
#         # TODO
#         print("di qua visitStruct_field_access")
#         return self.visitChildren(ctx)


# # array_element_access: array_element_access LSB expression RSB | ID;
#     def visitArray_element_access(self, ctx:MiniGoParser.Array_element_accessContext):
#         if ctx.getChildCount()==1:
#             return Id(ctx.ID().getText())

#         # arr=None
#         # if ctx.array_element_access():
#         arr=self.visit(ctx.array_element_access())
#         idx=self.visit(ctx.expression())

#         return ArrayCell(arr, idx)


#     # constants_declared: CONST ID ASSIGN expression endcode;
#     def visitConstants_declared(self, ctx:MiniGoParser.Constants_declaredContext):
#         print("di qua visitConstants_declared")

#         constant = Id(ctx.ID().getText())
#         value = self.visit(ctx.expression())
#         print("end visitConstants_declared")
#         return ConstDecl(constant, value)


#     # function_declared: FUNC (LP ID ID RP)? (a_func) type_withID? LB (inside_part_func)? RB;
#     def visitFunction_declared(self, ctx:MiniGoParser.Function_declaredContext):
#         print("di qua visitFunction_declared")

#         name = Id(ctx.a_func().getChild(0).getText())
#         returnType = VoidType()
#         if ctx.type_withID():
#             returnType=self.visit(ctx.type_withID())
#         methodReceiver=None
#         if ctx.ID():
#             variable = Id(ctx.ID()[0].getText())
#             varType = ClassType(Id(ctx.ID()[1].getText()))
#             methodReceiver=VariablesDecl(variable, varType, None)
#         param = []
#         if ctx.a_func().func_para_list():
#             param = self.visit(ctx.a_func().func_para_list())
#         stmts = [] 
#         if ctx.inside_part_func():
#             stmts = self.visit(ctx.inside_part_func())
#         return FunctionDecl(name, returnType, methodReceiver, param, stmts)
#         # return self.visitChildren(ctx)
    


#     # a_func: ID LP func_para_list? RP;
#     # foo( a int, b float )
#     def visitA_func(self, ctx:MiniGoParser.A_funcContext):
#         print("di qua visitA_func") 

#         return self.visitChildren(ctx)
        

#     # func_para_list: ID type_withID COMMA func_para_list | (ID type_withID) ;
#     # a int, b float
#     def visitFunc_para_list(self, ctx:MiniGoParser.Func_para_listContext):
#         print("di qua visitFunc_para_list")

#         variable = Id(ctx.ID().getText())
#         varType = self.visit(ctx.type_withID())
#         varInit = None
#         if ctx.func_para_list():
#             return [VariablesDecl(variable, varType, varInit)] + self.visit(ctx.func_para_list())
#         return [VariablesDecl(variable, varType, varInit)]



#     # inside_part_func: (statement endcode | declared | NEWLINE) inside_part_func
# 	# 			| (statement endcode | declared | NEWLINE);
#     def visitInside_part_func(self, ctx:MiniGoParser.Inside_part_funcContext):
#         print("di qua visitInside_part_func")
        
#         if ctx.inside_part_func():
#             if ctx.NEWLINE():
#                 return [] + self.visit(ctx.inside_part_func())
#             return [self.visit(ctx.getChild(0))] + self.visit(ctx.inside_part_func())
#         if ctx.NEWLINE():
#             return []
#         return [self.visit(ctx.getChild(0))]


#     # method_declared: TYPE ID type_withID LB (inside_part_func)? RB endcode;
#     def visitMethod_declared(self, ctx:MiniGoParser.Method_declaredContext):
#         # todo
#         return self.visitChildren(ctx)


#     #interface_declared: TYPE ID INTERFACE LB inside_part_interface? RB endcode;
#     # type Votien interface {
#     #     Add(x, y int) int; 
#     # }
#     def visitInterface_declared(self, ctx:MiniGoParser.Interface_declaredContext):
#         print("di qua visitInterface_declared")
#         name= Id(ctx.ID().getText())
#         fields=[]
#         if ctx.inside_part_interface():
#             fields=self.visit(ctx.inside_part_interface())
#         return InterfaceDecl(name, fields)


#     # inside_part_interface: (NEWLINE | sub_inside_part_interface) inside_part_interface | (NEWLINE | sub_inside_part_interface);
#     # Add(x, y int) int; (recusion)
#     def visitInside_part_interface(self, ctx:MiniGoParser.Inside_part_interfaceContext):
#         print("di qua visitInside_part_interface")
#         if ctx.inside_part_interface():
#             if ctx.NEWLINE():
#                 return [] + self.visit(ctx.inside_part_interface())
#             return [self.visit(ctx.sub_inside_part_interface())] + self.visit(ctx.inside_part_interface())
#         if ctx.NEWLINE():
#             return []
#         return [self.visit(ctx.sub_inside_part_interface())]    


# # Add(x, y int) int; 
# # sub_inside_part_interface: ID LP (interface_para_list)? RP type_withID? SEMICOLON?;
#     def visitSub_inside_part_interface(self, ctx:MiniGoParser.Sub_inside_part_interfaceContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitSub_inside_part_interface")

#         name=Id(ctx.ID().getText())
#         returnType=VoidType()
#         if ctx.type_withID():
#             returnType=self.visit(ctx.type_withID())
#         methodReceiver=None
#         param=[]
#         if ctx.interface_para_list():
#             param=self.visit(ctx.interface_para_list())
#         stmts= [] 
#         currType = VoidType()
#         for i in reversed(param):
#             if isinstance(i.varType, VoidType):
#                 i.varType = currType
#             else: 
#                 currType = i.varType    
#             # print(i)
            
#         return FunctionDecl(name, returnType, methodReceiver, param, stmts)


#     # interface_para_list: ID type_withID? COMMA interface_para_list | (ID type_withID?);
#     #   y int?
#     def visitInterface_para_list(self, ctx:MiniGoParser.Interface_para_listContext):
#         print("di qua visitInterface_para_list")
#         variable = Id(ctx.ID().getText())
#         varType = VoidType()  # Default type
#         varInit = None
        
#         # Visit type_withID if it exists
#         if ctx.type_withID():
#             varType = self.visit(ctx.type_withID())

#         # Handle the current variable declaration
#         declaration = VariablesDecl(variable, varType, varInit)

#         # If there is another parameter in the list, visit it recursively
#         if ctx.interface_para_list():
#             return [declaration] + self.visit(ctx.interface_para_list())
#         return [declaration]


#     # list_statement: statement list_statement | statement;
#     def visitList_statement(self, ctx:MiniGoParser.List_statementContext):
#         print("di qua visitList_statement")
#         if ctx.list_statement():
#             return [self.visit(ctx.statement())] + self.visit(ctx.list_statement())
#         return [self.visit(ctx.statement())]


#     # statement:
# 	# (
# 	# 	declared_statement
# 	# 	| assign_statement
# 	# 	| if_statement
# 	# 	| for_statement
# 	# 	| break_statement
# 	# 	| continue_statement
# 	# 	| call_statement
# 	# 	| return_statement
# 	# );
#     def visitStatement(self, ctx:MiniGoParser.StatementContext):
#         print("di qua visitStatement")
#         return self.visit(ctx.getChild(0))


#     # declared_statement: variables_declared | constants_declared;
#     def visitDeclared_statement(self, ctx:MiniGoParser.Declared_statementContext):
#         print("di qua visitDeclared_statement")
#         return self.visit(ctx.getChild(0))

#     # assign_op: COLONEQUAL | ADDEQUAL | SUBEQUAL | MULEQUAL | DIVEQUAL | DIVDIVEQUAL;
#     def visitAssign_op(self, ctx:MiniGoParser.Assign_opContext):
#         print("di qua visitAssign_op")
#         return ctx.getText()

# # assign_statement: lhs assign_op rhs;
#     def visitAssign_statement(self, ctx:MiniGoParser.Assign_statementContext):
#         print("di qua visitAssign_statement")
#         lhs=self.visit(ctx.lhs())
#         assign=self.visit(ctx.assign_op())
#         exp=self.visit(ctx.rhs())
#         return AssignStmt(lhs, assign, exp)


# # index: LSB expression RSB;
#     def visitIndex(self, ctx:MiniGoParser.IndexContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitIndex")
#         return self.visit(ctx.expression())


# # lhs: lhs (DOT ID index)
# # 		| lhs (DOT ID)
# # 		| lhs index
# # 		| ID;					//a[2].b.c[2]
#     def visitLhs(self, ctx:MiniGoParser.LhsContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitlhs")
#         if ctx.getChildCount()==1:
#             return Id(ctx.ID().getText())
#         if ctx.getChildCount()==2:
#             return ArrayCell(self.visit(ctx.lhs()), self.visit(ctx.index()))
#         if ctx.getChildCount()==3:
#             return FieldAccess(self.visit(ctx.lhs()), Id(ctx.ID().getText()))
    
#         arr=FieldAccess(self.visit(ctx.lhs()), Id(ctx.ID().getText()))
#         idx=self.visit(ctx.index())
#         return ArrayCell(arr, idx)
    

#     # rhs: expression;
#     def visitRhs(self, ctx:MiniGoParser.RhsContext):
#         print("di qua visitRhs")
#         return self.visit(ctx.expression())


# # if_statement: IF expression NEWLINE* LB (inside_part_func)? RB (NEWLINE* elif_part)? (NEWLINE* else_part)?;
#     def visitIf_statement(self, ctx:MiniGoParser.If_statementContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitIf_statement")
#         expr=self.visit(ctx.expression())
#         thenStmt = []
#         elifStmt = None
#         elseStmt = None
        
#         if ctx.inside_part_func():
#             thenStmt=self.visit(ctx.inside_part_func())
#         if ctx.elif_part():
#             elifStmt=self.visit(ctx.elif_part())
#         if ctx.else_part():
#             elseStmt=self.visit(ctx.else_part())        

#         return If(expr, thenStmt, elifStmt, elseStmt)


# # elif_part: ELSE IF expression NEWLINE* LB (inside_part_func)? RB NEWLINE* elif_part
# # 		| ELSE IF expression NEWLINE* LB (inside_part_func)? RB;
#     def visitElif_part(self, ctx:MiniGoParser.Elif_partContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitElif_part")
#         stmt=[]
#         if ctx.inside_part_func():
#             stmt = self.visit(ctx.inside_part_func())
#         if ctx.elif_part():
#             return [(self.visit(ctx.expression()), stmt)] + self.visit(ctx.elif_part())
#         return [(self.visit(ctx.expression()), stmt)]

# # else_part: ELSE NEWLINE* LB (inside_part_func)? RB;
#     def visitElse_part(self, ctx:MiniGoParser.Else_partContext):
#         # return self.visitChildren(ctx)
#         print("di qua visitElse_part")
#         if ctx.inside_part_func():
#             return self.visit(ctx.inside_part_func())
#         return []


#     # for_statement: FOR (expression | for_init_cond | for_range) LB (inside_part_func)? RB;
#     def visitFor_statement(self, ctx:MiniGoParser.For_statementContext):
#         print("di qua visitFor_statement")
#         initStmt=None
#         expr=None
#         postStmt=None
#         loop=[]
#         if ctx.expression():
#             expr=self.visit(ctx.expression())
#         elif ctx.for_init_cond():
#             initStmt=self.visit(ctx.for_init_cond().getChild(0))
#             expr=self.visit(ctx.for_init_cond().getChild(2))
#             postStmt=self.visit(ctx.for_init_cond().getChild(4))
#         elif ctx.for_range():
#             initStmt=Id(ctx.for_range().ID()[0].getText())
#             expr=Id(ctx.for_range().ID()[1].getText())
#             postStmt=self.visit(ctx.for_range().expression())

#         if ctx.inside_part_func():
#             loop=self.visit(ctx.inside_part_func())

#         return For(initStmt, expr, postStmt, loop)

#     # for_init_cond: (assign_statement | declared_init) SEMICOLON (expression) SEMICOLON (assign_statement);
#     # var i = 0; i < 10; i += 1
#     def visitFor_init_cond(self, ctx:MiniGoParser.For_init_condContext):
#         # todo nothing 
#         print("di qua visitFor_init_cond")
#         return self.visitChildren(ctx)


#     # for_range: ID COMMA ID COLONEQUAL RANGE expression;
#     # index, value := range array[2]
#     def visitFor_range(self, ctx:MiniGoParser.For_rangeContext):
#         # todo nothing
#         print("di qua visitFor_range")
#         return self.visitChildren(ctx)

#     # break_statement: BREAK;
#     def visitBreak_statement(self, ctx:MiniGoParser.Break_statementContext):
#         print("di qua visitBreak_statement")
#         return Break()


#     # continue_statement: CONTINUE;
#     def visitContinue_statement(self, ctx:MiniGoParser.Continue_statementContext):
#         print("di qua visitContinue_statement")
#         return Continue()


#     # call_statement: function_call | method_call;
#     def visitCall_statement(self, ctx:MiniGoParser.Call_statementContext):
#         print("di qua visitCall_statement")
#         return self.visitChildren(ctx)


#     # function_call: ID LP list_expression? RP;
#     def visitFunction_call(self, ctx:MiniGoParser.Function_callContext):
#         print("di qua visitFunction_call")
#         if ctx.list_expression():
#             return CallStmt(None, Id(ctx.ID().getText()), self.visit(ctx.list_expression()))
#         return CallStmt(None, Id(ctx.ID().getText()), [])


#     # method_call: lhs DOT function_call;
#     # a[2].foo(1,3);
#     def visitMethod_call(self, ctx:MiniGoParser.Method_callContext):
#         print("di qua visitMethod_call")
#         obj=self.visit(ctx.lhs()) 
#         print("di qua obj: ", obj)
#         method=Id(ctx.function_call().ID().getText())
#         param=[]
#         if ctx.function_call().list_expression():
#             param=self.visit(ctx.function_call().list_expression())
#         return CallStmt(obj, method, param)


#     # return_statement: RETURN expression?;
#     def visitReturn_statement(self, ctx:MiniGoParser.Return_statementContext):
#         print("di qua visitReturn_statement")
#         if ctx.expression():
#             return Return(self.visit(ctx.expression()))
#         return Return(None)


