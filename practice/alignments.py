class Alignments:
    def __init__(
        self, gap_penalty=-1, match_score=1, missmatch_penalty=0, sigma=-1, eps=-0.5
    ) -> None:
        self.GAP_PENALTY = gap_penalty
        self.MATCH_SCORE = match_score
        self.MISSMATCH_PENALTY = missmatch_penalty
        self.EPS = eps
        self.SIGMA = sigma
        pass

    def match(self, x, y):
        return int(x == y)

    def lcs_backtrack(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        s = [[0 for _ in range(m)] for _ in range(n)]

        backtrack = [[None for _ in range(m)] for _ in range(n)]

        for i in range(1, n):
            backtrack[i][0] = (i - 1, 0)

        for j in range(1, m):
            backtrack[0][j] = (0, j - 1)

        for i in range(1, n):
            for j in range(1, m):
                match = self.match(v[i - 1], w[j - 1])
                from_up = s[i - 1][j]
                from_left = s[i][j - 1]
                from_diag = s[i - 1][j - 1] + match
                s[i][j] = max(from_up, from_left, from_diag)

                if match == 1 and s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_up:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        lcs = ""
        i = n - 1
        j = m - 1
        while backtrack[i][j] != None:
            (i_new, j_new) = backtrack[i][j]
            if i_new == i - 1 and j_new == j - 1:
                lcs = v[i - 1] + lcs
            i = i_new
            j = j_new

        return lcs, s[n - 1][m - 1]

    def backtracking(self, backtrack, v, w, i, j, stop=0, s=None):
        v_align = ""
        w_align = ""

        while True:
            if backtrack[i][j] == None:
                break
            if s is not None and s[i][j] == stop:
                break

            (i_new, j_new) = backtrack[i][j]
            if (i_new, j_new) == (i - 1, j - 1):
                v_align = v[i - 1] + v_align
                w_align = w[j - 1] + w_align
            elif (i_new, j_new) == (i - 1, j):
                v_align = v[i - 1] + v_align
                w_align = "-" + w_align

            else:
                w_align = w[j - 1] + w_align
                v_align = "-" + v_align

            (i, j) = (i_new, j_new)

        return v_align, w_align

    def edit_distance(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        s = [[0 for _ in range(m)] for _ in range(n)]

        backtrack = [[None for _ in range(m)] for _ in range(n)]

        for i in range(1, n):
            s[i][0] = i
            backtrack[i][0] = (i - 1, 0)

        for j in range(1, m):
            s[0][j] = j
            backtrack[0][j] = (0, j - 1)

        for i in range(1, n):
            for j in range(1, m):
                match = self.match(v[i - 1], w[j - 1])
                from_up = s[i - 1][j] + 1
                from_left = s[i][j - 1] + 1
                from_diag = s[i - 1][j - 1] + 1 - match
                s[i][j] = min(from_up, from_left, from_diag)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_up:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        v_align, w_align = self.backtracking(backtrack, v, w, i, j, 0)

        return v_align, w_align

    def needleman_wunch(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        s = [[0 for _ in range(m)] for _ in range(n)]
        backtrack = [[None for _ in range(m)] for _ in range(n)]

        for i in range(1, n):
            s[i][0] = i * self.GAP_PENALTY
            backtrack[i][0] = (i - 1, 0)

        for j in range(1, m):
            s[0][j] = j * self.GAP_PENALTY
            backtrack[0][j] = (0, j - 1)

        for i in range(1, n):
            for j in range(1, m):
                match = self.match(v[i - 1], w[j - 1])
                match_score = 0
                if match == 1:
                    match_score = self.MATCH_SCORE
                else:
                    match_score = self.MISSMATCH_PENALTY

                from_up = s[i - 1][j] + self.GAP_PENALTY
                from_left = s[i][j - 1] + self.GAP_PENALTY
                from_diag = s[i - 1][j - 1] + match_score

                s[i][j] = max(from_up, from_left, from_diag)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_left:
                    backtrack[i][j] = (i, j - 1)
                else:
                    backtrack[i][j] = (i - 1, j)

        v_align, w_align = self.backtracking(backtrack, v, w, n - 1, m - 1, 0)

        return v_align, w_align

    def affine_gap_penaly_alignment(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        middle = [[0 for _ in range(m)] for _ in range(n)]
        upper = [[0 for _ in range(m)] for _ in range(n)]
        lower = [[0 for _ in range(m)] for _ in range(n)]

        backtrack = [[None for _ in range(m)] for _ in range(n)]

        for i in range(1, n):
            backtrack[i][0] = (i - 1, 0)

        for j in range(1, m):
            backtrack[0][j] = (0, j - 1)

        for i in range(1, n):
            for j in range(1, m):
                match = self.match(v[i - 1], w[j - 1])
                match_score = 0
                if match == 1:
                    match_score = self.MATCH_SCORE
                else:
                    match_score = self.MISSMATCH_PENALTY

                lower[i][j] = max(
                    lower[i - 1][j] + self.EPS, middle[i - 1][j] + self.SIGMA
                )

                upper[i][j] = max(
                    upper[i][j - 1] + self.EPS, middle[i][j - 1] + self.SIGMA
                )

                middle[i][j] = max(
                    middle[i - 1][j - 1] + match_score, lower[i][j], upper[i][j]
                )

                if middle[i][j] == middle[i - 1][j - 1] + match_score:
                    backtrack[i][j] = (i - 1, j - 1)
                elif middle[i][j] == lower[i][j]:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        v_align, w_align = self.backtracking(backtrack, v, w, n - 1, m - 1, 0)

        return v_align, w_align

    def smith_waterman(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        s = [[0 for _ in range(m)] for _ in range(n)]
        backtrack = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            backtrack[i][0] = (i - 1, 0)
        for j in range(m):
            backtrack[0][j] = (0, j - 1)

        max_score = float("-inf")
        max_score_i = 0
        max_score_j = 0

        for i in range(1, n):
            for j in range(1, m):
                match_score = 0
                match = self.match(v[i - 1], w[j - 1])
                if match == 1:
                    match_score = self.MATCH_SCORE
                else:
                    match_score = self.MISSMATCH_PENALTY

                from_up = s[i - 1][j] + self.GAP_PENALTY
                from_left = s[i][j - 1] + self.GAP_PENALTY
                from_diag = s[i - 1][j - 1] + match_score

                s[i][j] = max(from_up, from_left, from_diag)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_left:
                    backtrack[i][j] = (i, j - 1)
                else:
                    backtrack[i][j] = (i - 1, j)

                if s[i][j] >= max_score:
                    max_score = s[i][j]
                    max_score_i = i
                    max_score_j = j

        v_align, w_align = self.backtracking(
            backtrack, v, w, max_score_i, max_score_j, 0, s
        )

        return v_align, w_align


import unittest


class TestAlignments(unittest.TestCase):
    def test_smith_waterman_simple_case(self):
        al = Alignments(gap_penalty=-1, match_score=1, missmatch_penalty=0)
        v = "OIUGNOISGRVISDIOGHIODSHFGMLSVEODRGMSOVFOGHLSDGMOVIDFHGS"
        w = "DSHGMLSEOD"
        self.assertEqual(("DSHFGMLSVEOD", "DSH-GMLS-EOD"), al.smith_waterman(v, w))

    def test_needleman_wunch_simple_case_mismatch_favoring(self):
        al = Alignments(gap_penalty=-100, missmatch_penalty=-10, match_score=2)
        v = "abcd"
        w = "abad"
        self.assertEqual(("abcd", "abad"), al.needleman_wunch(v, w))

    def test_needleman_wunch_simple_case_gap_favoring(self):
        al = Alignments(gap_penalty=-1, missmatch_penalty=-10, match_score=2)
        v = "abcd"
        w = "abd"
        self.assertEqual(("abcd", "ab-d"), al.needleman_wunch(v, w))

    def test_lcs_backtrack_same_words(self):
        al = Alignments()
        v = "abcd"
        w = "abcd"
        self.assertEqual(("abcd", 4), al.lcs_backtrack(v, w))

    def test_lcs_backtrack_same_length_words(self):
        al = Alignments()
        v = "abcd"
        w = "abed"
        self.assertEqual(("abd", 3), al.lcs_backtrack(v, w))

    def test_lcs_backtrack_different_length_words(self):
        al = Alignments()
        v = "abcd"
        w = "abd"
        self.assertEqual(("abd", 3), al.lcs_backtrack(v, w))

    def test_edit_distance(self):
        al = Alignments()
        v = "abcd"
        w = "abd"
        self.assertEqual(("abcd", "ab-d"), al.edit_distance(v, w))

    def test_edit_distance_different_param_order(self):
        al = Alignments()
        v = "abd"
        w = "abcd"
        self.assertEqual(("ab-d", "abcd"), al.edit_distance(v, w))

    def test_affine_gap_penalty(self):
        al = Alignments(
            gap_penalty=-2, match_score=2, missmatch_penalty=-2, sigma=-1, eps=-0.1
        )
        v = "AGTACGCA"
        w = "TATGC"

        self.assertEqual(("AGTACGCA", "--TATGC-"), al.affine_gap_penaly_alignment(v, w))


if __name__ == "__main__":
    unittest.main()
