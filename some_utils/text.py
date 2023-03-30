# Author: Teshan Liyanage <teshanuka@gmail.com>

class TermColor(str):
    ENDC = "\033[0m"

    def __call__(self, s: str) -> str:
        return f"{self}{s}{self.ENDC}"


class TermColors:
    """Some colors to help print into terminal"""
    header = TermColor("\033[95m")
    red = TermColor("\033[0;31m")
    yellow = TermColor("\033[0;33m")
    okblue = TermColor("\033[94m")
    okgreen = TermColor("\033[92m")
    warning = TermColor("\033[93m")
    fail = TermColor("\033[91m")
    bold = TermColor("\033[1m")
    underline = TermColor("\033[4m")
    endc = TermColor("\033[0m")


class TermSymbols:
    check = "✓"
    cross = "✗"
    l_arrow = "←"
    r_arrow = "→"  


def box_text(text, fmt="regular", padding=(0, 0)):
    """ Put text into a box in unicode
    :param text: Text
    :param fmt: Options - [regular, bold, rounded]
    :param padding: horizontal and vertical padding
    :Example:
    >>>
        ┌─────────────┐     ╭─────────╮     ┏━━━━━━┓
        │ I'm a box!  ├─────┤ Rounded ┝━━━━━┫ Bold ┃
        └──────┬──────┘     ╰─────────╯     ┗━━━━━━┛
               │
         ┌─────┴────┐      ┌──────────┐
         │ Me too!  ├──────┤ Me Three │
         └──────────┘      └──────────┘

    .. Idea and the characters from:
        https://gist.github.com/carldunham/cf6738683c53be4510041a6ebbb42207
    """
    hl, vl = '─', '│'
    if fmt == "regular":
        tl, tr, bl, br = '┌', '┐', '└', '┘'
    elif fmt == "rounded":
        tl, tr, bl, br = '╭', '╮', '╰', '╯'
    elif fmt == "bold":
        hl, vl = '━', '┃'
        tl, tr, bl, br = '┏', '┓', '┗', '┛'
    else:
        raise NotImplementedError
    h_len = len(text) + 2 * padding[0]
    s = tl + hl * h_len + tr + '\n'
    for i in range(padding[1]):
        s += vl + ' ' * h_len + vl + '\n'
    s += vl + ' ' * padding[0] + text + ' ' * padding[0] + vl + '\n'
    for i in range(padding[1]):
        s += vl + ' ' * h_len + vl + '\n'
    s += bl + hl * h_len + br
    return s
    

def random_string(n):
    import random
    import string
    return ''.join(random.choice(string.digits+string.ascii_letters) for _ in range(n))
    
