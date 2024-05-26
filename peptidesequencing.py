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

import unittest


class PeptideSequencing:
    def __init__(self, amino_acid_masses):
        self.amino_acid_masses = amino_acid_masses

    def linear_spectrum(self, peptide):
        prefix_mass = [0]
        for aa in peptide:  # aa - amino acid
            amino_acid_mass = self.amino_acid_masses[aa]
            prefix_mass.append(prefix_mass[-1] + amino_acid_mass)

        n = len(peptide)
        spectrum = [0]
        for i in range(n):
            for j in range(i + 1, n + 1):
                spectrum.append(prefix_mass[j] - prefix_mass[i])

        spectrum.sort()
        return spectrum

    def cyclic_spectrum(self, peptide):
        prefix_mass = [0]
        for aa in peptide:  # aa - amino acid
            amino_acid_mass = self.amino_acid_masses[aa]
            prefix_mass.append(prefix_mass[-1] + amino_acid_mass)

        peptide_mass = prefix_mass[-1]  # ukupna masa peptida
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

    def expand(self, peptides):
        new_peptides = []
        for peptide in peptides:
            for aa in [
                available_aa
                for available_aa in self.amino_acid_masses.keys()
                if available_aa != ""
            ]:
                new_peptide = peptide + aa
                new_peptides.append(new_peptide)
        return new_peptides

    def mass(self, peptide_spectrum):
        return peptide_spectrum[-1]

    def consistent(self, peptide_spectrum, target_spectrum):
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

    def cyclopeptide_sequencing(self, spectrum):
        peptides = set([""])
        parent_mass = spectrum[-1]
        output = []

        while len(peptides) > 0:
            peptides = self.expand(peptides)
            to_remove = []
            for peptide in peptides:
                peptide_spectrum = self.cyclic_spectrum(peptide)

                if self.mass(peptide_spectrum) == parent_mass:
                    if peptide_spectrum == spectrum:
                        output.append(peptide)
                    to_remove.append(peptide)
                elif not self.consistent(self.linear_spectrum(peptide), spectrum):
                    to_remove.append(peptide)

            for peptide in to_remove:
                peptides.remove(peptide)

        return output


class TestPeptideSequencing(unittest.TestCase):
    def test_linear_spectrum(self):
        ps = PeptideSequencing(amino_acid_masses)
        print(ps.linear_spectrum("NQEL"))

    def test_cyclic_spectrum(self):
        ps = PeptideSequencing(amino_acid_masses)
        print(ps.cyclic_spectrum("NQEL"))

    def test_cyclopeptide_sequencing(self):
        ps = PeptideSequencing(amino_acid_masses)
        spectrum = [0, 113, 114, 128, 129, 227, 242, 242, 257, 355, 356, 370, 371, 484]
        print("Sequencing: ")
        print(ps.cyclopeptide_sequencing(spectrum))


if __name__ == "__main__":
    unittest.main()
