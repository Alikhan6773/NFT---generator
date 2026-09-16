class DuplicateChecker:

    def __init__(self):

        self.used = set()

    def exists(self, dna):

        return dna in self.used

    def add(self, dna):

        self.used.add(dna)