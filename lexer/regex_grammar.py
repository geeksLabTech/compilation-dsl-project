from grammar import Grammar
from lexer.lexer_ast import EpsilonNode, PlusNode, QuestionNode ,SymbolNode ,ConcatNode, ClosureNode, UnionNode, IntervalNode



REGEX_GRAMMAR = Grammar()

Exp = REGEX_GRAMMAR.NonTerminal('Exp',True)
Term,Term_2,Factor,Factor_2,Atom,Atom_2,CharClass,CharClass_2 = REGEX_GRAMMAR.NonTerminals('Term Term_2 Factor Factor_2 Atom Atom_2 CharClass CharClass_2')
CharClassItem,CharClassItem_2,Char_2,Char,CharCount = REGEX_GRAMMAR.NonTerminals('CharClassItem CharClassItem_2 Char_2 Char CharCount')
Integer,Integer_2,Integer_3,Digit,Digit_2,AnyCharExceprtMeta = REGEX_GRAMMAR.NonTerminals('Integer Integer_2 Integer_3 Digit Digit_2 EnyCharExceptMEta')
AnyChar,MetaChar = REGEX_GRAMMAR.NonTerminals('AnyChar MetaChar')
union,special, lbrasses,rbrasses,point,opar,cpar,lbrackets,rbrackets,starts = REGEX_GRAMMAR.Terminals('| \ { } . ( ) [ ] ^')
interval, comma,question,star, plus,epsilon, underscore = REGEX_GRAMMAR.Terminals('- , ? * + ε _')
zero,one,two,three,four,five,six,seven,eight,nine = REGEX_GRAMMAR.Terminals('0 1 2 3 4 5 6 7 8 9')
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z = REGEX_GRAMMAR.Terminals('a b c d e f g h i j k l m n o p q r s t u v w x y z')
A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z = REGEX_GRAMMAR.Terminals('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')


#################Productions###############
Exp %= Term + Term_2, lambda h,s: s[2], None, lambda h,s :s[1]

Term %= Factor + Factor_2, lambda h,s : ConcatNode(s[1],s[2]), None , None

Term_2 %= union + Exp, lambda h,s : UnionNode(h[0],s[2]), None , None
Term_2 %= REGEX_GRAMMAR.Epsilon , lambda h,s : EpsilonNode(h[0])

Factor %= Atom + Atom_2, lambda h,s: ConcatNode(s[1],s[2]), None,None

Factor_2 %= Term, lambda h,s: s[1], None
Factor_2 %= REGEX_GRAMMAR.Epsilon,lambda h,s : EpsilonNode(h[0])

Atom %= Char, lambda h,s:s[1]
Atom %= opar + Exp + cpar, lambda h,s : s[2], None, None,None
Atom %= lbrackets + CharClass + rbrackets, lambda h,s: s[2], None, None,None

Atom_2 %= MetaChar, lambda h,s :s[1], None
Atom_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

CharClass %= CharClassItem + CharClassItem_2,lambda h,s: ConcatNode(s[1],s[2]), None,None

# CharClass_2 %=CharClass, lambda h,s: s[1], None
# CharClass_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

CharClassItem %= Char + Char_2, lambda h,s: ConcatNode(s[1],s[2]), None,None

CharClassItem_2 %= CharClass, lambda h,s: s[1], None
CharClassItem_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

Char %= AnyChar, lambda h,s :s[1], None
Char %= special + AnyChar, lambda h,s : UnionNode(h[0],s[2]),None,None

Char_2 %= interval + Char, lambda h,s: IntervalNode(h[0],s[2]), None,None
Char_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

CharCount %= Integer + Integer_2,lambda h,s: ConcatNode(s[1],s[2]), None,None

Integer %= Digit + Digit_2,lambda h,s: ConcatNode(s[1],s[2]), None,None

Integer_2 %= comma + Integer_3, lambda h,s : ConcatNode(s[1],s[2]) #Revisar
Integer_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

Integer_3 %= Integer, lambda h,s: s[1], None
Integer_3 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

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
Digit_2 %= REGEX_GRAMMAR.Epsilon, lambda h,s: EpsilonNode(h[0])

