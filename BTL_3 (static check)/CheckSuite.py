import unittest
from TestUtils import TestChecker
from AST import *
import inspect

class CheckSuite(unittest.TestCase):
    def test_001(self):
        """
var VoTien = 1; 
var VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien", inspect.stack()[0].function))

    def test_002(self):
        """
var VoTien = 1; 
const VoTien = 2;
        """
        input = Program([VarDecl("VoTien", None,IntLiteral(1)),ConstDecl("VoTien",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: VoTien", inspect.stack()[0].function))

    def test_003(self):
        """
const VoTien = 1; 
var VoTien = 2;
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),VarDecl("VoTien", None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien", inspect.stack()[0].function))

    def test_004(self):
        """
const VoTien = 1; 
func VoTien () {return;}
        """
        input = Program([ConstDecl("VoTien",None,IntLiteral(1)),FuncDecl("VoTien",[],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Function: VoTien", inspect.stack()[0].function))

    def test_005(self):
        """ 
func VoTien () {return;}
var VoTien = 1;
        """
        input = Program([FuncDecl("VoTien",[],VoidType(),Block([Return(None)])),VarDecl("VoTien", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: VoTien", inspect.stack()[0].function))

    def test_006(self):
        """ 
var getInt = 1;
        """
        input = Program([VarDecl("getInt", None,IntLiteral(1))])
        self.assertTrue(TestChecker.test(input, "Redeclared Variable: getInt", inspect.stack()[0].function))

    def test_007(self):
        """ 
type  Votien struct {
    Votien int;
}
type TIEN struct {
    Votien string;
    TIEN int;
    TIEN float;
}
        """
        input = Program([StructType("Votien",[("Votien",IntType())],[]),StructType("TIEN",[("Votien",StringType()),("TIEN",IntType()),("TIEN",FloatType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Field: TIEN", inspect.stack()[0].function))

    def test_008(self):
        """ 
func (v TIEN) putIntLn () {return;}
func (v TIEN) getInt () {return;}
func (v TIEN) getInt () {return;}
type TIEN struct {
    Votien int;
}
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("putIntLn",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([Return(None)]))), StructType("TIEN",[("Votien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Method: getInt", inspect.stack()[0].function))

    def test_009(self):
        """ 
type VoTien interface {
    VoTien ();
    VoTien (a int);
}
        """
        input = Program([InterfaceType("VoTien",[Prototype("VoTien",[],VoidType()),Prototype("VoTien",[IntType()],VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Prototype: VoTien", inspect.stack()[0].function))

    def test_010(self):
        """ 
func Votien (a, a int) {return;}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("a",IntType()),ParamDecl("a",IntType())],VoidType(),Block([Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Parameter: a", inspect.stack()[0].function))

    def test_011(self):
        """ 
func Votien (b int) {
    var b = 1;
    var a = 1;
    const a = 1;
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([VarDecl("b", None,IntLiteral(1)),VarDecl("a", None,IntLiteral(1)),ConstDecl("a",None,IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a", inspect.stack()[0].function))

    def test_012(self):
        """ 
func Votien (b int) {
    for var a = 1; a < 1; a += 1 {
        const a = 2;
    }
}
        """
        input = Program([FuncDecl("Votien",[ParamDecl("b",IntType())],VoidType(),Block([ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("a"),BinaryOp("+", Id("a"), IntLiteral(1))),Block([ConstDecl("a",None,IntLiteral(2))]))]))])
        self.assertTrue(TestChecker.test(input, "Redeclared Constant: a", inspect.stack()[0].function))
    
    def test_013(self):
        """ 
type TIEN struct {Votien int;}
type TIEN interface {VoTien ();}

        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),InterfaceType("TIEN",[Prototype("VoTien",[],VoidType())])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: TIEN", inspect.stack()[0].function))

#     #! ----------- TASK 2---------------------
    def test_014(self):
        """ 
var a = 1;
var b = a;
var c = d;
        """
        input = Program([VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,Id("a")),VarDecl("c", None,Id("d"))])
        self.assertTrue(TestChecker.test(input, "Undeclared Identifier: d", inspect.stack()[0].function))

    def test_015(self):
        """ 
func Votien () int {return 1;}

func foo () {
    var b = Votien();
    foo_votine();
    return;
}
        """
        input = Program([FuncDecl("Votien",[],IntType(),Block([Return(IntLiteral(1))])),FuncDecl("foo",[],VoidType(),Block([VarDecl("b", None,FuncCall("Votien",[])),FuncCall("foo_votine",[]),Return(None)]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Function: foo_votine", inspect.stack()[0].function))

    def test_016(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    const c = v.Votien;
    var d = v.tien;
}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([ConstDecl("c",None,FieldAccess(Id("v"),"Votien")),VarDecl("d", None,FieldAccess(Id("v"),"tien"))])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Field: tien", inspect.stack()[0].function))

    def test_017(self):
        """ 
type TIEN struct {
    Votien int;
}

func (v TIEN) getInt () {
    v.getInt ();
    v.putInt ();
}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("getInt",[],VoidType(),Block([MethCall(Id("v"),"getInt",[]),MethCall(Id("v"),"putInt",[])])))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: putInt", inspect.stack()[0].function))

    def test_018(self):
        """ 
type TIEN struct {Votien int;}
type TIEN struct {v int;}
}
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),StructType("TIEN",[("v",IntType())],[])])
        self.assertTrue(TestChecker.test(input, "Redeclared Type: TIEN", inspect.stack()[0].function))
    

    def test_019(self):
        """ 
  
var v TIEN;      
type TIEN struct {
    a int;
} 
type VO interface {
    foo() int;
}

func (v TIEN) foo() int {return 1;}
func (b TIEN) koo() {b.koo();}
func foo() {
    var x VO;  
    const b = x.foo(); 
    x.koo(); 
}
        
        """
        input = Program([VarDecl("v",Id("TIEN"), None),StructType("TIEN",[("a",IntType())],[]),InterfaceType("VO",[Prototype("foo",[],IntType())]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[],IntType(),Block([Return(IntLiteral(1))]))),MethodDecl("b",Id("TIEN"),FuncDecl("koo",[],VoidType(),Block([MethCall(Id("b"),"koo",[])]))),FuncDecl("foo",[],VoidType(),Block([VarDecl("x",Id("VO"), None),ConstDecl("b",None,MethCall(Id("x"),"foo",[])),MethCall(Id("x"),"koo",[])]))])
        self.assertTrue(TestChecker.test(input, "Undeclared Method: koo", inspect.stack()[0].function))
    
    def test_020(self):
        """ 
var a = foo();
func foo () int {
    var a =  koo();
    var c = getInt();
    putInt(c);
    putIntLn(c);
    return 1;
}
var d = foo();
func koo () int {
    var a =  foo ();
    return 1;
}
        """
        input = Program([VarDecl("a", None,FuncCall("foo",[])),FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,FuncCall("koo",[])),VarDecl("c", None,FuncCall("getInt",[])),FuncCall("putInt",[Id("c")]),FuncCall("putIntLn",[Id("c")]),Return(IntLiteral(1))])),VarDecl("d", None,FuncCall("foo",[])),FuncDecl("koo",[],IntType(),Block([VarDecl("a", None,FuncCall("foo",[])),Return(IntLiteral(1))]))])
        self.assertTrue(TestChecker.test(input, "VOTIEN", inspect.stack()[0].function))
    
    #! ----------- TASK 2---------------------


    #! ----------- TASK 3---------------------
    def test_021(self):
        """ 
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien();}
type I2 interface {votien();}

func (s S1) votien() {return;}

var a S1;
var b S2;
var c I1 = a;
var d I2 = b;
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),InterfaceType("I2",[Prototype("votien",[],VoidType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],VoidType(),Block([Return(None)]))),VarDecl("a",Id("S1"), None),VarDecl("b",Id("S2"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("b"))])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: votien""", inspect.stack()[0].function))

    def test_022(self):
        """ 
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien();}
type I2 interface {votien() int;}

func (s S1) votien() {return;}

var a S1;
var b S2;
var c I2 = a;   
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),InterfaceType("I2",[Prototype("votien",[],IntType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],VoidType(),Block([Return(None)]))),VarDecl("a",Id("S1"), None),VarDecl("b",Id("S2"), None),VarDecl("c",Id("I2"),Id("a"))])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: votien""", inspect.stack()[0].function))

    def test_023(self):
        """ 
        
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien(e, e int) S1;}
type I2 interface {votien(a int) S1;}

func (s S1) votien(a, b int) S1 {return s;}

var a S1;
var c I1 = a;
var d I2 = a;
        
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[IntType(),IntType()],Id("S1"))]),InterfaceType("I2",[Prototype("votien",[IntType()],Id("S1"))]),MethodDecl("s",Id("S1"),FuncDecl("votien",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: votien""", inspect.stack()[0].function))

    def test_024(self):
        """ 
type S1 struct {votien int;}
type S2 struct {votien int;}
type I1 interface {votien(e, e int) S1;}
type I2 interface {votien(a int, b float) S1;}

func (s S1) votien(a, b int) S1 {return s;}

var a S1;
var c I1 = a;
var d I2 = a;
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[IntType(),IntType()],Id("S1"))]),InterfaceType("I2",[Prototype("votien",[IntType(),FloatType()],Id("S1"))]),MethodDecl("s",Id("S1"),FuncDecl("votien",[ParamDecl("a",IntType()),ParamDecl("b",IntType())],Id("S1"),Block([Return(Id("s"))]))),VarDecl("a",Id("S1"), None),VarDecl("c",Id("I1"),Id("a")),VarDecl("d",Id("I2"),Id("a"))])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: votien""", inspect.stack()[0].function))


    def test_025(self):
        """ 
func foo(){
    if (1) {
         var a float = 1.02;
    }
}      
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([If(IntLiteral(1), Block([VarDecl("a",FloatType(),FloatLiteral(1.2))]), None)]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: If(IntLiteral(1), Block([VarDecl("a",FloatType(),FloatLiteral(1.2))]), None)""", inspect.stack()[0].function))

    def test_026(self):
        """ 
        
func foo(){
    if (true) {
         var a float = 1.02;
    } else {
        var a int = 1.02;
    }
}

        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([If(BooleanLiteral(True), Block([VarDecl("a",FloatType(),FloatLiteral(1.2))]), Block([VarDecl("a",IntType(),FloatLiteral(1.2))]))]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("a",IntType(),FloatLiteral(1.2))""", inspect.stack()[0].function))


    def test_027(self):
        """ 
      
var a = [2] int {1, 2}
var c [3] int = a
        """
        input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(3)],IntType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("c",ArrayType([IntLiteral(3)],IntType()),Id("a"))""", inspect.stack()[0].function))


    def test_028(self):
        """ 
      
