def complementaryColor(my_hex):
    """
    Returns complementary RGB color

    Example:
    >>>complementaryColor('FFFFFF')
    '000000'
    """
    if my_hex[0] == '#':
        my_hex = my_hex[1:]
    rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
    comp = ['%02x' % (255 - int(a, 16)) for a in rgb]
    return '#' + ''.join(comp)