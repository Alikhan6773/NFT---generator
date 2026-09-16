import os

from models.collection import Collection
from models.layer import Layer
from models.trait import Trait


def load_collection(folder_path):

    collection = Collection("Meta Warriors")

    folders = os.listdir(folder_path)

    for folder in folders:

        layer = Layer(folder)

        folder_full_path = os.path.join(folder_path, folder)

        files = os.listdir(folder_full_path)

        for file in files:

            trait_name = os.path.splitext(file)[0]

            trait = Trait(
                trait_name,
                os.path.join(folder_full_path, file)
            )

            layer.add_trait(trait)

        collection.add_layer(layer)

    return collection