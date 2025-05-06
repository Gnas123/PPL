"""
 * Initial code for Assignment 1, 2
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/Shiba.Vo.Tien
 * Link Group : https://www.facebook.com/groups/khmt.ktmt.cse.bku
 * Date: 07.01.2025
"""
from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *
from functools import reduce

##! continue update
class ASTGeneration(MiniGoVisitor):
# program: dec_list EOF;
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        # print("di qua visitProgram")
        return Program(self.visit(ctx.dec_list()))

# dec_list: declared dec_list | declared;
    def visitDec_list(self, ctx:MiniGoParser.Dec_listContext):
        # # print("di qua visitDec_list")
        if ctx.dec_list():
            return [self.visit(ctx.declared())] + self.visit(ctx.dec_list())
        return [self.visit(ctx.declared())] 


# literal:
#     INT_LIT
#     | FLOAT_LIT
#     | STRING_LIT
#     | NIL
#     | TRUE
#     | FALSE
#     | array_literal
#     | struct_literal;
    def visitLiteral(self, ctx:MiniGoParser.LiteralContext):
        # return self.visitChildren(ctx)
        # print("di qua visitliteral")
        if ctx.INT_LIT():
            # print("di qua visitliteral: INT_LIT")
            return IntLiteral(ctx.INT_LIT().getText())
        if ctx.FLOAT_LIT():
            # print("di qua visitliteral: FLOAT_LIT")
            return FloatLiteral(ctx.FLOAT_LIT().getText())
        if ctx.TRUE():
            # print("di qua visitliteral: true")
            # return BooleanLiteral(True)
            return BooleanLiteral(ctx.TRUE().getText())
        if ctx.FALSE():
            # print("di qua visitliteral: false")
            # return BooleanLiteral(False)
            return BooleanLiteral(ctx.FALSE().getText())
        if ctx.STRING_LIT():
            # print("di qua visitliteral: STRING_LIT")
            return StringLiteral(ctx.STRING_LIT().getText())
        if ctx.NIL():
            # print("di qua visitliteral: NIL")
            return NilLiteral()
        if ctx.array_literal():
            # print("di qua visitliteral: ARRAY_LITERAL")
            return self.visit(ctx.array_literal())
        if ctx.struct_literal():
            # print("di qua visitliteral: STRUCT_LITERAL")
            return self.visit(ctx.struct_literal())


# primitive_types: INT | FLOAT | BOOLEAN | STRING;
    def visitPrimitive_types(self, ctx:MiniGoParser.Primitive_typesContext):
        # return self.visitChildren(ctx)
        # print("di qua visitPrimitive_types")
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.BOOLEAN():
            return BoolType()
        if ctx.STRING():
            return StringType()

# type_withID: primitive_types | type_array | ID;
    def visitType_withID(self, ctx:MiniGoParser.Type_withIDContext):
        # print("di qua visitType_withID")
        if ctx.ID():
            return Id(ctx.ID().getText())
        if ctx.primitive_types():
            return self.visit(ctx.primitive_types())
        # if ctx.type_array():
        return self.visit(ctx.type_array())


# literal_primitive: INT_LIT | FLOAT_LIT | STRING_LIT | TRUE | FALSE | NIL;
    def visitLiteral_primitive(self, ctx:MiniGoParser.Literal_primitiveContext):
        # print("di qua visitLiteral_primitive")
        if ctx.INT_LIT():
            # print("di qua visitLiteral_primitive: INT_LIT", int(ctx.INT_LIT().getText(), 0))
            # print("int: ", int(ctx.INT_LIT().getText(), 0))
            return IntLiteral(ctx.INT_LIT().getText())
        if ctx.FLOAT_LIT():
            # print("di qua visitLiteral_primitive: FLOAT_LIT")
            # print("float: ", float(ctx.FLOAT_LIT().getText()))
            return FloatLiteral(ctx.FLOAT_LIT().getText())
        if ctx.STRING_LIT():
            # print("di qua visitLiteral_primitive: STRING_LIT")
            return StringLiteral(ctx.STRING_LIT().getText())
        if ctx.TRUE():
            # print("di qua visitLiteral_primitive: TRUE")
            # return BooleanLiteral(True)
            return BooleanLiteral(ctx.TRUE().getText())
        if ctx.FALSE():
            # print("di qua visitLiteral_primitive: FALSE")
            # return BooleanLiteral(False)
            return BooleanLiteral(ctx.TRUE().getText())
        if ctx.NIL():
            # print("di qua visitLiteral_primitive: NIL")
            return NilLiteral()

