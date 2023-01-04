from grammar import Grammar
from lexer.lexer_ast import EpsilonNode, PlusNode, QuestionNode ,SymbolNode ,ConcatNode, ClosureNode, UnionNode, IntervalNode



REGEX_GRAMMAR = Grammar()

Exp = REGEX_GRAMMAR.NonTerminal('Exp',True)
Term,Term_2,Factor,Factor_2,Atom,Atom_2,CharClass,CharClass_2 = REGEX_GRAMMAR.NonTerminals('Term Term_2 Factor Factor_2 Atom Atom_2 CharClass CharClass_2')
CharClassItem,CharClassItem_2,Char_2,Char,CharCount = REGEX_GRAMMAR.NonTerminals('CharClassItem CharClassItem_2 Char_2 Char CharCount')
Integer,Integer_2,Integer_3,Digit,Digit_2,AnyCharExceprtMeta = REGEX_GRAMMAR.NonTerminals('Integer Integer_2 Integer_3 Digit Digit_2 EnyCharExceptMEta')
AnyChar,MetaChar = REGEX_GRAMMAR.NonTerminals('AnyChar MetaChar')
union,special, lbrasses,rbrasses,point,opar,cpar,lbrackets,rbrackets,starts = REGEX_GRAMMAR.Terminals('| \ { } . ( ) [ ] ^')
interval, comma,question,star_op, plus_op,epsilon, underscore = REGEX_GRAMMAR.Terminals('- , ? * + ε _')
zero,one,two,three,four,five,six,seven,eight,nine, any_char = REGEX_GRAMMAR.Terminals('0 1 2 3 4 5 6 7 8 9 any_char')
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = REGEX_GRAMMAR.Terminals('a b c d e f g h i j k l m n o p q r s t u v w x y z')
A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z = REGEX_GRAMMAR.Terminals('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')

#################Productions###############
Exp %= Term + Term_2, lambda h,s: s[2], None, lambda h,s :s[1]

Term %= Factor + Factor_2, lambda h,s : s[2], None , lambda h,s: s[1]

Term_2 %= union + Exp, lambda h,s : UnionNode(h[0],s[2]), None , None
Term_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s : h[0]

Factor %= Atom + Atom_2, lambda h,s: s[2], None,lambda h,s: s[1]

Factor_2 %= Term, lambda h,s: ConcatNode(h[0],s[1]), None
Factor_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s : h[0]

Atom %= Char, lambda h,s:s[1], None
Atom %= opar + Exp + cpar, lambda h,s : s[2], None, None,None
Atom %= lbrackets + CharClass + rbrackets, lambda h,s: s[2], None, None,None

Atom_2 %= MetaChar, lambda h,s :s[1], lambda h,s: h[0]
Atom_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: h[0]

CharClass %= CharClassItem + CharClassItem_2,lambda h,s: s[2], None,lambda h,s: s[1]

# CharClass_2 %=CharClass, lambda h,s: s[1], None
# CharClass_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

CharClassItem %= Char + Char_2, lambda h,s: s[2], None,lambda h,s: s[1]

CharClassItem_2 %= CharClass, lambda h,s: ConcatNode(h[0], s[1]), None
CharClassItem_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: h[0]

Char %= AnyChar, lambda h,s :s[1], None
Char %= special + AnyChar, lambda h,s : UnionNode(h[0],s[2]),None,None

Char_2 %= interval + Char, lambda h,s: IntervalNode(h[0],s[2]), None,None
Char_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: h[0]

CharCount %= Integer + Integer_2,lambda h,s: ConcatNode(s[1],s[2]), None,None

Integer %= Digit + Digit_2,lambda h,s: ConcatNode(s[1],s[2]), None,None

Integer_2 %= comma + Integer_3, lambda h,s : ConcatNode(s[1],s[2]), None, None #Revisar
Integer_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: h[0]

Integer_3 %= Integer, lambda h,s: s[1], None
Integer_3 %= REGEX_GRAMMAR.Epsilon, lambda h,s: h[0]

Digit %= zero,lambda h,s :SymbolNode(s[1]), None
Digit %= one,lambda h,s :SymbolNode(s[1]), None
Digit %= two,lambda h,s :SymbolNode(s[1]), None
Digit %= three,lambda h,s :SymbolNode(s[1]), None
Digit %= four,lambda h,s :SymbolNode(s[1]), None
Digit %= five,lambda h,s :SymbolNode(s[1]), None
Digit %= six,lambda h,s :SymbolNode(s[1]), None
Digit %= seven,lambda h,s :SymbolNode(s[1]), None
Digit %= eight,lambda h,s :SymbolNode(s[1]), None
Digit %= nine,lambda h,s :SymbolNode(s[1]), None

Digit_2 %= Integer, lambda h,s: s[1],None
Digit_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: h[0]

AnyChar %= Digit, lambda h,s: s[1], None
AnyChar %= any_char, lambda h,s :SymbolNode(s[1]), None

MetaChar %= question, lambda h,s : QuestionNode(h[0]), None
MetaChar %= star_op, lambda h,s : ClosureNode(h[0]), None
MetaChar %= plus_op, lambda h,s : PlusNode(h[0]), None





