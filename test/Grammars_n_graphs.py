import networkx as nx

syllabus_graph_triples1 = ['0 a 1',
                           '1 a 2',
                           '2 a 0',
                           '2 b 3',
                           '3 b 2']

syllabus_graph_triples2 = ['0 a 1',
                           '0 b 3',
                           '1 a 2',
                           '2 a 0',
                           '3 b 0']

correct_syllabus_hellings_answer = [
    ('A', 0, 1), ('A', 1, 2), ('A', 2, 0), ('B', 2, 3), ('B', 3, 2),
    ('S', 1, 3), ('S1', 1, 2), ('S', 0, 2), ('S1', 0, 3), ('S', 2, 3),
    ('S1', 2, 2), ('S', 1, 2), ('S1', 1, 3), ('S', 0, 3), ('S1', 0, 2),
    ('S', 2, 2), ('S1', 2, 3)]

correct_syllabus_s_acceptable = ['1 3',
                                 '0 2',
                                 '2 3',
                                 '1 2',
                                 '0 3',
                                 '2 2']

my_bracket_graph_triples = ['0 ( 1',
                            '1 ) 2',
                            '1 ( 3',
                            '3 ) 0',
                            '3 ) 4',
                            '4 ( 3',
                            '4 ) 5']

my_abc_graph_triples = ['0 a 1',
                        '1 b 0',
                        '1 c 2',
                        '1 c 3',
                        '1 b 4',
                        '2 c 2',
                        '2 a 6',
                        '4 c 5',
                        '5 a 3']

syllabus_grammar_rules = ['S A B',
                          'S A S1',
                          'S1 S B',
                          'A a',
                          'B b']

ambiguous_cbs_rules = ['S ( S )',
                       'S S S',
                       'S eps']

deterministic_cbs_rules = ['S ( S ) S',
                           'S eps']

cbs_rules_in_wcnf = ['A0 S A2',
                     'A1 (',
                     'A2 )',
                     'S A1 A0',
                     'S S S',
                     'S eps']

inherently_ambiguous_grammar = ['S A BC',
                                'S AB C',
                                'S eps',
                                'A a A',
                                'A eps',
                                'C c C',
                                'C eps',
                                'AB a AB b',
                                'AB eps',
                                'BC b BC c',
                                'BC eps']

correct_s_acceptable_abc_graph = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (6, 6), (5, 5),
                                  (1, 2), (1, 3), (4, 5), (0, 1), (5, 3), (2, 6), (0, 5),
                                  (0, 4), (1, 5)]

correct_bracket_graph_s_acceptable = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                      (0, 2), (1, 0), (1, 4), (4, 0), (1, 2), (4, 2),
                                      (0, 5), (1, 5), (4, 5)]


def make_syllabus_pda_graph1():
    syllabus_graph = nx.DiGraph()
    syllabus_graph.add_edge(0, 1, label=['a'])
    syllabus_graph.add_edge(1, 2, label=['S'])
    syllabus_graph.add_edge(1, 3, label=['b'])
    syllabus_graph.add_edge(2, 3, label=['b'])
    syllabus_graph.nodes[0]['is_start'] = True
    syllabus_graph.nodes[1]['is_start'] = False
    syllabus_graph.nodes[2]['is_start'] = False
    syllabus_graph.nodes[3]['is_start'] = False
    syllabus_graph.nodes[0]['is_final'] = False
    syllabus_graph.nodes[1]['is_final'] = False
    syllabus_graph.nodes[2]['is_final'] = False
    syllabus_graph.nodes[3]['is_final'] = True
    return syllabus_graph


def make_syllabus_pda_graph2():
    syllabus_graph = nx.DiGraph()
    syllabus_graph.add_edge(0, 1, label='a')
    syllabus_graph.add_edge(1, 2, label='S')
    syllabus_graph.add_edge(2, 3, label='b')
    syllabus_graph.add_edge(3, 4, label='S')
    syllabus_graph.nodes[0]['is_start'] = True
    syllabus_graph.nodes[1]['is_start'] = False
    syllabus_graph.nodes[2]['is_start'] = False
    syllabus_graph.nodes[3]['is_start'] = False
    syllabus_graph.nodes[4]['is_start'] = False
    syllabus_graph.nodes[0]['is_final'] = True
    syllabus_graph.nodes[1]['is_final'] = False
    syllabus_graph.nodes[2]['is_final'] = False
    syllabus_graph.nodes[3]['is_final'] = False
    syllabus_graph.nodes[4]['is_final'] = True
    return syllabus_graph


def make_syllabus_graph2():
    graph = nx.DiGraph()
    graph.add_edge(0, 1, label=['a'])
    graph.add_edge(1, 2, label=['b'])
    graph.add_edge(2, 3, label=['a'])
    graph.add_edge(3, 4, label=['b'])
    graph.add_edge(4, 5, label=['a'])
    graph.add_edge(5, 6, label=['b'])
    return graph


def make_syllabus_graph1():
    graph = nx.DiGraph()
    for (u, l, v) in [triple.split() for triple in syllabus_graph_triples1]:
        graph.add_edge(int(u), int(v), label=[l])
    return graph