# sub_inside_array_lit: LB sub_inside_array_lit RB
# 				| sub_inside_array_lit COMMA sub_inside_array_lit
# 				| ID
# 				| literal_primitive
# 				| struct_literal;
    def visitSub_inside_array_lit(self, ctx:MiniGoParser.Sub_inside_array_litContext):
        # print("di qua visitSub_inside_array_lit")
        if ctx.ID():
            # print("di qua visitSub_inside_array_lit: ID")
            return [Id(ctx.ID().getText())]
        if ctx.literal_primitive():
            # print("di qua visitSub_inside_array_lit: literal_primitive")
            return [self.visit(ctx.literal_primitive())]
        if ctx.struct_literal():
            # print("di qua visitSub_inside_array_lit: struct_literal")
            return [self.visit(ctx.struct_literal())]
        if ctx.LB():  # Handling case where we encounter a left bracket
            # print("di qua visitSub_inside_array_lit: LB")
            temp = [self.visit(ctx.sub_inside_array_lit()[0])]
            return temp
        #TODO
        # if ctx.COMMA():
            # print("di qua visitSub_inside_array_lit: COMMA")
        return self.visit(ctx.sub_inside_array_lit()[0]) + self.visit(ctx.sub_inside_array_lit()[1])


# {}{}
# inside_array_lit: LB sub_inside_array_lit RB inside_array_lit | sub_inside_array_lit;
    def visitInside_array_lit(self, ctx:MiniGoParser.Inside_array_litContext):
        if ctx.inside_array_lit():
            return [self.visit(ctx.sub_inside_array_lit())] + self.visit(ctx.inside_array_lit())
        return self.visit(ctx.sub_inside_array_lit())

# sub_type_array: LSB (INT_LIT | ID) RSB sub_type_array | LSB (INT_LIT | ID) RSB;	// [1][2]
    def visitSub_type_array(self, ctx: MiniGoParser.Sub_type_arrayContext):
        # print("di qua visitSub_type_array")
        
        temp = ctx.getChild(1).getText()
        if ctx.ID():
            temp = Id(temp)    
        else:
            # # print("maybe here? ")
            temp = IntLiteral(temp)
        if ctx.sub_type_array():
            return [temp] + self.visit(ctx.sub_type_array())
        return [temp] # int(temp)


# type_array: sub_type_array (primitive_types | STRUCT | ID);
    def visitType_array(self, ctx: MiniGoParser.Type_arrayContext):
        # print("di qua visitType_array")
        typ = ''
        if ctx.STRUCT():
            typ = ctx.STRUCT().getText()
        elif ctx.ID():
            typ = Id(ctx.ID().getText())
        else:
            typ = self.visit(ctx.primitive_types())  # Ensure this is a function call
        return ArrayType(self.visit(ctx.sub_type_array()), typ)


# array_literal: type_array LB inside_array_lit RB;	
    def visitArray_literal(self, ctx: MiniGoParser.Array_literalContext):
        # print("di qua visitArray_literal")

        dimens = self.visit(ctx.type_array().getChild(0))    
        # # print("dimens: ", dimens)
        eleType = None
        if ctx.type_array().ID():
            # print("di qua visitArray_literal: ID")
            eleType = Id(ctx.type_array().getChild(1).getText())
        elif ctx.type_array().STRUCT():
            # TODO
            # print("di qua visitArray_literal: STRUCT")
            eleType = None 
        else:    
            # print("di qua visitArray_literal: primitive_types")
            eleType = self.visit(ctx.type_array().getChild(1))
        # # print("eleType: ", eleType)
        value = self.visit(ctx.inside_array_lit())
        # # print("value: ", value)
        
        # print("end visitArray_literal")
        return ArrayLiteral(dimens, eleType, value)
    

# struct_literal: ID LB struct_list_element? RB;
    def visitStruct_literal(self, ctx:MiniGoParser.Struct_literalContext):
        # print("di qua visitStruct_literal")
        name=ctx.ID().getText()
        # elements: List[Tuple[str,Expr]] # [] if there is no elements
        elements=[]
        if ctx.struct_list_element():
            # print("co struct_list_element")
            elements=self.visit(ctx.struct_list_element())
        # else:
            # print("khong co struct_list_element")    
    
        return StructLiteral(name, elements)


# struct_list_element: ID COLON expression (COMMA struct_list_element)?;
    def visitStruct_list_element(self, ctx:MiniGoParser.Struct_list_elementContext):
        # print("di qua visitStruct_list_element")
        id = str(ctx.ID().getText())
        if ctx.struct_list_element():
            # print("co struct_list_element======================================")
            # print("[]", [(id, self.visit(ctx.expression()))])
            # print("ko", (id, self.visit(ctx.expression())))
            return [(id, self.visit(ctx.expression()))] + self.visit(ctx.struct_list_element())
        return [(id, self.visit(ctx.expression()))]

    
