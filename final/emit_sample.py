"""
 * Initial code for Assignment
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/profile.php?id=100056605580171
 * Link Group : https://www.facebook.com/groups/211867931379013
 * Date: 06.19.2024
"""
from Utils import *
# from StaticCheck import *
# from StaticError import *
# import main.CodeGenerator as cgen
from MachineCode import JasminCode
from AST import *
from main.CodeGenError import *


class MT22:
    create = 0
    def __init__(self, name : str, typ : Type):
        self.ID = MT22.create
        self.name = name
        self.typ = typ
        self.ast = None
        MT22.create += 1
        
class VarMT22(MT22):
    def __init__(self, name : str, typ: Type, index : int, init: Expr | None = None):
        super().__init__(name, typ)
        self.index = index
        self.init = init
        
    def __str__(self):
        return f"VarMT22(#{self.ID}, {self.name}, {str(self.typ)})"
        
class ParamMT22(MT22):
    def __init__(self, name : str, typ: Type, index : int, out : bool = False, inherit : bool = False):
        super().__init__(name, typ)
        self.index = index
        self.out = out
        self.inherit = inherit

    def __str__(self):
        return f"ParamMT22(#{self.ID}, {self.name}, {str(self.typ)}, {self.out}, inherit={self.inherit})"

class FuncMT22(MT22):
    def __init__(self, name : str, typ: Type, param : list[ParamMT22], parent : MT22 | None = None):
        super().__init__(name, typ)
        self.param = param
        self.parent = parent
        
    def __str__(self):
        return f"FuncMT22(#{self.ID}, {self.name}, {str(self.typ)}, [{", ".join([str(param) for param in self.param])}]{f", inherit=#{self.parent.ID}" if self.parent else ""})"      


class Tool():
    def printVarMT22(varMT22 : VarMT22 | ParamMT22):
        return str(varMT22)
    
    def printListVarMT22(ListVarMT22 : list[VarMT22 | ParamMT22]):
        return f"[ {', '.join(map(Tool.printVarMT22, ListVarMT22))} ]"

    def printListInListVarMT22(ListVarMT22 : list[list[VarMT22 | ParamMT22]]):
        return f"[\n\t{'\n\t'.join(map(Tool.printListVarMT22, ListVarMT22))}\n]"
    
    def printFunctionMT22(funcMT22 : FuncMT22):
        return str(funcMT22)
    
    def printListFunctionMT22(ListfuncMT22 : list[FuncMT22]):
        return f"[\n\t{'\n\t'.join(map(Tool.printFunctionMT22, ListfuncMT22))}\n]"
    

