from grammar import Grammar
from lexer_ast import EpsilonNode ,SymbolNode ,ConcatNode, ClosureNode, UnionNode, IntervalNode



REGEX_GRAMMAR = Grammar()

Exp = REGEX_GRAMMAR.NonTerminal('Exp',True)
Term,Term_2,Factor,Factor_2,Atom,Atom_2,CharClass,CharClass_2 = REGEX_GRAMMAR.NonTerminals('Term Term_2 Factor Factor_2 Atom Atom_2 CharClass CharClass_2')
CharClassItem,CharClassItem_2,Char_2,Char,CharCount = REGEX_GRAMMAR.NonTerminals('CharClassItem CharClassItem_2 Char_2 Char CharCount')
Integer,Integer_2,Integer_3,Digit,Digit_2,AnyCharExceprtMeta = REGEX_GRAMMAR.NonTerminals('Integer Integer_2 Integer_3 Digit Digit_2 EnyCharExceptMEta')
AnyChar,MetaChar = REGEX_GRAMMAR.NonTerminals('AnyChar MetaChar')
union,lbrasses,rbrasses,point,opar,cpar,lbrackets,rbrackets,starts = REGEX_GRAMMAR.Terminals(' \ { } . ( ) [ ] ^')
interval, comma,question,star, plus,epsilon = REGEX_GRAMMAR.Terminals('- , ? * + ε')
zero,one,two,three,four,five,six,seven,eight,nine = REGEX_GRAMMAR.Terminals('0 1 2 3 4 5 6 7 8 9')

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

Char %= AnyCharExceprtMeta, lambda h,s :s[1], None
Char %= union + AnyChar, lambda h,s : UnionNode(h[0],s[2]),None,None

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

AnyChar %= 


