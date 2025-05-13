from Utils import *
# from StaticCheck import *
# from StaticError import *
from Emitter import *
from Frame import Frame
from abc import ABC, abstractmethod
from functools import reduce
from Visitor import *
from AST import *

class CodeGenerator(BaseVisitor,Utils):
    def __init__(self):
        self.className = "MiniGoClass"
        self.astTree = None
        self.path = None
        self.emit = None
        self.function = None
        self.list_function = []
        self.arrayCell = None
        self.list_type = {}
        self.struct_typ: StructType = None


    def init(self):
        mem = [
            Symbol("getInt", MType([], IntType()), CName("io", True)),
            Symbol("putInt", MType([IntType()], VoidType()), CName("io", True)),
            Symbol("putIntLn", MType([IntType()], VoidType()), CName("io", True)),

            Symbol("getFloat", MType([], FloatType()), CName("io", True)),
            Symbol("putFloat", MType([FloatType()], VoidType()), CName("io", True)),
            Symbol("putFloatLn", MType([FloatType()], VoidType()), CName("io", True)),

            Symbol("getBool", MType([], BoolType()), CName("io", True)),
            Symbol("putBool", MType([BoolType()], VoidType()), CName("io", True)),
            Symbol("putBoolLn", MType([BoolType()], VoidType()), CName("io", True)),

            Symbol("getString", MType([], StringType()), CName("io", True)),
            Symbol("putString", MType([StringType()], VoidType()), CName("io", True)),
            Symbol("putStringLn", MType([StringType()], VoidType()), CName("io", True)),

            Symbol("putLn", MType([], VoidType()), CName("io", True)),
           ## TODO implement
        ]
        return mem
    def gen(self, ast, dir_):
        gl = self.init()
        self.astTree = ast
        self.path = dir_
        self.emit = Emitter(dir_ + "/" + self.className + ".j") # khoi tao emit khi vao dung vi tri file .j
        self.visit(ast, gl)
       
    # fram khoi tao voi ten init
    def emitObjectInit(self):
        frame = Frame("<init>", VoidType())  
        self.emit.printout(self.emit.emitMETHOD("<init>", MType([], VoidType()), False, frame))  # Bắt đầu định nghĩa phương thức <init>
        # sinh ra mã => .method public <init>()V
        frame.enterScope(True)  # Mỗi hàm có 1 frame riêng, và mỗi frame có 1 scope riêng, nên dùng enterScope để vào scope của frame này
        # sinh ra mã => .var 0 is this LMiniGoClass; from Label0 to Label1
        self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))  # Tạo biến "this" trong phương thức <init>
        # sinh ra mã => Label0: (nơi body method bắt đầu)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        # sinh ra mã => aload_0 (đưa biến this vào stack)
        self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame)) 
        # sinh ra mã => invokespecial java/lang/Object/<init>()V (gọi hàm khởi tạo của class cha là Object)  
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        # sinh ra mã => Label1: (nơi body method kết thúc)
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        # sinh ra mã => return (trả về từ hàm khởi tạo này)
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))  
        # sinh ra mã limit stack 1, limit locals 1, end method (kết thúc định nghĩa phương thức <init>)
        self.emit.printout(self.emit.emitENDMETHOD(frame))  

        frame.exitScope()  

    def emitObjectCInit(self, ast: Program, env):
        frame = Frame("<cinit>", VoidType())  
        self.emit.printout(self.emit.emitMETHOD("<clinit>", MType([], VoidType()), True, frame)) 
        frame.enterScope(True)  
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        env['frame'] = frame
        # self.visit(Block([
        #     #  Assign(#TODO ...) for item in ast.decl if isinstance(item, (VarDecl, ConstDecl))       => Block chứa danh sách các Assign
        # ]), env)
        # self.visit(Block([Assign(Id(item.varName), item.varInit) for item in ast.decl if Vardecl and item.varInit]), env)
        # dua vardecl va condecl vao 1 list de khoi tao bien toan cuc
        decl_list=[]
        for item in ast.decl:
            if isinstance(item, VarDecl) and item.varInit:
                decl_list.append(Assign(Id(item.varName), item.varInit))
            elif isinstance(item, ConstDecl):
                decl_list.append(Assign(Id(item.conName), item.iniExpr))
    

        self.visit(Block(decl_list), env)
        
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))  
        self.emit.printout(self.emit.emitENDMETHOD(frame))  
        frame.exitScope()

    def visitProgram(self, ast: Program, c):
        print("visitProgram", ast)
        #* di qua all program truoc

        self.list_function = c + [Symbol(item.name, MType(list(map(lambda x: x.parType, item.params)), item.retType), CName(self.className)) for item in ast.decl if isinstance(item, FuncDecl)]
        # interface type, struct type

        self.list_type = { x.name: x for x in ast.decl if isinstance(x, Type) }
        print("list_type: ", self.list_type)
        # todo, cập nhật method vào struct
        for item in ast.decl:
            if type(item) is MethodDecl:
                # print("MethodDecl: ", item)
                # print("item.receiver: ", item.receiver)
                # print("item.recType: ", item.recType)
                # print("item.fun", item.fun)
                if type(self.list_type[item.recType.name]) is StructType:
                    # print("StructType: ", self.list_type[item.recType.name])
                    self.list_type[item.recType.name].methods.append(item)
                else:
                    # print("InterfaceType: ", self.list_type[item.recType.name])
                    self.list_type[item.name].methods.append(item)
        # print("list_type2: ", self.list_type)

        env ={}
        env['env'] = [c]



        for item in self.list_type.values():
            self.struct_typ = item  # duyet qua struct/interface
            # tao file moi
            self.emit = Emitter(self.path + "/" + item.name + ".j")
            self.visit(item, {
                'env': env['env']
            })


        # emitPROLOG la bat dau 1 class moi
        # sinh ra mã => .source MiniGoClass.java
        #               .class public MiniGoClass
        #               .super java.lang.Object
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        # duyet qua cac static (bien toan cuc) va khoi tao truoc cac ham, bien toan cuc dung dau tien
        env = reduce(lambda a, x: self.visit(x, a) if type(x) in [VarDecl, ConstDecl] else a, ast.decl, env)

        # duyet qua cac func
        reduce(lambda a, x: self.visit(x, a) if isinstance(x, FuncDecl) else a, ast.decl, env)

        self.emitObjectInit()
        self.emitObjectCInit(ast, env)
        self.emit.printout(self.emit.emitEPILOG())

        # for item in self.list_type.values():
        #     self.struct = item  # duyet qua struct/interface
        #     # tao file moi
        #     self.emit = Emitter(self.path + "/" + item.name + ".j")
        #     self.visit(item, {
        #         'env': env['env']
        #     })

        return env

    ## TODO decl ------------------------------
    def visitFuncDecl(self, ast: FuncCall, o: dict) -> dict:
        print("visitFuncDecl: ", ast)

        self.function = ast
        frame = Frame(ast.name, ast.retType)
        isMain = ast.name == "main"
        if isMain:
            mtype = MType([ArrayType([None],StringType())], VoidType())
            # ast.body = Block([] + ast.body.member)
        else:
            mtype = MType(list(map(lambda x: x.parType, ast.params)), ast.retType)
        
        env = o.copy()
        env['frame'] = frame
        self.emit.printout(self.emit.emitMETHOD(ast.name, mtype,True, frame))
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        env['env'] = [[]] + env['env']
        
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType([None],StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            env = reduce(lambda acc,e: self.visit(e,acc),ast.params,env)

        self.visit(ast.body,env)
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        
        if type(ast.retType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame)) 
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        
        frame.exitScope()
        return o

    def visitParamDecl(self, ast: ParamDecl, o: dict) -> dict:
        print("visitParamDecl: ", ast)

        frame = o['frame']
        index = frame.getNewIndex()
        o['env'][0].append(Symbol(ast.parName, ast.parType, Index(index)))
        self.emit.printout(self.emit.emitVAR(index, ast.parName, ast.parType, frame.getStartLabel() ,frame.getEndLabel(), frame))     
        return o

    def visitVarDecl(self, ast: VarDecl, o: dict) -> dict:
        print("visitVarDecl: ", ast)
        
        varInit = ast.varInit
        # if type(varInit) is NilLiteral:

        varType = ast.varType

        # print("varinit: ", varInit) 

        env = o.copy()
        env['frame'] = Frame("<template_VT>", VoidType()) 