var a = [2] int {1, 2}
var c [3] float = a
        
        """
        input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(3)],FloatType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("c",ArrayType([IntLiteral(3)],FloatType()),Id("a"))""", inspect.stack()[0].function))


    def test_029(self):
        """ 
var a = [2] int {1, 2}
var c [3][2] int = a
        """
        input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(3),IntLiteral(2)],IntType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("c",ArrayType([IntLiteral(3),IntLiteral(2)],IntType()),Id("a"))""", inspect.stack()[0].function))


    def test_030(self):
        """ 
var a [2][3] int;
var b = a[1];
var c [3] int = b;
var d [3] string = b;
        """
        input = Program([VarDecl("a",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("b", None,ArrayCell(Id("a"),[IntLiteral(1)])),VarDecl("c",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("d",ArrayType([IntLiteral(3)],StringType()),Id("b"))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("d",ArrayType([IntLiteral(3)],StringType()),Id("b"))""", inspect.stack()[0].function))


    def test_031(self):
        """ 
var a [2][3] int;
var b = a[1][2];
var c int = b;
var d [1] string = b;
        """
        input = Program([VarDecl("a",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("b", None,ArrayCell(Id("a"),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",IntType(),Id("b")),VarDecl("d",ArrayType([IntLiteral(1)],StringType()),Id("b"))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("d",ArrayType([IntLiteral(1)],StringType()),Id("b"))""", inspect.stack()[0].function))


    def test_032(self):
        """ 

type S1 struct {votien int;}
type I1 interface {votien();}
var a I1;
var c I1 = nil;
var d S1 = nil;
func foo(){
    c := a;
    a := nil;
}

var e int = nil;
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),VarDecl("a",Id("I1"), None),VarDecl("c",Id("I1"),NilLiteral()),VarDecl("d",Id("S1"),NilLiteral()),FuncDecl("foo",[],VoidType(),Block([Assign(Id("c"),Id("a")),Assign(Id("a"),NilLiteral())])),VarDecl("e",IntType(),NilLiteral())])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",IntType(),NilLiteral())""", inspect.stack()[0].function))


    def test_033(self):
        """ 
var a int = 1 % 2;
var b int = 1 % 2.0;     
        """
        input = Program([VarDecl("a",IntType(),BinaryOp("%", IntLiteral(1), IntLiteral(2))),VarDecl("b",IntType(),BinaryOp("%", IntLiteral(1), FloatLiteral(2.0)))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp("%", IntLiteral(1), FloatLiteral(2.0))""", inspect.stack()[0].function))


    def test_034(self):
        """ 
var a boolean = 1 > 2;
var b boolean = 1.0 < 2.0;
var c boolean = "1" == "2";
var d boolean = 1 > 2.0;
        """
        input = Program([VarDecl("a", BoolType(), BinaryOp(">", IntLiteral(1), IntLiteral(2))),
                         VarDecl("b", BoolType(), BinaryOp("<", FloatLiteral(1.0), FloatLiteral(2.0))),
                         VarDecl("c", BoolType(), BinaryOp("==", StringLiteral("1"), StringLiteral("2"))),
                         VarDecl("d", BoolType(), BinaryOp(">", IntLiteral(1), FloatLiteral(2.0)))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: BinaryOp(">", IntLiteral(1), FloatLiteral(2.0))""", inspect.stack()[0].function))


    def test_035(self):
        """ 
func foo(){
    var arr [2] int;
    for a, b := range arr {
        var c int = a;
        var d int = b;
        var e string = a;
    }
}
    
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",IntType(),Id("b")),VarDecl("e",StringType(),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: a""", inspect.stack()[0].function))


    def test_036(self):
        """ 
type putLn struct {a int;};
        """
        input = Program([StructType("putLn",[("a",IntType())],[])])

        self.assertTrue(TestChecker.test(input, """Redeclared Type: putLn""", inspect.stack()[0].function))


    def test_037(self):
        """ 
var a int = getBool();

        """
        input = Program([VarDecl("a",IntType(),FuncCall("getBool",[]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("a",IntType(),FuncCall("getBool",[]))""", inspect.stack()[0].function))


    def test_038(self):
        """ 
func foo() {
    putFloat(getInt());
}      
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([FuncCall("putFloat",[FuncCall("getInt",[])])]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: FuncCall("putFloat",[FuncCall("getInt",[])])""", inspect.stack()[0].function))


    def test_039(self):
        """ 
type TIEN struct {a [2]int;} 

func foo() TIEN {
    return nil
}
             
        """
        input = Program([StructType("TIEN",[("a",ArrayType([IntLiteral(2)],IntType()))],[]),FuncDecl("foo",[],Id("TIEN"),Block([Return(NilLiteral())]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_040(self):
        """ 
func foo() int {
    var a = 1;
    if (a < 3) {
        var a = 1;
    } else if(a > 2) {
        var a = 2;
    }
    return a;
}
             
        """
        input = Program([FuncDecl("foo",[],IntType(),Block([VarDecl("a", None,IntLiteral(1)),If(BinaryOp("<", Id("a"), IntLiteral(3)), Block([VarDecl("a", None,IntLiteral(1))]), If(BinaryOp(">", Id("a"), IntLiteral(2)), Block([VarDecl("a", None,IntLiteral(2))]), None)),Return(Id("a"))]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_041(self):
        """ 
var A = 1;
type A struct {a int;}
        """
        input = Program([VarDecl("A", None,IntLiteral(1)),StructType("A",[("a",IntType())],[])])

        self.assertTrue(TestChecker.test(input, """Redeclared Type: A""", inspect.stack()[0].function))


    def test_042(self):
        """ 

type A interface {foo();}
const A = 2;
        """
        input = Program([InterfaceType("A",[Prototype("foo",[],VoidType())]),ConstDecl("A",None,IntLiteral(2))])

        self.assertTrue(TestChecker.test(input, """Redeclared Constant: A""", inspect.stack()[0].function))


    def test_043(self):
        """ 
type S1 struct {votien int;}
type I1 interface {votien();}

func (s S1) votien() {return;}

var b [2] S1;
var a [2] I1 = b;
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),InterfaceType("I1",[Prototype("votien",[],VoidType())]),MethodDecl("s",Id("S1"),FuncDecl("votien",[],VoidType(),Block([Return(None)]))),VarDecl("b",ArrayType([IntLiteral(2)],Id("S1")), None),VarDecl("a",ArrayType([IntLiteral(2)],Id("I1")),Id("b"))])

        self.assertTrue(TestChecker.test(input, """Redeclared Method: votien""", inspect.stack()[0].function))


    def test_044(self):
        """ 

func foo() [2] float {
    return [2] float {1.0, 2.0};
    return [2] int {1, 2};
}
        
        """
        input = Program([FuncDecl("foo",[],ArrayType([IntLiteral(2)],FloatType()),Block([Return(ArrayLiteral([IntLiteral(2)],FloatType(),[FloatLiteral(1.0),FloatLiteral(2.0)])),Return(ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: Return(ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)]))""", inspect.stack()[0].function))


    def test_045(self):
        """ 
func votien(a  [2]int ) {
    votien([3] int {1,2,3})
}
       
        """
        input = Program([FuncDecl("votien",[ParamDecl("a",ArrayType([IntLiteral(2)],IntType()))],VoidType(),Block([FuncCall("votien",[ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: FuncCall("votien",[ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])""", inspect.stack()[0].function))


    def test_046(self):
        """ 
var a [1 + 9] int;
var b [10] int = a;
        """
        input = Program([VarDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(9))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_047(self):
        """ 
var a [5 / 2] int;
var b [2] int = a;
        """
        input = Program([VarDecl("a",ArrayType([BinaryOp("/", IntLiteral(5), IntLiteral(2))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(2)],IntType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_048(self):
        """ 

const a = 2 + 3;
var b [a * 2 + a] int;
var c [15] int = b;

        """
        input = Program([ConstDecl("a",None,BinaryOp("+", IntLiteral(2), IntLiteral(3))),VarDecl("b",ArrayType([BinaryOp("+", BinaryOp("*", Id("a"), IntLiteral(2)), Id("a"))],IntType()), None),VarDecl("c",ArrayType([IntLiteral(15)],IntType()),Id("b"))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_049(self):
        """ 
var a = 1;
func foo () {
    const b = 1;
    for a, c := range [3]int{1, 2, 3} {
        var d = c;
    }
    var d = a;
    var a = 1;
}
var d = b;
        """
        input = Program([VarDecl("a", None,IntLiteral(1)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("b",None,IntLiteral(1)),ForEach(Id("a"),Id("c"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("d", None,Id("c"))])),VarDecl("d", None,Id("a")),VarDecl("a", None,IntLiteral(1))])),VarDecl("d", None,Id("b"))])

        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: c""", inspect.stack()[0].function))


    def test_050(self):
        """ 
var v string = "1";
const x = v;
var k string = x;
var y boolean = x;
        """
        input = Program([VarDecl("v",StringType(),StringLiteral("1")),ConstDecl("x",None,Id("v")),VarDecl("k",StringType(),Id("x")),VarDecl("y",StringType(),Id("x"))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_051(self):
        """ 
  
type S1 struct {votien int;}
type S2 struct {votien int;}

var v S1;
const x = v;
var z S1 = x;
var k S2 = x;
        
        """
        input = Program([StructType("S1",[("votien",IntType())],[]),StructType("S2",[("votien",IntType())],[]),VarDecl("v",Id("S1"), None),ConstDecl("x",None,Id("v")),VarDecl("z",Id("S1"),Id("x")),VarDecl("k",Id("S2"),Id("x"))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("k",Id("S2"),Id("x"))""", inspect.stack()[0].function))

    def test_052(self):
        """ 
type A interface {foo();}
const A = 2;
        """
        input = Program([InterfaceType("A",[Prototype("foo",[],VoidType())]),ConstDecl("A",None,IntLiteral(2))])
        self.assertTrue(TestChecker.test(input, """Redeclared Constant: A""", inspect.stack()[0].function))

    def test_053(self):
        """
func foo(a [2] float) {
    foo([2] float {1.0,2.0})
    foo([2] int {1,2})
}
        """
        input = Program([FuncDecl("foo",[ParamDecl("a",ArrayType([IntLiteral(2)],FloatType()))],VoidType(),Block([FuncCall("foo",[ArrayLiteral([IntLiteral(2)],FloatType(),[FloatLiteral(1.0),FloatLiteral(2.0)])]),FuncCall("foo",[ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])])]))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: FuncCall("foo",[ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])])""", inspect.stack()[0].function)) 


    def test_054(self):
        """
const v = 3;
const a = v + v;
var b [a * 2 + a] int;
var c [18] int = b;
        """
        input = Program([ConstDecl("v",None,IntLiteral(3)),ConstDecl("a",None,BinaryOp("+", Id("v"), Id("v"))),VarDecl("b",ArrayType([BinaryOp("+", BinaryOp("*", Id("a"), IntLiteral(2)), Id("a"))],IntType()), None),VarDecl("c",ArrayType([IntLiteral(18)],IntType()),Id("b"))])
        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function)) 


    def test_055(self):
        """
const a = 1 + 2;
var b [a] int;
var c [4] int = b; # sai vì 4 != 3
        """
        input = Program([ConstDecl("a", None, BinaryOp("+", IntLiteral(1), IntLiteral(2))),
                            VarDecl("b", ArrayType([Id("a")], IntType()), None),
                            VarDecl("c", ArrayType([IntLiteral(4)], IntType()), Id("b"))])
        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("c",ArrayType([IntLiteral(4)],IntType()),Id("b"))""", inspect.stack()[0].function)) 




    def test_056(self):
        """ 

var a [1 + 9] int;
var b [10] int = a;
        """
        input = Program([VarDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(9))],IntType()), None),VarDecl("b",ArrayType([IntLiteral(10)],IntType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_057(self):
        """ 

var a = [2] int {1, 2}
var c [2] float = a

        """
        input = Program([VarDecl("a", None,ArrayLiteral([IntLiteral(2)],IntType(),[IntLiteral(1),IntLiteral(2)])),VarDecl("c",ArrayType([IntLiteral(2)],FloatType()),Id("a"))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_058(self):
        """ 

const v = 3;
var c [3] int = [v * 1] int {1 , 2, 3};
        """
        input = Program([ConstDecl("v",None,IntLiteral(3)),VarDecl("c",ArrayType([IntLiteral(3)],IntType()),ArrayLiteral([BinaryOp("*", Id("v"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_059(self):
        """ 

const v = 3;
const k = v + 1;        # 4
func foo(a [1 + 2] int) {
    foo([k - 1] int {1,2,3})
} 
    
        """
        input = Program([ConstDecl("v",None,IntLiteral(3)),ConstDecl("k",None,BinaryOp("+", Id("v"), IntLiteral(1))),FuncDecl("foo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([FuncCall("foo",[ArrayLiteral([BinaryOp("-", Id("k"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_060(self):
        """ 

type K struct {a int;}
func (k K) koo(a [1 + 2] int) {return;}

const c = 4;
func foo() {
    var k K;
    k.koo([c - 1] int {1,2,3})
} 
        
        """
        input = Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([Return(None)]))),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],VoidType(),Block([VarDecl("k",Id("K"), None),MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_061(self):
        """ 
type K struct {a int;}
func (k K) koo(a [1 + 2] int) {return;}
type H interface {koo(a [1 + 2] int);}

const c = 4;
func foo() {
    var k H;
    k.koo([c - 1] int {1,2,3})
} 
     
        """
        input = Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],VoidType(),Block([Return(None)]))),InterfaceType("H",[Prototype("koo",[ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType())],VoidType())]),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],VoidType(),Block([VarDecl("k",Id("H"), None),MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_062(self):
        """ 

type K struct {a int;}
func (k K) koo(a [1 + 2] int) [1 + 2] int {return [3*1] int {1,2,3};}
type H interface {koo(a [1 + 2] int) [1 + 2] int;}

const c = 4;
func foo() [1 + 2] int{
    return foo()
    var k K;
    return k.koo([c - 1] int {1,2,3})
    var h H;
    return h.koo([c - 1] int {1,2,3})
} 
        """
        input = Program([StructType("K",[("a",IntType())],[]),MethodDecl("k",Id("K"),FuncDecl("koo",[ParamDecl("a",ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))],ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()),Block([Return(ArrayLiteral([BinaryOp("*", IntLiteral(3), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))]))),InterfaceType("H",[Prototype("koo",[ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType())],ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()))]),ConstDecl("c",None,IntLiteral(4)),FuncDecl("foo",[],ArrayType([BinaryOp("+", IntLiteral(1), IntLiteral(2))],IntType()),Block([Return(FuncCall("foo",[])),VarDecl("k",Id("K"), None),Return(MethCall(Id("k"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])])),VarDecl("h",Id("H"), None),Return(MethCall(Id("h"),"koo",[ArrayLiteral([BinaryOp("-", Id("c"), IntLiteral(1))],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_063(self):
        """ 

const a = 3;
const b = -a;
const c = -b;
var d [c] int = [3] int {1,2,3}

        """
        input = Program([ConstDecl("a",None,IntLiteral(3)),ConstDecl("b",None,UnaryOp("-",Id("a"))),ConstDecl("c",None,UnaryOp("-",Id("b"))),VarDecl("d",ArrayType([Id("c")],IntType()),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_064(self):
        """ 

const a = 1;
func foo() {
    a := 1.;
}

        """
        input = Program([ConstDecl("a",None,IntLiteral(1)),FuncDecl("foo",[],VoidType(),Block([Assign(Id("a"),FloatLiteral(1.0))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: Assign(Id("a"),FloatLiteral(1.0))""", inspect.stack()[0].function))


    def test_065(self):
        """ 
      
        """
        input = Program([VarDecl("a",IntType(),None),VarDecl("b",FloatType(),None),VarDecl("a",IntType(),None)])

        self.assertTrue(TestChecker.test(input, """Redeclared Variable: a""", inspect.stack()[0].function))


    def test_066(self):
        """ 
type TIEN struct {
    Votien int;
}
func (v TIEN) foo (v int) {return;}
func foo () {return;}
        
        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("foo",[ParamDecl("v",IntType())],VoidType(),Block([Return(None)]))),FuncDecl("foo",[],VoidType(),Block([Return(None)]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_067(self):
        """ 

const a = 2;
func foo () {
    const a = 1;
    for var a = 1; a < 1; b := 2 {
        const b = 1;
    }
}
       
        """
        input = Program([ConstDecl("a",None,IntLiteral(2)),FuncDecl("foo",[],VoidType(),Block([ConstDecl("a",None,IntLiteral(1)),ForStep(VarDecl("a", None,IntLiteral(1)),BinaryOp("<", Id("a"), IntLiteral(1)),Assign(Id("b"),IntLiteral(2)),Block([ConstDecl("b",None,IntLiteral(1))]))]))])

        self.assertTrue(TestChecker.test(input, """Redeclared Constant: b""", inspect.stack()[0].function))


    def test_068(self):
        """ 
const a = 2;
type STRUCT struct {x [a] int;}
func (s STRUCT) foo(x [a] int) [a] int {return s.x;}
func foo(x [a] int) [a] int  {
    const a = 3;
    return [a] int {1,2};
}

        """
        input = Program([ConstDecl("a",None,IntLiteral(2)),StructType("STRUCT",[("x",ArrayType([Id("a")],IntType()))],[]),MethodDecl("s",Id("STRUCT"),FuncDecl("foo",[ParamDecl("x",ArrayType([Id("a")],IntType()))],ArrayType([Id("a")],IntType()),Block([Return(FieldAccess(Id("s"),"x"))]))),FuncDecl("foo",[ParamDecl("x",ArrayType([Id("a")],IntType()))],ArrayType([Id("a")],IntType()),Block([ConstDecl("a",None,IntLiteral(3)),Return(ArrayLiteral([Id("a")],IntType(),[IntLiteral(1),IntLiteral(2)]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: Return(ArrayLiteral([Id("a")],IntType(),[IntLiteral(1),IntLiteral(2)]))""", inspect.stack()[0].function))

    def test_069(self):
        """
func (v TIEN) VO () {return ;}
func (v TIEN) Tien () {return ;}
type TIEN struct {
    Votien int;
    Tien int;
}
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("VO",[],VoidType(),Block([Return(None)]))),MethodDecl("v",Id("TIEN"),FuncDecl("Tien",[],VoidType(),Block([Return(None)]))),StructType("TIEN",[("Votien",IntType()),("Tien",IntType())],[])])
        self.assertTrue(TestChecker.test(input, """Redeclared Method: Tien""", inspect.stack()[0].function))



#     def test_070(self):
#         """
# func foo(a int) {
#     foo(1);
#     var foo = 1;
#     foo(2); // error
# }
#         """
#         input = Program([FuncDecl("foo",[ParamDecl("a",IntType())],VoidType(),Block([FuncCall("foo",[IntLiteral(1)]),VarDecl("foo", None,IntLiteral(1)),FuncCall("foo",[IntLiteral(2)])]))])
#         self.assertTrue(TestChecker.test(input, """Undeclared Function: foo""", inspect.stack()[0].function))


    def test_070(self):
        """ 

type TIEN struct {
    Votien int;
}
func (v TIEN) Votien () {return ;}

        """
        input = Program([StructType("TIEN",[("Votien",IntType())],[]),MethodDecl("v",Id("TIEN"),FuncDecl("Votien",[],VoidType(),Block([Return(None)])))])

        self.assertTrue(TestChecker.test(input, """Redeclared Method: Votien""", inspect.stack()[0].function))


    def test_071(self):
        """ 
func (v TIEN) Votien () {return ;}
type TIEN struct {
    Votien int;
}
        """
        input = Program([MethodDecl("v",Id("TIEN"),FuncDecl("Votien",[],VoidType(),Block([Return(None)]))),StructType("TIEN",[("Votien",IntType())],[])])

        self.assertTrue(TestChecker.test(input, """Redeclared Method: Votien""", inspect.stack()[0].function))


    def test_072(self):
        """ 
func foo() int {
    const foo = 1;
    return foo()
}
        """
        input = Program([FuncDecl("foo",[],IntType(),Block([ConstDecl("foo",None,IntLiteral(1)),Return(FuncCall("foo",[]))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Function: foo""", inspect.stack()[0].function))


    def test_073(self):
        """ 
func foo() {
    var a = foo
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("a", None,Id("foo"))]))])
        self.assertTrue(TestChecker.test(input, """Undeclared Identifier: foo""", inspect.stack()[0].function))


    def test_074(self):
        """ 
func foo () {
    var a = 1;
    var b = 1;
    for a, b := range [3]int {1, 2, 3} {
        var b = 1;
    }
}
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,IntLiteral(1)),ForEach(Id("a"),Id("b"),ArrayLiteral([IntLiteral(3)],IntType(),[IntLiteral(1),IntLiteral(2),IntLiteral(3)]),Block([VarDecl("b", None,IntLiteral(1))]))]))])

        self.assertTrue(TestChecker.test(input, """VOTIEN""", inspect.stack()[0].function))


    def test_075(self):
        """ 

func foo(){
    var arr [2] int;
    var a = 1;
    var b = 2;
    for a, b := range arr {
        var c int = a;
        var d int = b;
        var e string = a;
    }
}
   
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b", None,IntLiteral(2)),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",IntType(),Id("b")),VarDecl("e",StringType(),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",StringType(),Id("a"))""", inspect.stack()[0].function))


    def test_077(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_078(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_079(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_080(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_081(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_082(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_083(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_084(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_085(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_086(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_087(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_088(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_089(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_090(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_091(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_092(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_093(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_094(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_095(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_096(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_097(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_098(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_099(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))

    def test_100(self):
        """ 
func foo(){
    var arr [2][3] int;
    var a = 1;
    var b[3]int;
    for a, b := range arr {
        var c int = a;
        var d [3]int = b;
        var e [2]string = a;
    }
}
     
        """
        input = Program([FuncDecl("foo",[],VoidType(),Block([VarDecl("arr",ArrayType([IntLiteral(2),IntLiteral(3)],IntType()), None),VarDecl("a", None,IntLiteral(1)),VarDecl("b",ArrayType([IntLiteral(3)],IntType()), None),ForEach(Id("a"),Id("b"),Id("arr"),Block([VarDecl("c",IntType(),Id("a")),VarDecl("d",ArrayType([IntLiteral(3)],IntType()),Id("b")),VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))]))]))])

        self.assertTrue(TestChecker.test(input, """Type Mismatch: VarDecl("e",ArrayType([IntLiteral(2)],StringType()),Id("a"))""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))


    # def test_020(self):
    #     """ 
      
    #     """
    #     input = 
    #     self.assertTrue(TestChecker.test(input, """""", inspect.stack()[0].function))




    #! ----------- TASK 3---------------------
