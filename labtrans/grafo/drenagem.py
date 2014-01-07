# -*- coding:utf8 -*-

def nextnode(unexplored):
    if len(unexplored) == 1:
        return None, unexplored

    for key, __value in unexplored.items():
        value = __value[0]
        if value is not None:  # Não analiza o último nó
            # inicia o status de parent node
            status = True
            searchlist = unexplored.copy()
            searchlist.pop(key)

            for key_child, __value_child in searchlist.items():
                value_child = __value_child[0]
                if key in value_child:
                    status = False

            if status:
                unexplored.pop(key)
                return unexplored, {key: __value}
    return None, None

def determine_tc(T):
    unexplored = T.copy()

    explored = []

    unexplored, node = nextnode(unexplored)
    frontier = [node]

    while frontier:
        node = frontier.pop()
        key = node.keys()[0]
        childs = (node.items())[0][1][0]

        for c in childs:
            # pega valor atual do nó (node[key][1])
            # utiliza o valor de fluxo entre o nó e o nó filho (node[key][0][c])
            # soma os dois valores e atribui no nó filho
            unexplored[c] = (unexplored[c][0], node[key][1] + node[key][0][c])

        explored.append(node)
        unexplorer, node = nextnode(unexplored)

        if childs:
            frontier.append(node)


    return explored

def test():
    """
    T = {
        'Nó1': ({'Nó-filho1a': float-tf1a, 'Nó-filho2a': float-tf2a}, float-ti1),
        'Nó2': ({'Nó-filho1b': float-tf1b, 'Nó-filho2b': float-tf2b}, float-ti2)
    }
    """
    T = {
        '#F': ({}, None), # F é o final
        '#9': ({'#F': 4.2}, 42),
        '#13': ({'#9': 3.9},  62),
        '#10': ({'#9': 3.7}, 39),
        '#11': ({'#10': 5.}, 53),
        '#12': ({'#11': 3.4}, 52)
    }

    unexplorer, node = nextnode(T.copy())
    print node
    assert list(node)[0] in ['#13', '#12']
    assert len(unexplorer) == 5

    for x in range(1, 6):
        unexplorer, node = nextnode(unexplorer)
        if x == 5:
            assert unexplorer is None
        else:
            assert len(unexplorer) == (5 - x)

        print node

    assert unexplorer is None
    print determine_tc(T)

if __name__ == '__main__':
    test()