class Emitter():
    def __init__(self, filename):
        self.filename = filename
        self.buff = list() 
        self.jvm = JasminCode() #! gọi quá

    def getJVMType(self, inType):
        typeIn = type(inType)
        if typeIn is BooleanType: #* kiểu bool
            return "Z"
        elif typeIn is IntegerType: #* kiểu int
            return "I"
        elif typeIn is FloatType: #* kiểu float
            return "F"
        elif typeIn is StringType: #* kiểu string
            return "Ljava/lang/String;"
        elif typeIn is VoidType: #* kiểu void
            return "V"
        elif typeIn is ArrayType: #* kiểu array
            return "[" * len(inType.dimensions)  + self.getJVMType(inType.typ)
        elif typeIn is MT22: #* kiểu Zcode trương trình
            return "LZCodeClass;"
        elif typeIn is AutoType: #* kiểu VarZcode chỉ khi type = None, cần lưu line ở chỉnh sau này
            return "V"
        elif typeIn is FuncMT22: #* có 2 giống ý tưởng VarZcode
            return "(" + "".join(list(map(lambda x: self.getJVMType(x.typ), inType.param))) + ")" + self.getJVMType(inType.typ)
        
        return "Ljava/lang/Object;"

    """_Directives Generation APIs_
    
    """
    #* khởi tạo ban đầu của một class
    def emitPROLOG(self, name, parent):
        #& name: String, Tên class (name = ZCodeClass)
        #& parent: String, Tên class cha hiện tại là mặt định (parent = "")

        result = list()
        result.append(self.jvm.emitSOURCE(name + ".java"))
        result.append(self.jvm.emitCLASS("public " + name))
        result.append(self.jvm.emitSUPER("java/land/Object" if parent == "" else parent))
        return ''.join(result)

    #* ghi vào file .j để thực hiện biên dịch
    def emitEPILOG(self):
        file = open(self.filename, "w")
        file.write(''.join(self.buff))
        file.close()

    #* khơi tạo hàm 
    def emitMETHOD(self, lexeme, in_, isStatic, frame):
        #& lexeme: String (tên hàm)
        #& in_: Type (type của hàm FUNCZcode)
        #& isStatic: Boolean (chỉ có contrutor là không static còn lại là phải hết)
        #& frame: Frame

        return self.jvm.emitMETHOD(lexeme, self.getJVMType(in_), isStatic)

    #* gọi hàm static
    def emitINVOKESTATIC(self, lexeme, in_, frame):
        #& lexeme: String (tên hàm)
        #& in_: Type (kiểu funcMT22)
        #& frame: Frame

        typ = in_
        list(map(lambda x: frame.pop(), typ.param))
        if not type(typ.typ) is VoidType:
            frame.push()
        return self.jvm.emitINVOKESTATIC(lexeme, self.getJVMType(in_))
    
    #* gọi class cha invokespecial java/lang/Object/<init>()V
    def emitINVOKESPECIAL(self, frame, lexeme=None, in_=None):
        #& lexeme: String (bỏ qua luôn vì là java/lang/Object/<init>()V)
        #& in_: Type (bỏ qua luôn)
        #& frame: Frame

        if not lexeme is None and not in_ is None:
            typ = in_
            list(map(lambda x: frame.pop(), typ.param))
            frame.pop()
            if not type(typ.rettype) is VoidType:
                frame.push()
            return self.jvm.emitINVOKESPECIAL(lexeme, self.getJVMType(in_))
        elif lexeme is None and in_ is None:
            frame.pop()
            return self.jvm.emitINVOKESPECIAL()

    #* gọi concat, so sánh
    def emitINVOKEVIRTUAL(self, lexeme, in_, frame):
        # lexeme: String
        # in_: Type
        # frame: Frame

        typ = in_
        list(map(lambda x: frame.pop(), typ.param))
        if type(typ) is VoidType:
            frame.pop()
        return self.jvm.emitINVOKEVIRTUAL(lexeme, self.getJVMType(in_))
    
    
    #* cuối hàm dùng để xác định limit stack, limit locals
    def emitENDMETHOD(self, frame):
        # frame: Frame
        
        buffer = list()
        buffer.append(self.jvm.emitLIMITSTACK(frame.getMaxOpStackSize()))
        buffer.append(self.jvm.emitLIMITLOCAL(frame.getMaxIndex()))
        buffer.append(self.jvm.emitENDMETHOD())
        return ''.join(buffer)

    #* return 
    def emitRETURN(self, in_, frame):
        #& in_: Type
        #& frame: Frame

        if type(in_) is BooleanType:
            frame.pop()
            return self.jvm.emitIRETURN()
        elif type(in_) is IntegerType:
            frame.pop()
            return self.jvm.emitIRETURN()       
        elif type(in_) is FloatType:
            frame.pop()
            return self.jvm.emitFRETURN()
        elif type(in_) is VoidType:
            return self.jvm.emitRETURN()
        elif type(in_) is StringType or type(in_) is ArrayType:
            frame.pop()
            return self.jvm.emitARETURN()

    #* khởi tạo biến toàn cục thành biến static
    def emitATTRIBUTE(self, lexeme, in_, isFinal = False, value = None):
        #& lexeme: String (tên)
        #& in_: Type (kiểu)
        #& isFinal: Boolean (BTL này không sài cho FALSE)
        #& value: String (không sài luôn)

        return self.jvm.emitSTATICFIELD(lexeme, self.getJVMType(in_), isFinal)

    #* lấy giá trị của biến toàn cục
    def emitGETSTATIC(self, lexeme, in_, frame):
        #& lexeme: String (tên biến toàn cục)
        #& in_: Type (kiểu của biến toàn cục)
        #& frame: Frame

        frame.push()
        return self.jvm.emitGETSTATIC(lexeme, self.getJVMType(in_))

    #* cập nhật giá trị của biến toàn cục
    def emitPUTSTATIC(self, lexeme, in_, frame):
        #& lexeme: String (tên biến toàn cục)
        #& in_: Type (kiểu của biến toàn cục)
        #& frame: Frame

        frame.pop()
        return self.jvm.emitPUTSTATIC(lexeme, self.getJVMType(in_))

    #* limit stack _
    def emitLIMITSTACK(self, num):
        # num: Int
        return self.jvm.emitLIMITSTACK(num)
    #* limit locals _
    def emitLIMITLOCAL(self, num):
        # num: Int
        return self.jvm.emitLIMITLOCAL(num)

    #* cập nhật dòng lệnh vào self.buff
    def printout(self, in_):
        # in_: String
        self.buff.append(in_)
    
    #* lấy vị trí hàng vừa khởi tạo lưu vào line trong zcode
    def printIndexNew(self):
        return len(self.buff) - 1
    
    #* xóa tất cả
    def clearBuff(self):
        self.buff.clear()
        
         
    """_Operation Generation APIs_
    
    """
    #* Phép cộng, trừ 2 number (number ở đây là float)
    def emitADDOP(self, lexeme, in_, frame):
        #& lexeme: String (dấu +,-)
        #& in_: Type (integer | float)
        #& frame: Frame (TOÁN TỬ LẤY 2 GIÁ TRỊ VÀ TRẢ LẠI 1 GIÁ TRỊ)
        #& ..., value1, value2 -> ..., result

        frame.pop()
        if lexeme == "+":
            if type(in_) is IntegerType:
                return self.jvm.emitIADD()
            else:
                return self.jvm.emitFADD()
        else:
            if type(in_) is IntegerType:
                return self.jvm.emitISUB()
            else:
                return self.jvm.emitFSUB()

    #* Phép nhân, chia 2 number
    def emitMULOP(self, lexeme, in_, frame):
        #& lexeme: String (dấu *,/)
        #& in_: Type (integer | float)
        #& frame: Frame (TOÁN TỬ LẤY 2 GIÁ TRỊ VÀ TRẢ LẠI 1 GIÁ TRỊ)
        #& ..., value1, value2 -> ..., result

        frame.pop()
        if lexeme == "*":
            if type(in_) is IntegerType:
                return self.jvm.emitIMUL()
            else:
                return self.jvm.emitFMUL()
        else:
            if type(in_) is IntegerType:
                return self.jvm.emitIDIV()
            else:
                return self.jvm.emitFDIV()

    #* Phép and 2 bool
    def emitANDOP(self, frame):
        #& frame: Frame (TOÁN TỬ LẤY 2 GIÁ TRỊ VÀ TRẢ LẠI 1 GIÁ TRỊ)

        frame.pop()
        return self.jvm.emitIAND()
    
    #* Phép or 2 bool
    def emitOROP(self, frame):
        #& frame: Frame (TOÁN TỬ LẤY 2 GIÁ TRỊ VÀ TRẢ LẠI 1 GIÁ TRỊ)

        frame.pop()
        return self.jvm.emitIOR()

    #* so sánh 2 number trả về true/false
    def emitREOP(self, op, in_, frame):
        #& op: String
        #& in_: Type
        #& frame: Frame
        #& ..., value1, value2 -> ..., result

        result = list()
        labelF = frame.getNewLabel()
        labelO = frame.getNewLabel()

        frame.pop()
        frame.pop()
        if type(in_) is IntegerType or type(in_) is BooleanType:
            if op == ">":
                result.append(self.jvm.emitIFICMPLE(labelF))
            elif op == ">=":
                result.append(self.jvm.emitIFICMPLT(labelF))
            elif op == "<":
                result.append(self.jvm.emitIFICMPGE(labelF))
            elif op == "<=":
                result.append(self.jvm.emitIFICMPGT(labelF))
            elif op == "!=":
                result.append(self.jvm.emitIFICMPEQ(labelF))
            elif op == "==":
                result.append(self.jvm.emitIFICMPNE(labelF))
        elif type(in_) is FloatType:
            result.append(self.jvm.emitFCMPL())
            if op == ">":
                result.append(self.jvm.emitIFLE(labelF))
            elif op == ">=":
                result.append(self.jvm.emitIFLT(labelF))
            elif op == "<":
                result.append(self.jvm.emitIFGE(labelF))
            elif op == "<=":
                result.append(self.jvm.emitIFGT(labelF))
        result.append(self.emitPUSHCONST(True, BooleanType(), frame))
        frame.pop()
        result.append(self.emitGOTO(labelO, frame))
        result.append(self.emitLABEL(labelF, frame))
        result.append(self.emitPUSHCONST(False, BooleanType(), frame))
        result.append(self.emitLABEL(labelO, frame))
        return ''.join(result)

    def emitMOD(self, frame):
        # frame: Frame

        frame.pop()
        return self.jvm.emitIREM()

    #* lấy dấu âm
    def emitNEGOP(self, in_, frame):
        #& in_: Type
        #& frame: Frame
        #& ..., value -> ..., result

        if type(in_) is IntegerType:
            return self.jvm.emitINEG()
        else:
            return self.jvm.emitFNEG()


    #* hàm not
    def emitNOT(self, in_, frame):
        #& in_: Type
        #& frame: Frame

        label1 = frame.getNewLabel()
        label2 = frame.getNewLabel()
        result = list()
        result.append(self.emitIFTRUE(label1, frame))
        result.append(self.emitPUSHCONST(True, in_, frame))
        result.append(self.emitGOTO(label2, frame))
        result.append(self.emitLABEL(label1, frame))
        result.append(self.emitPUSHCONST(False, in_, frame))
        result.append(self.emitLABEL(label2, frame))
        return ''.join(result)

    #* CHUYỂN float->int
    def emitF2I(self, frame):
        # frame: Frame
        return '\tf2i\n'
    #* chuyển int->float
    def emitI2F(self, frame):
        # frame: Frame
        return self.jvm.emitI2F()
    
    """_Read/Write Variables APIs_
    """
    #* khởi tạo giá trị mặt định
    def emitPUSHCONST(self, in_, typ, frame):
        #& in_: String (giá trị)
        #& typ: Type (kiểu number/string/bool)
        #& frame: Frame
        frame.push()
        if type(typ) is IntegerType:
            i = in_
            if i >= -1 and i <= 5:
                return self.jvm.emitICONST(i)
            elif i >= -128 and i <= 127:
                return self.jvm.emitBIPUSH(i)
            elif i >= -32768 and i <= 32767:
                return self.jvm.emitSIPUSH(i)
            else:
                return self.jvm.emitLDC(str(i))
        elif type(typ) is FloatType:
            f = float(in_)
            rst = "{0:.4f}".format(f)
            if rst == "0.0" or rst == "1.0" or rst == "2.0":
                return self.jvm.emitFCONST(rst)
            else:
                return self.jvm.emitLDC(rst)    
        elif type(typ) is StringType:
            return self.jvm.emitLDC(in_)
        elif type(typ) is BooleanType:
            if in_:
                return self.jvm.emitICONST(1)
            else:
                return self.jvm.emitICONST(0)
        else:
            raise IllegalOperandException(in_)
    
    #* khởi tạo biến cục bộ
    def emitVAR(self, in_, varName, inType, fromLabel, toLabel, frame):
        #& in_: Int (vị trí index)
        #& varName: String (tên)
        #& inType: Type (kiểu)
        #& fromLabel: Int (tầm vực bắt đầu)
        #& toLabel: Int (tầm vực kết thúc)
        #& frame: Frame

        return self.jvm.emitVAR(in_, varName, self.getJVMType(inType), fromLabel, toLabel)

    def emitWRITEVAR(self, name, inType, index, frame):
        #& name: String
        #& inType: Type
        #& index: Int
        #& frame: Frame
        #& ..., value -> ...

        frame.pop()
        if type(inType) is FloatType:
            return self.jvm.emitFSTORE(index)
        if type(inType) is IntegerType:
            return self.jvm.emitISTORE(index)
        elif type(inType) is BooleanType:
            return self.jvm.emitISTORE(index)
        elif type(inType) is StringType:
            return self.jvm.emitASTORE(index)
        elif type(inType) is ArrayType:
            return self.jvm.emitASTORE(index)
        else:
            raise IllegalOperandException(name)  
        
    #* Đọc biến cục bộ các kiểu (number,bool,string)
    def emitREADVAR(self, name, inType, index, frame):
        #& name: String (tên biến để nén ra lỗi thôi)
        #& inType: Type (NumberType / StringType)
        #& index: Int (vị trí trong frame)
        #& frame: Frame (TRẢ LẠI 1)
        #& ... -> ..., value

        frame.push()
        if name == "this":
            return self.jvm.emitALOAD(index)
        elif type(inType) is BooleanType:
            return self.jvm.emitILOAD(index)
        elif type(inType) is IntegerType:
            return self.jvm.emitILOAD(index)        
        elif type(inType) is FloatType:
            return self.jvm.emitFLOAD(index)
        elif type(inType) is StringType:
            return self.jvm.emitALOAD(index)
        elif type(inType) is ArrayType:
            return self.jvm.emitALOAD(index)
        else:
            raise IllegalOperandException(name)

   #* Đọc mảng
    def emitALOAD(self, in_, frame):
        # in_: Type 
        # frame: Frame
        # ..., arrayref, index, value -> ...

        frame.pop()
        if type(in_) is BooleanType:
            return self.jvm.emitBALOAD()
        if type(in_) is IntegerType:
            return self.jvm.emitIALOAD()
        elif type(in_) is FloatType:
            return self.jvm.emitFALOAD()
        elif type(in_) is StringType or type(in_) is ArrayType:
            return self.jvm.emitAALOAD()
        else:
            raise IllegalOperandException(str(in_))        
        
    #* lưu mảng
    def emitASTORE(self, in_, frame):
        #& in_: Type
        #& frame: Frame
        #& ..., arrayref, index, value -> ...

        frame.pop()
        frame.pop()
        frame.pop()
        if type(in_) is FloatType:
            return self.jvm.emitFASTORE()
        if type(in_) is IntegerType:
            return self.jvm.emitIASTORE()
        if type(in_) is BooleanType:
            return self.jvm.emitBASTORE()
        elif  type(in_) is StringType or type(in_) is ArrayType:
            return self.jvm.emitAASTORE()
        else:
            raise IllegalOperandException(str(in_))


    """_biểu thức điều kiện và vòng lặp
    """
    #*nếu true thì nhảy
    def emitIFTRUE(self, label, frame):
        # label: Int
        # frame: Frame

        frame.pop()
        return self.jvm.emitIFGT(label)
    #* nếu false thì nhảy
    def emitIFFALSE(self, label, frame):
        # label: Int
        # frame: Frame

        frame.pop()
        return self.jvm.emitIFLE(label)
    #* nhãn
    def emitLABEL(self, label, frame):
        # label: Int
        # frame: Frame
        return self.jvm.emitLABEL(label)
    #* nhảy không cần điều kiện
    def emitGOTO(self, label, frame):
        # label: Int
        # frame: Frame
        return self.jvm.emitGOTO(str(label))

    """_new array
    """
    #* taoj ra array 1 chieue
    def emitNEWARRAY(self, in_, frame):
        # frame: Frame
        # in_: Type
        val = ""
        if type(in_) is IntegerType:
            val = "int"
        if type(in_) is FloatType:
            val = "float"
        elif type(in_) is BooleanType:
            val = "boolean"
        elif type(in_) is StringType:
            return self.emitANEWARRAY(in_, frame)
        return self.jvm.emitNEWARRAY(val)
    
    #* tạo ra array 1 chiều địa chỉ
    def emitANEWARRAY(self, in_, frame):
        # frame: Frame
        # in_: Type
        val = ""
        if type(in_) is FloatType:
            val = "float"
        if type(in_) is IntegerType:
            val = "int"
        elif type(in_) is BooleanType:
            val = "boolean"
        elif type(in_) is StringType:
            val = "java/lang/String"
        elif type(in_) is ArrayType:
            val = self.getJVMType(in_)
        return self.jvm.emitANEWARRAY(val)

    #* tạo ra array nhiều chiều
    def emitMULTIANEWARRAY(self, in_, frame):
        # frame: Frame
        # in_: Type
        if type(in_) is ArrayType:
            dimens = len(in_.size)
            return self.jvm.emitMULTIANEWARRAY(self.getJVMType(in_), str(dimens))
    
    #* nhân 2 vùng stack dùng cho array  
    def emitDUP(self, frame):
        # frame: Frame

        frame.push()
        return self.jvm.emitDUP()

    # def emitIFICMPGT(self, label, frame):
    #     # label: Int
    #     # frame: Frame

    #     frame.pop()
    #     return self.jvm.emitIFICMPGT(label)

    # def emitIFICMPLT(self, label, frame):
    #     # label: Int
    #     # frame: Frame

    #     frame.pop()
    #     return self.jvm.emitIFICMPLT(label)



    def emitPOP(self, frame):
        # frame: Frame

        frame.pop()
        return self.jvm.emitPOP()



 
