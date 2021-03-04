import editdistance


def compare_sentence(a: str, b: str, labels=None):
    """

    :param a:
    :param b:
    :param labels:
    :return: bool, 0:a->b;1:b->a
    """
    have_a_link: bool = True

    close_in_edit_distance = editdistance.eval(a.split(), b.split()) <= 1
    # TODO: overlap distance
    close_in_overlap_distance: bool = False

    have_a_link = close_in_edit_distance or close_in_overlap_distance

    return have_a_link, 0 if len(a.split()) < len(b.split()) else 1
