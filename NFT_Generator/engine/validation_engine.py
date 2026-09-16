import os


class ValidationEngine:

    def __init__(self):

        self.errors = []
        self.warnings = []
        self.info = []

    # ==========================================
    # Assets
    # ==========================================

    def validate_assets_folder(self, folder_path):

        if not os.path.exists(folder_path):

            self.errors.append(
                "Assets folder not found."
            )

    # ==========================================
    # Layers
    # ==========================================

    def validate_layers(self, collection):

        self.info.append(
            f"Layers Found: {len(collection.layers)}"
        )

        for layer in collection.layers:

            if len(layer.traits) == 0:

                self.errors.append(
                    f'Layer "{layer.name}" is empty.'
                )

    # ==========================================
    # Rarity / Distribution
    # ==========================================

    def validate_rarity(
        self,
        collection,
        collection_size
    ):

        for layer in collection.layers:

            if not layer.traits:

                continue

            mode = layer.traits[0].mode

            # ==================================
            # Check mixed modes
            # ==================================

            for trait in layer.traits:

                if trait.mode != mode:

                    self.errors.append(
                        f'Layer "{layer.name}" has '
                        f'mixed distribution modes.'
                    )

                    break

            # ==================================
            # COUNT
            # ==================================

            if mode == "count":

                total_count = 0

                for trait in layer.traits:

                    value = trait.value

                    if value < 0:

                        self.errors.append(
                            f'Count for trait '
                            f'"{trait.name}" in layer '
                            f'"{layer.name}" cannot '
                            f'be negative.'
                        )

                        continue

                    total_count += value

                if total_count > collection_size:

                    self.errors.append(
                        f'Count total for layer '
                        f'"{layer.name}" exceeds '
                        f'collection size '
                        f'({total_count} > '
                        f'{collection_size}).'
                    )

            # ==================================
            # PERCENTAGE
            # ==================================

            elif mode == "percentage":

                total_percentage = 0

                for trait in layer.traits:

                    value = trait.value

                    if value < 0:

                        self.errors.append(
                            f'Percentage for trait '
                            f'"{trait.name}" in layer '
                            f'"{layer.name}" cannot '
                            f'be negative.'
                        )

                        continue

                    if value > 100:

                        self.errors.append(
                            f'Percentage for trait '
                            f'"{trait.name}" in layer '
                            f'"{layer.name}" cannot '
                            f'exceed 100%.'
                        )

                        continue

                    total_percentage += value

                if total_percentage > 100:

                    self.errors.append(
                        f'Percentage total for layer '
                        f'"{layer.name}" exceeds '
                        f'100% '
                        f'({total_percentage}%).'
                    )

            # ==================================
            # AUTO
            # ==================================

            elif mode == "auto":

                pass

            # ==================================
            # Invalid Mode
            # ==================================

            else:

                self.errors.append(
                    f'Invalid distribution mode '
                    f'"{mode}" in layer '
                    f'"{layer.name}". '
                    f'Allowed modes: '
                    f'count, percentage, auto.'
                )

    # ==========================================
    # Report
    # ==========================================

    def print_report(self):

        print(
            "\n========== Validation Report ==========\n"
        )

        for item in self.info:

            print(
                f"ℹ️ {item}"
            )

        for item in self.warnings:

            print(
                f"⚠️ {item}"
            )

        for item in self.errors:

            print(
                f"❌ {item}"
            )

        if len(self.errors) == 0:

            print(
                "\n✅ Validation Passed"
            )