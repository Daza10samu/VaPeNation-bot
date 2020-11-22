import pathlib

pref_list = set()
black_list = set()
message = set()
def_words = set()


def get_words(file: pathlib.Path, spl: str=' ') -> set:
    words = set()
    f = open(file)
    words = set(f.read().split())
    f.close()
    return words


def update_words(file: pathlib.Path, words: set):
    f = open(file, 'w')
    for word in words:
        f.write(word + '\n')
    f.close()


def stemer(message: set, pref_list: set, def_words: set) -> set:
    words = set()
    for word in message:
        if word == ' ':
            continue
        word = word.lower()
        mark = '\'";:?.,()!-\n'
        new_word = ''
        for i in range(len(word) + 1):
            if (i == 0 or i != len(word) and ord(word[i]) != ord(word[i - 1])) and not (word[i] in mark):
                new_word += word[i]
            elif (i == len(word) or word[i] in mark) and new_word != '':
                words.add(new_word)
                new_word = ''

    for word in def_words:
        words.discard(word)

    message.clear()

    for word in words:
        for pref in pref_list:
            if len(word) > len(pref) and word[:len(pref)] == pref:
                word = word[len(pref):]
        if len(word) <= 3 and not word in black_list:
            continue
        message.add(word)
    words.clear()
    words.update(message)

    for word in def_words:
        words.discard(word)

    return words


def add_to_deflist(word: str):
    black_list.discard(word)
    def_words.add(word)


def check(word: str) -> int:
    mx_match = 0
    err = ''
    for bad_word in black_list:
        now_match = 0
        for i in range(min(len(word), len(bad_word))):
            now_match += ord(word[i]) == ord(bad_word[i])
        mx_match = max(mx_match, now_match)
        if mx_match == now_match:
            err = bad_word
    return mx_match


def blacklister(to_check_message: str) -> bool:
    ban = False
    global pref_list, def_words, message, black_list
    pref_list = get_words('pref_list.data')
    def_words = get_words('def_words.data')
    message = set(to_check_message.split())
    black_list = get_words('black_list.data')

    message = stemer(message, pref_list, def_words)

    for word in message:
        mx_match = check(word)
        if (mx_match * 1.0) / len(word) >= 0.5:
            black_list.add(word)
            ban = True

    if ban:
        update_words('black_list.data', black_list)
        return True
    return False
