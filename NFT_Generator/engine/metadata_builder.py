import json
import os


class MetadataBuilder:

    def build(
        self,
        nft_number,
        selected_traits,
        dna,
        output_folder
    ):

        metadata = {

            "name": f"NFT #{nft_number}",

            "image": f"{nft_number:04}.png",

            "dna": dna,

            "attributes": []

        }

        for layer_name, trait_name in selected_traits:

            metadata["attributes"].append({

                "trait_type": layer_name,

                "value": trait_name

            })

        path = os.path.join(

            output_folder,

            f"{nft_number:04}.json"

        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(

                metadata,

                file,

                indent=4,

                ensure_ascii=False

            )