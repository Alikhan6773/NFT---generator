class DNAEngine:

    def create(self, nft):

        parts = []

        for layer_name, trait_name in nft.attributes:

            parts.append(f"{layer_name}={trait_name}")

        return "|".join(parts)