#Nếu không có giá trị khởi tạo thì tự động gán cho nó 0, 0.0, false, "",..tùy vào kiểu biến:
# int -> 0, float -> 0.0, 
# bool -> false, string -> "", 
# array -> mảng chứa các giá trị "zero" tùy thuộc vào kiểu phần tử.
        def create_init(varType: Type, o: dict):
            # print("varType: ", varType) 

            if type(varType) is IntType:
                return IntLiteral(0)
            elif type(varType) is FloatType:
                return FloatLiteral(0.0)
            elif type(varType) is StringType:
                return StringLiteral("\"\"")
            elif type(varType) is BoolType:
                return BooleanLiteral("false")
            elif type(varType) is ArrayType:
                codeGen, arrType = self.visitArrayType(varType, env)
                return ArrayLiteral(varType.dimens, varType.eleType, arrType)
            elif type(varType) is StructLiteral:
                return StructLiteral()
            # elif type(varType) is NilLiteral:
            #     return varType  


        # todo Chỉnh lại Trường hợp Var mà không có khởi tạo mà là array thì cần gọi đến visitArrayType
        if not varInit:
            # if type(varType) is ArrayType:
            #     self.visitArrayType(varType, o)
            varInit = create_init(varType, o)

            ast.varInit = varInit               


        print("varInit: ", varInit)
        print("varType: ", varType)


        rhsCode, rhsType = self.visit(varInit, env)
        
        # print("rhsCode: ", rhsCode)
        
        # if not varType:
        varType = rhsType

        # thuoc tinh static dua bao env, va khai bao thuoc tinh
        if 'frame' not in o: # global var
            o['env'][0].append(Symbol(ast.varName, varType, CName(self.className)))
            self.emit.printout(self.emit.emitATTRIBUTE(ast.varName, varType, True, False, None))
        else:   # local var, co init
            frame = o['frame']
            
            index = frame.getNewIndex()
            o['env'][0].append(Symbol(ast.varName, varType, Index(index)))
            # self.emit.printout(## TODO implement))  
            self.emit.printout(self.emit.emitVAR(index, ast.varName, varType, frame.getStartLabel(), frame.getEndLabel(), frame)) 

            rhsCode, rhsType = self.visit(varInit, o)
            if type(varType) is FloatType and type(rhsType) is IntType:
                ## TODO implement: chuyen int sang float
                rhsCode = rhsCode + self.emit.emitI2F(frame)
                rhsType = FloatType()
                

            self.emit.printout(rhsCode)

            # print("rhsCode: ", rhsCode) 
            # print("leftCode: ", leftCode)

            self.emit.printout(self.emit.emitWRITEVAR(ast.varName, varType, index,  frame))                    
        
        # print("rhsCode: ", rhsCode) 
        
        return o

    def visitFuncCall(self, ast: FuncCall, o: dict) -> dict:
        print("visitFuncCall: ", ast)

        sym = next(filter(lambda x: x.name == ast.funName, self.list_function),None)
        env = o.copy()
        if o.get('stmt'):
            o["stmt"] = False
            # [str(self.visit(x, env)[0]) for x in ast.args]
        
            
            for arg in ast.args:
                self.visit(arg, env)
                
            output = "".join([str(self.visit(x, env)[0]) for x in ast.args])

            self.emit.printout(output)
            # invokestatic io/putInt(I)V...
            self.emit.printout(self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame']))
            # return ## TODO implement, case stmt
            
            # print("output: ", output)
            # print("test: ", self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame']))
            return o
        
        
        # for arg in ast.args:
        #     self.visit(arg, env)
            
        output = "".join([str(self.visit(x, env)[0]) for x in ast.args])
        # print("sym.value.value: ", sym.value.value)
        # print("ast.funName: ", ast.funName)
        # print("sym.mtype: ", sym.mtype)
        # print("o['frame']: ", o['frame'])
        output += self.emit.emitINVOKESTATIC(f"{sym.value.value}/{ast.funName}",sym.mtype, o['frame'])
        
        # self.emit.printout(output)

        # return ## TODO implement, case expr
        return output, sym.mtype.rettype

    def visitBlock(self, ast: Block, o: dict) -> dict:
        print("visitBlock: ", ast)

        env = o.copy()
        env['env'] = [[]] + env['env']
        env['frame'].enterScope(False)
        
        # self.emit.printout(self.emit.emitLABEL(## TODO implement, bat dau block va ket thuc block))
        self.emit.printout(self.emit.emitLABEL(env['frame'].getStartLabel(), env['frame']))

        for item in ast.member:
            if type(item) in [FuncCall, MethCall]:
                env["stmt"] = True
            env = self.visit(item, env)
            # self.visit(item, env)


        # self.emit.printout(self.emit.emitLABEL(## TODO implement))

        # print('env: ', env)

        # print("env['frame']: ", env['frame'])

        self.emit.printout(self.emit.emitLABEL(env['frame'].getEndLabel(), env['frame']))
        env['frame'].exitScope()
        return o
    
    def visitId(self, ast: Id, o: dict) -> dict:
        print("visitId: ", ast)

        sym = next(filter(lambda x: x.name == ast.name, [j for i in o['env'] for j in i]),None)
        
        #todo kiểu trả về là struct nào đang được duyệt qua
        if sym is None:
            if o.get('isLeft'):
                return self.emit.emitWRITEVAR(ast.name, ast.mtype, 0, o['frame']), ast.mtype
            return self.emit.emitREADVAR(ast.name, ast.mtype, 0, o['frame']), ast.mtype
                
        # print("sym: " + sym.__str__())
        # print("sym.name: ", sym.name)
        # print("sym.mtype: ", sym.mtype)
        # print("sym.value: ", sym.value)
        # check xem can doc hay ghi
        if o.get('isLeft'):
            if type(sym.value) is Index:
                # ghi bien cuc bo
                # return self.emit.emitWRITEVAR(## TODO implement), sym.mtype
                return self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, o['frame']), sym.mtype
            else:         
                # ghi thuoc tinh static
                # return self.emit.emitPUTSTATIC(## TODO implement),sym.mtype        
                return self.emit.emitPUTSTATIC(f"{sym.value.value}/{ast.name}", sym.mtype,o['frame']), sym.mtype
        if type(sym.value) is Index:
            # doc bien cuc bo
            # return self.emit.emitREADVAR(## TODO implement),sym.mtype
            return self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, o['frame']), sym.mtype
        else:         
            # doc thuoc tinh static
            # return self.emit.emitGETSTATIC(## TODO implement),sym.mtype
            return self.emit.emitGETSTATIC(f"{sym.value.value}/{ast.name}", sym.mtype, o['frame']), sym.mtype

    def visitAssign(self, ast: Assign, o: dict) -> dict:
        print("visitAssign: ", ast)
        # xác định xem biến đã được khởi tạo hay chưa
        # if type(ast.lhs) is Id and not next(filter(lambda x: ## TODO implement),None):
    
        # nếu chưa tồn tại cần khởi tạo gọi đên visitVar
        # if type(ast.lhs) is Id and not next(filter(lambda x: x.name == ast.lhs.name, [j for i in o['env'] for j in i]),None):
        #     # return # todo
        #     rhsCode, rhsType = self.visit(ast.rhs, o)
        #     return self.visitVarDecl(VarDecl(ast.lhs.name, rhsType, ast.rhs), o)
        if type(ast.lhs) is Id and not next(filter(lambda x: x.name == ast.lhs.name, [j for i in o['env'] for j in i]),None):
            return self.visit(VarDecl(ast.lhs.name, None, ast.rhs), o)

        # isLeft xác định đang LSH hay RHS        
        rhsCode, rhsType = self.visit(ast.rhs, o)
        o['isLeft'] = True
        lhsCode, lhsType = self.visit(ast.lhs, o)
        o['isLeft'] = False

        if type(lhsType) is FloatType and type(rhsType) is IntType:  
            ## TODO implement,  ép kiểu int -> float
            rhsCode = rhsCode + self.emit.emitI2F(o['frame'])
            rhsType = FloatType()

        # self.emit.printout(rhsCode)
        # self.emit.printout(lhsCode)
        # return o
    
        o['frame'].push()
        o['frame'].push()
    
        ## TODO      
        if type(ast.lhs) is FieldAccess:
            self.emit.printout(lhsCode)
            self.emit.printout(rhsCode)

            # !
        elif type(ast.lhs) is ArrayCell:
            self.emit.printout(lhsCode)
            self.emit.printout(rhsCode)
            # self.emit.printout(## TODO  )
            self.emit.printout(self.emit.emitASTORE(self.arrayCell, o['frame'])) # array cell
        # access id
        else:
            self.emit.printout(rhsCode)
            self.emit.printout(lhsCode)


        # print("lhsCode: ", lhsCode)
        # print("rhsCode: ", rhsCode)
        return o

    def visitReturn(self, ast: Return, o: dict) -> dict:
        print("visitReturn: ", ast)

        # Nếu mà có expr đưa các giá trị vào stack
        # Truyền type đúng để trả về kết quả tương thích với type expr/voidtype
        if ast.expr:
            self.emit.printout(self.visit(ast.expr, o)[0])
        
        # self.emit.printout(self.emit.emitRETURN(## TODO implement, o['frame']))
        self.emit.printout(self.emit.emitRETURN(self.function.retType, o['frame']))

        return o

    ## TODO END decl ------------------------------

    ## TODO basic expression ------------------------------
    def visitBinaryOp(self, ast: BinaryOp, o: dict) -> tuple[str, Type]:
        print("visitBinaryOp: ", ast)

        op = ast.op
        frame = o['frame']
        codeLeft, typeLeft = self.visit(ast.left, o)
        codeRight, typeRight = self.visit(ast.right, o)

        if op in ['+', '-'] and type(typeLeft) in [FloatType, IntType]:
            # intType neu ca 2 la int
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emitI2F(frame)
                ## TODO implement
                elif type(typeRight) is IntType:
                    codeRight += self.emit.emitI2F(frame)
            # return codeLeft + codeRight + ## TODO implement
            return codeLeft + codeRight + self.emit.emitADDOP(op, typeReturn, frame), typeReturn
        
        if op in ['*', '/']:
            # typeReturn = ## TODO implement
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emitI2F(frame)
                ## TODO implement
                elif type(typeRight) is IntType:
                    codeRight += self.emit.emitI2F(frame)
            # return codeLeft + codeRight + ## TODO implement 
            return codeLeft + codeRight + self.emit.emitMULOP(op, typeReturn, frame), typeReturn 
        if op in ['%']:
            # return codeLeft + codeRight + ## TODO implement
            return codeLeft + codeRight + self.emit.emitMOD(frame), IntType()
        if op in ['==', '!=', '<', '>', '>=', '<='] and type(typeLeft) in [FloatType, IntType]:
            # return codeLeft + codeRight + ## TODO implement
            return codeLeft + codeRight + self.emit.emitREOP(op, type(typeLeft)(), frame), BoolType()
            # return codeLeft + codeRight + self.emit.emitREOP(op, IntType(), frame), BoolType()
        if op in ['||']:
            # return codeLeft + codeRight + ## TODO implement
            return codeLeft + codeRight + self.emit.emitOROP(frame), BoolType()
        if op in ['&&']:
            return codeLeft + codeRight + self.emit.emitANDOP(frame), BoolType()  

        # string        
        if op in ['+', '-'] and type(typeLeft) in [StringType]:
            # return codeLeft + codeRight + ## TODO implement, StringType()    
            
            gentype = MType([StringType()], StringType())
            # return codeLeft + codeRight + "TODO" ## TODO sinh mã cho hàm concat(nằm trong java/lang/String/concat) + trả về kiểu trả về là stringtype  
            return codeLeft + codeRight + self.emit.emitINVOKEVIRTUAL("java/lang/String/concat", gentype, frame), StringType()

        # ! sai thi sua check lai phan nay thu, va ca phan emitREOP trong emitter
        if op in ['==', '!=', '<', '>', '>=', '<='] and type(typeLeft) in [StringType]:
            code = codeLeft + codeRight + self.emit.emitREOP(op, StringType(), frame)

            return code, BoolType()
        
    def visitUnaryOp(self, ast: UnaryOp, o: dict) -> tuple[str, Type]:
        print("visitUnaryOp: ", ast)

        code, type_return = self.visit(ast.body, o)

        if ast.op == '!':
            return code + self.emit.emitNOT(BoolType(), o['frame']), type_return
            # return code + self.emit.emitNOT(BoolType(), o['frame']), type_return

        ## TODO implement
        # case '-'
        return code + self.emit.emitNEGOP(type_return, o['frame']), type_return
    
    def visitIntLiteral(self, ast: IntLiteral, o: dict) -> tuple[str, Type]:
        # print("visitIntLiteral: ", ast)
        return self.emit.emitPUSHICONST(ast.value, o['frame']), IntType()
    
    def visitFloatLiteral(self, ast: FloatLiteral, o: dict) -> tuple[str, Type]:
        ## TODO implement
        # print("visitFloatLiteral: ", ast)
        return self.emit.emitPUSHFCONST(ast.value, o['frame']), FloatType()
    
    def visitBooleanLiteral(self, ast: BooleanLiteral, o: dict) -> tuple[str, Type]:
        ## TODO implement
        # print("visitBooleanLiteral: ", ast)
        # if type(ast.value) is bool:
        # print("BooleanLiteral: ", ast)
        # print("type(ast.value): ", type(ast.value))

        return self.emit.emitPUSHICONST("true" if ast.value=="true" else "false", o['frame']), BoolType()
    
    def visitStringLiteral(self, ast: StringLiteral, o: dict) -> tuple[str, Type]:
        ## TODO implement
        # print("visitStringLiteral: ", ast)
        return self.emit.emitPUSHCONST(ast.value, StringType(), o['frame']), StringType()
    
    def visitConstDecl(self, ast:ConstDecl, o: dict) -> dict:
        print("visitConstDecl: ", ast) 

        return self.visit(VarDecl(ast.conName, ast.conType, ast.iniExpr), o)
    
    def visitArrayType(self, ast:ArrayType, o):
        print("visitArrayType: ", ast)

        codeGen = ""
        # TODO : Lặp qua dimens để thêm code vào codeGen,
        # todo dùng visit và lưu ý rằng visit sẽ trả về cặp mã và kiểu của nó.
        for dim in ast.dimens:
            codeGen += self.visit(dim, o)[0]

        # Cuối cùng đủ tham số thì dùng emitMULTIANEWARRAY để tạo mảng mới.
        codeGen += self.emit.emitMULTIANEWARRAY(ast, o['frame'])
        return codeGen, ast
    ## TODO END basic expression ------------------------------

