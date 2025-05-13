
class CodeGenVisitor(Visitor):
    def __init__(self, astTree, path):
        self.astTree = astTree
        self.path = path
        self.className = "MT22"
        self.emit = Emitter(self.path + "/" + self.className  + ".j")
        self.list_function = []
        self.function = None 
        self.has_return = False
        self.globalVariable = False
    
    class Access():
        def __init__(self, frame : Frame, symbol : list[list[VarMT22 | ParamMT22]], isLeft):
            self.frame = frame 
            self.symbol = symbol 
            self.isLeft = isLeft 
        
        def __str__(self):
            return f"Access(\n typeLeft = {self.typeLeft}\n symbol = {Tool.printListInListVarMT22(self.symbol)})"

    def visitBinExpr(self, ast : BinExpr, o : Access):
        codeLeft, typeLeft = self.visit(ast.left, o)
        codeRight, typeRight = self.visit(ast.right, o)
        op = ast.op
        frame = o.frame
        if op in ['+', '-']:
            typeReturn = IntegerType() if type(typeLeft) is IntegerType and type(typeRight) is IntegerType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntegerType:
                    codeLeft += self.emit.emitI2F(frame)
                if type(typeRight) is IntegerType:
                    codeRight += self.emit.emitI2F(frame)
            return codeLeft + codeRight + self.emit.emitADDOP(op, typeReturn, frame), typeReturn
        if op in ['*', '/']:
            typeReturn = IntegerType() if type(typeLeft) is IntegerType and type(typeRight) is IntegerType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntegerType:
                    codeLeft += self.emit.emitI2F(frame)
                if type(typeRight) is IntegerType:
                    codeRight += self.emit.emitI2F(frame)
            return codeLeft + codeRight + self.emit.emitMULOP(op, typeReturn, frame), typeReturn        
        if op in ['%']:
            return codeLeft + codeRight + self.emit.emitMOD(frame), IntegerType()    
        if op in ['==', '!=', '<', '>', '>=', '<=']:
            if type(typeLeft) is FloatType:
                codeLeft += self.emit.emitF2I(frame)
            if type(typeRight) is FloatType:
                codeRight += self.emit.emitF2I(frame)
            return codeLeft + codeRight + self.emit.emitREOP(op, BooleanType(), frame), BooleanType()     
        if op in ['||']:
            return codeLeft + codeRight + self.emit.emitOROP(frame), BooleanType()   
        if op in ['&&']:
            return codeLeft + codeRight + self.emit.emitANDOP(frame), BooleanType()          
        if op in ['::']:
            return codeLeft + codeRight + self.emit.emitINVOKEVIRTUAL("java/lang/String/concat", FuncMT22("java/lang/String/concat", StringType(), [ParamMT22("s", StringType(), -1)]), frame), StringType()    

    def visitUnExpr(self, ast : UnExpr, o : Access):
        if ast.op == '!':
            code, type_return = self.visit(ast.val, o)
            return code + self.emit.emitNOT(BooleanType(), o.frame), BooleanType()

        code, type_return = self.visit(ast.val, o)
        return code + self.emit.emitNEGOP(type_return , o.frame), type_return

    def visitId(self, ast, o : Access):
        #TODO : implement 1
        global_variable = o.symbol[-1] if self.globalVariable else []
        local_variable = o.symbol[:-1] if self.globalVariable else o.symbol

        #TODO : implement 2
        for variables in local_variable:
            for variable in variables:
                if variable.name == ast.name:
                    if o.isLeft:
                        return self.emit.emitWRITEVAR(variable.name, variable.typ, variable.index, o.frame), variable.typ
                    else:
                        return self.emit.emitREADVAR(variable.name, variable.typ, variable.index, o.frame), variable.typ

        #TODO : implement 3
        for variable in global_variable:
            if variable.name == ast.name:
                if o.isLeft:
                    return self.emit.emitPUTSTATIC(self.className + "." + variable.name, variable.typ, o.frame), variable.typ
                else:
                    return self.emit.emitGETSTATIC(self.className + "." + variable.name, variable.typ, o.frame), variable.typ

    def visitArrayCell(self, ast : ArrayCell, o : Access):
        newO = self.Access(o.frame, o.symbol, False)
        codeGen, arr = self.visit(Id(ast.name), newO)

        for idx, item in enumerate(ast.cell):
            codeGen += self.visit(item, newO)[0]
            if idx != len(ast.cell) - 1:
                codeGen += self.emit.emitALOAD(StringType(), o.frame)

        retType = None
        if len(arr.dimensions) == len(ast.cell):
            retType = arr.typ 
            if not o.isLeft:
                codeGen += self.emit.emitALOAD(retType, o.frame)
            else:
                self.arrayCell = retType
        else:
            retType = ArrayType(arr.dimensions[len(ast.cell): ], arr.typ)
            if not o.isLeft:
                codeGen += self.emit.emitALOAD(retType, o.frame)
            else:
                self.arrayCell = retType
        return codeGen, retType

    def visitIntegerLit(self, ast, o : Access):
        return self.emit.emitPUSHCONST(ast.val, IntegerType(), o.frame), IntegerType()
    
    def visitFloatLit(self, ast, o : Access):
        return self.emit.emitPUSHCONST(ast.val, FloatType(), o.frame), FloatType()
    
    def visitStringLit(self, ast, o : Access):
        return self.emit.emitPUSHCONST("\"" + ast.val + "\"", StringType(), o.frame), StringType()
    
    def visitBooleanLit(self, ast, o : Access):
        return self.emit.emitPUSHCONST(ast.val, BooleanType(), o.frame), BooleanType()
    
    def visitArrayLit(self, ast : ArrayLit, o : Access):
        frame = o.frame
        _, type_element_array = self.visit(ast.explist[0], o)
        codeGen = self.emit.emitPUSHCONST(len(ast.explist), IntegerType(), frame)

        if type(type_element_array) is not ArrayType: 
            codeGen += self.emit.emitNEWARRAY(type_element_array, frame)
        else: 
            codeGen += self.emit.emitANEWARRAY(type_element_array, frame)

        for idx, item in enumerate(ast.explist):
            codeGen += self.emit.emitDUP(frame)
            codeGen += self.emit.emitPUSHCONST(idx, IntegerType(), frame)
            codeGen += self.visit(item, self.Access(frame, o.symbol, False))[0] 
            codeGen += self.emit.emitASTORE(type_element_array, frame)

        if type(type_element_array) is not ArrayType:
            return  codeGen, ArrayType([len(ast.explist)], type_element_array)
        return  codeGen, ArrayType([len(ast.explist)] + type_element_array.dimensions, type_element_array.typ)

    def visitFuncCall(self, ast : FuncCall, o : Access):
        frame = o.frame
        # function print
        if ast.name == "readInteger": 
            return self.emit.emitINVOKESTATIC(f"io/{ast.name}", FuncMT22(ast.name, IntegerType(), []), frame), IntegerType()
        elif ast.name == "readFloat": 
            return self.emit.emitINVOKESTATIC(f"io/{ast.name}", FuncMT22(ast.name, FloatType(), []), frame), FloatType()
        elif ast.name == "readBoolean": 
            return self.emit.emitINVOKESTATIC(f"io/{ast.name}", FuncMT22(ast.name, BooleanType(), []), frame), BooleanType()
        elif ast.name == "readString": 
            return self.emit.emitINVOKESTATIC(f"io/{ast.name}", FuncMT22(ast.name, StringType(), []), frame), StringType()
        
        # funcion other
        else:
            function = next(filter(lambda item: item.name == ast.name, self.list_function), None)
            code = ""
            for index, arg in enumerate(ast.args, 0):
                codeArgs, typeArgs = self.visit(arg, o)
                code += codeArgs
                if type(typeArgs) is IntegerType and type(function.param[index].typ) is FloatType:
                    code += self.emit.emitI2F(frame)
               
            return code + self.emit.emitINVOKESTATIC(self.className + "." + ast.name, function, frame), function.typ

    ######################################################################################
    def visitAssignStmt(self, ast, o : Access):
        frame = o.frame
        rhsCode, rhsType = self.visit(ast.rhs, self.Access(frame, o.symbol, False))
        lhsCode, lhsType = self.visit(ast.lhs, self.Access(frame, o.symbol, True))
        frame.push()
        frame.push()
        if type(lhsType) is FloatType and type(rhsType) is IntegerType:
            rhsCode += self.emit.emitI2F(frame)
        # access array
        if type(ast.lhs) is ArrayCell:
            self.emit.printout(lhsCode)
            self.emit.printout(rhsCode)
            self.emit.printout(self.emit.emitASTORE(self.arrayCell, frame))
        # access id
        else:
            self.emit.printout(rhsCode)
            self.emit.printout(lhsCode)

    def visitBlockStmt(self, ast : BlockStmt, o : Access):
        # init scope new
        o.frame.enterScope(False)
        self.emit.printout(self.emit.emitLABEL(o.frame.getStartLabel(), o.frame))

        # body
        newBody = [[]] + o.symbol
        [self.visit(item, self.Access(o.frame, newBody, False)) for item in ast.body]
        
        # exit scope new
        self.emit.printout(self.emit.emitLABEL(o.frame.getEndLabel(), o.frame))
        o.frame.exitScope()

    def visitIfStmt(self, ast : IfStmt, o : Access):
        frame = o.frame

        # init label
        label_exit = frame.getNewLabel()
        label_end_if = frame.getNewLabel()

        # condition in if
        self.emit.printout(self.visit(ast.cond, o)[0])
        self.emit.printout(self.emit.emitIFFALSE(label_end_if, frame))  

        # body if and exit if (condition = true)
        self.visit(ast.tstmt, o)
        self.emit.printout(self.emit.emitGOTO(label_exit, frame))

        # label end if (condition = false)
        self.emit.printout(self.emit.emitLABEL(label_end_if, frame))

        # body else
        if ast.fstmt is not None:
            self.visit(ast.fstmt, o)
        
        #lable exit
        self.emit.printout(self.emit.emitLABEL(label_exit, frame))  

    def visitForStmt(self, ast : ForStmt, o : Access):
        frame = o.frame
        # INIT loop
        frame.enterLoop()
        lable_new = frame.getNewLabel() # label start
        lable_Break = frame.getBreakLabel() # label break
        lable_Continue = frame.getContinueLabel() # label continue

        # assgin
        self.visit(ast.init, o)

        #label new
        self.emit.printout(self.emit.emitLABEL(lable_new, frame)) 

        # condition
        self.emit.printout(self.visit(ast.cond, o)[0])
        self.emit.printout(self.emit.emitIFFALSE(lable_Break, frame))  

        #visit body
        self.visit(ast.stmt, o)

        #lable continue
        self.emit.printout(self.emit.emitLABEL(lable_Continue, frame))

        # upd
        self.visit(AssignStmt(ast.init.lhs, BinExpr('+', ast.init.lhs, ast.upd)), o)

        #goto lable_new
        self.emit.printout(self.emit.emitGOTO(lable_new, frame))

        #đặt lable_Break
        self.emit.printout(self.emit.emitLABEL(lable_Break, frame))

        # exit loop
        frame.exitLoop()

    def visitWhileStmt(self, ast : WhileStmt, o : Access):
        frame = o.frame
        # INIT loop
        frame.enterLoop()
        lable_new = frame.getNewLabel() # label start
        lable_Break = frame.getBreakLabel() # label break
        lable_Continue = frame.getContinueLabel() # label continue

        #label new
        self.emit.printout(self.emit.emitLABEL(lable_new, frame)) 

        # condition
        self.emit.printout(self.visit(ast.cond, o)[0])
        self.emit.printout(self.emit.emitIFFALSE(lable_Break, frame))  

        #visit body
        self.visit(ast.stmt, o)

        #lable continue
        self.emit.printout(self.emit.emitLABEL(lable_Continue, frame))

        #goto lable_new
        self.emit.printout(self.emit.emitGOTO(lable_new, frame))

        #đặt lable_Break
        self.emit.printout(self.emit.emitLABEL(lable_Break, frame))

        # exit loop
        frame.exitLoop()

    def visitDoWhileStmt(self, ast, o : Access):
        frame = o.frame
        # INIT loop
        frame.enterLoop()
        lable_new = frame.getNewLabel() # label start
        lable_Break = frame.getBreakLabel() # label break
        lable_Continue = frame.getContinueLabel() # label continue

        #label new
        self.emit.printout(self.emit.emitLABEL(lable_new, frame)) 

        #visit body
        self.visit(ast.stmt, o)

        #lable continue
        self.emit.printout(self.emit.emitLABEL(lable_Continue, frame))

        # condition
        self.emit.printout(self.visit(ast.cond, o)[0])
        self.emit.printout(self.emit.emitIFTRUE(lable_new, frame))  

        #đặt lable_Break
        self.emit.printout(self.emit.emitLABEL(lable_Break, frame))

        # exit loop
        frame.exitLoop()
    
    def visitBreakStmt(self, ast, o : Access):
        self.emit.printout(self.emit.emitGOTO(o.frame.getBreakLabel(), o.frame))

    def visitContinueStmt(self, ast, o : Access):
        self.emit.printout(self.emit.emitGOTO(o.frame.getContinueLabel(), o.frame))

    def visitReturnStmt(self, ast : ReturnStmt, o : Access):
        frame = o.frame
        # return value
        if ast.expr:
            expCode, expType = self.visit(ast.expr, o)

            if type(self.function.typ) is FloatType and type(expType) is IntegerType:
                expCode += self.emit.emitI2F(frame)
            self.emit.printout(expCode)
            self.emit.printout(self.emit.emitRETURN(self.function.typ, frame))    
        # return void   
        else:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))

    def visitCallStmt(self, ast : CallStmt, o : Access):
        frame = o.frame
        # function print
        if ast.name in ["printInteger", "printFloat", "printBoolean", "printString"]:
            argsCode, argsType = self.visit(ast.args[0], o)
            self.emit.printout(argsCode)
            self.emit.printout(self.emit.emitINVOKESTATIC(f"io/{ast.name}", FuncMT22(ast.name, VoidType(), [ParamMT22("input", argsType, -1)]), frame))
        # funcion other
        else:
            function = next(filter(lambda item: item.name == ast.name, self.list_function), None)
            code = ""
            for index, arg in enumerate(ast.args, 0):
                codeArgs, typeArgs = self.visit(arg, o)
                code += codeArgs
                if type(typeArgs) is IntegerType and type(function.param[index].typ) is FloatType:
                    code += self.emit.emitI2F(frame)
               
            self.emit.printout(code + self.emit.emitINVOKESTATIC(self.className + "." + ast.name, function, frame))
            if type(function.typ) is not VoidType:
                self.emit.printout(self.emit.emitPOP(frame))
        
    ######################################################################################
    def visitVarDecl(self, ast : VarDecl, o : Access):
        frame = o.frame
        index = frame.getNewIndex()
        o.symbol[0].append(VarMT22(name = ast.name, typ = ast.typ, index = index))
        self.emit.emitVAR(index, ast.name, ast.typ, frame.getStartLabel() ,frame.getEndLabel(), frame)
        self.visit(AssignStmt(lhs = Id(ast.name), rhs = ast.init), o) 

    def visitParamDecl(self, ast : ParamDecl, o : Access):
        frame = o.frame
        index = frame.getNewIndex()
        o.symbol[0].append(ParamMT22(ast.name, ast.typ,  index, ast.out, ast.inherit))
        self.emit.emitVAR(index, ast.name, ast.typ, frame.getStartLabel() ,frame.getEndLabel(), frame)        

    def visitFuncDecl(self, ast : FuncDecl, o : Access):
        # start function
        self.has_return = False
        frame = Frame(ast.name, self.function)
        self.emit.printout(self.emit.emitMETHOD(ast.name, self.function, isStatic=True, frame=frame))
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
    
        # list param
        [self.visit(item, self.Access(frame, o.symbol, False)) for item in ast.params]

        # body
        self.visit(ast.body, self.Access(frame, [[]] + o.symbol, False))

        # end function
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))   
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()    

    def visitProgram(self, ast, o : Access):
    #TODO : implement 1 => init program MT22
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        symbol_global_variable: list[VarMT22] = []
        for item in ast.decls:
            if type(item) is FuncDecl:  
                self.list_function.append(FuncMT22(item.name, item.return_type, [ParamMT22(item.name, item.typ, -1, item.out, item.inherit) for item in item.params]))
            else:
                self.globalVariable = True  
                symbol_global_variable.append(VarMT22(item.name, item.typ, -1, item.init))
                self.emit.printout(self.emit.emitATTRIBUTE(item.name, item.typ, False, self.className)) 

    #TODO : implement 2 => khởi tạo contructor và các giá trị cho biến toàn cục
        #! 2.1 init contructor MT22
        frame = Frame("<init>", VoidType())
        self.emit.printout(self.emit.emitMETHOD(lexeme = "<init>", in_ = FuncMT22("init", VoidType(), []), isStatic = False, frame = frame))
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", Type(), frame.getStartLabel(), frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitREADVAR("this", self.className, 0, frame))
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))   
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()    
         
        #! 2.2 giá trị cho biến toàn cục
        frame = Frame("<clinit>", VoidType())
        self.emit.printout(self.emit.emitMETHOD(lexeme="<clinit>", in_ = FuncMT22("clinit", VoidType(), []), isStatic = True, frame = frame))
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        for global_variable in symbol_global_variable:
            self.visit(AssignStmt(Id(global_variable.name), global_variable.init),self.Access(frame, [symbol_global_variable], False)) 
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame)) 
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))  
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()    

    #TODO : implement 3 => khởi tạo cho các function còn lại và hàm main
        index = 0
        for item in ast.decls:
            if type(item) is FuncDecl:
                self.function = self.list_function[index]

                #! 3.1 init function main
                if item.name == "main":
                    #* khởi tạo hàm main
                    frame = Frame("main", VoidType)
                    self.emit.printout(self.emit.emitMETHOD(lexeme="main", in_= FuncMT22("main", VoidType(), [ParamMT22("args", ArrayType([1], StringType()), -1)]), isStatic = True, frame = frame))
                    frame.enterScope(True)
                    self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
                    self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType([], StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
                    self.visit(item.body, self.Access(frame, [[]] + [symbol_global_variable], False))
                    self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
                    self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))   
                    self.emit.printout(self.emit.emitENDMETHOD(frame))
                    frame.exitScope()    
                #! 3.2 function other
                else :
                    self.visit(item, self.Access(frame, [[]] + [symbol_global_variable], False))

                index += 1

        # result file .j
        self.emit.emitEPILOG()