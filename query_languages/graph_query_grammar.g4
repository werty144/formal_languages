grammar graph_query_grammar;

script
    : EOF
    | (stmt Semi)*
    ;

stmt
    : Kw_connect Kw_to String
    | Kw_list Kw_all Kw_graphs
    | select_stmt
    | named_pattern
    | Kw_write select_stmt Kw_to String
    ;

named_pattern
    : Nt_name Op_eq pattern
    ;

select_stmt
    : Kw_select obj_expr Kw_from String Kw_where where_expr
    ;

obj_expr
    : vs_info
    | Kw_count Lbr vs_info Rbr
    | Kw_exists Lbr vs_info Rbr
    | Kw_isolated Lbr vs_info Rbr
    | Kw_count_neighbours Lbr vs_info Rbr
    | Kw_singular Lbr vs_info Rbr
    | Kw_adjacent Lbr vs_info Rbr
    ;

vs_info
    : Lbr Ident Comma Ident Rbr
    | Ident
    ;

where_expr
    : Lbr v_expr Rbr Op_minus pattern Op_minus Op_gr Lbr v_expr Rbr
    ;

v_expr
    : Ident
    | Underscore
    | Ident Dot Kw_id Op_eq Int
    | Kw_random
    ;

pattern
    : alt_elem
    | alt_elem Mid pattern
    ;

alt_elem
    : seq
    | Lbr Rbr
    ;

seq
    : seq_elem
    | seq_elem seq
    ;

seq_elem
    : prim_pattern
    | prim_pattern Op_star
    | prim_pattern Op_plus
    | prim_pattern Op_q
    ;

prim_pattern
    : Ident
    | Nt_name
    | Lbr pattern Rbr
    ;

Lbr: '(';
Rbr: ')';
Comma: ',';
Semi: ';';
Mid: '|';
Dot: '.';
Op_star: '*';
Op_plus: '+';
Op_q: '?';
Op_minus: '-';
Op_gr: '>';
Op_eq: '=';
Kw_id: 'ID';
Kw_count: 'COUNT';
Kw_count_neighbours: 'COUNT_NEIGHBOURS';
Kw_isolated: 'ISOLATED';
Kw_singular: 'SINGULAR';
Kw_adjacent: 'ADJACENT';
Kw_exists: 'EXISTS';
Kw_from: 'FROM';
Kw_select: 'SELECT';
Kw_write: 'WRITE';
Kw_where: 'WHERE';
Kw_list: 'LIST';
Kw_all: 'ALL';
Kw_graphs: 'GRAPHS';
Kw_connect: 'CONNECT';
Kw_random: 'RANDOM';
Kw_to: 'TO';
Underscore: '_';

Ident
    : [a-z][a-z]*
    ;

Int
    : [0] | [1-9][0-9]*
    ;

Nt_name
    : [A-Z][a-z]*
    ;

String
    : '[' ([a-zA-Z] | [0-9] | ('-'|' '|'_'|'/'|'.'))* ']'
    ;

WS : [ \t\r\n]+ -> skip ;