class VerificationEngine:

    def __init__(self, collection):

        self.collection = collection

        self.errors = []
        self.info = []

    # ==========================================
    # Collection Size
    # ==========================================

    def verify_collection_size(self, expected_size):

        actual_size = len(self.collection)

        self.info.append(
            f"Collection Size: "
            f"{actual_size} / {expected_size}"
        )

        if actual_size != expected_size:

            self.errors.append(
                f"Collection size mismatch: "
                f"{actual_size} instead of "
                f"{expected_size}."
            )

    # ==========================================
    # Unique DNA
    # ==========================================

    def verify_unique_dna(self):

        dna_list = [
            nft.dna
            for nft in self.collection
        ]

        unique_dna = set(dna_list)

        duplicates = (
            len(dna_list)
            - len(unique_dna)
        )

        self.info.append(
            f"Unique DNA: "
            f"{len(unique_dna)} / {len(dna_list)}"
        )

        self.info.append(
            f"Duplicates: {duplicates}"
        )

        if duplicates > 0:

            self.errors.append(
                f"Found {duplicates} "
                "duplicate DNA values."
            )

    # ==========================================
    # Trait Count
    # ==========================================

    def verify_trait_count(
        self,
        layer_name,
        trait_name,
        expected_count
    ):

        actual_count = 0

        for nft in self.collection:

            for layer, trait in nft.attributes:

                if (
                    layer == layer_name
                    and trait == trait_name
                ):

                    actual_count += 1

        self.info.append(
            f"{layer_name}.{trait_name}: "
            f"{actual_count} / "
            f"{expected_count}"
        )

        if actual_count != expected_count:

            self.errors.append(
                f"Trait count mismatch for "
                f"'{layer_name}.{trait_name}': "
                f"{actual_count} instead of "
                f"{expected_count}."
            )

    # ==========================================
    # Rule Verification
    # ==========================================

    def verify_rules(self, rule_engine):

        forbidden_violations = 0
        required_violations = 0

        for nft in self.collection:

            selected_traits = {
                layer: trait
                for layer, trait
                in nft.attributes
            }

            if not rule_engine._check_forbidden(
                selected_traits
            ):

                forbidden_violations += 1

            if not rule_engine._check_required(
                selected_traits
            ):

                required_violations += 1

        self.info.append(
            f"Forbidden Violations: "
            f"{forbidden_violations}"
        )

        self.info.append(
            f"Required Violations: "
            f"{required_violations}"
        )

        if forbidden_violations > 0:

            self.errors.append(
                f"Found {forbidden_violations} "
                "forbidden rule violations."
            )

        if required_violations > 0:

            self.errors.append(
                f"Found {required_violations} "
                "required rule violations."
            )

    # ==========================================
    # Report
    # ==========================================

    def print_report(self):

        print(
            "\n========== "
            "Collection Verification "
            "==========\n"
        )

        for item in self.info:

            print(
                f"ℹ️ {item}"
            )

        for error in self.errors:

            print(
                f"❌ {error}"
            )

        if not self.errors:

            print(
                "\n🎉 COLLECTION VERIFIED"
            )

        else:

            print(
                "\n❌ COLLECTION VERIFICATION FAILED"
            )

        print(
            "\n========================================\n"
        )

    # ==========================================
    # Run
    # ==========================================

    def run(
        self,
        expected_size,
        rule_engine=None,
        trait_expectations=None
    ):

        self.verify_collection_size(
            expected_size
        )

        self.verify_unique_dna()

        if trait_expectations:

            for expectation in trait_expectations:

                self.verify_trait_count(
                    layer_name=expectation["layer"],
                    trait_name=expectation["trait"],
                    expected_count=expectation["count"]
                )

        if rule_engine is not None:

            self.verify_rules(
                rule_engine
            )

        self.print_report()

        return not self.errors