"""Tabela masa aminokiselina, uključujući masu 0 "praznog" proteina"""

amino_acid_masses = {
    "": 0,
    "G": 57,
    "A": 71,
    "S": 87,
    "P": 97,
    "V": 99,
    "T": 101,
    "C": 103,
    "I": 113,
    "L": 113,
    "N": 114,
    "D": 115,
    "K": 128,
    "Q": 128,
    "E": 129,
    "M": 131,
    "H": 137,
    "F": 147,
    "R": 156,
    "Y": 163,
    "W": 186,
}


class PeptideSequencing:
    def __init__(self, amino_acid_masses) -> None:
        self.amino_acid_masses = amino_acid_masses

    def linear_spectrum(self, peptide):
        prefix_mass = [0]
        spectrum = [0]
        n = len(peptide)

        for aa in peptide:
            prefix_mass.append(prefix_mass[-1] + self.amino_acid_masses[aa])

        for i in range(0, n):
            for j in range(i + 1, n + 1):
                spectrum.append(prefix_mass[j] - prefix_mass[i])

        return sorted(spectrum)

    def cyclic_spectrum(self, peptide):
        prefix_mass = [0]

        for aa in peptide:
            amino_acid_mass = self.amino_acid_masses[aa]
            prefix_mass.append(prefix_mass[-1] + amino_acid_mass)

        peptide_mass = prefix_mass[-1]
        n = len(peptide)
        spectrum = [0]

        for i in range(n):
            for j in range(i + 1, n + 1):
                fragment_mass = prefix_mass[j] - prefix_mass[i]
                spectrum.append(fragment_mass)
                if i > 0 and j < n:
                    spectrum.append(peptide_mass - fragment_mass)

        spectrum.sort()
        return spectrum

    def is_consistent(self, peptide_spectrum, target_spectrum):
        n = len(peptide_spectrum)
        m = len(target_spectrum)

        i = 0
        j = 0

        while i < n:
            if peptide_spectrum[i] == target_spectrum[j]:
                i += 1

            elif peptide_spectrum[i] < target_spectrum[j]:
                return False

            j += 1
            if j == m:
                return i == n

        return True

    def mass(self, spectrum):
        return spectrum[-1]

    def expand(self, peptides):
        available_amino_acids = [aa for aa in self.amino_acid_masses.keys() if aa != ""]

        new_peptides = []
        for peptide in peptides:
            for aa in available_amino_acids:
                new_peptides.append(peptide + aa)

        return new_peptides

    def cyclopeptide_sequencing(self, spectrum):
        output = []
        peptides = set([""])

        parent_mass = self.mass(spectrum)

        while len(peptides) > 0:
            peptides = self.expand(peptides)
            to_remove = []

            for peptide in peptides:
                peptide_spectrum = self.cyclic_spectrum(peptide)
                if self.mass(peptide_spectrum) == parent_mass:
                    if peptide_spectrum == spectrum:
                        output.append(peptide)
                    to_remove.append(peptide)

                elif not self.is_consistent(self.linear_spectrum(peptide), spectrum):
                    to_remove.append(peptide)

            for p in to_remove:
                peptides.remove(p)

        return output


import unittest


class TestPeptideSeqencing(unittest.TestCase):
    def test_linerar_spectrum(self):
        ps = PeptideSequencing(amino_acid_masses)

        peptide = "NQEL"

        self.assertEqual(
            [0, 113, 114, 128, 129, 242, 242, 257, 370, 371, 484],
            ps.linear_spectrum(peptide),
        )

    def test_cyclopeptide_sequencing(self):
        ps = PeptideSequencing(amino_acid_masses)
        peptide = "NQEL"
        spectrum = ps.cyclic_spectrum(peptide)

        self.assertEqual("NQEL", ps.cyclopeptide_sequencing(spectrum))


if __name__ == "__main__":
    unittest.main()
