class Alignments:
    def __init__(
        self, gap_penalty=-1, match_score=1, missmatch_penalty=0, sigma=-1, eps=-0.5
    ):
        self.GAP_PENALTY = gap_penalty
        self.MATCH_SCORE = match_score
        self.MISSMATCH_PENALTY = missmatch_penalty
        self.SIGMA = sigma
        self.EPS = eps

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
                elif s[i][j] == from_up:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

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

    def needleman_wunsch_last_line(self, v, w):
        n = len(v) + 1
        m = len(w) + 1

        s = [[0 for _ in range(m)] for _ in range(2)]
        # inicijalizacija
        for j in range(m):
            s[0][j] = j * self.GAP_PENALTY

        for i in range(1, n):
            s[1][0] = i * self.GAP_PENALTY

            for j in range(1, m):
                match = self.match(v[i - 1], w[j - 1])
                match_score = 0
                if match == 1:
                    match_score = self.MATCH_SCORE
                else:
                    match_score = self.MISSMATCH_PENALTY

                from_up = s[0][j] + self.GAP_PENALTY
                from_left = s[1][j - 1] + self.GAP_PENALTY
                from_diag = s[0][j - 1] + match_score

                s[1][j] = max(from_diag, from_up, from_left)

            s[0][:] = s[1][:]
        return s[1]

    def hirschberg(self, v, w):
        v_align = ""
        w_align = ""
        n = len(v)
        m = len(w)

        if n == 0:
            v_align = m * "-"
            w_align = w
        elif m == 0:
            v_align = v
            w_align = n * "-"
        elif n == 1 or m == 1:
            _, v_align, w_align = self.needleman_wunsch(v, w)
        else:
            x_mid = n // 2
            score_l = self.needleman_wunsch_last_line(v[:x_mid], w)
            score_r = self.needleman_wunsch_last_line(v[x_mid:][::-1], w[::-1])[::-1]

            max_score = float("-inf")
            y_mid = None  # Max score indx

            for i in range(m):
                curr_score = score_l[i] + score_r[i]
                if curr_score > max_score:
                    max_score = curr_score
                    y_mid = i

            v1_align, w1_align = self.hirschberg(v[:x_mid], w[:y_mid])
            v2_align, w2_align = self.hirschberg(v[x_mid:], w[y_mid:])

            v_align = v1_align + v2_align
            w_align = w1_align + w2_align

        return v_align, w_align

    def affine_gap_penaly_alignment(self, v, w):
        n = len(v) + 1
        m = len(w) + 1
        middle = [[0 for _ in range(m)] for _ in range(n)]
        upper = [[0 for _ in range(m)] for _ in range(n)]
        lower = [[0 for _ in range(m)] for _ in range(n)]

        backtrack = [[None for _ in range(m)] for _ in range(n)]

        # initialization
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

                if middle[i][j] == middle[i - 1][j - 1] + match_score:  # from_diag
                    backtrack[i][j] = (i - 1, j - 1)
                elif middle[i][j] == lower[i][j]:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        v_align, w_align = self.backtracking(
            backtrack, v, w, n - 1, m - 1, middle, None
        )
        print(backtrack)
        return middle[n - 1][m - 1], v_align, w_align


import unittest


class TestAlignment(unittest.TestCase):
    def test_affine_gap_penaly_alignment(self):
        al = Alignments(gap_penalty=-2, match_score=2, missmatch_penalty=-1)
        v = "AGTACGCA"
        w = "TATGC"
        self.assertEqual(
            (6, "ACTACGC", "--TATGC-"), al.affine_gap_penaly_alignment(v, w)
        )

    def test_hirschberg(self):
        alignment = Alignments(-2, 2, -1)
        v = "AGTACGCA"
        w = "TATGC"
        self.assertEqual(("AGTACGC", "--TATGC-"), alignment.hirschberg(v, w))

    def test_needleman_wunsch_last_line(self):
        alignments = Alignments(gap_penalty=-1, match_score=1, missmatch_penalty=0)
        v = "ABCAD"
        w = "ABDE"
        self.assertEqual(
            [-5, -3, -1, 1, 1], alignments.needleman_wunsch_last_line(v, w)
        )

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

    def test_needleman_wunsch_from_wiki_example(self):
        alignments = Alignments(gap_penalty=-2, match_score=2, missmatch_penalty=-1)
        v = "AGTACGCA"
        w = "TATGC"

        self.assertEqual((1, "TACGC", "--TATGC-"), alignments.needleman_wunsch(v, w))

    def test_lcs_backtrack(self):
        alignmnent = Alignments()
        self.assertEqual("ABD", alignmnent.lcs_backtrack("ABCD", "ABED"))

    def test_edit_distance(self):
        alignmnent = Alignments()
        self.assertEqual("AB-D", alignmnent.edit_distance("ABD", "ABCD")[1])


if __name__ == "__main__":
    unittest.main()