# endcode: SEMICOLON NEWLINE* | NEWLINE+;
    def visitEndcode(self, ctx: MiniGoParser.EndcodeContext):
        # print("di qua visitEndcode--------------------------")
        # if ctx.SEMICOLON():
        #     return [ctx.SEMICOLON().getText()]+[i.getText() for i in ctx.NEWLINE()]
        # else:
        #     return [i.getText() for i in ctx.NEWLINE()]
        
        return self.visitChildren(ctx)


# list_expression: expression COMMA list_expression | expression;
    def visitList_expression(self, ctx:MiniGoParser.List_expressionContext):
        # return self.visitChildren(ctx)
        # print("di qua visitList_expression")
        exp=self.visit(ctx.getChild(0))
        if ctx.getChildCount() == 1:
            return [exp]
        return [exp] + self.visit(ctx.list_expression())


# expression: expression OR expression1 | expression1;     
    def visitExpression(self, ctx:MiniGoParser.ExpressionContext):
        # return self.visitChildren(ctx)
        # # print("di qua visitExpression")
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression1())
        
        op=ctx.OR().getText()
        left=self.visit(ctx.expression())
        right=self.visit(ctx.expression1())
        return BinaryOp(op, left, right)

# expression1: expression1 ANDAND expression2 | expression2;
    def visitExpression1(self, ctx:MiniGoParser.Expression1Context):
        # return self.visitChildren(ctx)
        # # print("di qua visitExpression1")
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression2())
        
        op=ctx.ANDAND().getText()
        left=self.visit(ctx.expression1())
        right=self.visit(ctx.expression2())
        return BinaryOp(op, left, right)
    

# expression2: expression2 (EQUALEQUAL | NOEQUAL | L | LEQUAL | R | REQUAL) expression3 | expression3;
    def visitExpression2(self, ctx:MiniGoParser.Expression2Context):
        # return self.visitChildren(ctx)
        # # print("di qua visitExpression2")
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression3())
        
        # (EQUALEQUAL | NOEQUAL | L | LEQUAL | R | REQUAL)
        op=''
        if ctx.EQUALEQUAL():
            op=ctx.EQUALEQUAL().getText()
        elif ctx.NOEQUAL():
            op=ctx.NOEQUAL().getText()
        elif ctx.L():
            op=ctx.L().getText()
        elif ctx.LEQUAL():
            op=ctx.LEQUAL().getText()
        elif ctx.R():
            op=ctx.R().getText()
        elif ctx.REQUAL():
            op=ctx.REQUAL().getText()

        left=self.visit(ctx.expression2())
        right=self.visit(ctx.expression3())
        return BinaryOp(op, left, right)
        


# expression3: expression3 (ADD | SUB) expression4 | expression4;
    def visitExpression3(self, ctx:MiniGoParser.Expression3Context):
        # return self.visitChildren(ctx)
        # # print("di qua visitExpression3")
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression4())
        
        op=''
        if ctx.ADD():
            op=ctx.ADD().getText()
        elif ctx.SUB():
            op=ctx.SUB().getText()

        left=self.visit(ctx.expression3())
        right=self.visit(ctx.expression4())
        return BinaryOp(op, left, right)


# expression4: expression4 (MUL | DIV | DIVDIV) expression5 | expression5;
    def visitExpression4(self, ctx:MiniGoParser.Expression4Context):
        # return self.visitChildren(ctx)
        # # print("di qua visitExpression4")
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression5())
        
        op=''
        if ctx.MUL():
            op=ctx.MUL().getText()
        elif ctx.DIV():
            op=ctx.DIV().getText()
        elif ctx.DIVDIV():
            op=ctx.DIVDIV().getText()

        left=self.visit(ctx.expression4())
        right=self.visit(ctx.expression5())
        return BinaryOp(op, left, right)


# expression5: (NOSIG | SUB) expression5 | expression6
    def visitExpression5(self, ctx:MiniGoParser.Expression5Context):
        # return self.visitChildren(ctx)
        # # print("di qua visitExpression5")
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression6())
        
        op=''
        if ctx.NOSIG():
            op=ctx.NOSIG().getText()
        elif ctx.SUB():
            op=ctx.SUB().getText()

        right=self.visit(ctx.expression5())
        return UnaryOp(op, right)    

