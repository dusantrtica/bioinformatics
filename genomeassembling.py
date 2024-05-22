class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
    
    def __str__(self):
        return f'{self.adjacency_list}'

class DeBrujin(Graph):
    def __init__(self, reads, k):
        kmers = self.get_kmers(reads, k) # array of triples
        adjacency_list = {}

        for kmer in kmers:
            u = kmer[:-1]
            v = kmer[1:]
            if u not in adjacency_list:
                adjacency_list[u] = []

            if v not in adjacency_list:
                adjacency_list[u] =[]

            adjacency_list[u].append(v)
        
        super().__init__(adjacency_list=adjacency_list)


    def get_kmers(self, reads, k):
        kmers =[]
        for read in reads:
            n = len(read)
            for i in range(n-k+1):
                kmer = read[i:i+k]
                kmers.append(kmer)
        return kmers

import unittest

class TestDebrujin(unittest.TestCase):
    def test_debrujin(self):
        reads = ['AATT']
        dg = DeBrujin(reads=reads, k=3)
        self.assertEqual("{'AA': ['AT'], 'AT': ['TT']}", str(dg))
        G = {
        'A': ['B'],
        'B': ['C', 'E'],
        'C': ['D'],
        'D': ['B', 'A'],
        'E': ['G', 'F'],
        'F': ['G'],
        'G': ['D', 'E']
    }

if __name__ == '__main__':
    unittest.main()