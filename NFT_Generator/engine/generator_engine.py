import random

from models.generated_nft import GeneratedNFT


class GeneratorEngine:

    def __init__(
        self,
        queues,
        rule_engine=None
    ):
        self.queues = queues
        self.rule_engine = rule_engine

        self.pending = None

        self.collection = []
        self.current_index = 0

        self._prepared = False

    # ==========================================
    # Build Trait Pools
    # ==========================================

    def _build_pools(self):

        pools = {}
        collection_size = 0

        for layer_name, selector in self.queues.items():

            pool = []

            for item in selector.traits:

                trait = item["trait"]
                remaining = item["remaining"]

                for _ in range(remaining):

                    pool.append(trait)

            if not pool:

                raise Exception(
                    f"Layer '{layer_name}' has no traits."
                )

            pools[layer_name] = pool

            if collection_size == 0:

                collection_size = len(pool)

            elif len(pool) != collection_size:

                raise Exception(
                    f"Layer '{layer_name}' has "
                    f"{len(pool)} traits instead of "
                    f"{collection_size}."
                )

        return pools, collection_size

    # ==========================================
    # Rule Helpers
    # ==========================================

    def _required_rules(self):

        if self.rule_engine is None:

            return []

        return self.rule_engine.required

    def _forbidden_rules(self):

        if self.rule_engine is None:

            return []

        return self.rule_engine.forbidden

    # ==========================================
    # Parse Trait Reference
    # ==========================================

    def _parse_trait_ref(self, value):

        if "." not in value:

            return None, None

        return value.split(".", 1)

    # ==========================================
    # Build Layer Assignments
    # ==========================================

    def _build_assignments(
        self,
        pools,
        collection_size
    ):

        assignments = {
            layer_name: [None] * collection_size
            for layer_name in pools
        }

        reserved = {
            layer_name: set()
            for layer_name in pools
        }

        # ======================================
        # Required Rules
        # ======================================

        for rule in self._required_rules():

            source_ref = rule["trait"]
            target_ref = rule["with"]

            source_layer, source_trait = (
                self._parse_trait_ref(
                    source_ref
                )
            )

            target_layer, target_trait = (
                self._parse_trait_ref(
                    target_ref
                )
            )

            if (
                source_layer is None
                or target_layer is None
            ):

                continue

            if source_layer not in pools:

                raise Exception(
                    f"Required rule references "
                    f"unknown layer "
                    f"'{source_layer}'."
                )

            if target_layer not in pools:

                raise Exception(
                    f"Required rule references "
                    f"unknown layer "
                    f"'{target_layer}'."
                )

            source_pool = pools[
                source_layer
            ]

            target_pool = pools[
                target_layer
            ]

            source_traits = [
                trait
                for trait in source_pool
                if trait.name == source_trait
            ]

            target_traits = [
                trait
                for trait in target_pool
                if trait.name == target_trait
            ]

            source_count = len(
                source_traits
            )

            target_count = len(
                target_traits
            )

            if target_count < source_count:

                raise Exception(
                    f"Required rule cannot be "
                    f"satisfied: "
                    f"{source_ref} requires "
                    f"{target_ref}, but "
                    f"{target_count} target "
                    f"traits exist for "
                    f"{source_count} source "
                    f"traits."
                )

            # ----------------------------------
            # Find source slots
            # ----------------------------------

            available_slots = [
                index
                for index in range(collection_size)
                if assignments[
                    source_layer
                ][index] is None
            ]

            if len(available_slots) < source_count:

                raise Exception(
                    f"Unable to reserve enough "
                    f"slots for rule "
                    f"'{source_ref} -> "
                    f"{target_ref}'."
                )

            random.shuffle(
                available_slots
            )

            source_slots = (
                available_slots[
                    :source_count
                ]
            )

            # ----------------------------------
            # Assign source + target together
            # ----------------------------------

            for slot in source_slots:

                source_trait_object = (
                    random.choice(
                        source_traits
                    )
                )

                assignments[
                    source_layer
                ][slot] = (
                    source_trait_object
                )

                reserved[
                    source_layer
                ].add(slot)

                # --------------------------------
                # Target trait
                # --------------------------------

                target_trait_object = (
                    random.choice(
                        target_traits
                    )
                )

                assignments[
                    target_layer
                ][slot] = (
                    target_trait_object
                )

                reserved[
                    target_layer
                ].add(slot)

        # ======================================
        # Fill Remaining Layers
        # ======================================

        for layer_name, pool in pools.items():

            remaining_traits = list(pool)

            # Remove traits already assigned
            for trait in assignments[layer_name]:

                if trait is None:
                    continue

                try:

                    remaining_traits.remove(
                        trait
                    )

                except ValueError:

                    pass

            free_slots = [
                index
                for index in range(collection_size)
                if assignments[
                    layer_name
                ][index] is None
            ]

            random.shuffle(
                remaining_traits
            )

            if len(remaining_traits) != len(
                free_slots
            ):

                raise Exception(
                    f"Trait allocation mismatch "
                    f"in layer "
                    f"'{layer_name}'."
                )

            for slot, trait in zip(
                free_slots,
                remaining_traits
            ):

                assignments[
                    layer_name
                ][slot] = trait

        return assignments, reserved

    # ==========================================
    # Build NFT From Slot
    # ==========================================

    def _build_nft_from_slot(
        self,
        assignments,
        slot
    ):

        nft = GeneratedNFT()

        for layer_name in assignments:

            trait = assignments[
                layer_name
            ][slot]

            if trait is None:

                return None

            nft.image_paths.append(
                trait.file_path
            )

            nft.attributes.append(
                (
                    layer_name,
                    trait.name
                )
            )

        dna_parts = []

        for layer_name, trait_name in nft.attributes:

            dna_parts.append(
                f"{layer_name}={trait_name}"
            )

        nft.dna = "|".join(
            dna_parts
        )

        return nft

    # ==========================================
    # Check Rules
    # ==========================================

    def _is_valid_nft(
        self,
        nft
    ):

        if self.rule_engine is None:

            return True

        selected_traits = {
            layer: trait
            for layer, trait
            in nft.attributes
        }

        return self.rule_engine.validate(
            selected_traits
        )

    # ==========================================
    # Try To Repair Forbidden Rules
    # ==========================================

    def _repair_forbidden(
        self,
        assignments,
        reserved,
        collection_size
    ):

        if self.rule_engine is None:

            return True

        max_rounds = 1000

        for _ in range(max_rounds):

            violations = []

            for slot in range(
                collection_size
            ):

                nft = self._build_nft_from_slot(
                    assignments,
                    slot
                )

                if nft is None:

                    return False

                if not self._is_valid_nft(
                    nft
                ):

                    violations.append(
                        slot
                    )

            if not violations:

                return True

            repaired = False

            # ----------------------------------
            # Try swapping one layer
            # ----------------------------------

            for bad_slot in violations:

                for rule in self._forbidden_rules():

                    layer_a, trait_a = (
                        self._parse_trait_ref(
                            rule["trait"]
                        )
                    )

                    layer_b, trait_b = (
                        self._parse_trait_ref(
                            rule["with"]
                        )
                    )

                    if (
                        layer_a not in assignments
                        or layer_b not in assignments
                    ):

                        continue

                    bad_a = assignments[
                        layer_a
                    ][bad_slot]

                    bad_b = assignments[
                        layer_b
                    ][bad_slot]

                    if (
                        bad_a.name != trait_a
                        or bad_b.name != trait_b
                    ):

                        continue

                    # --------------------------------
                    # Swap target with another slot
                    # --------------------------------

                    candidate_slots = [
                        slot
                        for slot in range(
                            collection_size
                        )
                        if slot != bad_slot
                    ]

                    random.shuffle(
                        candidate_slots
                    )

                    for other_slot in (
                        candidate_slots
                    ):

                        # Do not break Required slots
                        if (
                            other_slot
                            in reserved[
                                layer_b
                            ]
                        ):

                            continue

                        other_trait = assignments[
                            layer_b
                        ][other_slot]

                        if (
                            other_trait.name
                            == trait_b
                        ):

                            continue

                        assignments[
                            layer_b
                        ][bad_slot], \
                        assignments[
                            layer_b
                        ][other_slot] = (
                            assignments[
                                layer_b
                            ][other_slot],
                            assignments[
                                layer_b
                            ][bad_slot]
                        )

                        new_bad_nft = (
                            self._build_nft_from_slot(
                                assignments,
                                bad_slot
                            )
                        )

                        if (
                            new_bad_nft is not None
                            and self._is_valid_nft(
                                new_bad_nft
                            )
                        ):

                            repaired = True
                            break

                        # Undo swap
                        assignments[
                            layer_b
                        ][bad_slot], \
                        assignments[
                            layer_b
                        ][other_slot] = (
                            assignments[
                                layer_b
                            ][other_slot],
                            assignments[
                                layer_b
                            ][bad_slot]
                        )

                    if repaired:
                        break

                if repaired:
                    break

            if not repaired:

                return False

        return False

    # ==========================================
    # Prepare Collection
    # ==========================================

    def _prepare_collection(self):

        if self._prepared:

            return

        pools, collection_size = (
            self._build_pools()
        )

        max_attempts = 1000

        for attempt in range(
            max_attempts
        ):

            # Fresh copy every attempt
            working_pools = {
                layer_name: list(pool)
                for layer_name, pool
                in pools.items()
            }

            assignments, reserved = (
                self._build_assignments(
                    working_pools,
                    collection_size
                )
            )

            # ----------------------------------
            # Repair Forbidden combinations
            # ----------------------------------

            repaired = self._repair_forbidden(
                assignments,
                reserved,
                collection_size
            )

            if not repaired:

                continue

            candidates = []
            used_dna = set()

            valid = True

            # ----------------------------------
            # Build full collection
            # ----------------------------------

            for slot in range(
                collection_size
            ):

                nft = self._build_nft_from_slot(
                    assignments,
                    slot
                )

                if nft is None:

                    valid = False
                    break

                if not self._is_valid_nft(
                    nft
                ):

                    valid = False
                    break

                if nft.dna in used_dna:

                    valid = False
                    break

                used_dna.add(
                    nft.dna
                )

                candidates.append(
                    nft
                )

            if not valid:

                continue

            if len(candidates) != (
                collection_size
            ):

                continue

            # ----------------------------------
            # Success
            # ----------------------------------

            self.collection = candidates
            self._prepared = True

            return

        raise Exception(
            "Unable to create a valid unique "
            "collection with the current "
            "trait distribution and rules."
        )

    # ==========================================
    # Find Next Valid NFT
    # ==========================================

    def find_next_valid(
        self,
        dna_engine,
        duplicate_checker
    ):

        self._prepare_collection()

        if self.current_index >= len(
            self.collection
        ):

            return None

        nft = self.collection[
            self.current_index
        ]

        if duplicate_checker.exists(
            nft.dna
        ):

            raise Exception(
                f"Unexpected duplicate DNA found: "
                f"{nft.dna}"
            )

        self.pending = nft

        self.current_index += 1

        return nft

    # ==========================================
    # Commit
    # ==========================================

    def commit(self):

        self.pending = None

    # ==========================================
    # Rollback
    # ==========================================

    def rollback(self):

        if self.current_index > 0:

            self.current_index -= 1

        self.pending = None