# expression6:
#     expression6 LSB expression RSB
#     | expression6 DOT ID
#     | expression6 DOT ID LP list_expression? RP
#     | expression7;
    def visitExpression6(self, ctx:MiniGoParser.Expression6Context):
        # print("di qua visitExpression6")
        # expression7
        if ctx.getChildCount()==1:
            return self.visit(ctx.expression7())
        # expression6 LSB expression RSB
        if ctx.expression():
            # print("di qua visitExpression6: expression6 LSB expression RSB")
            # arr = self.visit(ctx.expression6())
            # idx = [self.visit(ctx.expression())]
            # # # print("di qua visitExpression6: arraycell")
            # return ArrayCell(arr, idx)
        
            expression6 = self.visit(ctx.expression6())
            if type(expression6) == ArrayCell:
                return ArrayCell(expression6.arr, expression6.idx  + [self.visit(ctx.expression())])
            return ArrayCell(expression6, [self.visit(ctx.expression())])
        # expression6 DOT ID        
        if ctx.getChildCount()==3:
            # print("di qua visitExpression6: expression6 DOT ID")
            return FieldAccess(self.visit(ctx.expression6()), ctx.ID().getText())
        
        # expression6 DOT ID LP list_expression? RP
        # print("di qua visitExpression6: expression6 DOT ID LP list_expression? RP")
        receiver=self.visit(ctx.expression6())
        metName=ctx.ID().getText()
        args = []
        
        if ctx.list_expression():
            # print("co list_expression")
            args=self.visit(ctx.list_expression())
        # print("di qua visitExpression6: callexp")    
        return MethCall(receiver, metName, args)
        

# expression7: ID
# 			| literal
# 			| LP expression RP
# 			| ID LP list_expression? RP;
    def visitExpression7(self, ctx:MiniGoParser.Expression7Context):
        # print("di qua expresion7")
        if ctx.getChildCount()==1:
            if ctx.ID():
                # print("di qua expresion7: ID")
                return Id(ctx.ID().getText())
            # print("di qua expresion7: literal")
            return self.visit(ctx.literal())
        # LP expression RP
        if ctx.expression():
            # print("di qua expresion7: LP expression RP")
            return self.visit(ctx.expression())
        # ID LP list_expression RP;
        funName=ctx.ID().getText()
        args=[] 
        if ctx.list_expression():
            # print("di qua expresion7: ID LP list_expression RP;")
            args=self.visit(ctx.list_expression()) 
            return FuncCall(funName, args)
        # ID LP RP
        # print("di qua expresion7: ID LP RP;")
        return FuncCall(funName, args)
         
    
# declared:
#     variables_declared
#     | constants_declared
#     | function_declared
#     | method_declared
#     | struct_declared
#     | interface_declared;
    def visitDeclared(self, ctx:MiniGoParser.DeclaredContext):
        # print("di qua visitDeclared")
        return self.visit(ctx.getChild(0))


# variables_declared: (declared_init | declared_no_init) endcode;
    def visitVariables_declared(self, ctx:MiniGoParser.Variables_declaredContext):
        # print("di qua visitVariables_declared")
        return self.visit(ctx.getChild(0))       


# declared_init: VAR ID type_withID? ASSIGN (expression | lhs) ;
    def visitDeclared_init(self, ctx:MiniGoParser.Declared_initContext):
        # print("di qua visitDeclared_init")
        varName = ctx.ID().getText()
        varType = None
        varInit = None
        if ctx.type_withID():
            varType = self.visit(ctx.type_withID())
        if ctx.expression():
            varInit = self.visit(ctx.expression())
        else:
            varInit = self.visit(ctx.lhs())

        return VarDecl(varName, varType, varInit)


# declared_no_init: VAR ID type_withID;
    def visitDeclared_no_init(self, ctx:MiniGoParser.Declared_no_initContext):
        # print("di qua visitDeclared_no_init")
        varName = ctx.ID().getText()
        varType  = self.visit(ctx.type_withID())
        varInit  = None
        return VarDecl(varName, varType, varInit)



# constants_declared: CONST ID ASSIGN expression endcode;
    def visitConstants_declared(self, ctx:MiniGoParser.Constants_declaredContext):
        # print("di qua visitConstants_declared")

        conName = ctx.ID().getText()
        conType = None
        iniExpr = self.visit(ctx.expression())
        
        # # print("end visitConstants_declared")
        return ConstDecl(conName, conType, iniExpr)

