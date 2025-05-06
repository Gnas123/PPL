from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce
from typing import List, Tuple


from StaticError import Type as StaticErrorType
from AST import Type

class FuntionType(Type):
    def __str__(self):
        return "FuntionType"

    def accept(self, v, param):
        return v.visitFuntionType(self, v, param)


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
        self.list_type: List[Union[StructType, InterfaceType]] = []
        self.list_function: List[FuncDecl] =  [
                FuncDecl("getInt", [], IntType(), Block([])),
                FuncDecl("putInt", [ParamDecl("SANG", IntType())], VoidType(), Block([])),
                FuncDecl("putIntLn", [ParamDecl("SANG", IntType())], VoidType(), Block([])),
                
                FuncDecl("getString", [], IntType(), Block([])),
                FuncDecl("putString", [ParamDecl("SANG", IntType())], VoidType(), Block([])),
                FuncDecl("putStringLn", [ParamDecl("SANG", StringType())], VoidType(), Block([])),
                FuncDecl("putLn", [], VoidType(), Block([])),

                FuncDecl("getFloat", [], FloatType(), Block([])),
                FuncDecl("putFloat", [ParamDecl("SANG", FloatType())], VoidType(), Block([])),
                FuncDecl("putFloatLn", [ParamDecl("SANG", FloatType())], VoidType(), Block([])),

                FuncDecl("getBool", [], BoolType(), Block([])),
                FuncDecl("putBool", [ParamDecl("SANG", BoolType())], VoidType(), Block([])),
                FuncDecl("putBoolLn", [ParamDecl("SANG", BoolType())], VoidType(), Block([])),
            ]
        self.function_current: FuncDecl = None

    def check(self):
        self.visit(self.ast, None)

    def checkType(self, LSH_type: Type, RHS_type: Type, list_type_permission: List[Tuple[Type, Type]] = []) -> bool:
        if type(RHS_type) == StructType and RHS_type.name == "":
            if isinstance(LSH_type, Id):
                res = self.lookup(LSH_type.name, self.list_type, lambda x: x.name)
                if not res is None:
                    return True
            return False
            # return True        

        LSH_type = self.lookup(LSH_type.name, self.list_type, lambda x: x.name) if isinstance(LSH_type, Id) else LSH_type
        RHS_type = self.lookup(RHS_type.name, self.list_type, lambda x: x.name) if isinstance(RHS_type, Id) else RHS_type

        if (type(LSH_type), type(RHS_type)) in list_type_permission:
            if isinstance(LSH_type, InterfaceType) and isinstance(RHS_type, StructType):
                list_prototype_interface= LSH_type.methods
                list_prototype_struct = [method.fun for method in RHS_type.methods]
                # # print("list_prototype: ", list_prototype_interface)
                # # print("list_prototype_struct: ", list_prototype_struct)
                for item in list_prototype_interface:
                    # kiem tra name
                    res=self.lookup(item.name, list_prototype_struct, lambda x: x.name)
                    if res is None:
                        return False
                    # kiem tra type
                    if not self.checkType(item.retType, res.retType):
                        return False
                    # kiem tra param
                    if len(item.params) != len(res.params):
                        return False
                    # Check if the types of parameters in the interface method match the corresponding parameters in the struct method
                    for param, arg in zip(item.params, res.params):
                        # # print("param: ", param)
                        # # print("arg: ", arg)

                        if not self.checkType(param, arg.parType):
                            return False

                return True                                                    

            return True

        if (isinstance(LSH_type, InterfaceType) and isinstance(RHS_type, InterfaceType)) or (isinstance(LSH_type, StructType) and isinstance(RHS_type, StructType)):
            return LSH_type.name == RHS_type.name

        if isinstance(LSH_type, ArrayType) and isinstance(RHS_type, ArrayType):
            if len(LSH_type.dimens) != len(RHS_type.dimens):
                return False
            if LSH_type.eleType != RHS_type.eleType:
                return False
            if LSH_type.dimens != RHS_type.dimens:
                return False
            # if list_type_permission == []:
            #     for idx1, idx2 in zip(LSH_type.dimens, RHS_type.dimens):
            #         if idx1.value != idx2.value:
            #             return False

            # for idx1, idx2 in zip(LSH_type.dimens, RHS_type.dimens):
            #     # print("idx1: ", idx1)
            #     # print("idx2: ", idx2)
            #     if self.evaluate_ast(idx1.value, None) != self.evaluate_ast(idx2.value, None):
            #         return False
            return self.checkType(LSH_type.eleType, RHS_type.eleType, list_type_permission)
        return type(LSH_type) == type(RHS_type)


    def visitProgram(self, ast: Program,c : None):
        def visitMethodDecl(ast: MethodDecl, c: StructType) -> MethodDecl:
            # TODO: Implement
            # check Redeclared method trong stuct
            if any(ast.fun.name == ele[0] for ele in c.elements):
                raise Redeclared(Method(), ast.fun.name)

            res = self.lookup(ast.fun.name, c.methods, lambda x: x.fun.name)
            if not res is None:
                raise Redeclared(Method(), ast.fun.name)
            
            c.methods.append(ast)
            return ast

        # check redeclared method vs field ~ elements
        dictionary_struct = {}

        list_str = ["getInt", "putInt", "putIntLn", "getFloat", "putFloat", "putFloatLn",
                    "getBool", "putBool", "putBoolLn", "getString", "putString", "putStringLn", "putLn"]
        for item in ast.decl:
            # interfacetype, structtype, var, const, func
            # khong co method
            if isinstance(item, Type):
                if item.name in list_str:
                    raise Redeclared(StaticErrorType(), item.name)                       
                list_str.append(item.name)
                # self.list_type.append(item)
            elif isinstance(item, VarDecl):
                if item.varName in list_str:
                    raise Redeclared(Variable(), item.varName)
                list_str.append(item.varName)
            elif isinstance(item, ConstDecl):
                if item.conName in list_str:
                    raise Redeclared(Constant(), item.conName)
                list_str.append(item.conName)
            elif isinstance(item, FuncDecl):
                if item.name in list_str:
                    raise Redeclared(Function(), item.name)
                list_str.append(item.name)


        # dua structtype, InterfaceType vao list_type
        self.list_type = reduce(lambda acc, ele: [self.visit(ele, acc)] + acc if isinstance(ele, Type) else acc, ast.decl, [])
        # dua function vao list_function
        self.list_function = self.list_function + list(filter(lambda item: isinstance(item, FuncDecl), ast.decl))
        
        # dua methoddecl vao structtype
        list(map(
            lambda item: visitMethodDecl(item, self.lookup(item.recType.name, self.list_type, lambda x: x.name)), 
             list(filter(lambda item: isinstance(item, MethodDecl), ast.decl))
        ))

        reduce(
            lambda acc, ele: [
                ([result] + acc[0]) if isinstance(result := self.visit(ele, acc), Symbol) else acc[0]
            ] + acc[1:], 
            # loc ra method, function, var, const
            filter(lambda item: isinstance(item, Decl), ast.decl), 
            # tam vuc dau tien= list built-in function
            [[
                Symbol("getInt", FuntionType()),
                Symbol("putInt", FuntionType()),
                Symbol("putIntLn", FuntionType()),

                Symbol("getFloat", FuntionType()),
                Symbol("putFloat", FuntionType()),
                Symbol("putFloatLn", FuntionType()),

                Symbol("getBool", FuntionType()),
                Symbol("putBool", FuntionType()),
                Symbol("putBoolLn", FuntionType()),

                Symbol("getString", FuntionType()),
                Symbol("putString", FuntionType()),
                Symbol("putStringLn", FuntionType()),
                Symbol("putLn", FuntionType()),
            ]]
        ) 


    def visitStructType(self, ast: StructType, c : List[Union[StructType, InterfaceType]]) -> StructType:
        # # print("visitStructType: ", ast)
        
        res = self.lookup(ast.name, c, lambda x: x.name)
        if not res is None:
            raise Redeclared(StaticErrorType(), ast.name)
        
        def visitElements(element: Tuple[str,Type], c: List[Tuple[str,Type]]) -> Tuple[str,Type]:
            # TODO: Implement
            res = self.lookup(element[0], c, lambda x: x[0])
            if not res is None:
                raise Redeclared(Field(), element[0])
            return element

        ast.elements = reduce(lambda acc,ele: [visitElements(ele,acc)] + acc , ast.elements , [])
        return ast

    def visitPrototype(self, ast: Prototype, c: List[Prototype]) -> Prototype:
        # TODO: Implement
        # # print("visitPrototype: ", ast)
        res = self.lookup(ast.name, c, lambda x: x.name)
        if not res is None:
            raise Redeclared(Prototype(), ast.name)
        return ast

    def visitInterfaceType(self, ast: InterfaceType, c : List[Union[StructType, InterfaceType]]) -> InterfaceType:
        res = self.lookup(ast.name, c, lambda x: x.name)
        if not res is None:
            raise Redeclared(StaticErrorType(), ast.name)  
        ast.methods = reduce(lambda acc,ele: [self.visit(ele,acc)] + acc , ast.methods , [])
        return ast
    
    def visitFuncDecl(self, ast: FuncDecl, c : List[List[Symbol]]) -> Symbol:
        # # print("visitFuncDecl: ", ast)
        # TODO: Implement
        res = self.lookup(ast.name, c[0], lambda x: x.name)
        if not res is None:     # if res in c[0]:
            raise Redeclared(Function(), ast.name) 


        if isinstance(ast.retType, ArrayType):
            # # print("ast.retType: ", ast.retType)
            ast.retType.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), ast.retType.dimens))
        
        self.function_current = ast
        # # print("self.function_current.retType: ", self.function_current.retType)


        self.visit(ast.body, [list(reduce(lambda acc,ele: [self.visit(ele,acc)] + acc, ast.params, []))] + c)
        return Symbol(ast.name, FuntionType(), None)
    

    def visitParamDecl(self, ast: ParamDecl, c: List[Symbol]) -> Symbol:
        # # print("visitParamDecl: ", ast)
        # # print("c: ")
        # for x in c:
            # print(x)
        # self.view_symbol_table(c)
        # TODO: Implement
        res = self.lookup(ast.parName, c, lambda x: x.name)
        if not res is None:     # if res in c[0]:
            raise Redeclared(Parameter(), ast.parName)
        
        return Symbol(ast.parName, ast.parType, None)

    def visitMethodDecl(self, ast: MethodDecl, c : List[List[Symbol]]) -> None:
        # TODO: Implement
        # # print("visitMethodDecl: ", ast)
        self.function_current = ast.fun

        # self.visit(ast.fun.body, [list(reduce(lambda acc,ele: [self.visit(ele,acc)] + acc, ast.fun.params, []+[Symbol(ast.receiver, ast.recType, None)]))] + c)

        receiver_scope = [Symbol(ast.receiver, ast.recType, None)]
        # for x in receiver_scope:
        #     # print("receiver_scope: ", x)
        # # check luon redeclared param

        param_scope = [list(reduce(lambda acc,ele: [self.visit(ele,acc)] + acc, ast.fun.params, []))]
        param_scope[0].extend(receiver_scope)
        # for x in param_scope:
        #     for i in x:
        #         # print("param_scope: ", i)
        func_scope = param_scope + c
        self.visit(ast.fun.body, func_scope)
        
        return None
        
    def visitVarDecl(self, ast: VarDecl, c : List[List[Symbol]]) -> Symbol:
        # # print("visitVarDecl: ", ast)
        res = self.lookup(ast.varName, c[0], lambda x: x.name)
        if not res is None:
            raise Redeclared(Variable(), ast.varName) 
        

        # lay LHS and RHS type
        LHS_type = ast.varType if ast.varType else None
        if isinstance(ast.varType, ArrayType):
            LHS_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), ast.varType.dimens))
                
        RHS_type = self.visit(ast.varInit, c) if ast.varInit else None
        if isinstance(ast.varInit, ArrayLiteral):
            RHS_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), ast.varInit.dimens))
        




        if RHS_type is None:
            return Symbol(ast.varName, LHS_type, None)
        elif LHS_type is None:
            value = None
            if type(RHS_type) == IntType:
                value = IntLiteral(self.evaluate_ast(ast.varInit, c))            
            return Symbol(ast.varName, RHS_type, value)
        # elif isinstance(LHS_type, ArrayType) and RHS_type in [IntType, FloatType, StringType, BoolType, StructType]:
        #     if self.checkType(LHS_type.eleType, RHS_type, [(FloatType, IntType), (InterfaceType, StructType)]):
        #         return Symbol(ast.varName, LHS_type, None)
        elif self.checkType(LHS_type, RHS_type, [(FloatType, IntType), (InterfaceType, StructType)]):
            value = None
            if type(RHS_type) == IntType:
                value = IntLiteral(self.evaluate_ast(ast.varInit, c))   
            return Symbol(ast.varName, LHS_type, value)
            # return Symbol(ast.varName, LHS_type, None)
        
        raise TypeMismatch(ast)
        

    def visitConstDecl(self, ast: ConstDecl, c : List[List[Symbol]]) -> Symbol:
        # TODO: Implement
        # # print("visitConstDecl: ", ast)

        # tim redeclared
        res = self.lookup(ast.conName, c[0], lambda x: x.name)
        if not res is None:
            raise Redeclared(Constant(), ast.conName) 
        
        ast.conType = self.visit(ast.iniExpr, c)
        
        # # print("ast.conType: ", ast.conType)
        # # print("ast.iniExpr: ", ast.iniExpr)

        if type(self.visit(ast.iniExpr, c)) == IntType:
            value= IntLiteral(self.evaluate_ast(ast.iniExpr, c))
            return Symbol(ast.conName, ast.conType, value)

        return Symbol(ast.conName, ast.conType, ast.iniExpr)


    def visitBlock(self, ast: Block, c: List[List[Symbol]]) -> None:
        acc = [[]] + c 

        for ele in ast.member:
            result = self.visit(ele, (acc, True)) if isinstance(ele, (FuncCall, MethCall)) else self.visit(ele, acc)
            if isinstance(result, Symbol):
                acc[0] = [result] + acc[0]


    def visitForBasic(self, ast: ForBasic, c : List[List[Symbol]]) -> None: 
        # if # TODO: Implement:
        if type(self.visit(ast.cond, c)) != BoolType:
            raise TypeMismatch(ast)
        self.visit(ast.loop, c)
        # self.visit(Block(ast.loop.member), c)


    def visitForStep(self, ast: ForStep, c: List[List[Symbol]]) -> None: 
        symbol = self.visit(ast.init, [[]] +  c)
        # # print("symbol: ", symbol)
        # test a:=1 -> var a = 1
        # # print("upda: ", ast.upda)

        # upda_var = None
        # if type(ast.upda.rhs) != BinaryOp:
        #     upda_var = Symbol(ast.upda.lhs.name, self.visit(ast.upda.rhs, c), ast.upda.rhs)

        # # print("upda_var: ", upda_var)

        # if # TODO: Implement:
        if type(self.visit(ast.cond, [[symbol]]+c)) != BoolType:    
            raise TypeMismatch(ast)
        
        # # print("ast.loop.member: ", ast.loop.member)
        self.visit(Block([ast.init] + [ast.upda] + ast.loop.member), c)
    
    def visitForEach(self, ast: ForEach, c: List[List[Symbol]]) -> None: 
        # self.visit(Block([VarDecl(ast.idx.name, None, None), VarDecl(ast.value.name, None, None)] + ast.loop.member), c)

        type_array = self.visit(ast.arr, c)
        if not type(type_array) == ArrayType:
            raise TypeMismatch(ast)

                
        self.visit(Block([VarDecl(ast.idx.name, IntType(), None),
                        VarDecl(ast.value.name, 
                                type_array.eleType if len(type_array.dimens) == 1 else ArrayType(type_array.dimens[1:], type_array.eleType),
                                    None)] + ast.loop.member)
                        , c)

    def visitId(self, ast: Id, c: List[List[Symbol]]) -> Type:
        # res = # TODO: Implement
        # # print("visitId: ", ast)

        res = next(filter(None,[self.lookup(ast.name, scope, lambda x: x.name) for scope in c]), None)
    
        if res and not isinstance(res.mtype, Function):
            return res.mtype
        raise Undeclared(Identifier(), ast.name)
    
    def visitFuncCall(self, ast: FuncCall, c: Union[List[List[Symbol]], Tuple[List[List[Symbol]], bool]]) -> Type:
        # # print("visitFuncCall: ", ast)
        
        is_stmt = False
        # case funcall, MethCall
        if isinstance(c, tuple):
            c, is_stmt = c
        
        # # print("list_function: ")
        # for x in self.list_function:
        #     # print(x)
        res = next(filter(None,[self.lookup(ast.funName, scope, lambda x: x.name) for scope in c]), None)
        # # print("res: ", res)
        # # print("res.mtype: ", res.mtype)
        if res:
            if not isinstance(res.mtype, FuntionType):
                raise Undeclared(Function(), ast.funName)

        # lay function hien tai
        res = self.lookup(ast.funName, self.list_function, lambda x: x.name)
        if res:
            if len(res.params) != len(ast.args):
                raise TypeMismatch(ast)
            
            for param, arg in zip(res.params, ast.args):
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
                
                # # print("param.parType: ", param.parType)
                # test=self.visit(arg, c)
                # # print("test: ", test)
                # if type(param.parType) != type(test):
                #     raise TypeMismatch(ast)
                # if not self.checkType(param.parType, self.visit(arg, c)):
                #     raise TypeMismatch(ast)

            # stmt, voidtype => dung
            if is_stmt and not type(res.retType) == VoidType:
                raise TypeMismatch(ast)
            # expr, khong voidtype => dung
            if not is_stmt and type(res.retType) == VoidType:
                raise TypeMismatch(ast)
            return res.retType
        raise Undeclared(Function(), ast.funName)

    def visitFieldAccess(self, ast: FieldAccess, c: List[List[Symbol]]) -> Type:
        receiver_type = self.visit(ast.receiver, c)
        if isinstance(receiver_type, Id):
            receiver_type = self.lookup(receiver_type.name, self.list_type, lambda x: x.name)
        if not isinstance(receiver_type, StructType):
            raise TypeMismatch(ast)
        
        res = self.lookup(ast.field, receiver_type.elements, lambda x: x[0])
        if res is None:
            raise Undeclared(Field(), ast.field)
        return res[1]

    def visitMethCall(self, ast: MethCall, c: Union[List[List[Symbol]], Tuple[List[List[Symbol]], bool]]) -> Type:
        is_stmt = False
        if isinstance(c, tuple):
            c, is_stmt = c
        receiver_type = self.visit(ast.receiver, c)
        receiver_type = self.lookup(receiver_type.name,self.list_type,lambda x:x.name) if isinstance(receiver_type, Id) else receiver_type
        if not isinstance(receiver_type, StructType) and not isinstance(receiver_type, InterfaceType):
            raise TypeMismatch(ast)
        res = self.lookup(ast.metName, receiver_type.methods, lambda x: x.fun.name) if isinstance(receiver_type, StructType) else self.lookup(ast.metName, receiver_type.methods, lambda x: x.name)
        if res:
            if type(receiver_type) == StructType:
                if len(res.fun.params) != len(ast.args):
                    raise TypeMismatch(ast)
                for param, arg in zip(res.fun.params, ast.args):
                    arg_type = self.visit(arg, c)
                    # # print("arg_type: ", arg_type)
                    if isinstance(param.parType, ArrayType) and isinstance(arg_type, ArrayType):
                        param.parType.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), param.parType.dimens))
                        arg_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), arg_type.dimens))
                        
                        # # print("param: ", param)
                        # # print("arg_type: ", arg_type)

                        if param.parType.dimens != arg_type.dimens:
                            raise TypeMismatch(ast)
                        if param.parType.eleType != arg_type.eleType:
                            raise TypeMismatch(ast)
                        
                    if not self.checkType(param.parType, arg_type, [(FloatType, IntType), (InterfaceType, StructType)]):
                        raise TypeMismatch(ast)
                if is_stmt and not self.checkType(res.fun.retType, VoidType()):
                    raise TypeMismatch(ast)
                if not is_stmt and self.checkType(res.fun.retType, VoidType()):
                    raise TypeMismatch(ast)
                return res.fun.retType
            
            if type(receiver_type) == InterfaceType:
                if len(res.params) != len(ast.args):
                    raise TypeMismatch(ast)
                for param, arg in zip(res.params, ast.args):
                    arg_type = self.visit(arg, c)
                    # # print("param: ", param)
                    # # print("arg_type: ", arg_type)

                    if isinstance(param, ArrayType) and isinstance(arg_type, ArrayType):
                        param.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), param.dimens))
                        arg_type.dimens = list(map(lambda item: IntLiteral(self.evaluate_ast(item, c)), arg_type.dimens))
                        
                        # if param.parType.dimens != arg_type.dimens:
                        #     raise TypeMismatch(ast)
                        # if param.parType.eleType != arg_type.eleType:
                        #     raise TypeMismatch(ast)
                        
                    if not self.checkType(param, arg_type, [(FloatType, IntType), (InterfaceType, StructType)]):
                        raise TypeMismatch(ast)
                if is_stmt and not self.checkType(res.retType, VoidType()):
                    raise TypeMismatch(ast)
                if not is_stmt and self.checkType(res.retType, VoidType()):
                    raise TypeMismatch(ast)
                return res.retType
        raise Undeclared(Method(), ast.metName)

    def visitIntType(self, ast, c: List[List[Symbol]]) -> Type: return ast
    def visitFloatType(self, ast, c: List[List[Symbol]])-> Type: return ast
    def visitBoolType(self, ast, c: List[List[Symbol]])-> Type: return ast
    def visitStringType(self, ast, c: List[List[Symbol]]) -> Type: return ast
    def visitVoidType(self, ast, c: List[List[Symbol]]) -> Type: return ast
    def visitArrayType(self, ast: ArrayType, c: List[List[Symbol]]):
        # list(map(lambda item: # TODO: Implement, ast.dimens))
        list(map(lambda item: self.visit(item, c), ast.dimens))
        return ast
    
    def visitAssign(self, ast: Assign, c: List[List[Symbol]]) -> None:
        # # # print("visitAssign: ", ast)
        # # self.view_symbol_table(c)
        if type(ast.lhs) == VoidType:
            raise TypeMismatch(ast)
        
        if type(ast.lhs) is Id:
            # TÌM KIẾM XEM BIẾN ĐÃ ĐƯỢC KHAI BÁO CHƯA ĐƯỢC KHAI BÁO THÌ TRẢ VỀ Symbol(ast.lhs.name, self.visit(ast.rhs, c), None)
            # auto declare neu chua declare
            flatten_list = [item for sublist in c for item in sublist]


            res= self.lookup(ast.lhs.name, flatten_list, lambda x: x.name)
            # res= next([self.lookup(ast.lhs.name, scope, lambda x: x.name) for scope in c], None)
            # res = next(filter(None,[self.lookup(ast.name, scope, lambda x: x.name) for scope in c]), None)
            if res is None:
                return Symbol(ast.lhs.name, self.visit(ast.rhs, c), ast.rhs)

        LHS_type = self.visit(ast.lhs, c)
        RHS_type = self.visit(ast.rhs, c)

        # # # print("LHS_type: ", LHS_type)
        # # print("RHS_type: ", RHS_type)

        if not self.checkType(LHS_type, RHS_type, [(FloatType, IntType), (InterfaceType, StructType)]):
            raise TypeMismatch(ast)
        
    def visitIf(self, ast: If, c: List[List[Symbol]]) -> None: 
        # if # TODO: Implement:
        # # print("visitIf: ", ast)

        if type(self.visit(ast.expr, c)) != BoolType:
            raise TypeMismatch(ast)
        self.visit(ast.thenStmt, c)
        if ast.elseStmt:
            self.visit(ast.elseStmt, c)

    def visitContinue(self, ast, c: List[List[Symbol]]) -> None: return None
    def visitBreak(self, ast, c: List[List[Symbol]]) -> None: return None
    def visitReturn(self, ast, c: List[List[Symbol]]) -> None: 
        # # print("visitReturn: ", ast)
        # if not self.checkType(# TODO: Implement, self.function_current.retType):
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
    
    def visitBinaryOp(self, ast: BinaryOp, c: List[List[Symbol]]):
        LHS_type = self.visit(ast.left, c)
        RHS_type = self.visit(ast.right, c)

        # # print("LHS_type: ", LHS_type)
        # # print("RHS_type: ", RHS_type)
        # # print("ast.op: ", ast.op)
        # # print("left: ", ast.left)
        # # print("right: ", ast.right)

        if ast.op in ['+']:
            if self.checkType(LHS_type, RHS_type, [(IntType, FloatType), (FloatType, IntType)]):
                if type(LHS_type) == StringType and type(RHS_type) == StringType:
                    return StringType()
                elif type(LHS_type) == FloatType:
                    return FloatType()
                elif type(RHS_type) == FloatType:
                    return FloatType()
                elif type(LHS_type) == IntType:
                    return IntType()
        # TODO: Implement
        if ast.op in ['-']:
            if self.checkType(LHS_type, RHS_type, [(IntType, FloatType), (FloatType, IntType)]):
                if type(LHS_type) == StringType:
                    raise TypeMismatch(ast)
                elif type(LHS_type) == FloatType:
                    return FloatType()
                elif type(RHS_type) == FloatType:
                    return FloatType()
                elif type(LHS_type) == IntType:
                    return IntType()
        if ast.op in ['*']:
            if self.checkType(LHS_type, RHS_type, [(IntType, FloatType), (FloatType, IntType)]):
                if type(LHS_type) == FloatType:
                    return FloatType()
                elif type(RHS_type) == FloatType:
                    return FloatType()
                elif type(LHS_type) == IntType:
                    return IntType()
        if ast.op in ['/']:
            if self.checkType(LHS_type, RHS_type, [(IntType, FloatType), (FloatType, IntType)]):
                if type(LHS_type) == FloatType:
                    return FloatType()
                elif type(RHS_type) == FloatType:
                    return FloatType()
                elif type(LHS_type) == IntType:
                    return IntType()
        if ast.op in ['%']:
            if self.checkType(LHS_type, RHS_type, [(IntType, FloatType), (FloatType, IntType)]):
                if type(LHS_type) == IntType and type(RHS_type) == IntType:
                    return IntType()
        if ast.op in ['==', '!=', '<', '<=', '>', '>=']:
            if self.checkType(LHS_type, RHS_type, [(IntType, FloatType), (FloatType, IntType)]):
                if type(LHS_type) == StringType and type(RHS_type) == StringType:
                    return BoolType()
                elif type(LHS_type) == FloatType and type(RHS_type) == FloatType:
                    return BoolType()
                elif type(LHS_type) == IntType and type(RHS_type) == IntType:
                    return BoolType()
        if ast.op in ['&&', '||']:
            if self.checkType(LHS_type, RHS_type, [(BoolType, BoolType)]):
                return BoolType()

        raise TypeMismatch(ast)

    def visitUnaryOp(self, ast: UnaryOp, c: List[List[Symbol]]):
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
    
    def visitArrayCell(self, ast: ArrayCell, c: List[List[Symbol]]):
        # array_type = # TODO: Implement
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

    def visitIntLiteral(self, ast, c: List[List[Symbol]]) -> Type: return IntType()
    def visitFloatLiteral(self, ast, c: List[List[Symbol]]) -> Type: return FloatType()
    def visitBooleanLiteral(self, ast, c: List[List[Symbol]]) -> Type: return BoolType()
    def visitStringLiteral(self, ast, c: List[List[Symbol]]) -> Type: return StringType()
    def visitArrayLiteral(self, ast:ArrayLiteral , c: List[List[Symbol]]) -> Type:  
        def nested2recursive(dat: Union[Literal, List['NestedList']], c: List[List[Symbol]]):
            if isinstance(dat,list):
                list(map(lambda value: nested2recursive(value, c), dat))
            else:
                self.visit(dat, c)
        # nested2recursive(# TODO: Implement)
        nested2recursive(ast.value, c)
        return ArrayType(ast.dimens, ast.eleType)
    
    def visitStructLiteral(self, ast:StructLiteral, c: List[List[Symbol]]) -> Type: 
        list(map(lambda value: self.visit(value[1], c), ast.elements))
        # return # TODO: Implement
        struct = self.lookup(ast.name, self.list_type, lambda x: x.name)
        return struct

    def visitNilLiteral(self, ast:NilLiteral, c: List[List[Symbol]]) -> Type: return StructType("", [], [])


    def view_symbol_table(self, symbol_table: List[List[Symbol]]):
        print("--- Symbol Table ---------------------------------")
        for i, scope in enumerate(symbol_table):
            print(f"Scope {i}:")
            if not scope:
                print("  (Empty)")
            else:
                for symbol in scope:
                    print(f"  {symbol}")
        print("--- End of Symbol Table ------------------------------")

    def evaluate_ast(self, node: AST, c : List[List[Symbol]]) -> int:
        # # print("evaluate_ast: ", node)

        if type(node) == IntLiteral:
            return int(node.value)

        elif type(node) == Id:
            # res = self.lookup(node.name, c[0], lambda x: x.name)
            res = next(filter(None,[self.lookup(node.name, scope, lambda x: x.name) for scope in c]), None)
            # # print("res: ", res)
            if res:
                return int(res.value.value) if res.value else 0
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
            res= self.evaluate_ast(node.body, c)
            if node.op == '-':
                return int(-res)
        return 0        