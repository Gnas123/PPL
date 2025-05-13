"""
 * Initial code for Assignment
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/profile.php?id=100056605580171
 * Link Group : https://www.facebook.com/groups/211867931379013
 * Date: 02.04.2024
"""
import unittest
from TestUtils import TestCodeGen
import inspect
from AST import *




"""
    (
    cd java_byte_code/test_000 

    && 

    java  -jar ../jasmin.jar MiniGoClass.j 

    && 

    java -cp ../_io:. MiniGoClass
    )
    
    java -cp ../_io;. MiniGoClass)
"""
class CodeGenSuite(unittest.TestCase):


    def test_001(self):
        input = """
func foo(a int, c int) {
    var b = a + c;
    putInt(b)
}
func main() {
    foo(2, 3)
}
func foo1() int {return 1;}
        """
        self.assertTrue(TestCodeGen.test(input, "5", inspect.stack()[0].function))  

    def test_176(self):
        input = """
type Student struct {
    name string;
    score int;
}

func sortStudents(students [3]Student, n int) {
    for i := 0; i < n - 1; i += 1 {
        for j := 0; j < n - i - 1; j += 1 {
            if (students[j].score > students[j + 1].score) {
                var temp Student = students[j];
                students[j] := students[j + 1];
                students[j + 1] := temp;
            }
        }
    }
}

func main(){
    var students = [3] Student {Student{name: "John", score: 85}, Student{name: "Alice", score: 92}, Student{name: "Bob", score: 78}};
    sortStudents(students, 3);
    for i := 0; i < 3; i += 1 {
        putString(students[i].name + " ");
        putInt(students[i].score);
        putLn();
    }
}
        """
        output = """
Bob 78
John 85
Alice 92

"""
        self.assertTrue(TestCodeGen.test(input, output, inspect.stack()[0].function))


    def test_181(self):
        input = """
func foo(){
    a := 5;
    putInt(a)
}

var a int = 10
        
func main(){
    foo()
    putInt(a)
}
        """
        self.assertTrue(TestCodeGen.test(input, "510", inspect.stack()[0].function))        