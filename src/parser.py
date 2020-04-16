from lark import Lark

gr = """
    start: NT " " expr
    expr: NT 
            | T 
            | ready_expr
            | star_expr 
            | or_expr
            | set_expr
    NT: ("A".."Z") | ("A".."Z")("0".."9")+
    T: "eps" | ("a".."z") | ("a".."z")("0".."9")+
    or_expr: expr " | " expr
            | "(" expr " | " expr ")"
    star_expr: NT "*"
            | T "*"
            | "(" ready_expr ")" "*"
            | "(" expr ")" "*"
    ready_expr: ((NT|T) " ")+ (NT|T)
    set_expr: (expr " ")+ expr
"""

p = Lark(gr)


def parse_line(line):
    return p.parse(line)
