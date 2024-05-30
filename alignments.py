class Alignments:
    def __init__(self, gap_penalty=-1, match_score=1, missmatch_penalty=0):
        self.GAP_PENALTY = gap_penalty
        self.MATCH_SCORE = match_score
        self.MISSMATCH_PENALTY = missmatch_penalty

    def match(self, x, y):
        return int(x == y)

    def backtracking(self, backtrack, v, w, i, j, s, stop_condition=None):
        v_align = ""  #  = ["" for _ in range(num_elements)]
        w_align = ""
        while backtrack[i][j] != None and s[i][j] != stop_condition:
            (i_new, j_new) = backtrack[i][j]
            if (i_new, j_new) == (i - 1, j - 1):
                v_align = v[i - 1] + v_align
                w_align = w[j - 1] + w_align

            elif (i_new, j_new) == (i - 1, j):
                w_align = "-" + w_align
            else:
                v_align = "-" + v_align
            i = i_new
            j = j_new

        return v_align, w_align

    def edit_distance(self, v, w):
        n = len(v) + 1
        m = len(w) + 1
        s = [[0 for j in range(m)] for i in range(n)]
        backtrack = [[None for j in range(m)] for i in range(n)]

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
                from_diag = s[i - 1][j - 1] + (1 - match)
                s[i][j] = min(from_up, from_left, from_diag)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_up:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        v_align, w_align = self.backtracking(backtrack, v, w, n - 1, m - 1, s)
        return s[n - 1][m - 1], v_align, w_align

    # Longest commont subsequence
    def lcs_backtrack(self, v, w):
        n = len(v) + 1
        m = len(w) + 1
        s = [[0 for j in range(m)] for i in range(n)]
        backtrack = [[None for j in range(m)] for i in range(n)]

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

        lcs = ["" for _ in range(s[n - 1][m - 1])]
        i = n - 1
        j = m - 1
        k = s[n - 1][m - 1] - 1
        while backtrack[i][j] != None:
            (i_new, j_new) = backtrack[i][j]
            if (i_new, j_new) == (i - 1, j - 1):
                lcs[k] = v[i - 1]
                k -= 1
            i = i_new
            j = j_new

        return "".join(lcs)

    # Globalno poravnanje
    def needleman_wunsch(self, v, w):
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

                from_diag = s[i - 1][j - 1] + match_score
                from_up = s[i - 1][j] + self.GAP_PENALTY
                from_left = s[i][j - 1] + self.GAP_PENALTY
                s[i][j] = max(from_diag, from_up, from_left)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_left:
                    backtrack[i][j] = (i, j - 1)
                else:
                    backtrack[i][j] = (i - 1, j)

        v_align, w_align = self.backtracking(backtrack, v, w, n - 1, m - 1, s)
        return s[n - 1][m - 1], v_align, w_align

    # Lokalno poravnanje
    def smith_waterman(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        s = [[0 for _ in range(m)] for _ in range(n)]
        backtrack = [[None for _ in range(m)] for _ in range(n)]

        for i in range(1, n):
            backtrack[i][0] = (i - 1, 0)
        for j in range(1, m):
            backtrack[0][j] = (0, j - 1)

        max_score = 0
        max_score_pos = (0, 0)

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

                s[i][j] = max(from_diag, from_up, from_left, 0)

                if s[i][j] > max_score:
                    max_score = s[i][j]
                    max_score_pos = (i, j)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_up:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        (i, j) = max_score_pos
        v_align, w_align = self.backtracking(backtrack, v, w, i, j, s, 0)

        return (max_score, v_align, w_align)


import unittest


class TestAlignment(unittest.TestCase):

    def test_smith_waterman(self):
        alignments = Alignments(gap_penalty=-1, match_score=1, missmatch_penalty=0)
        v = "ABCAD"
        w = "ABDE"
        self.assertEqual((2, "AB", "AB"), alignments.smith_waterman(v, w))

    def test_smit_waterman_with_mismatch(self):
        al = Alignments(gap_penalty=-1, match_score=1, missmatch_penalty=0)
        v = "OIUGNOISGRVISDIOGHIODSHFGMLSVEODRGMSOVFOGHLSDGMOVIDFHGS"
        w = "DSHGMLSEOD"
        self.assertEqual((8, "DSHGMLSEOD", "DSH-GMLS-EOD"), al.smith_waterman(v, w))

    def test_needleman_wunsch(self):
        alignments = Alignments(gap_penalty=-1, match_score=1, missmatch_penalty=0)
        v = "ABCAD"
        w = "ABDE"

        self.assertEqual((1, "ABAD", "AB-DE"), alignments.needleman_wunsch(v, w))

    def test_lcs_backtrack(self):
        alignmnent = Alignments()
        self.assertEqual("ABD", alignmnent.lcs_backtrack("ABCD", "ABED"))

    def test_edit_distance(self):
        alignmnent = Alignments()
        self.assertEqual("AB-D", alignmnent.edit_distance("ABD", "ABCD")[1])


if __name__ == "__main__":
    unittest.main()
