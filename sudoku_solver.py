puzzle0 = [
    [5,2,9,None,None,None,4,8,None],
    [4,3,None,1,2,8,None,None,5],
    [None,None,None,None,4,9,None,3,2],
    [None,None,5,None,3,None,2,9,None],
    [None,None,2,4,5,None,8,None,None],
    [3,7,None,9,None,None,None,6,None],
    [9,1,3,None,None,None,None,None,None],
    [None,None,None,None,1,5,None,None,9],
    [None,None,None,None,None,3,1,None,6]
]

def remove_none(array):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] is None:
                array[i][j] = 0

    return array

def to_dictionaries(puzzle):
    array = []
    for row in puzzle:
        row_array = []
        for cell in row:
            row_array.append(
                {'n':cell if cell is not None else 0, 'p':list(range(1,10) if cell is None else [])}
            )
        array.append(row_array)
    return array

def to_list(array):
    puzzle = []
    for row in array:
        puzzle.append([cell['n'] for cell in row])
    return puzzle

def possibility_check(array):
    updated = 0
    for row in range(9):
        for column in range(9):
            cell = array[row][column]['n']
            if cell is None or cell == 0:
                continue

            #horizontally
            for i in range(9):
                if i==column:
                    continue
                if cell in array[row][i]['p']:
                    updated += 1
                    array[row][i]['p'].remove(cell)

            #vertically
            for i in range(9):
                if i == row:
                    continue
                if cell in array[i][column]['p']:
                    array[i][column]['p'].remove(cell)
                    updated += 1
    return updated

def filling(array):
    filled = 0
    for i in range(0,9,3):
        for j in range(0,9,3):
            found_numbers = []
            positions = []
            for row in range(i,i+3):
                for column in range(j,j+3):
                    positions.append([row,column])
                    cell = array[row][column]['n']
                    if cell is None or cell == 0:
                        continue
                    found_numbers.append(cell)
            # print()

            for number in range(1,10):
                if number in found_numbers:
                    continue
                available = 0
                last_position = None
                for position in positions:
                    row, column = position
                    if number in array[row][column]['p']:
                        available += 1
                        last_position = [row, column]

                if available == 1:
                    row, column = last_position
                    array[row][column] = {'n':number,'p':[]}
                    filled += 1
    return filled


def final_result(puzzle, solved_puzzle):
    for j in range(len(puzzle)):
        print(puzzle[j], end='\t\t')
        print(solved_puzzle[j])


# when there are several original answers
def try_random(array):
    found = False
    for row in array:
        if found:
            break
        for cell in row:
            if cell['n'] is None or cell['n'] == 0:
                cell['n'] = cell['p'][0]
                cell['p'] = []
                found = True
                break


def summary(array):
    remaining = 0
    for row in array:
        for cell in row:
            if cell['n'] is None or cell['n'] == 0:
                remaining += 1

    return remaining


def fill_one_possibility(array):
    filled = 0
    for row in array:
        for cell in row:
            if len(cell['p']) == 1:
                filled += 1
                cell['n'] = cell['p'][0]
                cell['p'] = []
    return filled

def solver(puzzle):
    turn = 0
    array = to_dictionaries(puzzle)
    while True:
        if summary(array) == 0:
            print('\n\n\t\t\tDone!')
            solved_puzzle = to_list(array)
            final_result(remove_none(puzzle), solved_puzzle)
            return
        turn += 1
        updated = possibility_check(array)
        filled = filling(array)
        if filled == 0:
            one_filled = fill_one_possibility(array)
            print(f'[*] Tried one possibilities - {str(one_filled)} ')
            if one_filled == 0:
                try_random(array)
                print('[*] Random filled')
                filled = filling(array)
                if filled == 0:
                    try_random(array)
                    print('[*] Random filled')
                    filled = filling(array)
                    if filled == 0:
                        print('\n\n\t\tCant Complete!')
                        final_result(array)
                        return
        print(f'[+] Turn - {str(turn)} Filled - {str(filled)} Possibility Updated - {str(updated)}')


solver(puzzle0)


