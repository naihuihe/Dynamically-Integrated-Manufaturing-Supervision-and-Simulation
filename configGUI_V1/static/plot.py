

def plot_machine_graph(x, y, size = "20x20"):
    """
    :param x: int, the horizontal position of machine
    :param y: int, the vertical position of machine
    :param size: string, the area size of machine, Height X Width, default value = 20px X 20px
    :return: bbox
    """

    size = size.split("x")
    h = int(size[0])
    w = int(size[1])

    bbox = [
        (x, y)   # top-left corner of the square/rectangle box
        (x + w, y + h)   # bottom-right corner
    ]

    return bbox



