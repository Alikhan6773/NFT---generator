class Collection:

    def __init__(self, name):

        self.name = name
        self.layers = []

    def add_layer(self, layer):

        self.layers.append(layer)

    def show_collection(self):

        print(f"\nCollection: {self.name}")

        print("\nLayers:")

        for layer in self.layers:

            print(f"- {layer.name}")

    # متد جدید
    def show_details(self):

        print(f"\nCollection: {self.name}")

        for layer in self.layers:

            print(f"\nLayer: {layer.name}")

            for trait in layer.traits:

                print(f"   - {trait.name}")