class Alignments:

    def match(self, x, y):
        return int(x == y)

    def backtracking(self, backtrack, v, w, i, j):
        v_align = ""  #  = ["" for _ in range(num_elements)]
        w_align = ""
        while backtrack[i][j] != None:
            (i_new, j_new) = backtrack[i][j]
            if (i_new, j_new) == (i - 1, j - 1):
                v_align = v[i - 1] + v_align
                w_align = w[j - 1] + w_align

            if (i_new, j_new) == (i - 1, j):
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
                from_up = s[i - i][j] + 1
                from_left = s[i][j - 1] + 1
                from_diag = s[i - 1][j - 1] + (1 - match)
                s[i][j] = min(from_up, from_left, from_diag)

                if s[i][j] == from_diag:
                    backtrack[i][j] = (i - 1, j - 1)
                elif s[i][j] == from_up:
                    backtrack[i][j] = (i - 1, j)
                else:
                    backtrack[i][j] = (i, j - 1)

        v_align, w_align = self.backtracking(
            backtrack,
            v,
            w,
            n - 1,
            m - 1,
        )
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
                from_up = s[i - i][j]
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


import unittest


class TestAlignment(unittest.TestCase):
    def test_lcs_backtrack(self):
        alignmnent = Alignments()
        self.assertEqual("ABD", alignmnent.lcs_backtrack("ABCD", "ABED"))

    def test_edit_distance(self):
        alignmnent = Alignments()
        self.assertEqual("ABD", alignmnent.edit_distance("ABD", "ABCD"))


if __name__ == "__main__":
    unittest.main()
