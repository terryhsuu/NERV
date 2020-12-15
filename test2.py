def how_close_to_edge(label):
    edge = {0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,15,23,31,39,47,55,57,58,59,60,61,62,63}
    degree = 63
    for i in edge:
        if degree > abs(enum[label]-i):
            degree = abs(enum[label]-i)
            if degree == 0: break
    return degree #(label, int )

how_close_to_edge('1A')