# function_declared: FUNC (a_func) type_withID? LB (inside_part_func)? RB endcode;
    def visitFunction_declared(self, ctx:MiniGoParser.Function_declaredContext):
        # return self.visitChildren(ctx)
        # print("di qua visitFunction_declared")

        name = ctx.a_func().getChild(0).getText()
        params = []
        if ctx.a_func().func_para_list():
            params = self.visit(ctx.a_func().func_para_list())
        retType = VoidType()
        if ctx.type_withID():
            retType=self.visit(ctx.type_withID())
        body = Block([])
        if ctx.inside_part_func():
            body = Block(self.visit(ctx.inside_part_func()))
                
        return FuncDecl(name, params, retType, body)


# a_func: ID LP func_para_list? RP;
# foo( a int, b float )
    def visitA_func(self, ctx:MiniGoParser.A_funcContext):
        # print("di qua visitA_func") 

        return self.visitChildren(ctx)


# func_para_list: param COMMA func_para_list | param ;
# a int, b float
    def visitFunc_para_list(self, ctx:MiniGoParser.Func_para_listContext):
        # print("di qua visitFunc_para_list")

        return self.visit(ctx.param()) if ctx.getChildCount() == 1 else self.visit(ctx.param()) + self.visit(ctx.func_para_list())


# param: list_ID type_withID COMMA param | list_ID type_withID;
    def visitParam(self, ctx:MiniGoParser.ParamContext):
        # return self.visitChildren(ctx)

        # print("di qua visitParam")
        list_ID = self.visit(ctx.list_ID())
        type_withID = self.visit(ctx.type_withID())
        return [ParamDecl(item, type_withID) for item in list_ID] + (self.visit(ctx.param()) if ctx.param() else [])


# list_ID: ID COMMA list_ID | ID;
    def visitList_ID(self, ctx:MiniGoParser.List_IDContext):
        # return self.visitChildren(ctx)
        return [ctx.ID().getText()] if ctx.getChildCount() == 1 else [ctx.ID().getText()] + self.visit(ctx.list_ID())


# inside_part_func: (statement endcode | declared) inside_part_func
# 				| (statement endcode | declared);
    def visitInside_part_func(self, ctx:MiniGoParser.Inside_part_funcContext):
        # print("di qua visitInside_part_func")
        
        if ctx.inside_part_func():
            return [self.visit(ctx.getChild(0))] + self.visit(ctx.inside_part_func())
        return [self.visit(ctx.getChild(0))]


# method_declared: FUNC (LP ID ID RP) (a_func) type_withID? LB (inside_part_func)? RB endcode;
    def visitMethod_declared(self, ctx:MiniGoParser.Method_declaredContext):
        # print("di qua visitMethod_declared")
        # return self.visitChildren(ctx)

        name = ctx.a_func().getChild(0).getText()
        params = []
        if ctx.a_func().func_para_list():
            params = self.visit(ctx.a_func().func_para_list())
        retType = VoidType()
        if ctx.type_withID():
            retType=self.visit(ctx.type_withID())
        body = Block([])
        if ctx.inside_part_func():
            body = Block(self.visit(ctx.inside_part_func()))
                
        return MethodDecl(
            ctx.ID()[0].getText(),
            Id(ctx.ID()[1].getText()),
            FuncDecl(name, params, retType, body)   
        )


# struct_declared: TYPE ID STRUCT LB inside_part_struct_type RB endcode;
    def visitStruct_declared(self, ctx:MiniGoParser.Struct_declaredContext):
        # print("di qua visitStruct_declared")

        name = ctx.ID().getText()
        elements = self.visit(ctx.inside_part_struct_type())
        # methods:List[MethodDecl]
        #todo
        methods = []
        
        return StructType(name, elements, methods)        
    

# inside_part_struct_type: (ID type_withID endcode) inside_part_struct_type
# 						| (ID type_withID endcode);
# a int;
    def visitInside_part_struct_type(self, ctx:MiniGoParser.Inside_part_struct_typeContext):
        variable=ctx.ID().getText()
        varType=self.visit(ctx.type_withID())

        if ctx.inside_part_struct_type():
            return [(variable, varType)] + self.visit(ctx.inside_part_struct_type())
        return [(variable, varType)]

                

# type Votien interface {
#     Add(x, y int) int; 
# }
# interface_declared: TYPE ID INTERFACE LB inside_part_interface RB endcode;
    def visitInterface_declared(self, ctx:MiniGoParser.Interface_declaredContext):
        # print("di qua visitInterface_declared")

        name= ctx.ID().getText()
        methods=self.visit(ctx.inside_part_interface())

        return InterfaceType(name, methods)

