import unittest

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
    def __init__(self, amino_acid_mass) -> None:
        self.amino_acid_masses = amino_acid_masses

    def linear_spectrum(self, peptide):
        spectrum = [0]
        for char in peptide:
            spectrum.append(spectrum[-1] + self.amino_acid_masses[char])

        peptide_spectrum = []
        n = len(peptide)
        for i in range(n):
            for j in range(i + 1, n + 1):
                peptide_spectrum.append(spectrum[j] - spectrum[i])

        return sorted(peptide_spectrum)

    def expand(self, peptides):
        pass

    def cyclic_spectrum(self, peptide):
        pass

    def mass(self, spectrum):
        return spectrum[-1]

    def is_consistent(self, spectrum1, spectrum2):
        n = len(spectrum1)
        m = len(spectrum2)

        while True:
            break

    def cyclopeptide_sequencing(self, spectrum):
        peptides = set([""])
        parent_mass = spectrum[-1]
        output = []
        while len(peptides) > 0:
            to_remove = []
            peptides = self.expand(peptides)
            for peptide in peptides:
                peptide_spectrum = self.cyclic_spectrum(peptide)
                if self.mass(peptide_spectrum) == parent_mass:
                    if self.is_consistent(peptide_spectrum, spectrum):
                        output.append(peptide)
                    to_remove.append(peptide)

                else:
                    to_remove.append(peptide)

            for peptide_to_remove in to_remove:
                peptides.remove(peptide_to_remove)

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


import ctypes


def whoops():
    inc_ref = ctypes.pythonapi.Py_IncRef
    inc_ref.argtypes = [ctypes.py_object]
    inc_ref.resttype = None
    obj = list(range(10_000_000))
    inc_ref(obj)

    whoops()
