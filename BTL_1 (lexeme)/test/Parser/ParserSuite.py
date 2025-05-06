"""
 * Initial code for Assignment 1, 2
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/Shiba.Vo.Tien
 * Link Group : https://www.facebook.com/groups/khmt.ktmt.cse.bku
 * Date: 07.01.2025
"""

import unittest
from TestUtils import TestParser
import inspect

class ParserSuite(unittest.TestCase):
    # def test_001(self):
    #     input = """const VoTien = 1; """
    #     # expect = ConstDecl("VoTien", None, IntLiteral(1))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_002(self):
    #     """ chuyển đổi sang kiểu int hết """
    #     input = """const VoTien = 0b11; """
    #     # expect = ConstDecl("VoTien", None, IntLiteral(3))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_003(self):
    #     input = """const VoTien = 0o70; """
    #     # expect = ConstDecl("VoTien", None, IntLiteral(56))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_004(self):
    #     input = """const VoTien = 0Xa1; """
    #     # expect = ConstDecl("VoTien", None, IntLiteral(161))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_005(self):
    #     input = """const VoTien = 01.e-1; """
    #     # expect = ConstDecl("VoTien", None, FloatLiteral(0.1))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_006(self):
    #     """ đầu vào là giá trị True False chứ không phải string """
    #     input = """const VoTien = true; """
    #     # expect = ConstDecl("VoTien", None, BooleanLiteral(True))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_007(self):
    #     input = """const VoTien = false; """
    #     # expect = ConstDecl("VoTien", None, BooleanLiteral(False))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_008(self):
    #     """ loại bỏ "" ở trước và sau string """
    #     input = """const VoTien = "votien"; """
    #     # expect = ConstDecl("VoTien", None, StringLiteral("votien"))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_009(self):
    #     input = """const VoTien = nil; """
    #     # expect = ConstDecl("VoTien", None, NilLiteral())
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))
    
    # def test_010(self):
    #     input = """const VoTien = STRUCT {}; """
    #     # expect = ConstDecl("VoTien", None, StructLiteral("STRUCT",[]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_011(self):
    #     input = """const VoTien = STRUCT {
    #         a : 1,
    #         b : false}; """
    #     # expect = ConstDecl("VoTien", None, StructLiteral("STRUCT",[("a",IntLiteral(1)),("b",BooleanLiteral(False))]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_012(self):
    #     input = """const VoTien = [ID] int {1}; """
    #     # expect = ConstDecl("VoTien", None, ArrayLiteral([Id("ID")],IntType(),[IntLiteral(1)]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_013(self):
    #     input = """const VoTien = [1][2] int {1., STRUCT{}, nil}; """
    #     # expect = ConstDecl("VoTien", None, ArrayLiteral([IntLiteral(1),IntLiteral(2)],IntType(),[FloatLiteral(1.0),StructLiteral("STRUCT",[]),NilLiteral()]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_014(self):
    #     input = """const VoTien = [1][2] STRUCT {{1, {3}}, {2}}; """
    #     # expect = ConstDecl("VoTien", None, ArrayLiteral([IntLiteral(1),IntLiteral(2)],Id("STRUCT"),[[IntLiteral(1), [IntLiteral(3)]],[IntLiteral(2)]]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_015(self):
    #     input = """const VoTien = 1 || 2 || 3; """
    #     # expect = ConstDecl("VoTien", None, BinaryOp("||", BinaryOp("||", IntLiteral(1), IntLiteral(2)), IntLiteral(3)))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_016(self):
    #     input = """const VoTien = 1 && 2 && 3; """
    #     # expect = ConstDecl("VoTien", None, BinaryOp("&&", BinaryOp("&&", IntLiteral(1), IntLiteral(2)), IntLiteral(3)))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_017(self):
    #     input = """const VoTien = 1 >= 2 <= 3 > 4 < 5 == 6 != 7; """
    #     # expect = ConstDecl("VoTien", None, BinaryOp("!=", BinaryOp("==", BinaryOp("<", BinaryOp(">", BinaryOp("<=", BinaryOp(">=", IntLiteral(1), IntLiteral(2)), IntLiteral(3)), IntLiteral(4)), IntLiteral(5)), IntLiteral(6)), IntLiteral(7)))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))
    
    # def test_018(self):
    #     input = """const VoTien = 1 + 2 - 3; """
    #     # expect = ConstDecl("VoTien", None, BinaryOp("-", BinaryOp("+", IntLiteral(1), IntLiteral(2)), IntLiteral(3)))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_019(self):
    #     input = """const VoTien = 1 * 2 / 3 % 4; """
    #     # expect = ConstDecl("VoTien", None, BinaryOp("%", BinaryOp("/", BinaryOp("*", IntLiteral(1), IntLiteral(2)), IntLiteral(3)), IntLiteral(4)))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_020(self):
    #     input = """const VoTien = ! - 1; """
    #     # expect = ConstDecl("VoTien", None, UnaryOp("!",UnaryOp("-",IntLiteral(1))))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_021(self):
    #     input = """const VoTien = a; """
    #     # expect = ConstDecl("VoTien", None, Id("a"))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_022(self):
    #     input = """const VoTien = (1+2)*3; """
    #     # expect = ConstDecl("VoTien", None, BinaryOp("*", BinaryOp("+", IntLiteral(1), IntLiteral(2)), IntLiteral(3)))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_023(self):
    #     input = """const VoTien = foo(); """
    #     # expect = ConstDecl("VoTien", None, FuncCall("foo",[]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_024(self):
    #     input = """const VoTien = foo(1, 2); """
    #     # expect = ConstDecl("VoTien", None, FuncCall("foo",[IntLiteral(1),IntLiteral(2)]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_025(self):
    #     input = """const VoTien = a[2][3]; """
    #     # expect = ConstDecl("VoTien", None, ArrayCell(ArrayCell(Id("a"),[IntLiteral(2)]),[IntLiteral(3)]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_026(self):
    #     input = """const VoTien = a.b.c; """
    #     # expect = ConstDecl("VoTien", None, FieldAccess(FieldAccess(Id("a"),"b"),"c"))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_027(self):
    #     input = """const VoTien = a.b().c(1, 2); """
    #     # expect = ConstDecl("VoTien", None, MethCall(MethCall(Id("a"),"b",[]),"c",[IntLiteral(1),IntLiteral(2)]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))

    # def test_028(self):
    #     input = """const VoTien = a.b[2].c.d(); """
    #     # expect = ConstDecl("VoTien", None, MethCall(FieldAccess(ArrayCell(FieldAccess(Id("a"),"b"),[IntLiteral(2)]),"c"),"d",[]))
    #     self.assertTrue(TestParser.test(input, "successful", inspect.stack()[0].function))






    def test_001(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = 1;","successful", inspect.stack()[0].function))

    def test_002(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = true;","successful", inspect.stack()[0].function))

    def test_003(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = [5][0]string{1, \"string\"};","successful", inspect.stack()[0].function))

    def test_004(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = [1.]ID{1, 3};","Error on line 1 col 16: 1.", inspect.stack()[0].function))

    def test_005(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = Person{name: \"Alice\", age: 30};","successful", inspect.stack()[0].function))

    def test_006(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = 1 || 2 && c + 3 / 2 - -1;","successful", inspect.stack()[0].function))

    def test_007(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = 1[2] + foo()[2] + ID[2].b.b;","successful", inspect.stack()[0].function))

    def test_008(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = ca.foo(132) + b.c[2];","successful", inspect.stack()[0].function))

    def test_009(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = a.a.foo();","successful", inspect.stack()[0].function))

    def test_010(self):
        """declared variables"""
        self.assertTrue(TestParser.test("""
            var x int = foo() + 3 / 4;
            var y = "Hello" / 4;   
            var z str;
        ""","successful", inspect.stack()[0].function))

    def test_011(self):
        """declared constants"""
        self.assertTrue(TestParser.test("""
            const VoTien = a.b() + 2;
        ""","successful", inspect.stack()[0].function))

    def test_012(self):
        """declared function"""
        self.assertTrue(TestParser.test("""
            func VoTien(x int, y int) int {return;}
            func VoTien1() [2][3] ID {return;};        
            func VoTien2() {return;}                                       
        ""","successful", inspect.stack()[0].function))

    def test_013(self):
        """declared method"""
        self.assertTrue(TestParser.test("""
            func (c Calculator) VoTien(x int) int {return;};  
            func (c Calculator) VoTien() ID {return;}      
            func (c Calculator) VoTien(x int, y [2]VoTien) {return;}                                                      
        ""","successful", inspect.stack()[0].function))

    def test_014(self):
        """declared struct"""
        self.assertTrue(TestParser.test("""
            type VoTien struct {
                VoTien string ;
                VoTien [1][3]VoTien ;                     
            }                                                                     
        ""","successful", inspect.stack()[0].function))

    def test_015(self):
        """declared Interface"""
        self.assertTrue(TestParser.test("""
            type VoTien struct {}                                                                       
        ""","Error on line 2 col 32: }", inspect.stack()[0].function))

    def test_016(self):
        """declared Interface"""
        self.assertTrue(TestParser.test("""
            type Calculator interface {
                                        
                Add(x, y int) int;
                Subtract(a, b float, c int) [3]ID;
                Reset()
                                        
                SayHello(name string);
                                        
            }
            type VoTien interface {}                                                                       
        ""","Error on line 11 col 35: }", inspect.stack()[0].function))

    def test_017(self):
        """declared_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                var x int = foo() + 3 / 4;
                var y = "Hello" / 4;   
                var z str;
                                        
                const VoTien = a.b() + 2;
            }                                       
        ""","successful", inspect.stack()[0].function))


    def test_018(self):
        """assign_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                x  := foo() + 3 / 4;
                x.c[2][4] := 1 + 2;                       
            }                                       
        ""","successful", inspect.stack()[0].function))

    def test_019(self):
        """for_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                if (x > 10) {return; } 
                if (x > 10) {
                  return; 
                } else if (x == 10) {
                    var z str;
                } else {
                    var z ID;
                }
            }
        ""","successful", inspect.stack()[0].function))

    def test_020(self):
        """if_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                for i < 10 {return; }
                for i := 0; i < 10; i += 1 {return; }
                for index, value := range array {return; }
            }
        ""","successful", inspect.stack()[0].function))


    def test_021(self):
        """break and continue, return, Call  statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {                           
                for i < 10 {break;}
                break;
                continue;
                return 1;
                return
                foo(2 + x, 4 / y); m.goo();                        
             }
                                        
        ""","successful", inspect.stack()[0].function))
       
    def test_021(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const a = 0b11;                         
        ""","successful", inspect.stack()[0].function))

    def test_022(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const a = 1.;                         
        ""","successful", inspect.stack()[0].function))

    def test_023(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN 1;                         
        ""","Error on line 2 col 25: 1", inspect.stack()[0].function))
    
    def test_024(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = int{1};                         
        ""","Error on line 2 col 27: int", inspect.stack()[0].function))

    def test_025(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = [true]int{1};                         
        ""","Error on line 2 col 28: true", inspect.stack()[0].function))

    def test_026(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = []int{1};                         
        ""","Error on line 2 col 28: ]", inspect.stack()[0].function))

    def test_027(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = []int{1};                         
        ""","Error on line 2 col 28: ]", inspect.stack()[0].function))

    def test_028(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = [2]int{1;                         
        ""","Error on line 2 col 35: ;", inspect.stack()[0].function))
    
    def test_029(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = [2]int{1,3,4;                         
        ""","Error on line 2 col 39: ;", inspect.stack()[0].function))

    def test_030(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = [2]int{};                         
        ""","Error on line 2 col 34: }", inspect.stack()[0].function))

    def test_031(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = ID {};                         
        ""","successful", inspect.stack()[0].function))

    def test_032(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = ID {a: 2, b: 2 + 2 + ID {a: 1}};                         
        ""","successful", inspect.stack()[0].function))

    def test_033(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = int {};                         
        ""","Error on line 2 col 27: int", inspect.stack()[0].function))

    def test_034(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = ID + 3;                         
        ""","successful", inspect.stack()[0].function))
    
    def test_035(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = ID {a: };                         
        ""","Error on line 2 col 34: }", inspect.stack()[0].function))

    def test_036(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = 1 && 2 && 3 || 1 || 1;                         
        ""","successful", inspect.stack()[0].function))
    
    def test_037(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a >= 2 <= "string" > a[2][3] < ID{A: 2} >= [2]S{2};                         
        ""","successful", inspect.stack()[0].function))

    def test_038(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a + b - [2]int{2} + c - z;                         
        ""","successful", inspect.stack()[0].function))

    def test_039(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a * b / d % e * 2;                         
        ""","successful", inspect.stack()[0].function))

    def test_040(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a.b.a.c.e.g;                         
        ""","successful", inspect.stack()[0].function))

    def test_041(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a[2][3][a + 2];                         
        ""","successful", inspect.stack()[0].function))

    def test_042(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a[2, 3];                         
        ""","Error on line 2 col 30: ,", inspect.stack()[0].function))

    def test_043(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a[];                         
        ""","Error on line 2 col 29: ]", inspect.stack()[0].function))

    def test_044(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a.a.a[2].foo();                         
        ""","successful", inspect.stack()[0].function))

    def test_045(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a.a.a[2].foo(1);                         
        ""","successful", inspect.stack()[0].function))

    def test_046(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a.a.a[2].c[2].foo(1, a.b);                         
        ""","successful", inspect.stack()[0].function))

    def test_047(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a.a.a[2].c[2].foo(1,);                         
        ""","Error on line 2 col 47: )", inspect.stack()[0].function))

    def test_048(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = foo() + foo(2) + foo(2, 3, 4) + a;                         
        ""","successful", inspect.stack()[0].function))

    def test_049(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = (a + 23) * 3 && (1 + 1);                         
        ""","successful", inspect.stack()[0].function))

    def test_050(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = foo().a[2].goo();                         
        ""","successful", inspect.stack()[0].function))

    def test_051(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k = [2]int{1}[3][4].foo();                         
        ""","successful", inspect.stack()[0].function))

    def test_052(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k = ID {a : 2}.c[2] + 2[2] + true.foo() + (2).foo();                         
        ""","successful", inspect.stack()[0].function))

    def test_053(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k = -a + -!-!c - ---[2]int{2};                         
        ""","successful", inspect.stack()[0].function))

    def test_054(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k = foo() + foo(a{a:2}) + foo(2, 3,4);                         
        ""","successful", inspect.stack()[0].function))

    def test_055(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k =  int;                         
        ""","Error on line 2 col 23: int", inspect.stack()[0].function))

    def test_056(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k =  (1, 2);                         
        ""","Error on line 2 col 25: ,", inspect.stack()[0].function))

    def test_057(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var a VOTIEN = 2 + 3 / 4;
        ""","successful", inspect.stack()[0].function))

    def test_058(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var a [2][3]int = 2 + 3 / 4;
        ""","successful", inspect.stack()[0].function))

    def test_059(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var a [][3]int = 2 + 3 / 4;
        ""","Error on line 2 col 19: ]", inspect.stack()[0].function))

    def test_060(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var a = a.foo()[2];
        ""","successful", inspect.stack()[0].function))

    def test_061(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var a = ;
        ""","Error on line 2 col 20: ;", inspect.stack()[0].function))

    def test_062(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var a 1;
        ""","Error on line 2 col 18: 1", inspect.stack()[0].function))

    def test_063(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var c [2][3]int;
        ""","successful", inspect.stack()[0].function))

    def test_064(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var c [2][3]ID
        ""","successful", inspect.stack()[0].function))

    def test_065(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            const a;
        ""","Error on line 2 col 19: ;", inspect.stack()[0].function))

    def test_066(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            const a := 1 + foo.a[2];
        ""","Error on line 2 col 20: :=", inspect.stack()[0].function))

    def test_067(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            const a =;
        ""","Error on line 2 col 21: ;", inspect.stack()[0].function))

    def test_068(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            
            var a int; var d = 2;
                                        
            var d = 2;
                                        
            const a = 2; var d int = 3;
                                        
            
            var d = 2;""","successful", inspect.stack()[0].function))
        
    def test_069(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add(x int, y [2]int) [2]id {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_070(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add() [2]id {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_071(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add(a) [2]id {return ;}
""","Error on line 2 col 22: )", inspect.stack()[0].function))
        
    def test_072(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add(int a) int {return ;}
""","Error on line 2 col 21: int", inspect.stack()[0].function))
        
    def test_073(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add() {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_074(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add(a int, ) {}
""","Error on line 2 col 28: )", inspect.stack()[0].function))
        
    def test_075(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator struct {value int}
""","Error on line 2 col 45: }", inspect.stack()[0].function))
        
    def test_076(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator struct {value int;}
""","successful", inspect.stack()[0].function))
        
    def test_077(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator struct {
                                        
                value int;
                a [2]int; a [2]ID;
                c Calculator                    
            }
""","successful", inspect.stack()[0].function))
        
    def test_078(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator struct {
                c Calculator
                c Cal a int;         
            }
""","Error on line 4 col 22: a", inspect.stack()[0].function))
        
    def test_079(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator struct {
                a int = 2;       
            }
""","Error on line 3 col 22: =", inspect.stack()[0].function))
        
    def test_080(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {
                Add(x, y [2]ID) [2]int;
                Subtract(a, b float, c, e int);
                Reset()
                SayHello(name string)
            }
""","successful", inspect.stack()[0].function))
        
    def test_081(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {Reset()}
""","Error on line 2 col 46: }", inspect.stack()[0].function))
        
    def test_082(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {Reset()
        }
""","successful", inspect.stack()[0].function))
        
    def test_083(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {Reset();}
""","successful", inspect.stack()[0].function))
        
    def test_084(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {
                Add(x int,c,d ID); Add()
        }
""","successful", inspect.stack()[0].function))
        
    def test_085(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {
                Add(x int,c,d ID){}
        }
""","Error on line 3 col 33: {", inspect.stack()[0].function))
        
    def test_086(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {Reset();} type Person struct{value int;}
""","Error on line 2 col 49: type", inspect.stack()[0].function))
        
    def test_087(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {Reset();}; type Person struct{value int;}
""","successful", inspect.stack()[0].function))
        
    def test_088(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            func Add(x int, y int) int  {return ;};
""","successful", inspect.stack()[0].function))
        
    def test_089(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (c Calculator) Add(x int) int {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_089(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (c int) Add(x int) int {return ;}
""","Error on line 2 col 20: int", inspect.stack()[0].function))
        
    def test_090(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (c c) Add(x int) {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_091(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (c c) Add(x, c int) {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_092(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (c [2]c) Add(x int) {return ;}
""","Error on line 2 col 20: [", inspect.stack()[0].function))
        
    def test_093(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (int c) Add(x int) {return ;}
""","Error on line 2 col 18: int", inspect.stack()[0].function))
        
    def test_094(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
            func (c c) Add(x int) {return ;};
""","successful", inspect.stack()[0].function))
        
    def test_095(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
                                        
            func (c c) Add(x int) {return ;}
                                        
            func Add(x int) {return ;}; var c int;
                                        
            var c int; type Calculator struct{c int;}; type Calculator struct{c int;} var c int;
""","Error on line 7 col 86: var", inspect.stack()[0].function))
        
    def test_096(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
                                        
            var c int func (c c) Add(x int) {return ;}
""","Error on line 3 col 22: func", inspect.stack()[0].function))
        
    def test_097(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
                                        
            const a = 2 func (c c) Add(x int) {return ;}
""","Error on line 3 col 24: func", inspect.stack()[0].function))
        
    def test_098(self):
        """Declared"""
        self.assertTrue(TestParser.test("""
                                        
            const MaxSize = 100 + 50; func (c c) Add() {return ;}
""","successful", inspect.stack()[0].function))
        
    def test_099(self):
        """Declared"""
        self.assertTrue(TestParser.test("""

""","Error on line 3 col 0: <EOF>", inspect.stack()[0].function))
        
    def test_100(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
            func Add() {
                                        }
""","successful", inspect.stack()[0].function))
        
    def test_101(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                         var a int = 2;      
                                    };""","successful", inspect.stack()[0].function))

    def test_102(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                         var a int;      
                                    };""","successful", inspect.stack()[0].function))
        
    def test_103(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                         var a = a[2].b;      
                                    };""","successful", inspect.stack()[0].function))
        
    def test_104(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                         const a = a[2].b;      
                                    };""","successful", inspect.stack()[0].function))
        
    def test_105(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        const a = a[2].b
                                        var a = a[2].b; var a = "s";           
                                    };""","successful", inspect.stack()[0].function))
        
    def test_106(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        const a = a[2].b
                                        var a = a[2].b var a = "s";           
                                    };""","Error on line 4 col 55: var", inspect.stack()[0].function))

    def test_107(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a += 2;
                                        a -= a[2].b();
                                        a /= 2
                                        a *= 2
                                        a %= 2;       
                                    };""","successful", inspect.stack()[0].function))
        

    def test_108(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a[2].b := 2;       
                                    };""","successful", inspect.stack()[0].function))
        

    def test_109(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a.c[2].e[3].k += 2;       
                                    };""","successful", inspect.stack()[0].function))

    def test_110(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a.foo() += 2;       
                                    };""","Error on line 3 col 48: +=", inspect.stack()[0].function))

    def test_111(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        2 + 2 += 2;       
                                    };""","Error on line 3 col 40: 2", inspect.stack()[0].function))
        
    def test_112(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                       ID {id:2}.c += 2;       
                                    };""","Error on line 3 col 42: {", inspect.stack()[0].function))
        
    def test_113(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                       a[2+3&&2] += foo().b[2];       
                                    };""","successful", inspect.stack()[0].function))
        
    def test_114(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (x.foo().b[2]) {
                                            a := 2;
                                        } else if (a && b) {
                                            return; 
                                        } else {
                                            a := 2;
                                        }   
                                    };""","successful", inspect.stack()[0].function))
        
    def test_115(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (x.foo().b[2]) {
                                            if (){return;}
                                        } 
                                    };""","Error on line 4 col 48: )", inspect.stack()[0].function))
        
    def test_116(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (x.foo().b[2]) {
                                            if (1){return; } else {return; }

                                        } else if(2) {return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_117(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (x.foo().b[2]) {return
                                        } else if(){
                                        }
                                    };""","Error on line 4 col 50: )", inspect.stack()[0].function))
        
    def test_118(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (x.foo().b[2]) {return; 
                                        } else if(1){return; 
                                        }else if(1){return; 
                                        }else if(2){return
                                        }else {return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_119(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for true {return; }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_120(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for true + 2 + foo().b {return; }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_121(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for int {return; }
                                    };""","Error on line 3 col 44: int", inspect.stack()[0].function))
        
    def test_122(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for int {return; }
                                    };""","Error on line 3 col 44: int", inspect.stack()[0].function))
        
    def test_123(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for i := 0; i < 10; i += 1 {
                                           return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_124(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i = 0; i < 10; i += 1 {
                                           return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_125(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for const i = 0; i < 10; i += 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 44: const", inspect.stack()[0].function))
        
    def test_126(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i [2] int = 0; foo().a.b(); i[3] := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 77: [", inspect.stack()[0].function))
        
    def test_127(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i [2]int = 0; foo().a.b();  {
                                            return; 
                                        }
                                    };""","Error on line 3 col 76: {", inspect.stack()[0].function))
        
    def test_128(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i [2]int = 0; foo().a.b(); var i [2]int = 0 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 75: var", inspect.stack()[0].function))
        
    def test_129(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index, value := range arr {
                                        // index: 0, 1, 2
                                        // value: 10, 20, 30
                                        return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_130(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index[2], value := range arr {
                                        // index: 0, 1, 2
                                        // value: 10, 20, 30
                                        return; 
                                        }
                                    };""","Error on line 3 col 52: ,", inspect.stack()[0].function))
        
    def test_131(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index.ab, value := range arr {
                                        // index: 0, 1, 2
                                        // value: 10, 20, 30
                                        return; 
                                        }
                                    };""","Error on line 3 col 52: ,", inspect.stack()[0].function))
        
    def test_132(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index, value[2] := range arr {
                                        // index: 0, 1, 2
                                        return; 
                                        }
                                    };""","Error on line 3 col 56: [", inspect.stack()[0].function))
        
    def test_133(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index, value := range arr[2] {return
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_134(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index, value := range 23 {return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_135(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index, value := range 23 {
                                            for index, value := range 23 {return; }
                                        }
                                    };""","successful", inspect.stack()[0].function))
        
    def test_136(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        break;
                                        continue
                                        break; continue; break
                                    };""","successful", inspect.stack()[0].function))
        
    def test_137(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        return
                                        return 2 + a[2].b()
                                        return; return a
                                    };""","successful", inspect.stack()[0].function))
        
    def test_138(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        return return 2 + a[2].b()
                    
                                    };""","Error on line 3 col 47: return", inspect.stack()[0].function))
        
    def test_139(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        break continue
                    
                                    };""","Error on line 3 col 46: continue", inspect.stack()[0].function))
        
    def test_140(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a.foo();
                                        foo()
                                    };""","successful", inspect.stack()[0].function))
        
    def test_141(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a.foo(2 + 3, a {a:2})
                                        foo(2 + 3, a {a:2});
                                    };""","successful", inspect.stack()[0].function))
        
    def test_142(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        (1+2).foo(2 + 3, a {a:2})
                                    };""","Error on line 3 col 40: (", inspect.stack()[0].function))
        
    def test_143(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a[2][3].foo(2 + 3, a {a:2})
                                    };""","successful", inspect.stack()[0].function))
        
    def test_144(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        {break;}
                                    };""","Error on line 3 col 40: {", inspect.stack()[0].function))
        
    def test_145(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                        break;
                                    func Add() {
                                    };""","Error on line 2 col 40: break", inspect.stack()[0].function))
        
    def test_146(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        return (2 + 3).b
                                        return -1.c
                                    };""","Error on line 4 col 50: c", inspect.stack()[0].function))
        
    def test_147(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        return (2 + 3)[b]
                                        return -1.c[c]
                                    };""","Error on line 4 col 50: c", inspect.stack()[0].function))
        
    def test_148(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (1) {return struct;}
                                        else if(2) {return string;}
                                        else if(3) {reutrn int;}
                                    };""","Error on line 3 col 55: struct", inspect.stack()[0].function))
        
    def test_149(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (1) {return;}else if(2) {return string;}else if(3) {reutrn int;}
                                    };""","Error on line 3 col 75: string", inspect.stack()[0].function))
        
    def test_150(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (1) {return;}else if(2) {return string;}else if(3) {reutrn int;}else  {return struct;}
                                    };""","Error on line 3 col 75: string", inspect.stack()[0].function))
        
    def test_151(self):
        """array_literal"""
        self.assertTrue(TestParser.test("""const a = [1]int{1+1}                    