# Add(x, y int) int; (recusion)
# inside_part_interface: (sub_inside_part_interface) inside_part_interface
# 					| (sub_inside_part_interface);
    def visitInside_part_interface(self, ctx:MiniGoParser.Inside_part_interfaceContext):
        # print("di qua visitInside_part_interface")

        if ctx.inside_part_interface():
            return [self.visit(ctx.sub_inside_part_interface())] + self.visit(ctx.inside_part_interface())
        return [self.visit(ctx.sub_inside_part_interface())]    


# Add(x, y int) int; 
# sub_inside_part_interface: ID LP (interface_para_list)? RP type_withID? endcode;
    def visitSub_inside_part_interface(self, ctx:MiniGoParser.Sub_inside_part_interfaceContext):
        # return self.visitChildren(ctx)
        # print("di qua visitSub_inside_part_interface")

        name = ctx.ID().getText()
        # list type trong ()
        retType=VoidType()
        if ctx.type_withID():
            retType=self.visit(ctx.type_withID())

        # methodReceiver=None
        params=[]
        if ctx.interface_para_list():
            params=self.visit(ctx.interface_para_list())
        # stmts= [] 
        # currType = VoidType()
        # for i in reversed(param):
        #     if isinstance(i.varType, VoidType):
        #         i.varType = currType
        #     else: 
        #         currType = i.varType    
        #     # # print(i)
            
        return Prototype(name, params, retType)



# interface_para_list: param_interface COMMA interface_para_list | param_interface; ;
# a int, b float
    def visitInterface_para_list(self, ctx:MiniGoParser.Interface_para_listContext):
        # print("di qua visitInterface_para_list")

        return self.visit(ctx.param_interface()) if ctx.getChildCount() == 1 else self.visit(ctx.param_interface()) + self.visit(ctx.interface_para_list())


# param_interface: list_ID_interface type_withID COMMA param_interface | list_ID_interface type_withID;
    def visitParam_interface(self, ctx:MiniGoParser.Param_interfaceContext):
        # return self.visitChildren(ctx)

        # print("di qua visitParam_interface")
        list_ID = self.visit(ctx.list_ID_interface())
        type_withID = self.visit(ctx.type_withID())
        list_type = []
        for item in list_ID:
            list_type.append(type_withID)            
        return list_type + (self.visit(ctx.param_interface()) if ctx.param_interface() else [])


# list_ID_interface: ID COMMA list_ID_interface | ID;
    def visitList_ID_interface(self, ctx:MiniGoParser.List_ID_interfaceContext):
        # return self.visitChildren(ctx)
        return [ctx.ID().getText()] if ctx.getChildCount() == 1 else [ctx.ID().getText()] + self.visit(ctx.list_ID_interface())


    # list_statement: statement list_statement | statement;
    def visitList_statement(self, ctx:MiniGoParser.List_statementContext):
        return self.visitChildren(ctx)

        # # print("di qua visitList_statement")
        # if ctx.list_statement():
        #     return [self.visit(ctx.statement())] + self.visit(ctx.list_statement())
        # return [self.visit(ctx.statement())]


# statement:
# (
# 	declared_statement
# 	| assign_statement
# 	| if_statement
# 	| for_statement
# 	| break_statement
# 	| continue_statement
# 	| call_statement
# 	| return_statement
# );
    def visitStatement(self, ctx:MiniGoParser.StatementContext):
        # return self.visitChildren(ctx)

        # print("di qua visitStatement")
        return self.visit(ctx.getChild(0))


# declared_statement: variables_declared | constants_declared;
    def visitDeclared_statement(self, ctx:MiniGoParser.Declared_statementContext):
        # return self.visitChildren(ctx)

        # print("di qua visitDeclared_statement")
        return self.visit(ctx.getChild(0))

# assign_op: COLONEQUAL | ADDEQUAL | SUBEQUAL | MULEQUAL | DIVEQUAL | DIVDIVEQUAL;
    def visitAssign_op(self, ctx:MiniGoParser.Assign_opContext):
        # return self.visitChildren(ctx)

        # print("di qua visitAssign_op")
        return ctx.getText()

# assign_statement: lhs assign_op rhs;
    def visitAssign_statement(self, ctx:MiniGoParser.Assign_statementContext):
        # return self.visitChildren(ctx)

        # print("di qua visitAssign_statement")

        lhs=self.visit(ctx.lhs())
        # print("lhs: ", lhs)
        op=self.visit(ctx.assign_op())
        # print("op: ", op)
        rhs=self.visit(ctx.rhs())
        # print("rhs: ", rhs)


        if op == ":=":
            return Assign(lhs, rhs)
        if op == "+=":
            return Assign(lhs, BinaryOp("+", lhs, rhs))
        if op == "-=":
            return Assign(lhs, BinaryOp("-", lhs, rhs))
        if op == "*=":
            return Assign(lhs, BinaryOp("*", lhs, rhs))
        if op == "/=":
            return Assign(lhs, BinaryOp("/", lhs, rhs))
        if op == "%=":
            return Assign(lhs, BinaryOp("%", lhs, rhs)) 

        # print("error in visitAssign_statement: no op")     



