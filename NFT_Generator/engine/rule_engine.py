class RuleEngine:

    def __init__(self, rules):

        self.forbidden = rules.get(
            "forbidden",
            []
        )

        self.required = rules.get(
            "required",
            []
        )

    def validate(self, selected_traits):

        if not self._check_forbidden(
            selected_traits
        ):

            return False

        if not self._check_required(
            selected_traits
        ):

            return False

        return True

    # ==========================================
    # Forbidden
    # ==========================================

    def _check_forbidden(
        self,
        selected_traits
    ):

        for rule in self.forbidden:

            trait_a = rule["trait"]
            trait_b = rule["with"]

            if (
                self._has_trait(
                    selected_traits,
                    trait_a
                )
                and
                self._has_trait(
                    selected_traits,
                    trait_b
                )
            ):

                return False

        return True

    # ==========================================
    # Required
    # ==========================================

    def _check_required(
        self,
        selected_traits
    ):

        for rule in self.required:

            trait_a = rule["trait"]
            trait_b = rule["with"]

            if self._has_trait(
                selected_traits,
                trait_a
            ):

                if not self._has_trait(
                    selected_traits,
                    trait_b
                ):

                    return False

        return True

    # ==========================================
    # Trait Lookup
    # ==========================================

    def _has_trait(
        self,
        selected_traits,
        target
    ):

        if "." not in target:

            return False

        layer_name, trait_name = (
            target.split(
                ".",
                1
            )
        )

        selected = selected_traits.get(
            layer_name
        )

        if selected is None:

            return False

        if hasattr(
            selected,
            "name"
        ):

            return selected.name == trait_name

        return selected == trait_name