""","Error on line 1 col 18: +", inspect.stack()[0].function))
        
    def test_152(self):
        """array_literal"""
        self.assertTrue(TestParser.test("""const a = [1]int{{1, 0x1}, ID{}, {{ID{}}}}                    
""","successful", inspect.stack()[0].function))
        
    def test_153(self):
        """array_literal"""
        self.assertTrue(TestParser.test("""const a = [1]int{}                    
""","Error on line 1 col 17: }", inspect.stack()[0].function))
        
    def test_154(self):
        """array_literal"""
        self.assertTrue(TestParser.test("""const a = [1]int{[1]int{1}}                    
""","Error on line 1 col 17: [", inspect.stack()[0].function))
        
    def test_155(self):
        """array_literal"""
        self.assertTrue(TestParser.test("""const a = [1]int{{1, 0x1}, ID{}, 1.2, "s", true, false, nil} + nil                    
""","successful", inspect.stack()[0].function))
        
    def test_156(self):
        self.assertTrue(TestParser.test("""
        func Add(x, y int, b float) {return ;}           
""","successful", inspect.stack()[0].function))
        
    def test_157(self):
        self.assertTrue(TestParser.test("""
        func (c c) Add(x, y int, b float) {return ;}           
""","successful", inspect.stack()[0].function))
        
    def test_158(self):
        self.assertTrue(TestParser.test("""
        type Person struct {
            func (p Person) Greet() string {
                return "Hello, " + p.name
            }
            c c
            func (c c) Add(x, y int, b float) {return ;}  
            value int;                            
        }      