# index: LSB expression RSB;
    def visitIndex(self, ctx:MiniGoParser.IndexContext):
        # return self.visitChildren(ctx)

        # print("di qua visitIndex")
        return [self.visit(ctx.expression())]


# lhs: lhs (DOT ID index)
# 		| lhs (DOT ID)
# 		| lhs index
# 		| ID;					//a[2].b.c[2]
    def visitLhs(self, ctx:MiniGoParser.LhsContext):
        # return self.visitChildren(ctx)

        # print("di qua visitlhs")
        # todo
        if ctx.getChildCount()==1:
            # print("1")
            return Id(ctx.ID().getText())
        if ctx.getChildCount()==2:
            # print("2")
            # return ArrayCell(self.visit(ctx.lhs()), self.visit(ctx.index()))
            lhs = self.visit(ctx.lhs())
            if type(lhs) == ArrayCell:
                return ArrayCell(lhs.arr, lhs.idx  + self.visit(ctx.index()))
            return ArrayCell(lhs, self.visit(ctx.index()))
        if ctx.getChildCount()==3:
            # print("3")
            return FieldAccess(self.visit(ctx.lhs()), ctx.ID().getText())

        # print("4")
        arr=FieldAccess(self.visit(ctx.lhs()), ctx.ID().getText())
        idx=self.visit(ctx.index())
        return ArrayCell(arr, idx)
    

# rhs: expression;
    def visitRhs(self, ctx:MiniGoParser.RhsContext):
        # return self.visitChildren(ctx)

        # print("di qua visitRhs")
        return self.visit(ctx.expression())


    

# if_statement: IF expression LB (inside_part_func)? RB (elif_part)? (else_part)?;
    def visitIf_statement(self, ctx:MiniGoParser.If_statementContext):
        # return self.visitChildren(ctx)
        def recursive_if(list_else_if_statement:List[tuple[Expr,Block]], else_statement: Block):
            if len(list_else_if_statement) == 0:
                return else_statement
            exp, block = list_else_if_statement[0]
            return If(
                exp,
                block,
                recursive_if(list_else_if_statement[1:], else_statement)
            )
    
        # print("di qua visitIf_statement")
        expr=self.visit(ctx.expression())
        thenStmt = None
        if ctx.inside_part_func():
            thenStmt=Block(self.visit(ctx.inside_part_func()))
        elseStmt = None
        
        elif_part=[]
        else_part=None
        if ctx.elif_part():
            elif_part=self.visit(ctx.elif_part())
        if ctx.else_part():
            else_part=self.visit(ctx.else_part())

        # print("elif_part: ", elif_part) 
        # print("else_part: ", else_part)

        elseStmt=recursive_if(elif_part, else_part)        

        # print("end visitIf_statement")
        # print("expr: ", expr)
        # print("thenStmt: ", thenStmt)
        # print("elseStmt: ", elseStmt)
        return If(expr, thenStmt, elseStmt)


# elif_part: ELSE IF expression LB (inside_part_func)? RB elif_part
# 		| ELSE IF expression LB (inside_part_func)? RB;
    def visitElif_part(self, ctx:MiniGoParser.Elif_partContext):
        # return self.visitChildren(ctx)

        # print("di qua visitElif_part")
        exp = self.visit(ctx.expression())
        block = Block(self.visit(ctx.inside_part_func())) if ctx.inside_part_func() else Block([])

        if ctx.elif_part():
            return [(exp, block)] + self.visit(ctx.elif_part())
        return [(exp, block)]

# else_part: ELSE LB (inside_part_func)? RB;
    def visitElse_part(self, ctx:MiniGoParser.Else_partContext):
        # return self.visitChildren(ctx)

        # print("di qua visitElse_part")
        if ctx.inside_part_func():
            return Block(self.visit(ctx.inside_part_func()))
        return Block([])