## TODO array ------------------------------
    def visitArrayCell(self, ast: ArrayCell, o: dict) -> tuple[str, Type]:
        print("visitArrayCell: ", ast)
        
        newO = o.copy()
        newO['isLeft'] = False
        #todo: visit thằng expr của array cell này, nên nhớ arraycell gồm phần expr phía trước và index phía sau.
        codeGen, arrType = self.visit(ast.arr, newO)
    
        for idx, item in enumerate(ast.idx):
            codeGen += self.visit(item, newO)[0]
            if idx != len(ast.idx) - 1:
                codeGen += self.emit.emitALOAD(arrType, o['frame'])


        retType = None
        if len(arrType.dimens) == len(ast.idx): #* primary Type
            retType = arrType.eleType 
            if not o.get('isLeft'):
                #TODO: thêm mã cho trường hợp này => dùng emitALOAD để lấy giá trị của phần tử trong mảng ra
                codeGen += self.emit.emitALOAD(retType, o['frame'])
            else:
                # print("left arraycell")
                # print("arrType: ", arrType)
                # print("rettype: ", retType)
                # TODO: Nếu nó arraycell nằm bên vế trái thì mình gán vào biến này để biết đang duyệt vào arraycell nào, dùng sau này.
                self.arrayCell = retType
        else:
            retType = ArrayType(arrType.dimens[len(ast.idx): ], arrType.eleType)
            if not o.get('isLeft'):
                #TODO: thêm mã cho trường hợp này => dùng emitALOAD để lấy giá trị của phần tử trong mảng ra
                codeGen += self.emit.emitALOAD(retType, o['frame'])
            else:
                # TODO: Nếu nó arraycell nằm bên vế trái thì mình gán vào biến này để biết đang duyệt vào arraycell nào, dùng sau này.
                self.arrayCell = retType
        #TODO trả vè mã nãy giờ tạo để thằng nào gọi thằng đó in và type -> tuple[str, Type]:

        return codeGen, retType