AnyChar %= Digit, lambda h,s: s[1], None
AnyChar %= a,lambda h,s :SymbolNode(s[1]), None
AnyChar %= b,lambda h,s :SymbolNode(s[1]), None
AnyChar %= c,lambda h,s :SymbolNode(s[1]), None
AnyChar %= d,lambda h,s :SymbolNode(s[1]), None
AnyChar %= e,lambda h,s :SymbolNode(s[1]), None
AnyChar %= f,lambda h,s :SymbolNode(s[1]), None
AnyChar %= g,lambda h,s :SymbolNode(s[1]), None
AnyChar %= h,lambda h,s :SymbolNode(s[1]), None
AnyChar %= i,lambda h,s :SymbolNode(s[1]), None
AnyChar %= j,lambda h,s :SymbolNode(s[1]), None
AnyChar %= k,lambda h,s :SymbolNode(s[1]), None
AnyChar %= l,lambda h,s :SymbolNode(s[1]), None
AnyChar %= m,lambda h,s :SymbolNode(s[1]), None
AnyChar %= n,lambda h,s :SymbolNode(s[1]), None
AnyChar %= o,lambda h,s :SymbolNode(s[1]), None
AnyChar %= p,lambda h,s :SymbolNode(s[1]), None
AnyChar %= q,lambda h,s :SymbolNode(s[1]), None
AnyChar %= r,lambda h,s :SymbolNode(s[1]), None
AnyChar %= s,lambda h,s :SymbolNode(s[1]), None
AnyChar %= t,lambda h,s :SymbolNode(s[1]), None
AnyChar %= u,lambda h,s :SymbolNode(s[1]), None
AnyChar %= v,lambda h,s :SymbolNode(s[1]), None
AnyChar %= w,lambda h,s :SymbolNode(s[1]), None
AnyChar %= x,lambda h,s :SymbolNode(s[1]), None
AnyChar %= y,lambda h,s :SymbolNode(s[1]), None
AnyChar %= z,lambda h,s :SymbolNode(s[1]), None
AnyChar %= A,lambda h,s :SymbolNode(s[1]), None
AnyChar %= B,lambda h,s :SymbolNode(s[1]), None
AnyChar %= C,lambda h,s :SymbolNode(s[1]), None
AnyChar %= D,lambda h,s :SymbolNode(s[1]), None
AnyChar %= E,lambda h,s :SymbolNode(s[1]), None
AnyChar %= F,lambda h,s :SymbolNode(s[1]), None
AnyChar %= G,lambda h,s :SymbolNode(s[1]), None
AnyChar %= H,lambda h,s :SymbolNode(s[1]), None
AnyChar %= I,lambda h,s :SymbolNode(s[1]), None
AnyChar %= J,lambda h,s :SymbolNode(s[1]), None
AnyChar %= K,lambda h,s :SymbolNode(s[1]), None
AnyChar %= L,lambda h,s :SymbolNode(s[1]), None
AnyChar %= M,lambda h,s :SymbolNode(s[1]), None
AnyChar %= N,lambda h,s :SymbolNode(s[1]), None
AnyChar %= O,lambda h,s :SymbolNode(s[1]), None
AnyChar %= P,lambda h,s :SymbolNode(s[1]), None
AnyChar %= Q,lambda h,s :SymbolNode(s[1]), None
AnyChar %= R,lambda h,s :SymbolNode(s[1]), None
AnyChar %= S,lambda h,s :SymbolNode(s[1]), None
AnyChar %= T,lambda h,s :SymbolNode(s[1]), None
AnyChar %= U,lambda h,s :SymbolNode(s[1]), None
AnyChar %= V,lambda h,s :SymbolNode(s[1]), None
AnyChar %= W,lambda h,s :SymbolNode(s[1]), None
AnyChar %= X,lambda h,s :SymbolNode(s[1]), None
AnyChar %= Y,lambda h,s :SymbolNode(s[1]), None
AnyChar %= Z,lambda h,s :SymbolNode(s[1]), None
AnyChar %= underscore, lambda h,s :SymbolNode(s[1]), None

MetaChar %= question, lambda h,s : QuestionNode(h[0]), None
MetaChar %= star, lambda h,s : ClosureNode(h[0]), None
MetaChar %= plus, lambda h,s : PlusNode(h[0]), None




