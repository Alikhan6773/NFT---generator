class Layer:

    def __init__(self, name):

        self.name = name

        self.traits = []
        self.enabled = True

        self.order = 0

    def add_trait(self, trait):

        self.traits.append(trait)

    def show_traits(self):

        print(f"\nLayer: {self.name}")

        for trait in self.traits:

            print(f"- {trait.name}")