#  var a [2][3] int ;
# ArrayLiteral([IntLiteral(2),IntLiteral(3)],IntType,[[IntLiteral(0),IntLiteral(0)],[IntLiteral(0),IntLiteral(0),IntLiteral(0)]])
    def visitArrayLiteral(self, ast:ArrayLiteral , o: dict) -> tuple[str, Type]:
        print("visitArrayLiteral: ", ast)
        
        # Phần ArrayLiteral.value là 1 nested list nên mình sẽ dùng đệ quy để duyệt nó.
        def nested2recursive(dat: Union[Literal, list['NestedList']], o: dict) -> tuple[str, Type]:
            #* dat 1 Literal/1 list chứa các Literal
            # dat Literal không cần đệ quy nữa, tham số o là 0
            if not isinstance(dat,list): 
                return self.visit(dat, 0)
            #* dat là 1 list
            frame = o['frame']
            #* số lượng phần tử của mảng vào stack [2][3]...
            codeGen = self.emit.emitPUSHCONST(len(dat), IntType(), frame) 
            #* trường hợp mảng một chiều, [IntLiteral(2),IntLiteral(3)]
            if not isinstance(dat[0], list):
                _, type_element_array = self.visit(dat[0], o)  # gọi hàm visit cho phần tử đầu tiên để lấy kiểu của nó
                # cần dùng 1 trong 2 emitNEWARRAY hoặc emitANEWARRAY để tạo mảng với kiểu phần tử là type_element_array
                codeGen += self.emit.emitNEWARRAY(type_element_array, frame)
                # Lặp qua từng phần tử trong danh sách:
                for idx, item in enumerate(dat):
                    # TODO Nhân đôi tham chiếu mảng trên stack (emitDUP).
                    codeGen += self.emit.emitDUP(frame)  
                    # TODO Đẩy chỉ số của phần tử (emitPUSHCONST) lên stack.
                    codeGen += self.emit.emitPUSHCONST(idx, IntType(), frame)
                    # TODO Gọi self.visit(item, o) để xử lý giá trị phần tử.
                    codeGen += self.visit(item, o)[0]
                    # TODO Lưu giá trị vào mảng (emitASTORE).
                    codeGen += self.emit.emitASTORE(type_element_array, frame)
                #TODO: Chú ý dùng đến len(dat)

                # print("codeGen: ", codeGen) 

                return codeGen , ArrayType([len(dat)], type_element_array) 
            #* trường hợp mảng 2 chiều
            # Nếu phần tử đầu tiên của danh sách là một danh sách khác (danh sách lồng nhau), thì:
            # Gọi đệ quy nested2recursive(dat[0], o) để xử lý danh sách con.
            _, type_element_array = nested2recursive(dat[0], o)
            # Sinh mã code để tạo một mảng mới với kiểu phần tử là kiểu của danh sách con.
            # cần dùng 1 trong 2 emitNEWARRAY hoặc emitANEWARRAY để tạo mảng với kiểu phần tử là type_element_array
            # print("type_element_array: ", type_element_array)
            codeGen += self.emit.emitANEWARRAY(type_element_array, frame) 

            # TODO, Lặp qua từng phần tử trong danh sách:
            for idx, item in enumerate(dat):
                # print("item: ", item)
                # print("idx: ", idx)
                # Nhân đôi tham chiếu mảng trên stack (emitDUP).
                codeGen += self.emit.emitDUP(frame)
                # Đẩy chỉ số của phần tử (emitPUSHCONST)./ iconst_0, iconst_1, iconst_2,...
                codeGen += self.emit.emitPUSHCONST(idx, IntType(), frame)
                # Gọi đệ quy nested2recursive(item, o) để xử lý danh sách con.
                code, type_element_array = nested2recursive(item, o)
                # print("code: ", code)
                # print("type_element_array: ", type_element_array)
                codeGen += code
                # Lưu giá trị vào mảng (emitASTORE).
                codeGen += self.emit.emitASTORE(type_element_array, frame)

                # print("codeGen: ", codeGen)
            #? trả về mã và kiểu của mảng vừa tạo, kiểu là ArrayType với kích thước là len(dat) và kiểu phần tử là type_element_array 
            # todo return  codeGen, ArrayType("TODO") #TODO: Chú ý dùng đến len(dat)
            return  codeGen, ArrayType([len(dat)]+type_element_array.dimens, type_element_array.eleType) 

        if type(ast.value) is ArrayType:
            return self.visit(ast.value, o)
        #Gọi hàm đệ quy trong đó tham số truyền vào là ast.value, o
        return nested2recursive(ast.value, o)
    


