# Author: Teshan Liyanage <teshanuka@gmail.com>


class CmdColors:
    """Some colors to help print into terminal"""
    HEADER = '\033[95m'
    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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