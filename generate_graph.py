dinner_matrix = [
    '0 1 1 0 0 \n',
    '1 0 0 1 0 \n',
    '1 0 0 0 1 \n',
    '0 1 0 0 1 \n',
    '0 0 1 1 0',
]

with open('dinner_graph.txt', '+w') as txt:
    txt.writelines(dinner_matrix)