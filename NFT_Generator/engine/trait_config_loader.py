import json


class TraitConfigLoader:

    def load(self, config_path):

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def apply(self, collection, config):

        for layer in collection.layers:

            layer_config = config.get(
                layer.name,
                {}
            )

            mode = layer_config.get(
                "mode",
                "auto"
            )

            traits_config = layer_config.get(
                "traits",
                {}
            )

            for trait in layer.traits:

                trait.mode = mode

                if trait.name in traits_config:

                    trait.value = traits_config[
                        trait.name
                    ]

                else:

                    trait.value = 0