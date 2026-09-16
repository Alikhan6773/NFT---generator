import random


class TraitSelector:

    def __init__(self, traits):

        self.traits = []
        self.pending_index = None

        self._build_traits(traits)

    def _build_traits(self, traits):

        counts = {}

        for trait in traits:

            key = (
                trait.name,
                trait.file_path
            )

            if key not in counts:

                counts[key] = {
                    "trait": trait,
                    "remaining": 0
                }

            counts[key]["remaining"] += 1

        self.traits = list(counts.values())

    def preview(self):

        available = [
            item
            for item in self.traits
            if item["remaining"] > 0
        ]

        if not available:

            self.pending_index = None

            return None

        item = random.choice(available)

        self.pending_index = self.traits.index(item)

        return item["trait"]

    def advance(self):

        return self.preview() is not None

    def commit(self):

        if self.pending_index is None:

            return

        item = self.traits[self.pending_index]

        item["remaining"] -= 1

        self.pending_index = None

        self.traits = [
            item
            for item in self.traits
            if item["remaining"] > 0
        ]

    def rollback(self):

        self.pending_index = None