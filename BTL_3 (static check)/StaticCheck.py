from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce
from typing import List 
from typing import Tuple

from StaticError import Type as StaticErrorType
from AST import Type

class FunctionType(Type):
    def __str__(self):
        return "FunctionType"

    def accept(self, v, param):
        return v.visitFunctionType(self, v, param)


class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + str(self.name) + "," + str(self.mtype) + ("" if self.value is None else "," + str(self.value)) + ")"

class StaticChecker(BaseVisitor,Utils):
        
    
    def __init__(self,ast):
        self.ast = ast
        self.list_type = []
        self.list_function: List[FuncDecl] =  [
                FuncDecl("getFloat", [], FloatType(), Block([])),
                FuncDecl("putFloat", [ParamDecl("SANG", FloatType())], VoidType(), Block([])),
                FuncDecl("putFloatLn", [ParamDecl("SANG", FloatType())], VoidType(), Block([])),
                
                FuncDecl("getBool", [], BoolType(), Block([])),
                FuncDecl("putBool", [ParamDecl("SANG", BoolType())], VoidType(), Block([])),
                FuncDecl("putBoolLn", [ParamDecl("SANG", BoolType())], VoidType(), Block([])),
                
                FuncDecl("getInt", [], IntType(), Block([])),
                FuncDecl("putInt", [ParamDecl("SANG", IntType())], VoidType(), Block([])),
                FuncDecl("putIntLn", [ParamDecl("SANG", IntType())], VoidType(), Block([])),

                
                FuncDecl("getString", [], IntType(), Block([])),
                FuncDecl("putString", [ParamDecl("SANG", IntType())], VoidType(), Block([])),
                FuncDecl("putStringLn", [ParamDecl("SANG", StringType())], VoidType(), Block([])),
                FuncDecl("putLn", [], VoidType(), Block([])),
            ]
        self.function_current = None

    def check(self):
        self.visit(self.ast, None)

    def checkType(self, left, right, list_type_permission = []):
        if type(right) == StructType and right.name == "":
            if isinstance(left, Id):
                ketqua = self.lookup(left.name, self.list_type, lambda x: x.name)
                if ketqua != None:
                    return True
            return False

        left = self.lookup(left.name, self.list_type, lambda x: x.name) if isinstance(left, Id) else left
        right = self.lookup(right.name, self.list_type, lambda x: x.name) if isinstance(right, Id) else right

        if (type(left), type(right)) in list_type_permission:
            if isinstance(left, InterfaceType) and isinstance(right, StructType):
                list_prototype_interface= left.methods
                list_prototype_struct = [method.fun for method in right.methods]
                # # print("list_prototype: ", list_prototype_interface)
                # # print("list_prototype_struct: ", list_prototype_struct)
                for item in list_prototype_interface:
                    # kiem tra name
                    ketqua=self.lookup(item.name, list_prototype_struct, lambda x: x.name)
                    if ketqua is None:
                        return False
                    # kiem tra type
                    if not self.checkType(item.retType, ketqua.retType):
                        return False
                    # kiem tra param
                    if len(item.params) != len(ketqua.params):
                        return False
                    # Check if the types of parameters in the interface method match the corketquaponding parameters in the struct method
                    for param, arg in zip(item.params, ketqua.params):
                        # # print("param: ", param)
                        # # print("arg: ", arg)

                        if not self.checkType(param, arg.parType):
                            return False

                return True                                                    

            return True

        if (isinstance(left, InterfaceType) and isinstance(right, InterfaceType)) or (isinstance(left, StructType) and isinstance(right, StructType)):
            return left.name == right.name

        if isinstance(left, ArrayType) and isinstance(right, ArrayType):
            if len(left.dimens) != len(right.dimens):
                return False
            if left.eleType != right.eleType:
                return False
            if left.dimens != right.dimens:
                return False

            return self.checkType(left.eleType, right.eleType, list_type_permission)
        return type(left) == type(right)


    def visitProgram(self, ast, c ):
        def visitMethodDecl_sub(ast, c) -> MethodDecl:
            # TODO: Implement
            # check Redeclared method trong stuct
            if any(ast.fun.name == ele[0] for ele in c.elements):
                raise Redeclared(Method(), ast.fun.name)

            ketqua = self.lookup(ast.fun.name, c.methods, lambda x: x.fun.name)
            if ketqua != None:
                raise Redeclared(Method(), ast.fun.name)
            
            c.methods.append(ast)
            return ast

        # check redeclared method vs field ~ elements
        dictionary_struct = {}

        global_list = ["getInt", "putInt", "putIntLn", "getFloat", "putFloat", "putFloatLn",
                    "getBool", "putBool", "putBoolLn", "getString", "putString", "putStringLn", "putLn"]
        for item in ast.decl:
            # interfacetype, structtype, var, const, func
            # khong co method
            if isinstance(item, Type):
                if item.name in global_list:
                    raise Redeclared(StaticErrorType(), item.name)                       
                global_list.append(item.name)
                # self.list_type.append(item)
            elif isinstance(item, VarDecl):
                if item.varName in global_list:
                    raise Redeclared(Variable(), item.varName)
                global_list.append(item.varName)
            elif isinstance(item, ConstDecl):
                if item.conName in global_list:
                    raise Redeclared(Constant(), item.conName)
                global_list.append(item.conName)
            elif isinstance(item, FuncDecl):
                if item.name in global_list:
                    raise Redeclared(Function(), item.name)
                global_list.append(item.name)


        # dua structtype, InterfaceType vao list_type
        self.list_type = reduce(lambda acc, ele: [self.visit(ele, acc)] + acc if isinstance(ele, Type) else acc, ast.decl, [])
        # dua function vao list_function
        # self.list_function = self.list_function + list(filter(lambda item: isinstance(item, FuncDecl), ast.decl))
        for item in ast.decl:
            if isinstance(item, FuncDecl):
                self.list_function.append(item)

        # dua methoddecl vao structtype
        list(map(
            lambda item: visitMethodDecl_sub(item, self.lookup(item.recType.name, self.list_type, lambda x: x.name)), 
             list(filter(lambda item: isinstance(item, MethodDecl), ast.decl))
        ))

        # Initialize the first scope with built-in function symbols
        initial_scope = [
            Symbol("getInt", FunctionType()),
            Symbol("putInt", FunctionType()),
            Symbol("putIntLn", FunctionType()),
            Symbol("getFloat", FunctionType()),
            Symbol("putFloat", FunctionType()),
            Symbol("putFloatLn", FunctionType()),
            Symbol("getBool", FunctionType()),
            Symbol("putBool", FunctionType()),
            Symbol("putBoolLn", FunctionType()),
            Symbol("getString", FunctionType()),
            Symbol("putString", FunctionType()),
            Symbol("putStringLn", FunctionType()),
            Symbol("putLn", FunctionType()),
        ]

        # Filter declarations from ast.decl
        filtered_decls = filter(lambda item: isinstance(item, Decl), ast.decl)

        # Initialize accumulator
        accumulator = [initial_scope]

        # Iterate through filtered declarations
        for ele in filtered_decls:
            ketquault = self.visit(ele, accumulator)
            if isinstance(ketquault, Symbol):
                accumulator = [[ketquault] + accumulator[0]] + accumulator[1:]

    def visitStructType(self, ast, c ):
        # # print("visitStructType: ", ast)
        
        ketqua = self.lookup(ast.name, c, lambda x: x.name)
        if ketqua != None:
            raise Redeclared(StaticErrorType(), ast.name)
        
        def visitElements(element, c):
            ketqua = self.lookup(element[0], c, lambda x: x[0])
            if ketqua != None:
                raise Redeclared(Field(), element[0])
            return element

        ast.elements = reduce(lambda acc,ele: [visitElements(ele,acc)] + acc , ast.elements , [])
        return ast

    def visitPrototype(self, ast, c):
        ketqua = self.lookup(ast.name, c, lambda x: x.name)
        if ketqua != None:
            raise Redeclared(Prototype(), ast.name)
        return ast

    def visitInterfaceType(self, ast, c ):
        ketqua = self.lookup(ast.name, c, lambda x: x.name)
        if ketqua != None:
            raise Redeclared(StaticErrorType(), ast.name)  
        ast.methods = reduce(lambda acc,ele: [self.visit(ele,acc)] + acc , ast.methods , [])
        return ast
    
    def visitFuncDecl(self, ast, c ):
        ketqua = self.lookup(ast.name, c[0], lambda x: x.name)
        if ketqua != None:     # if ketqua in c[0]:
            raise Redeclared(Function(), ast.name) 

        if isinstance(ast.retType, ArrayType):
            # # print("ast.retType: ", ast.retType)
            ast.retType.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), ast.retType.dimens))
        
        self.function_current = ast
        # # print("self.function_current.retType: ", self.function_current.retType)

        self.visit(ast.body, [list(reduce(lambda acc,ele: [self.visit(ele,acc)] + acc, ast.params, []))] + c)

        return Symbol(ast.name, FunctionType(), None)
    

    def visitParamDecl(self, ast, c):
        # # print("visitParamDecl: ", ast)
        # # print("c: ")
        # for x in c:
            # print(x)
        # self.view_symbol_table(c)
        # TODO: Implement
        ketqua = self.lookup(ast.parName, c, lambda x: x.name)
        if ketqua != None:     # if ketqua in c[0]:
            raise Redeclared(Parameter(), ast.parName)
        
        return Symbol(ast.parName, ast.parType, None)

    def visitMethodDecl(self, ast, c ):
        # TODO: Implement
        # # print("visitMethodDecl: ", ast)
        self.function_current = ast.fun

        receiver_scope = [Symbol(ast.receiver, ast.recType, None)]

        param_scope = [list(reduce(lambda acc,ele: [self.visit(ele,acc)] + acc, ast.fun.params, []))]
        param_scope[0].extend(receiver_scope)
        # for x in param_scope:
        #     for i in x:
        #         # print("param_scope: ", i)
        func_scope = param_scope + c
        self.visit(ast.fun.body, func_scope)
        
        return None
        
    def visitVarDecl(self, ast, c ):
        # print("visitVarDecl: ", ast)
        ketqua = self.lookup(ast.varName, c[0], lambda x: x.name)
        if ketqua != None:
            raise Redeclared(Variable(), ast.varName) 
        

        # lay LHS and RHS type
        left = ast.varType if ast.varType else None
        if isinstance(ast.varType, ArrayType):
            left.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), ast.varType.dimens))
                
        right = self.visit(ast.varInit, c) if ast.varInit else None
        if isinstance(ast.varInit, ArrayLiteral):
            right.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), ast.varInit.dimens))
        




        if right is None:
            return Symbol(ast.varName, left, None)
        elif left is None:
            value = None
            if type(right) == IntType:
                value = IntLiteral(self.evaluate_ast(ast.varInit, c))            
            return Symbol(ast.varName, right, value)
        elif self.checkType(left, right, [(FloatType, IntType), (InterfaceType, StructType)]):
            value = None
            if type(right) == IntType:
                value = IntLiteral(self.evaluate_ast(ast.varInit, c))   
            return Symbol(ast.varName, left, value)
        
        raise TypeMismatch(ast)
        

    def visitConstDecl(self, ast, c ):
        # tim redeclared
        ketqua = self.lookup(ast.conName, c[0], lambda x: x.name)
        if ketqua != None:
            raise Redeclared(Constant(), ast.conName) 
        
        ast.conType = self.visit(ast.iniExpr, c)
        
        # # print("ast.conType: ", ast.conType)
        # # print("ast.iniExpr: ", ast.iniExpr)

        if type(self.visit(ast.iniExpr, c)) == IntType:
            value= IntLiteral(self.evaluate_ast(ast.iniExpr, c))
            return Symbol(ast.conName, ast.conType, value)

        return Symbol(ast.conName, ast.conType, ast.iniExpr)


    def visitBlock(self, ast, c):
        acc = [[]] + c 

        for ele in ast.member:
            if isinstance(ele, (FuncCall, MethCall)):
                ketquault = self.visit(ele, (acc, True))
            else:
                ketquault = self.visit(ele, acc)
            # ketquault = self.visit(ele, (acc, True)) if isinstance(ele, (FuncCall, MethCall)) else self.visit(ele, acc)
            if isinstance(ketquault, Symbol):
                acc[0] = [ketquault] + acc[0]


    def visitForBasic(self, ast, c ): 
        # if # TODO: Implement:
        if type(self.visit(ast.cond, c)) != BoolType:
            raise TypeMismatch(ast)
        self.visit(ast.loop, c)
        # self.visit(Block(ast.loop.member), c)


    def visitForStep(self, ast, c): 
        symbol = self.visit(ast.init, [[]] +  c)
        # # print("symbol: ", symbol)
        # test a:=1 -> var a = 1
        # # print("upda: ", ast.upda)

        # upda_var = None
        # if type(ast.upda.rhs) != BinaryOp:
        #     upda_var = Symbol(ast.upda.lhs.name, self.visit(ast.upda.rhs, c), ast.upda.rhs)

        # # print("upda_var: ", upda_var)

        symbol_list = [[symbol]]+c
        if type(self.visit(ast.cond, symbol_list)) != BoolType:    
            raise TypeMismatch(ast)
        
        # # print("ast.loop.member: ", ast.loop.member)
        self.visit(Block([ast.init] + [ast.upda] + ast.loop.member), c)
    
    def visitForEach(self, ast: ForEach, c: List[List[Symbol]]) -> None: 
        def makeArrayType_value(type_array):
            if len(type_array.dimens) == 1:
                return type_array.eleType
            return ArrayType(type_array.dimens[1:], type_array.eleType)
        
        # arr khong phai arraytype thi raise TypeMismatch
        type_array = self.visit(ast.arr, c)
        if type(self.visit(ast.arr, c)) != ArrayType:
            raise TypeMismatch(ast)
        
        # check idx de raise Redeclared
        type_idx = self.visit(ast.idx, c)
        # print("type_idx: ", type_idx)
        if type(type_idx) != IntType:
            raise TypeMismatch(ast)
        
        # check type cua var vs arr
        type_value = self.visit(ast.value, c)
        # print("type_value: ", type_value)
        # print("type_array: ", type_array)
        # print("type_array.eleType: ", type_array.eleType)
        type_value_arr = makeArrayType_value(type_array)
        if not self.checkType(type_value, type_value_arr):
            raise TypeMismatch(ast)          

        self.visit(Block(ast.loop.member), c)


    def visitId(self, ast, c):
        # # print("visitId: ", ast)
        ketqua = next(filter(None,[self.lookup(ast.name, scope, lambda x: x.name) for scope in c]), None)
    
        if ketqua and not isinstance(ketqua.mtype, Function):
            return ketqua.mtype
        raise Undeclared(Identifier(), ast.name)
    
    def visitFuncCall(self, ast, c):
        c, is_statement = c if isinstance(c, tuple) else (c, False)
        
        # # print("list_function: ")
        # for x in self.list_function:
        #     # print(x)
        ketqua = next(filter(None,[self.lookup(ast.funName, scope, lambda x: x.name) for scope in c]), None)
        # # print("ketqua: ", ketqua)
        # # print("ketqua.mtype: ", ketqua.mtype)
        if ketqua:
            if not isinstance(ketqua.mtype, FunctionType):
                raise Undeclared(Function(), ast.funName)

        # lay function hien tai
        ketqua = self.lookup(ast.funName, self.list_function, lambda x: x.name)
        if ketqua:
            if len(ketqua.params) != len(ast.args):
                raise TypeMismatch(ast)
            
            for param, arg in zip(ketqua.params, ast.args):
                arg_type = self.visit(arg, c)
                # # print("arg_type: ", arg_type)
                if isinstance(param.parType, ArrayType) and isinstance(arg_type, ArrayType):
                    param.parType.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), param.parType.dimens))
                    arg_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), arg_type.dimens))
                    
                    if param.parType.dimens != arg_type.dimens:
                        raise TypeMismatch(ast)
                    if param.parType.eleType != arg_type.eleType:
                        raise TypeMismatch(ast)
                
                # if not self.checkType(param.parType,self.visit(arg, c), [(FloatType, IntType), (InterfaceType, StructType)]):
                if not self.checkType(param.parType, arg_type):
                    raise TypeMismatch(ast)
                
            # stmt, voidtype => dung
            if is_statement and not type(ketqua.retType) == VoidType:
                raise TypeMismatch(ast)
            # expr, khong voidtype => dung
            if not is_statement and type(ketqua.retType) == VoidType:
                raise TypeMismatch(ast)
            return ketqua.retType
        raise Undeclared(Function(), ast.funName)

    def visitFieldAccess(self, ast, c):
        receiver_type = self.visit(ast.receiver, c)
        if isinstance(receiver_type, Id):
            receiver_type = self.lookup(receiver_type.name, self.list_type, lambda x: x.name)
        if not isinstance(receiver_type, StructType):
            raise TypeMismatch(ast)
        
        ketqua = self.lookup(ast.field, receiver_type.elements, lambda x: x[0])
        if ketqua is None:
            raise Undeclared(Field(), ast.field)
        return ketqua[1]

    def visitMethCall(self, ast, c):
        c, is_statement = c if isinstance(c, tuple) else (c, False)
        
        receiver_type = self.visit(ast.receiver, c)
        if isinstance(receiver_type, Id):
            receiver_type = self.lookup(receiver_type.name,self.list_type,lambda x:x.name) 
        # receiver_type = self.lookup(receiver_type.name,self.list_type,lambda x:x.name) if isinstance(receiver_type, Id) else receiver_type
        if not isinstance(receiver_type, StructType) and not isinstance(receiver_type, InterfaceType):
            raise TypeMismatch(ast)
         
        ketqua = self.lookup(ast.metName, receiver_type.methods, lambda x: x.fun.name) if isinstance(receiver_type, StructType) else self.lookup(ast.metName, receiver_type.methods, lambda x: x.name)
        
        if not ketqua:
            raise Undeclared(Method(), ast.metName)

        if type(receiver_type) == StructType:
            if len(ketqua.fun.params) != len(ast.args):
                raise TypeMismatch(ast)
            for param, arg in zip(ketqua.fun.params, ast.args):
                arg_type = self.visit(arg, c)
                # # print("arg_type: ", arg_type)
                if isinstance(param.parType, ArrayType) and isinstance(arg_type, ArrayType):
                    param.parType.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), param.parType.dimens))
                    arg_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), arg_type.dimens))

                    if param.parType.dimens != arg_type.dimens:
                        raise TypeMismatch(ast)
                    if param.parType.eleType != arg_type.eleType:
                        raise TypeMismatch(ast)
                    
                if not self.checkType(param.parType, arg_type, [(FloatType, IntType), (InterfaceType, StructType)]):
                    raise TypeMismatch(ast)
            if is_statement and not self.checkType(ketqua.fun.retType, VoidType()):
                raise TypeMismatch(ast)
            if not is_statement and self.checkType(ketqua.fun.retType, VoidType()):
                raise TypeMismatch(ast)
            return ketqua.fun.retType
        
        if type(receiver_type) == InterfaceType:
            if len(ketqua.params) != len(ast.args):
                raise TypeMismatch(ast)
            for param, arg in zip(ketqua.params, ast.args):
                arg_type = self.visit(arg, c)

                if isinstance(param, ArrayType) and isinstance(arg_type, ArrayType):
                    param.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), param.dimens))
                    arg_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), arg_type.dimens))
                    
                if not self.checkType(param, arg_type, [(FloatType, IntType), (InterfaceType, StructType)]):
                    raise TypeMismatch(ast)
            if is_statement and not self.checkType(ketqua.retType, VoidType()):
                raise TypeMismatch(ast)
            if not is_statement and self.checkType(ketqua.retType, VoidType()):
                raise TypeMismatch(ast)
            return ketqua.retType

    def visitIntType(self, ast, c): return ast
    def visitFloatType(self, ast, c): return ast
    def visitBoolType(self, ast, c): return ast
    def visitStringType(self, ast, c): return ast
    def visitVoidType(self, ast, c): return ast
    def visitArrayType(self, ast, c):
        list(map(lambda item: self.visit(item, c), ast.dimens))
        return ast
    
    def visitAssign(self, ast, c):
        # # # print("visitAssign: ", ast)
        # # self.view_symbol_table(c)
        if type(ast.lhs) == VoidType:
            raise TypeMismatch(ast)
        
        if type(ast.lhs) is Id:
            # TÌM KIẾM XEM BIẾN ĐÃ ĐƯỢC KHAI BÁO CHƯA ĐƯỢC KHAI BÁO THÌ TRẢ VỀ Symbol(ast.lhs.name, self.visit(ast.rhs, c), None)
            # auto declare neu chua declare
            flatten_list = [item for sublist in c for item in sublist]


            ketqua= self.lookup(ast.lhs.name, flatten_list, lambda x: x.name)
            # ketqua= next([self.lookup(ast.lhs.name, scope, lambda x: x.name) for scope in c], None)
            # ketqua = next(filter(None,[self.lookup(ast.name, scope, lambda x: x.name) for scope in c]), None)
            if ketqua is None:
                return Symbol(ast.lhs.name, self.visit(ast.rhs, c), ast.rhs)

        left = self.visit(ast.lhs, c)
        right = self.visit(ast.rhs, c)

        # # # print("left: ", left)
        # # print("right: ", right)

        if not self.checkType(left, right, [(FloatType, IntType), (InterfaceType, StructType)]):
            raise TypeMismatch(ast)
        
    def visitIf(self, ast, c): 
        if type(self.visit(ast.expr, c)) != BoolType:
            raise TypeMismatch(ast)
        self.visit(ast.thenStmt, c)
        if ast.elseStmt:
            self.visit(ast.elseStmt, c)

    def visitContinue(self, ast, c): return None
    def visitBreak(self, ast, c): return None
    def visitReturn(self, ast, c): 
        # # print("visitReturn: ", ast)
        # # print("c: ")
        # self.view_symbol_table(c)

        # neu ko co expr thi VoidType
        return_type=self.visit(ast.expr, c) if ast.expr else VoidType()

        if isinstance(return_type, ArrayType):
            return_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), return_type.dimens))
        if isinstance(self.function_current.retType, ArrayType):
            # # print("self.function_current.retType: ", self.function_current.retType)

            self.function_current.retType.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), self.function_current.retType.dimens))
        

        # # print("return_type: ", return_type) 
        # # print("self.function_current.retType: ", self.function_current.retType)

        if not self.checkType(self.function_current.retType, return_type):
            raise TypeMismatch(ast)
        return None
    
    def visitBinaryOp(self, ast, c):
        left = self.visit(ast.left, c)
        right = self.visit(ast.right, c)

        # # print("left: ", left)
        # # print("right: ", right)
        # # print("ast.op: ", ast.op)
        # # print("left: ", ast.left)
        # # print("right: ", ast.right)

        if ast.op in ['+']:
            if type(left) == StringType and type(right) == StringType:
                return StringType()
            if self.checkType(left, right, [(IntType, FloatType), (FloatType, IntType)]):
                if type(left) == FloatType:
                    return FloatType()
                elif type(right) == FloatType:
                    return FloatType()
                elif type(left) == IntType:
                    return IntType()
        # TODO: Implement
        if ast.op in ['-']:
            if self.checkType(left, right, [(IntType, FloatType), (FloatType, IntType)]):
                if type(left) == StringType:
                    raise TypeMismatch(ast)
                elif type(left) == FloatType:
                    return FloatType()
                elif type(right) == FloatType:
                    return FloatType()
                elif type(left) == IntType:
                    return IntType()
        if ast.op in ['*']:
            if self.checkType(left, right, [(IntType, FloatType), (FloatType, IntType)]):
                if type(left) == FloatType:
                    return FloatType()
                elif type(right) == FloatType:
                    return FloatType()
                elif type(left) == IntType:
                    return IntType()
        if ast.op in ['/']:
            if self.checkType(left, right, [(IntType, FloatType), (FloatType, IntType)]):
                if type(left) == FloatType:
                    return FloatType()
                elif type(right) == FloatType:
                    return FloatType()
                elif type(left) == IntType:
                    return IntType()
        if ast.op in ['%']:
            if self.checkType(left, right, [(IntType, FloatType), (FloatType, IntType)]):
                if type(left) == IntType and type(right) == IntType:
                    return IntType()
        if ast.op in ['==', '!=', '<', '<=', '>', '>=']:
            if self.checkType(left, right, [(IntType, FloatType), (FloatType, IntType)]):
                if type(left) == StringType and type(right) == StringType:
                    return BoolType()
                elif type(left) == FloatType and type(right) == FloatType:
                    return BoolType()
                elif type(left) == IntType and type(right) == IntType:
                    return BoolType()
        if ast.op in ['&&', '||']:
            if self.checkType(left, right, [(BoolType, BoolType)]):
                return BoolType()

        raise TypeMismatch(ast)

    def visitUnaryOp(self, ast, c):
        unary_type = self.visit(ast.body, c)
        if ast.op in ['-']:    
            if isinstance(unary_type, IntType):
                return IntType()
            if isinstance(unary_type, FloatType):
                return FloatType()
        if ast.op in ['!']:
            if isinstance(unary_type, BoolType):
                return BoolType()

        raise TypeMismatch(ast)    
    
    def visitArrayCell(self, ast, c):
        array_type = self.visit(ast.arr, c)

        if not isinstance(array_type, ArrayType):
            raise TypeMismatch(ast)
       
        # if not all(map(lambda item: self.checkType(self.visit(item, c), # TODO: Implement), ast.idx)):
        # check inttype cho index
        if not all(map(lambda item: self.checkType(self.visit(item, c), IntType()), ast.idx)):
            raise TypeMismatch(ast)
        if len(array_type.dimens) == len(ast.idx):
            # return # TODO: Implement
            return array_type.eleType
        elif len(array_type.dimens) > len(ast.idx):
            # return # TODO: Implement
            return ArrayType(array_type.dimens[len(ast.idx):], array_type.eleType)
        raise TypeMismatch(ast)

    def visitIntLiteral(self, ast, c): return IntType()
    def visitFloatLiteral(self, ast, c): return FloatType()
    def visitBooleanLiteral(self, ast, c): return BoolType()
    def visitStringLiteral(self, ast, c): return StringType()
    def visitArrayLiteral(self, ast , c):  
        def nested2recursive(dat, c):
            if isinstance(dat,list):
                list(map(lambda value: nested2recursive(value, c), dat))
            else:
                self.visit(dat, c)
        nested2recursive(ast.value, c)
        return ArrayType(ast.dimens, ast.eleType)
    
    def visitStructLiteral(self, ast, c): 
        list(map(lambda value: self.visit(value[1], c), ast.elements))
        struct = self.lookup(ast.name, self.list_type, lambda x: x.name)
        return struct

    def visitNilLiteral(self, ast, c): return StructType("", [], [])


    def view_symbol_table(self, symbol_table):
        print("--- Symbol Table ---------------------------------")
        for i, scope in enumerate(symbol_table):
            print(f"Scope {i}:")
            if not scope:
                print("  (Empty)")
            else:
                for symbol in scope:
                    print(f"  {symbol}")
        print("--- End of Symbol Table ------------------------------")

    def evaluate_ast(self, node, c ):
        # # print("evaluate_ast: ", node)

        if type(node) == IntLiteral:
            return int(node.value)

        elif type(node) == Id:
            # ketqua = self.lookup(node.name, c[0], lambda x: x.name)
            ketqua = next(filter(None,[self.lookup(node.name, scope, lambda x: x.name) for scope in c]), None)
            # # print("ketqua: ", ketqua)
            if ketqua:
                return int(ketqua.value.value) if ketqua.value else 0
## TODO binary và Unary, các trường hợp còn lại sẽ không hợp lệ vì sẽ không là kiểu int và thầy đã thông báo trên forum    
        elif type(node) == BinaryOp:
            left_value = self.evaluate_ast(node.left, c)
            right_value = self.evaluate_ast(node.right, c)
            if node.op == '+':
                return int(left_value + right_value)
            elif node.op == '-':
                return int(left_value - right_value)
            elif node.op == '*':
                return int(left_value * right_value)
            elif node.op == '/':
                return int(left_value / right_value)
            elif node.op == '%':
                return int(left_value % right_value)
        elif type(node) == UnaryOp:
            ketqua= self.evaluate_ast(node.body, c)
            if node.op == '-':
                return int(-ketqua)
        return 0        