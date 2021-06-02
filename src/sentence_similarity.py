import editdistance


def longest_common_substring(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return mmax


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
    close_in_overlap_distance: bool = longest_common_substring(a.split(), b.split()) >= 10

    have_a_link = close_in_edit_distance or close_in_overlap_distance

    return have_a_link, 0 if len(a.split()) < len(b.split()) else 1


if __name__ == '__main__':
    a = longest_common_substring("what are you talking".split(), "are you".split())
    print(a)