# todo if, for ----------------------------------------------
    def visitIf(self, ast: If, o: dict) -> dict:
        frame = o['frame']
        label_exit = frame.getNewLabel()
        label_end_if = frame.getNewLabel()

        # visit condition of if
        condCode, _ = self.visit(ast.expr, o)

        self.emit.printout(condCode)

        # *case false: di toi label_end_if, de bat dau else
        self.emit.printout(self.emit.emitIFFALSE(label_end_if, frame))

        # *case true: thuc hien body + di toi label_exit
        self.visit(ast.thenStmt, o)
        self.emit.printout(self.emit.emitGOTO(label_exit, frame))

        # *label_end_if
        self.emit.printout(self.emit.emitLABEL(label_end_if, frame))
        # *case else: thuc hien body else (neu co)
        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, o)

        self.emit.printout(self.emit.emitLABEL(label_exit, frame))
        return o
    

    def visitForBasic(self, ast: ForBasic, o: dict) -> dict:
        print("visitForBasic: ", ast)

        frame = o['frame']

        frame.enterLoop()

        lable_new = frame.getNewLabel()
        lable_Break = frame.getBreakLabel() 
        lable_Cont = frame.getContinueLabel()
        
        # * label_new
        self.emit.printout(self.emit.emitLABEL(lable_new, frame))
        # * condition
        self.emit.printout(self.visit(ast.cond, o)[0])
        # * case false: di toi label_Break, de thoat khoi loop
        self.emit.printout(self.emit.emitIFFALSE(lable_Break, frame))
        # * case true, thuc hien body
        self.visit(ast.loop, o)
        # * label_Continue
        self.emit.printout(self.emit.emitLABEL(lable_Cont, frame))
        
        # * update
        # updateCode, _ = self.visit(ast.upda, o)
        # self.emit.printout(updateCode)

        self.emit.printout(self.emit.emitGOTO(lable_new, frame))
        # ! label_Break
        self.emit.printout(self.emit.emitLABEL(lable_Break, frame))

        frame.exitLoop()
        return o
    
    def visitForStep(self, ast: ForStep, o: dict) -> dict:
        print("visitForStep: ", ast)
        ## TODO
        
        env = o.copy()
        env['env'] = [[]] + env['env']
        env['frame'].enterScope(False)
        self.emit.printout(self.emit.emitLABEL(o['frame'].getStartLabel(), o['frame']))

        # frame = o['frame']
        frame = env['frame']
        # assgin
        self.visit(ast.init, env)

        frame.enterLoop()

        lable_new = frame.getNewLabel()
        lable_Break = frame.getBreakLabel() 
        lable_Cont = frame.getContinueLabel()
        self.emit.printout(self.visit(ast.cond, env)[0])


        # * label_new
        self.emit.printout(self.emit.emitLABEL(lable_new, frame))
        # * condition
        # * case false: di toi label_Break, de thoat khoi loop
        self.emit.printout(self.visit(ast.cond, env)[0])
        self.emit.printout(self.emit.emitIFFALSE(lable_Break, frame))
        # * case true, thuc hien body
        self.visit(ast.loop, env)
        # * label_Continue
        self.emit.printout(self.emit.emitLABEL(lable_Cont, frame))
        # * update
        self.visit(ast.upda, env)
        self.emit.printout(self.emit.emitGOTO(lable_new, frame))
        # * label_Break
        self.emit.printout(self.emit.emitLABEL(lable_Break, frame))


        frame.exitLoop()

        self.emit.printout(self.emit.emitLABEL(env['frame'].getEndLabel(), env['frame']))
        env['frame'].exitScope()
        return o

    def visitForEach(self, ast, o: dict) -> dict:
        # thẩy bỏ qua
        return o

    def visitContinue(self, ast, o: dict) -> dict:
        print("visitContinue: ", ast)

        # self.emit.printout(## TODO)
        self.emit.printout(self.emit.emitGOTO(o['frame'].getContinueLabel(), o['frame']))
            
        return o

    def visitBreak(self, ast, o: dict) -> dict:
        print("visitBreak: ", ast)
        # self.emit.printout(## TODO)
        self.emit.printout(self.emit.emitGOTO(o['frame'].getBreakLabel(), o['frame']))
            
        return o