# for_assign: ID assign_op expression;		// x := 1
    def visitFor_assign(self, ctx:MiniGoParser.For_assignContext):
        # return self.visitChildren(ctx)
        # print("di qua visitFor_assign")

        lhs=Id(ctx.ID().getText())
        # print("lhs: ", lhs)
        op=self.visit(ctx.assign_op())
        # print("op: ", op)
        rhs=self.visit(ctx.expression())
        # print("rhs: ", rhs)


        if op == ":=":
            return Assign(lhs, rhs)
        if op == "+=":
            return Assign(lhs, BinaryOp("+", lhs, rhs))
        if op == "-=":
            return Assign(lhs, BinaryOp("-", lhs, rhs))
        if op == "*=":
            return Assign(lhs, BinaryOp("*", lhs, rhs))
        if op == "/=":
            return Assign(lhs, BinaryOp("/", lhs, rhs))
        if op == "%=":
            return Assign(lhs, BinaryOp("%", lhs, rhs)) 



# for_statement: for_basic | for_init_cond | for_range;
    def visitFor_statement(self, ctx:MiniGoParser.For_statementContext):
        # return self.visitChildren(ctx)
        # print("di qua visitFor_statement")

        return self.visit(ctx.getChild(0))


# for_basic: FOR (expression) LB (inside_part_func)? RB;
    def visitFor_basic(self, ctx:MiniGoParser.For_basicContext):
        # return self.visitChildren(ctx)
        # print("di qua visitFor_basic")

        cond=self.visit(ctx.expression())
        loop=None
        if ctx.inside_part_func():
            loop=Block(self.visit(ctx.inside_part_func()))
        
        return ForBasic(cond, loop)

# forstep
# for_init_cond: FOR ((for_assign | declared_init) SEMICOLON (expression) SEMICOLON for_assign) LB (inside_part_func)? RB;
    def visitFor_init_cond(self, ctx:MiniGoParser.For_init_condContext):
        # return self.visitChildren(ctx)
        
        # print("di qua visitFor_init_cond")
        init=self.visit(ctx.getChild(1))
        # print("init: ", init)
        cond=self.visit(ctx.expression())
        # print("cond: ", cond)
        upda=self.visit(ctx.getChild(5))
        # print("upda: ", upda)
        loop=None
        if ctx.inside_part_func():
            loop=Block(self.visit(ctx.inside_part_func()))
        return ForStep(init, cond, upda, loop)


# ForEach
# for_range: FOR (ID COMMA ID COLONEQUAL RANGE expression) LB (inside_part_func)? RB;
    def visitFor_range(self, ctx:MiniGoParser.For_rangeContext):
        # return self.visitChildren(ctx)

        # print("di qua visitFor_range")
        idx = Id(ctx.ID()[0].getText())
        value = Id(ctx.ID()[1].getText())
        arr = self.visit(ctx.expression())
        loop=None
        if ctx.inside_part_func():
            loop=Block(self.visit(ctx.inside_part_func()))
        return ForEach(idx, value, arr, loop)



# break_statement: BREAK;
    def visitBreak_statement(self, ctx:MiniGoParser.Break_statementContext):
        # return self.visitChildren(ctx)

        # print("di qua visitBreak_statement")
        return Break()


# continue_statement: CONTINUE;
    def visitContinue_statement(self, ctx:MiniGoParser.Continue_statementContext):
        # return self.visitChildren(ctx)
        
        # print("di qua visitContinue_statement")
        return Continue()


# call_statement: function_call | method_call;
    def visitCall_statement(self, ctx:MiniGoParser.Call_statementContext):
        # return self.visitChildren(ctx)

        # print("di qua visitCall_statement")
        return self.visit(ctx.getChild(0))


# function_call: ID LP list_expression? RP;
    def visitFunction_call(self, ctx:MiniGoParser.Function_callContext):
        # return self.visitChildren(ctx)

        # print("di qua visitFunction_call")

        funName=ctx.ID().getText()
        args=[] # [] if there is no arg 
        if ctx.list_expression():
            args=self.visit(ctx.list_expression())
        return FuncCall(funName, args)


# method_call: lhs DOT (ID LP list_expression? RP);
    def visitMethod_call(self, ctx:MiniGoParser.Method_callContext):
        # return self.visitChildren(ctx)

        # print("di qua visitMethod_call")

        receiver=self.visit(ctx.lhs()) 
        metName = ctx.ID().getText()
        args=[]
        if ctx.list_expression():
            args=self.visit(ctx.list_expression())

        return MethCall(receiver, metName, args)


# return_statement: RETURN expression?;
    def visitReturn_statement(self, ctx:MiniGoParser.Return_statementContext):
        # return self.visitChildren(ctx)

        # print("di qua visitReturn_statement")
        if ctx.expression():
            return Return(self.visit(ctx.expression()))
        return Return(None)

