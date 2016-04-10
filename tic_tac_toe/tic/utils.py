

def shrink(line):
    count = 1
    cur = line[0]
    result = []
    for x in line[1:]:
        if x == cur:
            count += 1
        else:
            result.append((cur, count))
            cur = x
            count = 1
    result.append((cur, count))
    return result


def rotate(state):
    new_state = []
    columns = len(state[0])
    rows = len(state)
    for j in range(columns):
        line = ""
        for i in range(rows):
            line += state[i][j]
        new_state.append(line[::-1])
    return new_state


def back_rotate(state):
    new_state = []
    columns = len(state[0])
    rows = len(state)
    for j in range(columns):
        line = ""
        for i in range(rows):
            line += state[i][-j-1]
        new_state.append(line)
    return new_state


class StatesCache():
    """
    Cache for saving states of the game.
    """

    def all_equivalent_states(self, state):
        state, is_max = state
        if (''.join(state), is_max) in self._eq_cache:
            return self._eq_cache[(''.join(state), is_max)]
        result = set()
        for _ in range(4):
            new_state = []
            for line in state:
                new_state.append(line[::-1])
            result.add((''.join(new_state), is_max))
            new_state = rotate(state)
            result.add((''.join(new_state), is_max))
            state = new_state
        self._eq_cache[(''.join(state), is_max)] = result
        return result

    def __init__(self, *args):
        self._eq_cache = {}
        self._cache = {}

    def __setitem__(self, key, value):
        for state in self.all_equivalent_states(key):
            if state in self._cache:
                self._cache[state] = value
                return
        self._cache[state] = value

    def __getitem__(self, key):
        for state in self.all_equivalent_states(key):
            if state in self._cache:
                return self._cache[state]
        # Let it raise error.
        return self._cache[state]