""","successful", inspect.stack()[0].function))
        
    def test_158(self):
        self.assertTrue(TestParser.test("""
        type Person struct {
            c int  c int;                                                    
        }      
""","Error on line 3 col 19: c", inspect.stack()[0].function))
        
    def test_159(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                for i := 0
                    i < 10
                    i += 1 {
                    return
                }
                for i := 0
                    i < 10
                    i += 1 
                {
                    return
                }
            };  
""","Error on line 10 col 27: ;", inspect.stack()[0].function))
        
    def test_160(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                if (1) {return;}
                else if (1)
                {}
            };  
""","Error on line 4 col 16: else", inspect.stack()[0].function))
        
    def test_161(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                if (1) {return;
                }else if (1) {}
            };  
""","successful", inspect.stack()[0].function))
        
    def test_162(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                if (1) {return;
                }else {}
            };  
""","successful", inspect.stack()[0].function))
        
    def test_163(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                if (1) {}
            };  
""","successful", inspect.stack()[0].function))
        
    def test_164(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                for i < 10 {
// loop body
}
            };  
""","successful", inspect.stack()[0].function))
        
    def test_165(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                for i := 0; i < 10; i += 1 {
// loop body
}
            };  
""","successful", inspect.stack()[0].function))
        
    def test_166(self):
        self.assertTrue(TestParser.test("""
            func (p Person) Greet() string {
                for index, value := range STRUCT{} {
// loop body                                   
};
            };  
""","successful", inspect.stack()[0].function))

    def test_167(self):
        self.assertTrue(TestParser.test("""
        const a = a.2; 
""","Error on line 2 col 20: 2", inspect.stack()[0].function))
        
    def test_168(self):
        self.assertTrue(TestParser.test("""
        const a = a.b.c().d().e[2].k()[2]; 
""","successful", inspect.stack()[0].function))
        
    def test_169(self):
        self.assertTrue(TestParser.test("""
        const a = [1]int{1, 2 
""","Error on line 2 col 30: ;", inspect.stack()[0].function))
        
    def test_170(self):
        self.assertTrue(TestParser.test("""
        const a = foo(1, 2
""","Error on line 2 col 26: ;", inspect.stack()[0].function))

    def test_171(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i [2] int = 0; foo().a.b(); i.b := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 77: .", inspect.stack()[0].function))
        
    def test_172(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i [2] int = 0; foo().a.b(); i[2].c += 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 77: [", inspect.stack()[0].function))

    def test_173(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for i[2] := 1; foo().a.b(); i := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 49: :=", inspect.stack()[0].function))
        
    def test_174(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for i.c[2] := 1; foo().a.b(); i := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 51: :=", inspect.stack()[0].function))
        
    def test_175(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for i.c[2] := 1; foo().a.b(); i := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 51: :=", inspect.stack()[0].function))
        
    def test_176(self):
        self.assertTrue(TestParser.test("""
        type Person struct {
            func (p Person) Greet() string {
                return "Hello, " + p.name
            };                                                 
        }      
""","Error on line 3 col 12: func", inspect.stack()[0].function))
        
    def test_177(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var b; foo().a.b(); i := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 49: ;", inspect.stack()[0].function))

    def test_178(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var b int; foo().a.b(); i := 1 {
                                            return; 
                                        }
                                    };""","Error on line 3 col 53: ;", inspect.stack()[0].function))

    def test_179(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var b [2]ID = 1 + 2 / 4; foo().a.b(); i := 1 {
                                            return; 
                                        }
                                    };""","successful", inspect.stack()[0].function))

    def test_180(self):
        self.assertTrue(TestParser.test("""
                                            const a = [ID][2][VT]int{{{1}}, ID, a, {b}}                              
                                        ""","successful", inspect.stack()[0].function))

    def test_181(self):
        self.assertTrue(TestParser.test("""
                                            var a;
                                        ""","Error on line 2 col 49: ;", inspect.stack()[0].function))
    def test_182(self):
        self.assertTrue(TestParser.test("""
                                            var a = {1, 2};
                                        ""","Error on line 2 col 52: {", inspect.stack()[0].function))
                                                                                          
    def test_183(self):
        self.assertTrue(TestParser.test("""
                                            var a = {1, 2};
                                        ""","Error on line 2 col 52: {", inspect.stack()[0].function))
                                                                                          
    def test_184(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        {
                                            return;
                                        }
                                    };""","Error on line 3 col 40: {", inspect.stack()[0].function))

    def test_185(self):
        self.assertTrue(TestParser.test("""
                                            const a = [ID][2][VT]int{a, b, {c}}                              
                                        ""","successful", inspect.stack()[0].function))
        
    def test_186(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                            return;
                                    };""","successful", inspect.stack()[0].function))
        







        