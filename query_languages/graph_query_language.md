#Язык зпаросов к графам
###Описание синтаксиса


script &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | ε <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | stmt SEMI script <br/>
<br/>
stmt &nbsp;  &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | KW_CONNECT KW_TO STRING<br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; | LIST <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; | select_stmt <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |  named_pattern_stmt <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | KW_WRITE select_stmt KW_TO STRING
<br/>

named_pattern &nbsp;| NT_NAME OP_EQ pattern <br/>

select_stmt &nbsp; &nbsp; &nbsp; &nbsp;| KW_SELECT LBR obj_expr RBR KW_FROM STRING KW_WHERE where_expr <br/>

obj_expr &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | vs_info<br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| KW_COUNT vs_info <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| KW_EXISTS vs_info <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| KW_ISOLATED vs_info<br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| KW_COUNT_NEIGHBOURS vs_info<br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| KW_SINGULAR vs_info<br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| KW_ADJACENT vs_info vs_info<br/>


vs_info &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;| LBR IDENT COMMA IDENT RBR <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;| IDENT <br/>

where_expr &nbsp; &nbsp; &nbsp;&nbsp;| LBR v_expr RBR <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | OP_MINUS pattern OP_MINUS OP_GR <br/>

v_expr &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | IDENT <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;| UNDERSCORE <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | IDENT DOT KW_ID OP_EQ INT <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | IDENT DOT KW_ID OP_GR INT<br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | KW_RANDOM

pattern &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| alt_elem <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | alt_elem MID pattern <br/>

alt_elem &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| seq <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;| LBR RBR <br/>

seq &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| seq_elem <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;| seq_elem seq <br/>

seq_elem &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| prim_pattern <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| prim_pattern OP_STAR <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| prim_pattern OP_PLUS <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| prim_pattern OP_Q <br/>

prim_pattern &nbsp; &nbsp;&nbsp;| IDENT <br/> 
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;| NT _NAME <br/>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | LBR pattern RBR
#### Терминальный альфавит
LBR = ' ( ' <br/>
RBR = ' ) '<br/>
COMMA = ' , '<br/>
SEMI = ' ; '<br/>
MID = ' | '<br/>
DOT = ' . '<br/>
OP_STAR = ' ∗ '<br/>
OP_PLUS = ' + '<br/>
OP_Q = ' ? '<br/>
OP_MINUS = ' − '<br/>
OP_GR = ' > '<br/>
OP_EQ = ' = '<br/>
KW_ID = ' ID '<br/>
KW_COUNT = ' COUNT '<br/>
KW_COUNT_NEIGHBOURS = ' COUNT_NEIGHBOURS '<br/>
KW_ISOLATED = ' ISOLATED '<br/>
KW_SINGULAR = ' SINGULAR '<br/>
KW_ADJACENT = ' ADJACENT ' <br/>
KW_EXISTS = ' EXISTS '<br/>
KW_FROM = ' FROM '<br/>
KW_SELECT = ' SELECT '<br/>
KW_WRITE = ' WRITE '<br/>
KW_WHERE = ' WHERE '<br/>
KW_LIST = ' LIST '<br/>
KW_ALL = ' ALL '<br/>
KW_GRAPHS = ' GRAPHS '<br/>
KW_CONNECT = ' CONNECT '<br/>
KW_RANDOM = ' RANDOM ' <br/>
KW_TO = ' TO ' <br/>
IDENT =[a − z][a − z] ∗<br/>
INT =0 | [1 − 9][0 − 9] ∗<br/>
NT_NAME =[A − Z][a − z] ∗<br/>
STRING = ' [ ' ([aA − zZ] | [0 − 9] | ( ' − ' | ' ' | ' _ ' | ' / ' | ' . ' )) ∗' ] '<br/>
UNDERSCORE = ' _ '
###Описание языка
Язык скриптов задаются следующей грамматикой:<br/>
``script  eps | statement ; script``<br/>
##### Основные типы запросов
1. Подгрузить файл с графом <br/>
`` CONNECT TO [<graph_file>]``
2. Сделать запрос к графу  <br/>
``SELECT <funciton over set> FROM [<graph_file>] WHERE <set filter>``<br/>
Возможные запросы к множествам:
    * ``ISOLATED vertex`` - правда ли, что множество вершин изолированно
    * ``SINGULAR vertex`` - правда ли, что множество содержит единственную вершину
    * ``COUNT_NEIGHBOURS vertex`` - количество соседей
    * ``ADJACENT vertex1 vertex2`` - правда ли, что есть ребро ``vertex1 -- vertex2``<br/>
3. Задать правило для нетерминала <br/>
`` Nonterminal_name = regular_exrpession``
3. Загрузуить результат запроса в файл <br/>
``WRITE select_statement TO [<file_name>]``
###Примеры запросов
* Пример из конспекта
    ```
    CONNECT TO [\home\user\graph_db];
    S = a S b S | () ;
    SELECT COUNT(u) FROM [g1.txt] where (v.id = 10) - S -> (u);
    ```
* Пример, находящий все изолированные вершины 
    ``
    SELECT ISOLATED(u) FROM [my_graph.txt] where (_);
    ``
* Пример, записывающий количество соседей вершины с номером 2 в файл
    ```
    WRITE SELECT COUNT_NEIGHBOURS(u) FROM [my_graph.txt] where (u.id = 2) TO [output.txt];
    ```

   