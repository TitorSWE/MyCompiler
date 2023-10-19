from pprint import pp
import sys
import lark

grammar = (r"""

exp : SIGNED_NUMBER                     -> exp_nombre
| INTEGER                               -> exp_var_int
| exp OPBIN exp                         -> exp_opbin
| "(" exp ")"                           -> exp_bracket

bcmd : (cmd)*
cmd : IDENTIFIER "=" exp ";"                   -> assignment
| "if" "(" exp ")" "{" bcmd "}"         -> if
| "while" "(" exp ")" "{" bcmd "}"      -> while
| "print" "(" exp ")"                   -> print

prg : "main" "(" var_list ")" "{" bcmd "return" "(" exp ")" ";" "}" 

var_list :                              -> void
| IDENTIFIER ("," IDENTIFIER)*          -> aumoinsune
IDENTIFIER : INTEGER

INTEGER: /[a-zA-Z0-9]+/
OPBIN : /[+*\->]/ 

%import common.WS
%import common.SIGNED_NUMBER
%ignore WS
""")
grammairePrg = lark.Lark(grammar, start = "cmd")

def pp_exp(e) :
    if e.data in {"exp_nombre", "exp_var_int", "exp_var_tab"} :
        return e.children[0].value
    elif e.data == "exp_par":
        return f"({pp_exp(e.children[0])})"
    elif e.data == "exp_opbin":
        return f"({pp_exp(e.children[0])} {e.children[1].value} {pp_exp(e.children[2])})"
    elif e.data == "exp_bracket":
        return f"({pp_exp(e.children[0])})"
    
def pp_cmd(cmd) :
    if cmd.data == "assignment":
        return f"({cmd.children[0].value} = {pp_exp(cmd.children[1])})"

code = "a=a+2;"
input = grammairePrg.parse(code)

print(pp_cmd(input))