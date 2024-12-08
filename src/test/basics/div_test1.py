# Mamy nieskonczony ciag taktow
# Kazdy takt jest wyliczany dynamicznie
# W polowie kazdego chcemy wyliczyc nastepny
# Musimy wiedziec gdzie sie ostatnio zatrzymalismy, albo musimy przekazac ta informacje
# Zacznij od time - zakladamy na razie 4/4
# Przyklad: ((4, 4, 4, 4), (2, 2), (2, 4, 4), (8, 8, 4, 2))
# Next pobiera jeden tak => yield zwraca jeden tak i w ponownym callu kolejny

from itertools import count


# reset generates new generator
def bars(file_with_cmp):
    for bar_num in count(1):
        pass