# todo method va struct-----------------------------------------------------------
    def visitFieldAccess(self, ast:FieldAccess, o: dict) -> tuple[str, Type]:
        print("visitFieldAccess: ", ast)
        # pass

        code, typ = self.visit(ast.receiver, o)
        typ = self.list_type[typ.name]
        # print("typ: ", typ)
        # field = ## TODO
        for tup in typ.elements:
            if tup[0] == ast.field:
                field = tup
        # field = next(filter(lambda x: x.name == ast.fieldname, typ.members), None)
        # return code + self.emit.emitGETFIELD(## TODO), field[1]
        # -> tuple[str, Type], trong đó Type là kiểu trả về của field
        return code + self.emit.emitGETFIELD(f"{typ.name}/{ast.field}", field[1], o['frame']), field[1]

            

    ## chia 2 trường hợp giống function (hiện tại anh chưa chia)
    def visitMethCall(self, ast: MethCall, o: dict) -> tuple[str, Type]:
        print("visitMethCall: ", ast)

        # print("o: ", o)
        # env = o.copy

        code, typ = self.visit(ast.receiver, o)
        if isinstance(typ, ClassType):
            typ = self.list_type.get(typ.name)

        # print("typ: ", typ)

        is_stmt = o.pop("stmt", False)

        for arg in ast.args:
            arg_code, _ = self.visit(arg, o)
            code += arg_code

        returnType = None
        # * case rev la struct
        if isinstance(typ, StructType):
            method = next(filter(lambda x: ast.metName == x.fun.name, typ.methods), None)  

            mtype = MType(method.fun.params, method.fun.retType)
            returnType = method.fun.retType

            lexeme = f"{typ.name}/{ast.metName}"
            code += self.emit.emitINVOKEVIRTUAL(lexeme, mtype, o['frame'])
            

        #* case interface
        elif isinstance(typ, InterfaceType):
            method = next(filter(lambda x: x.name == ast.methodname, typ.methods), None)

            mtype = MType(method.params, method.retType)
            returnType = method.retType

            code += self.emit.emitINVOKEINTERFACE(f"TODO_2", mtype, o['frame'])

        # * case statement, in mã.
        if is_stmt:
            self.emit.printout(code)
            return o

        # * case expr
        return code, returnType

    def visitStructLiteral(self, ast:StructLiteral, o: dict) -> tuple[str, Type]:
        print("visitStructLiteral: ", ast)

        # todo
        code = self.emit.emitNEW(ast.name, o['frame'])
        code += self.emit.emitDUP(o['frame'])
        #!
        # list_type = []
        for item in ast.elements:
            # code += ## TODO
            ele_name, ele_expr = item
            codeGen, ele_type = self.visit(ele_expr, o)
            ele_type = MType([ele_type], VoidType())
            code += codeGen + self.emit.emitINVOKESPECIAL(o['frame'], ast.name+"/<init>", ele_type)
        # code += ## TODO
        # code += self.emit.emitINVOKEVIRTUAL(

        return code, ClassType(ast.name)

    def visitNilLiteral(self, ast: NilLiteral, o: dict) -> tuple[str, Type]:
        # Gợi ý:
        # 1. Sử dụng self.emit.emitPUSHNULL để đẩy giá trị null lên stack.
        code = self.emit.emitPUSHNULL(o['frame'])
        # Trả về mã và kiểu của 'nil'.
        # Gợi ý:
        # 1. Kiểu của 'nil' thường là một kiểu tham chiếu đặc biệt hoặc có thể được biểu diễn bằng một Id rỗng.
        return code, Id("")



    def visitStructType(self, ast: StructType, o):
        print("visitStructType: ", ast)

        # khởi tạo đầu file mô tả tên
        self.emit.printout(self.emit.emitPROLOG(self.struct_typ.name, "java.lang.Object")) 
        # VD ở visitProgram: self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))


        # .implements name
        # VD sau dùng cho đoạn for bên dưới:
            #INPUT:
                # type Worker interface { 
                #     study(); 
                #     play(); 
                # }
                # type PPL4 struct {number int;}
                # func (p PPL4) study() { putInt(p.number); }
                # func (p PPL4) play()  { putInt(p.number + 5); }
            #CODE OUTPUT:
                # .source PPL4.java
                # .class public  PPL4
                # .super java.lang.Object    ---------------> khúc này trở lên là emitPROLOG
                # .implements Worker         --------------------> lệnh implement được nằm ở đây nè
                # .field public number I
                # .method public <init>(I)V
                # .......
                # .method public <init>()V
                # .......
                # .method public study()V
                # .......
                # .method public play()V
                # .......

        # ***LƯU Ý***: ..... là còn code ở đó, code VD ở trên nằm trong file PPL4.j (tên struct được khai báo ở trên), tương tự là có file Worker.j

        # Lặp qua các type đc khai báo(interface/struct)
        for item in self.list_type.values(): 
            # Lệnh if - tìm interface mà struct này đang implement(ast là struct mà mình visit), hàm checkType sẽ check 1 struct implement đc interface
            if ast.name == item.name and self.checkType(item, ast, [(InterfaceType, StructType)]): 
                self.emit.printout(f".implements {item.name}") # Sinh ra đoạn .implement ___ như ở ví dụ bên trên.

        for item in ast.elements:
            #**Lưu ý: item có type là Tuple[str,Type] -> nhờ dùng item[0], item[1]
            #Chỗ này mình tạo code cho attribute cho struct nên mã code VD sẽ là:
                # .field public name Ljava/lang/String;
                # .field public age I
            # với input:
                #  type Person struct {
                #     name string;
                #     age int;
                # }
            #từ đó mà điền tham số cho hàm emit cho phù hợp nhé, nhớ đọc hàm này trong Emiter.py
            lexeme = f"public {item[0]}"
            self.emit.printout(self.emit.emitATTRIBUTE(lexeme, item[1], False, False, False)) # danh sách các thuộc tính cần khởi tạo
        
        # khởi tạo Method contructor có giá trị parram (khác với constructor rỗng nha)
        #code VD cho hàm constructor cho class PPL4 ở phía trên:      
                # type PPL4 struct {number int;}

                # .method public <init>(I)V
                # .var 0 is this LPPL4; from Label0 to Label1  -------------------> param mặc định "this"
                # Label0:
                # 	aload_0
                # 	invokespecial java/lang/Object/<init>()V
                # .var 1 is number I from Label0 to Label1 --------> param đầu tiên number int;
                # Label2:    ------------------> Label2 đếm Label3 là khúc Block(..) bên dưới, bên trong là phép gán attribute
                # 	aload_0
                # 	iload_1
                # 	putfield PPL4/number I
                # Label3:
                # Label1:
                # 	return
                # .limit stack 2
                # .limit locals 2
                # .end method
        # !
        self.visit(MethodDecl(None, None, FuncDecl("<init>", [ParamDecl(item[0], item[1]) for item in ast.elements], VoidType(),
                                                   
                            Block([Assign(item[0], item[1]) for item in ast.elements]))), o) 
        # Hãy xem bên trong giống như các phép gán this.fieldName = fieldName ứng với mỗi item trong ast.elements => Dùng Assign và FieldAcess


        # khởi tạo Method contructor rỗng
        # .method public <init>()V
        # .var 0 is this LPPL4; from Label0 to Label1
        # Label0:
        #     aload_0
        #     invokespecial java/lang/Object/<init>()V
        # Label2:
        # Label3:
        # Label1:
        #     return
        # .limit stack 1
        # .limit locals 1
        # .end method
        # self.visit(MethodDecl(None, None, FuncDecl("TODO"), o))
        self.visit(MethodDecl(None, None, FuncDecl("", [], VoidType(), Block([])), o))


        # duyệt qua method
        for item in ast.methods: self.visit(item, o)
        # kết thúc khai báo của struct
        self.emit.printout(self.emit.emitEPILOG())

    

    
    def visitMethodDecl(self, ast: MethodDecl, o):
        self.function = ast.fun
        frame = Frame(ast.fun.name, ast.fun.retType)
        # giống visitFuncDecl thôi
        # mtype =  
        mtype = MType(list(map(lambda x: x.parType, ast.fun.params)), ast.fun.retType)
        
        env = o.copy()
        env['frame'] = frame
        self.emit.printout(self.emit.emitMETHOD(ast.fun.name, mtype,False, frame))
        frame.enterScope(True) #vào trong thân method giống visitFuncDecl thôi
        # biến this
        #todo emitVAR cho biến this với inType là Id(...)
        self.emit.printout(self.emit.emitVAR(0, "this", Id("this"), frame.getStartLabel(), frame.getEndLabel(), frame))
        
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        # contructor thì hơi đặt biệt cần gọi đến class cha của nó .super java.lang.Object
        if ast.receiver is None:
            self.emit.printout(self.emit.emitREADVAR("java.lang.Object", ClassType("this"), 0, frame))  
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))  

        env['env'] = [[]] + env['env']
        # cập nhật param và duyệt block
        #todo: Này duyệt và cập nhật param giống visitFuncDecl 
        # env = #cập nhật param cho frame
        env = reduce(lambda acc,e: self.visit(e,acc),ast.params,env)


        self.visit(ast.body, env)


        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(ast.fun.retType) is VoidType:
            # trường hợp void phải có return tránh trường hợp ko có return trong block
            # self.emit.printout("TODO")
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame)) 

        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()
        return o
    

    def visitInterfaceType(self, ast: InterfaceType, o):
        # type Course interface {study();}

        # .source Course.java
        # .class public interface Course
        # .super java.lang.Object

        # .method public abstract study()V
        # .end method

        #Giống struct type thôi nhưng đơn giản hơn
        self.emit.printout(self.emit.emitPROLOG(ast.name, "java.lang.Object", True))
        for item in ast.methods:
            #TODO sinh mẫ cho các prototype, nhớ này là abstract method
            #TODO end method
            pass
        self.emit.printout(self.emit.emitEPILOG())






















































    def checkType(self, left: Type, right: Type, list_type_permission: List[tuple[Type, Type]] = []) -> bool:
        # Kiểm tra xem hai kiểu có tương thích hay không.
        # Gợi ý:
        # 1. Xử lý trường hợp RHS_type là StructType có tên rỗng (thường là nil literal).
        if type(right) == StructType and right.name == "":
            #  nil có thể gán cho InterfaceType, StructType hoặc Id.
            # return "TODO"
            if type(right) == StructType and right.name == "":
                if isinstance(left, Id):
                    ketqua = self.lookup(left.name, self.list_type, lambda x: x.name)
                    if ketqua != None:
                        return True
                return False

        # Resolve Id types thành kiểu thực tế từ self.list_type.
        left = self.lookup(left.name, self.list_type.values(), lambda x: x.name) if isinstance(left, Id) else left
        right = self.lookup(right.name, self.list_type.values(), lambda x: x.name) if isinstance(right, Id) else right

        #  Kiểm tra các trường hợp dựa trên danh sách các cặp kiểu cho phép.
        if (type(left), type(right)) in list_type_permission:
            # Xử lý kiểm tra tương thích giữa InterfaceType và StructType.
            if isinstance(left, InterfaceType) and isinstance(right, StructType):
                #  Kiểm tra xem StructType có implement tất cả các phương thức của InterfaceType không.
                return all(
                    any(
                        # So sánh tên, kiểu trả về và kiểu tham số của phương thức.
                        struct_methods.fun.name == inteface_method.name and
                        self.checkType(struct_methods.fun.retType, inteface_method.retType) and
                        len(struct_methods.fun.params) == len(inteface_method.params) and
                        reduce(
                            lambda x, i: x and self.checkType(struct_methods.fun.params[i].parType, inteface_method.params[i]),
                            range(len(struct_methods.fun.params)),
                            True
                        )
                        for struct_methods in right.methods
                    )
                    for inteface_method in left.methods
                )
            # Kiểm tra tương thích giữa hai InterfaceType hoặc hai StructType.
            if (isinstance(left, InterfaceType) and isinstance(right, InterfaceType)) or (isinstance(left, StructType) and isinstance(right, StructType)):
                return left.name == right.name

                # # Hai kiểu này tương thích nếu chúng có cùng tên.
                # return "TODO"

        #  Kiểm tra tương thích giữa hai ArrayType.
        if isinstance(left, ArrayType) and isinstance(right, ArrayType):
            # Hai kiểu mảng tương thích nếu số chiều bằng nhau, kích thước các chiều tương ứng bằng nhau và kiểu phần tử tương thích.
            return (len(left.dimens) == len(right.dimens)
                    and all(
                        l.value == r.value  for l, r in zip(left.dimens, right.dimens)
                    )
                    and self.checkType(left.eleType, right.eleType, [list_type_permission[0]] if len(list_type_permission) != 0 else []))

        #  Kiểm tra tương thích giữa các kiểu cơ bản (IntType, FloatType, StringType, BoolType).
        # Gợi ý: Hai kiểu cơ bản tương thích nếu chúng cùng loại.
        # return "TODO"
        return type(left) == type(right)