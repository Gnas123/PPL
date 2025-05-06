# Generated from main/MiniGo.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from lexererr import *



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2@")
        buf.write("\u01ea\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\3\2\3\2\3\2\3\3\3\3\3\3\3\3")
        buf.write("\3\3\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b")
        buf.write("\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\n\3")
        buf.write("\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\f\3\f\3\f")
        buf.write("\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21")
        buf.write("\3\21\3\22\3\22\3\22\3\22\3\22\3\22\3\23\3\23\3\23\3\23")
        buf.write("\3\24\3\24\3\24\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\25")
        buf.write("\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\33")
        buf.write("\3\33\3\33\3\34\3\34\3\34\3\35\3\35\3\36\3\36\3\36\3\37")
        buf.write("\3\37\3 \3 \3 \3!\3!\3!\3\"\3\"\3\"\3#\3#\3$\3$\3%\3%")
        buf.write("\3%\3&\3&\3&\3\'\3\'\3\'\3(\3(\3(\3)\3)\3)\3*\3*\3*\3")
        buf.write("+\3+\3,\3,\3-\3-\3.\3.\3/\3/\3\60\3\60\3\61\3\61\3\62")
        buf.write("\3\62\3\63\3\63\3\64\3\64\3\65\3\65\7\65\u0151\n\65\f")
        buf.write("\65\16\65\u0154\13\65\3\66\3\66\3\66\3\66\5\66\u015a\n")
        buf.write("\66\3\67\3\67\3\67\7\67\u015f\n\67\f\67\16\67\u0162\13")
        buf.write("\67\5\67\u0164\n\67\38\38\38\68\u0169\n8\r8\168\u016a")
        buf.write("\39\39\39\69\u0170\n9\r9\169\u0171\3:\3:\3:\6:\u0177\n")
        buf.write(":\r:\16:\u0178\3;\6;\u017c\n;\r;\16;\u017d\3;\5;\u0181")
        buf.write("\n;\3;\3;\7;\u0185\n;\f;\16;\u0188\13;\3;\5;\u018b\n;")
        buf.write("\3<\3<\5<\u018f\n<\3<\6<\u0192\n<\r<\16<\u0193\3=\3=\7")
        buf.write("=\u0198\n=\f=\16=\u019b\13=\3=\3=\3>\3>\5>\u01a1\n>\3")
        buf.write("?\3?\3?\3@\3@\3@\3A\5A\u01aa\nA\3A\3A\3A\3B\3B\3B\3B\3")
        buf.write("B\7B\u01b4\nB\fB\16B\u01b7\13B\3B\3B\3B\3B\3B\3C\3C\3")
        buf.write("C\3C\7C\u01c2\nC\fC\16C\u01c5\13C\3C\3C\3D\6D\u01ca\n")
        buf.write("D\rD\16D\u01cb\3D\3D\3E\3E\3E\3F\3F\7F\u01d5\nF\fF\16")
        buf.write("F\u01d8\13F\3F\3F\3F\5F\u01dd\nF\3F\3F\3G\3G\7G\u01e3")
        buf.write("\nG\fG\16G\u01e6\13G\3G\3G\3G\3\u01b5\2H\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65")
        buf.write("\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60")
        buf.write("_\61a\62c\63e\64g\65i\66k\67m\2o\2q\2s\2u8w\2y9{\2}\2")
        buf.write("\177\2\u0081:\u0083;\u0085<\u0087=\u0089>\u008b?\u008d")
        buf.write("@\3\2\23\5\2C\\aac|\6\2\62;C\\aac|\3\2\63;\3\2\62;\4\2")
        buf.write("DDdd\3\2\62\63\4\2QQqq\3\2\629\4\2ZZzz\5\2\62;CHch\4\2")
        buf.write("GGgg\4\2--//\5\2\f\f$$^^\7\2$$^^ppttvv\3\2\f\f\5\2\n\13")
        buf.write("\16\17\"\"\3\3\f\f\2\u01fa\2\3\3\2\2\2\2\5\3\2\2\2\2\7")
        buf.write("\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2")
        buf.write("\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2")
        buf.write("\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2")
        buf.write("\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2")
        buf.write("\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63")
        buf.write("\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2")
        buf.write("\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2")
        buf.write("\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3")
        buf.write("\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y")
        buf.write("\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2")
        buf.write("c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2")
        buf.write("\2u\3\2\2\2\2y\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2\2")
        buf.write("\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2\u008b")
        buf.write("\3\2\2\2\2\u008d\3\2\2\2\3\u008f\3\2\2\2\5\u0092\3\2\2")
        buf.write("\2\7\u0097\3\2\2\2\t\u009b\3\2\2\2\13\u00a2\3\2\2\2\r")
        buf.write("\u00a7\3\2\2\2\17\u00ac\3\2\2\2\21\u00b3\3\2\2\2\23\u00bd")
        buf.write("\3\2\2\2\25\u00c4\3\2\2\2\27\u00c8\3\2\2\2\31\u00ce\3")
        buf.write("\2\2\2\33\u00d6\3\2\2\2\35\u00dc\3\2\2\2\37\u00e0\3\2")
        buf.write("\2\2!\u00e9\3\2\2\2#\u00ef\3\2\2\2%\u00f5\3\2\2\2\'\u00f9")
        buf.write("\3\2\2\2)\u00fe\3\2\2\2+\u0104\3\2\2\2-\u0106\3\2\2\2")
        buf.write("/\u0108\3\2\2\2\61\u010a\3\2\2\2\63\u010c\3\2\2\2\65\u010e")
        buf.write("\3\2\2\2\67\u0111\3\2\2\29\u0114\3\2\2\2;\u0116\3\2\2")
        buf.write("\2=\u0119\3\2\2\2?\u011b\3\2\2\2A\u011e\3\2\2\2C\u0121")
        buf.write("\3\2\2\2E\u0124\3\2\2\2G\u0126\3\2\2\2I\u0128\3\2\2\2")
        buf.write("K\u012b\3\2\2\2M\u012e\3\2\2\2O\u0131\3\2\2\2Q\u0134\3")
        buf.write("\2\2\2S\u0137\3\2\2\2U\u013a\3\2\2\2W\u013c\3\2\2\2Y\u013e")
        buf.write("\3\2\2\2[\u0140\3\2\2\2]\u0142\3\2\2\2_\u0144\3\2\2\2")
        buf.write("a\u0146\3\2\2\2c\u0148\3\2\2\2e\u014a\3\2\2\2g\u014c\3")
        buf.write("\2\2\2i\u014e\3\2\2\2k\u0159\3\2\2\2m\u0163\3\2\2\2o\u0165")
        buf.write("\3\2\2\2q\u016c\3\2\2\2s\u0173\3\2\2\2u\u017b\3\2\2\2")
        buf.write("w\u018c\3\2\2\2y\u0195\3\2\2\2{\u01a0\3\2\2\2}\u01a2\3")
        buf.write("\2\2\2\177\u01a5\3\2\2\2\u0081\u01a9\3\2\2\2\u0083\u01ae")
        buf.write("\3\2\2\2\u0085\u01bd\3\2\2\2\u0087\u01c9\3\2\2\2\u0089")
        buf.write("\u01cf\3\2\2\2\u008b\u01d2\3\2\2\2\u008d\u01e0\3\2\2\2")
        buf.write("\u008f\u0090\7k\2\2\u0090\u0091\7h\2\2\u0091\4\3\2\2\2")
        buf.write("\u0092\u0093\7g\2\2\u0093\u0094\7n\2\2\u0094\u0095\7u")
        buf.write("\2\2\u0095\u0096\7g\2\2\u0096\6\3\2\2\2\u0097\u0098\7")
        buf.write("h\2\2\u0098\u0099\7q\2\2\u0099\u009a\7t\2\2\u009a\b\3")
        buf.write("\2\2\2\u009b\u009c\7t\2\2\u009c\u009d\7g\2\2\u009d\u009e")
        buf.write("\7v\2\2\u009e\u009f\7w\2\2\u009f\u00a0\7t\2\2\u00a0\u00a1")
        buf.write("\7p\2\2\u00a1\n\3\2\2\2\u00a2\u00a3\7h\2\2\u00a3\u00a4")
        buf.write("\7w\2\2\u00a4\u00a5\7p\2\2\u00a5\u00a6\7e\2\2\u00a6\f")
        buf.write("\3\2\2\2\u00a7\u00a8\7v\2\2\u00a8\u00a9\7{\2\2\u00a9\u00aa")
        buf.write("\7r\2\2\u00aa\u00ab\7g\2\2\u00ab\16\3\2\2\2\u00ac\u00ad")
        buf.write("\7u\2\2\u00ad\u00ae\7v\2\2\u00ae\u00af\7t\2\2\u00af\u00b0")
        buf.write("\7w\2\2\u00b0\u00b1\7e\2\2\u00b1\u00b2\7v\2\2\u00b2\20")
        buf.write("\3\2\2\2\u00b3\u00b4\7k\2\2\u00b4\u00b5\7p\2\2\u00b5\u00b6")
        buf.write("\7v\2\2\u00b6\u00b7\7g\2\2\u00b7\u00b8\7t\2\2\u00b8\u00b9")
        buf.write("\7h\2\2\u00b9\u00ba\7c\2\2\u00ba\u00bb\7e\2\2\u00bb\u00bc")
        buf.write("\7g\2\2\u00bc\22\3\2\2\2\u00bd\u00be\7u\2\2\u00be\u00bf")
        buf.write("\7v\2\2\u00bf\u00c0\7t\2\2\u00c0\u00c1\7k\2\2\u00c1\u00c2")
        buf.write("\7p\2\2\u00c2\u00c3\7i\2\2\u00c3\24\3\2\2\2\u00c4\u00c5")
        buf.write("\7k\2\2\u00c5\u00c6\7p\2\2\u00c6\u00c7\7v\2\2\u00c7\26")
        buf.write("\3\2\2\2\u00c8\u00c9\7h\2\2\u00c9\u00ca\7n\2\2\u00ca\u00cb")
        buf.write("\7q\2\2\u00cb\u00cc\7c\2\2\u00cc\u00cd\7v\2\2\u00cd\30")
        buf.write("\3\2\2\2\u00ce\u00cf\7d\2\2\u00cf\u00d0\7q\2\2\u00d0\u00d1")
        buf.write("\7q\2\2\u00d1\u00d2\7n\2\2\u00d2\u00d3\7g\2\2\u00d3\u00d4")
        buf.write("\7c\2\2\u00d4\u00d5\7p\2\2\u00d5\32\3\2\2\2\u00d6\u00d7")
        buf.write("\7e\2\2\u00d7\u00d8\7q\2\2\u00d8\u00d9\7p\2\2\u00d9\u00da")
        buf.write("\7u\2\2\u00da\u00db\7v\2\2\u00db\34\3\2\2\2\u00dc\u00dd")
        buf.write("\7x\2\2\u00dd\u00de\7c\2\2\u00de\u00df\7t\2\2\u00df\36")
        buf.write("\3\2\2\2\u00e0\u00e1\7e\2\2\u00e1\u00e2\7q\2\2\u00e2\u00e3")
        buf.write("\7p\2\2\u00e3\u00e4\7v\2\2\u00e4\u00e5\7k\2\2\u00e5\u00e6")
        buf.write("\7p\2\2\u00e6\u00e7\7w\2\2\u00e7\u00e8\7g\2\2\u00e8 \3")
        buf.write("\2\2\2\u00e9\u00ea\7d\2\2\u00ea\u00eb\7t\2\2\u00eb\u00ec")
        buf.write("\7g\2\2\u00ec\u00ed\7c\2\2\u00ed\u00ee\7m\2\2\u00ee\"")
        buf.write("\3\2\2\2\u00ef\u00f0\7t\2\2\u00f0\u00f1\7c\2\2\u00f1\u00f2")
        buf.write("\7p\2\2\u00f2\u00f3\7i\2\2\u00f3\u00f4\7g\2\2\u00f4$\3")
        buf.write("\2\2\2\u00f5\u00f6\7p\2\2\u00f6\u00f7\7k\2\2\u00f7\u00f8")
        buf.write("\7n\2\2\u00f8&\3\2\2\2\u00f9\u00fa\7v\2\2\u00fa\u00fb")
        buf.write("\7t\2\2\u00fb\u00fc\7w\2\2\u00fc\u00fd\7g\2\2\u00fd(\3")
        buf.write("\2\2\2\u00fe\u00ff\7h\2\2\u00ff\u0100\7c\2\2\u0100\u0101")
        buf.write("\7n\2\2\u0101\u0102\7u\2\2\u0102\u0103\7g\2\2\u0103*\3")
        buf.write("\2\2\2\u0104\u0105\7-\2\2\u0105,\3\2\2\2\u0106\u0107\7")
        buf.write("/\2\2\u0107.\3\2\2\2\u0108\u0109\7,\2\2\u0109\60\3\2\2")
        buf.write("\2\u010a\u010b\7\61\2\2\u010b\62\3\2\2\2\u010c\u010d\7")
        buf.write("\'\2\2\u010d\64\3\2\2\2\u010e\u010f\7?\2\2\u010f\u0110")
        buf.write("\7?\2\2\u0110\66\3\2\2\2\u0111\u0112\7#\2\2\u0112\u0113")
        buf.write("\7?\2\2\u01138\3\2\2\2\u0114\u0115\7>\2\2\u0115:\3\2\2")
        buf.write("\2\u0116\u0117\7>\2\2\u0117\u0118\7?\2\2\u0118<\3\2\2")
        buf.write("\2\u0119\u011a\7@\2\2\u011a>\3\2\2\2\u011b\u011c\7@\2")
        buf.write("\2\u011c\u011d\7?\2\2\u011d@\3\2\2\2\u011e\u011f\7(\2")
        buf.write("\2\u011f\u0120\7(\2\2\u0120B\3\2\2\2\u0121\u0122\7~\2")
        buf.write("\2\u0122\u0123\7~\2\2\u0123D\3\2\2\2\u0124\u0125\7#\2")
        buf.write("\2\u0125F\3\2\2\2\u0126\u0127\7?\2\2\u0127H\3\2\2\2\u0128")
        buf.write("\u0129\7-\2\2\u0129\u012a\7?\2\2\u012aJ\3\2\2\2\u012b")
        buf.write("\u012c\7/\2\2\u012c\u012d\7?\2\2\u012dL\3\2\2\2\u012e")
        buf.write("\u012f\7,\2\2\u012f\u0130\7?\2\2\u0130N\3\2\2\2\u0131")
        buf.write("\u0132\7\61\2\2\u0132\u0133\7?\2\2\u0133P\3\2\2\2\u0134")
        buf.write("\u0135\7\'\2\2\u0135\u0136\7?\2\2\u0136R\3\2\2\2\u0137")
        buf.write("\u0138\7<\2\2\u0138\u0139\7?\2\2\u0139T\3\2\2\2\u013a")
        buf.write("\u013b\7*\2\2\u013bV\3\2\2\2\u013c\u013d\7+\2\2\u013d")
        buf.write("X\3\2\2\2\u013e\u013f\7}\2\2\u013fZ\3\2\2\2\u0140\u0141")
        buf.write("\7\177\2\2\u0141\\\3\2\2\2\u0142\u0143\7]\2\2\u0143^\3")
        buf.write("\2\2\2\u0144\u0145\7_\2\2\u0145`\3\2\2\2\u0146\u0147\7")
        buf.write("\60\2\2\u0147b\3\2\2\2\u0148\u0149\7.\2\2\u0149d\3\2\2")
        buf.write("\2\u014a\u014b\7<\2\2\u014bf\3\2\2\2\u014c\u014d\7=\2")
        buf.write("\2\u014dh\3\2\2\2\u014e\u0152\t\2\2\2\u014f\u0151\t\3")
        buf.write("\2\2\u0150\u014f\3\2\2\2\u0151\u0154\3\2\2\2\u0152\u0150")
        buf.write("\3\2\2\2\u0152\u0153\3\2\2\2\u0153j\3\2\2\2\u0154\u0152")
        buf.write("\3\2\2\2\u0155\u015a\5m\67\2\u0156\u015a\5o8\2\u0157\u015a")
        buf.write("\5q9\2\u0158\u015a\5s:\2\u0159\u0155\3\2\2\2\u0159\u0156")
        buf.write("\3\2\2\2\u0159\u0157\3\2\2\2\u0159\u0158\3\2\2\2\u015a")
        buf.write("l\3\2\2\2\u015b\u0164\7\62\2\2\u015c\u0160\t\4\2\2\u015d")
        buf.write("\u015f\t\5\2\2\u015e\u015d\3\2\2\2\u015f\u0162\3\2\2\2")
        buf.write("\u0160\u015e\3\2\2\2\u0160\u0161\3\2\2\2\u0161\u0164\3")
        buf.write("\2\2\2\u0162\u0160\3\2\2\2\u0163\u015b\3\2\2\2\u0163\u015c")
        buf.write("\3\2\2\2\u0164n\3\2\2\2\u0165\u0166\7\62\2\2\u0166\u0168")
        buf.write("\t\6\2\2\u0167\u0169\t\7\2\2\u0168\u0167\3\2\2\2\u0169")
        buf.write("\u016a\3\2\2\2\u016a\u0168\3\2\2\2\u016a\u016b\3\2\2\2")
        buf.write("\u016bp\3\2\2\2\u016c\u016d\7\62\2\2\u016d\u016f\t\b\2")
        buf.write("\2\u016e\u0170\t\t\2\2\u016f\u016e\3\2\2\2\u0170\u0171")
        buf.write("\3\2\2\2\u0171\u016f\3\2\2\2\u0171\u0172\3\2\2\2\u0172")
        buf.write("r\3\2\2\2\u0173\u0174\7\62\2\2\u0174\u0176\t\n\2\2\u0175")
        buf.write("\u0177\t\13\2\2\u0176\u0175\3\2\2\2\u0177\u0178\3\2\2")
        buf.write("\2\u0178\u0176\3\2\2\2\u0178\u0179\3\2\2\2\u0179t\3\2")
        buf.write("\2\2\u017a\u017c\t\5\2\2\u017b\u017a\3\2\2\2\u017c\u017d")
        buf.write("\3\2\2\2\u017d\u017b\3\2\2\2\u017d\u017e\3\2\2\2\u017e")
        buf.write("\u0180\3\2\2\2\u017f\u0181\5w<\2\u0180\u017f\3\2\2\2\u0180")
        buf.write("\u0181\3\2\2\2\u0181\u0182\3\2\2\2\u0182\u0186\7\60\2")
        buf.write("\2\u0183\u0185\t\5\2\2\u0184\u0183\3\2\2\2\u0185\u0188")
        buf.write("\3\2\2\2\u0186\u0184\3\2\2\2\u0186\u0187\3\2\2\2\u0187")
        buf.write("\u018a\3\2\2\2\u0188\u0186\3\2\2\2\u0189\u018b\5w<\2\u018a")
        buf.write("\u0189\3\2\2\2\u018a\u018b\3\2\2\2\u018bv\3\2\2\2\u018c")
        buf.write("\u018e\t\f\2\2\u018d\u018f\t\r\2\2\u018e\u018d\3\2\2\2")
        buf.write("\u018e\u018f\3\2\2\2\u018f\u0191\3\2\2\2\u0190\u0192\t")
        buf.write("\5\2\2\u0191\u0190\3\2\2\2\u0192\u0193\3\2\2\2\u0193\u0191")
        buf.write("\3\2\2\2\u0193\u0194\3\2\2\2\u0194x\3\2\2\2\u0195\u0199")
        buf.write("\7$\2\2\u0196\u0198\5{>\2\u0197\u0196\3\2\2\2\u0198\u019b")
        buf.write("\3\2\2\2\u0199\u0197\3\2\2\2\u0199\u019a\3\2\2\2\u019a")
        buf.write("\u019c\3\2\2\2\u019b\u0199\3\2\2\2\u019c\u019d\7$\2\2")
        buf.write("\u019dz\3\2\2\2\u019e\u01a1\n\16\2\2\u019f\u01a1\5}?\2")
        buf.write("\u01a0\u019e\3\2\2\2\u01a0\u019f\3\2\2\2\u01a1|\3\2\2")
        buf.write("\2\u01a2\u01a3\7^\2\2\u01a3\u01a4\t\17\2\2\u01a4~\3\2")
        buf.write("\2\2\u01a5\u01a6\7^\2\2\u01a6\u01a7\n\17\2\2\u01a7\u0080")
        buf.write("\3\2\2\2\u01a8\u01aa\7\17\2\2\u01a9\u01a8\3\2\2\2\u01a9")
        buf.write("\u01aa\3\2\2\2\u01aa\u01ab\3\2\2\2\u01ab\u01ac\7\f\2\2")
        buf.write("\u01ac\u01ad\bA\2\2\u01ad\u0082\3\2\2\2\u01ae\u01af\7")
        buf.write("\61\2\2\u01af\u01b0\7,\2\2\u01b0\u01b5\3\2\2\2\u01b1\u01b4")
        buf.write("\5\u0083B\2\u01b2\u01b4\13\2\2\2\u01b3\u01b1\3\2\2\2\u01b3")
        buf.write("\u01b2\3\2\2\2\u01b4\u01b7\3\2\2\2\u01b5\u01b6\3\2\2\2")
        buf.write("\u01b5\u01b3\3\2\2\2\u01b6\u01b8\3\2\2\2\u01b7\u01b5\3")
        buf.write("\2\2\2\u01b8\u01b9\7,\2\2\u01b9\u01ba\7\61\2\2\u01ba\u01bb")
        buf.write("\3\2\2\2\u01bb\u01bc\bB\3\2\u01bc\u0084\3\2\2\2\u01bd")
        buf.write("\u01be\7\61\2\2\u01be\u01bf\7\61\2\2\u01bf\u01c3\3\2\2")
        buf.write("\2\u01c0\u01c2\n\20\2\2\u01c1\u01c0\3\2\2\2\u01c2\u01c5")
        buf.write("\3\2\2\2\u01c3\u01c1\3\2\2\2\u01c3\u01c4\3\2\2\2\u01c4")
        buf.write("\u01c6\3\2\2\2\u01c5\u01c3\3\2\2\2\u01c6\u01c7\bC\3\2")
        buf.write("\u01c7\u0086\3\2\2\2\u01c8\u01ca\t\21\2\2\u01c9\u01c8")
        buf.write("\3\2\2\2\u01ca\u01cb\3\2\2\2\u01cb\u01c9\3\2\2\2\u01cb")
        buf.write("\u01cc\3\2\2\2\u01cc\u01cd\3\2\2\2\u01cd\u01ce\bD\3\2")
        buf.write("\u01ce\u0088\3\2\2\2\u01cf\u01d0\13\2\2\2\u01d0\u01d1")
        buf.write("\bE\4\2\u01d1\u008a\3\2\2\2\u01d2\u01d6\7$\2\2\u01d3\u01d5")
        buf.write("\5{>\2\u01d4\u01d3\3\2\2\2\u01d5\u01d8\3\2\2\2\u01d6\u01d4")
        buf.write("\3\2\2\2\u01d6\u01d7\3\2\2\2\u01d7\u01dc\3\2\2\2\u01d8")
        buf.write("\u01d6\3\2\2\2\u01d9\u01da\7\17\2\2\u01da\u01dd\7\f\2")
        buf.write("\2\u01db\u01dd\t\22\2\2\u01dc\u01d9\3\2\2\2\u01dc\u01db")
        buf.write("\3\2\2\2\u01dd\u01de\3\2\2\2\u01de\u01df\bF\5\2\u01df")
        buf.write("\u008c\3\2\2\2\u01e0\u01e4\7$\2\2\u01e1\u01e3\5{>\2\u01e2")
        buf.write("\u01e1\3\2\2\2\u01e3\u01e6\3\2\2\2\u01e4\u01e2\3\2\2\2")
        buf.write("\u01e4\u01e5\3\2\2\2\u01e5\u01e7\3\2\2\2\u01e6\u01e4\3")
        buf.write("\2\2\2\u01e7\u01e8\5\177@\2\u01e8\u01e9\bG\6\2\u01e9\u008e")
        buf.write("\3\2\2\2\32\2\u0152\u0159\u0160\u0163\u016a\u0171\u0178")
        buf.write("\u017d\u0180\u0186\u018a\u018e\u0193\u0199\u01a0\u01a9")
        buf.write("\u01b3\u01b5\u01c3\u01cb\u01d6\u01dc\u01e4\7\3A\2\b\2")
        buf.write("\2\3E\3\3F\4\3G\5")
        return buf.getvalue()


class MiniGoLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    IF = 1
    ELSE = 2
    FOR = 3
    RETURN = 4
    FUNC = 5
    TYPE = 6
    STRUCT = 7
    INTERFACE = 8
    STRING = 9
    INT = 10
    FLOAT = 11
    BOOLEAN = 12
    CONST = 13
    VAR = 14
    CONTINUE = 15
    BREAK = 16
    RANGE = 17
    NIL = 18
    TRUE = 19
    FALSE = 20
    ADD = 21
    SUB = 22
    MUL = 23
    DIV = 24
    DIVDIV = 25
    EQUALEQUAL = 26
    NOEQUAL = 27
    L = 28
    LEQUAL = 29
    R = 30
    REQUAL = 31
    ANDAND = 32
    OR = 33
    NOSIG = 34
    ASSIGN = 35
    ADDEQUAL = 36
    SUBEQUAL = 37
    MULEQUAL = 38
    DIVEQUAL = 39
    DIVDIVEQUAL = 40
    COLONEQUAL = 41
    LP = 42
    RP = 43
    LB = 44
    RB = 45
    LSB = 46
    RSB = 47
    DOT = 48
    COMMA = 49
    COLON = 50
    SEMICOLON = 51
    ID = 52
    INT_LIT = 53
    FLOAT_LIT = 54
    STRING_LIT = 55
    NEWLINE = 56
    COMMENT = 57
    LINE_COMMENT = 58
    WS = 59
    ERROR_CHAR = 60
    UNCLOSE_STRING = 61
    ILLEGAL_ESCAPE = 62

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'if'", "'else'", "'for'", "'return'", "'func'", "'type'", "'struct'", 
            "'interface'", "'string'", "'int'", "'float'", "'boolean'", 
            "'const'", "'var'", "'continue'", "'break'", "'range'", "'nil'", 
            "'true'", "'false'", "'+'", "'-'", "'*'", "'/'", "'%'", "'=='", 
            "'!='", "'<'", "'<='", "'>'", "'>='", "'&&'", "'||'", "'!'", 
            "'='", "'+='", "'-='", "'*='", "'/='", "'%='", "':='", "'('", 
            "')'", "'{'", "'}'", "'['", "']'", "'.'", "','", "':'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "IF", "ELSE", "FOR", "RETURN", "FUNC", "TYPE", "STRUCT", "INTERFACE", 
            "STRING", "INT", "FLOAT", "BOOLEAN", "CONST", "VAR", "CONTINUE", 
            "BREAK", "RANGE", "NIL", "TRUE", "FALSE", "ADD", "SUB", "MUL", 
            "DIV", "DIVDIV", "EQUALEQUAL", "NOEQUAL", "L", "LEQUAL", "R", 
            "REQUAL", "ANDAND", "OR", "NOSIG", "ASSIGN", "ADDEQUAL", "SUBEQUAL", 
            "MULEQUAL", "DIVEQUAL", "DIVDIVEQUAL", "COLONEQUAL", "LP", "RP", 
            "LB", "RB", "LSB", "RSB", "DOT", "COMMA", "COLON", "SEMICOLON", 
            "ID", "INT_LIT", "FLOAT_LIT", "STRING_LIT", "NEWLINE", "COMMENT", 
            "LINE_COMMENT", "WS", "ERROR_CHAR", "UNCLOSE_STRING", "ILLEGAL_ESCAPE" ]

    ruleNames = [ "IF", "ELSE", "FOR", "RETURN", "FUNC", "TYPE", "STRUCT", 
                  "INTERFACE", "STRING", "INT", "FLOAT", "BOOLEAN", "CONST", 
                  "VAR", "CONTINUE", "BREAK", "RANGE", "NIL", "TRUE", "FALSE", 
                  "ADD", "SUB", "MUL", "DIV", "DIVDIV", "EQUALEQUAL", "NOEQUAL", 
                  "L", "LEQUAL", "R", "REQUAL", "ANDAND", "OR", "NOSIG", 
                  "ASSIGN", "ADDEQUAL", "SUBEQUAL", "MULEQUAL", "DIVEQUAL", 
                  "DIVDIVEQUAL", "COLONEQUAL", "LP", "RP", "LB", "RB", "LSB", 
                  "RSB", "DOT", "COMMA", "COLON", "SEMICOLON", "ID", "INT_LIT", 
                  "DEC_INT", "BIN_INT", "OCT_INT", "HEX_INT", "FLOAT_LIT", 
                  "E_PART1", "STRING_LIT", "STR_CHAR", "ESC_SEQ", "ESC_ILLEGAL", 
                  "NEWLINE", "COMMENT", "LINE_COMMENT", "WS", "ERROR_CHAR", 
                  "UNCLOSE_STRING", "ILLEGAL_ESCAPE" ]

    grammarFileName = "MiniGo.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
        self.preType = None

    def emit(self):
        tk = self.type
        self.preType = tk;
        if tk == self.UNCLOSE_STRING:       
            result = super().emit();
            raise UncloseString(result.text);
        elif tk == self.ILLEGAL_ESCAPE:
            result = super().emit();
            raise IllegalEscape(result.text);
        elif tk == self.ERROR_CHAR:
            result = super().emit();
            raise ErrorToken(result.text); 
        else:
            return super().emit();


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[63] = self.NEWLINE_action 
            actions[67] = self.ERROR_CHAR_action 
            actions[68] = self.UNCLOSE_STRING_action 
            actions[69] = self.ILLEGAL_ESCAPE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            	change_list=[
            		self.ID,
            		self.INT_LIT,
            		self.FLOAT_LIT,
            		self.TRUE,
            		self.FALSE,
            		self.STRING_LIT,

            		self.INT,
            		self.FLOAT,
            		self.BOOLEAN,
            		self.STRING,

            		self.RETURN,
            		self.CONTINUE,
            		self.BREAK,

            		self.RP,
            		self.RB,
            		self.RSB,

            		self.NIL
            	]
            	if (self.preType in change_list) :
            		self.text=';'
            		self.type=self.SEMICOLON
            	else:
            		self.skip()	

     

    def ERROR_CHAR_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            raise ErrorToken(self.text)
     

    def UNCLOSE_STRING_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:

                if(len(self.text) >= 2 and self.text[-1] == '\n' and self.text[-2] == '\r'):
                    raise UncloseString(self.text[0:-2])
                elif (self.text[-1] == '\n'):
                    raise UncloseString(self.text[0:-1])
                else:
                    raise UncloseString(self.text)

     

    def ILLEGAL_ESCAPE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:

                raise IllegalEscape(self.text)

     


