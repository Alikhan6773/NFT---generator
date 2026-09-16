from models.plan import Plan
from models.plan_item import PlanItem
from models.layer_plan import LayerPlan


class PlannerEngine:

    def create_plan(self, collection, collection_size):

        plan = Plan()

        plan.collection_size = collection_size

        for layer in collection.layers:

            layer_plan = LayerPlan(
                layer.name
            )

            mode = "auto"

            if layer.traits:

                mode = layer.traits[0].mode

            configured_items = []
            auto_items = []

            for trait in layer.traits:

                item = PlanItem(
                    trait=trait,
                    amount=0
                )

                layer_plan.items.append(
                    item
                )

                if trait.value > 0:

                    configured_items.append(
                        item
                    )

                else:

                    auto_items.append(
                        item
                    )

            # ==================================
            # AUTO
            # ==================================

            if mode == "auto":

                self._apply_auto(
                    layer_plan,
                    collection_size
                )

            # ==================================
            # COUNT
            # ==================================

            elif mode == "count":

                self._apply_count(
                    layer,
                    layer_plan,
                    configured_items,
                    auto_items,
                    collection_size
                )

            # ==================================
            # PERCENTAGE
            # ==================================

            elif mode == "percentage":

                self._apply_percentage(
                    layer,
                    layer_plan,
                    configured_items,
                    auto_items,
                    collection_size
                )

            else:

                raise ValueError(
                    f"Invalid distribution mode "
                    f"'{mode}' for layer "
                    f"'{layer.name}'. "
                    f"Allowed modes: "
                    f"count, percentage, auto."
                )

            plan.layers.append(
                layer_plan
            )

        return plan

    # ======================================
    # AUTO
    # ======================================

    def _apply_auto(
        self,
        layer_plan,
        collection_size
    ):

        items = layer_plan.items

        if not items:

            return

        each = (
            collection_size
            // len(items)
        )

        extra = (
            collection_size
            % len(items)
        )

        for index, item in enumerate(items):

            item.amount = each

            if index < extra:

                item.amount += 1

    # ======================================
    # COUNT
    # ======================================

    def _apply_count(
        self,
        layer,
        layer_plan,
        configured_items,
        auto_items,
        collection_size
    ):

        used = 0

        for item in configured_items:

            amount = item.trait.value

            if amount < 0:

                raise ValueError(
                    f"Count cannot be negative "
                    f"for trait '{item.trait.name}'."
                )

            used += amount

            item.amount = amount

        if used > collection_size:

            raise ValueError(
                f"Count total for layer "
                f"'{layer.name}' exceeds "
                f"collection size."
            )

        remaining = (
            collection_size - used
        )

        if not auto_items:

            if remaining != 0:

                raise ValueError(
                    f"Layer '{layer.name}' "
                    f"has {remaining} unassigned "
                    f"NFTs. Add more counts or "
                    f"leave at least one trait "
                    f"without a value."
                )

            return

        self._distribute_evenly(
            auto_items,
            remaining
        )

    # ======================================
    # PERCENTAGE
    # ======================================

    def _apply_percentage(
        self,
        layer,
        layer_plan,
        configured_items,
        auto_items,
        collection_size
    ):

        used_percentage = 0

        for item in configured_items:

            percentage = item.trait.value

            if (
                percentage < 0
                or percentage > 100
            ):

                raise ValueError(
                    f"Percentage for trait "
                    f"'{item.trait.name}' must "
                    f"be between 0 and 100."
                )

            used_percentage += percentage

        if used_percentage > 100:

            raise ValueError(
                f"Percentage total for layer "
                f"'{layer.name}' exceeds 100%."
            )

        # ----------------------------------
        # Calculate exact amounts
        # ----------------------------------

        raw_amounts = []

        assigned = 0

        for item in configured_items:

            exact = (
                collection_size
                * item.trait.value
                / 100
            )

            base = int(exact)

            remainder = (
                exact - base
            )

            raw_amounts.append(
                (
                    item,
                    base,
                    remainder
                )
            )

            assigned += base

        for item, amount, _ in raw_amounts:

            item.amount = amount

        # ----------------------------------
        # Remaining percentage
        # ----------------------------------

        remaining_percentage = (
            100 - used_percentage
        )

        remaining_amount = (
            collection_size
            - assigned
        )

        if remaining_amount < 0:

            raise ValueError(
                f"Calculated percentage amounts "
                f"for layer '{layer.name}' exceed "
                f"collection size."
            )

        if not auto_items:

            # No Auto traits.
            # Give rounding leftovers to
            # configured percentage traits.

            raw_amounts.sort(
                key=lambda x: x[2],
                reverse=True
            )

            for i in range(
                collection_size - assigned
            ):

                raw_amounts[
                    i % len(raw_amounts)
                ][0].amount += 1

            return

        # ----------------------------------
        # Distribute remaining percentage
        # equally between Auto traits
        # ----------------------------------

        if remaining_percentage == 0:

            self._distribute_evenly(
                auto_items,
                0
            )

            return

        self._distribute_evenly(
            auto_items,
            remaining_amount
        )

    # ======================================
    # EVEN DISTRIBUTION
    # ======================================

    def _distribute_evenly(
        self,
        items,
        amount
    ):

        if not items:

            return

        each = (
            amount
            // len(items)
        )

        extra = (
            amount
            % len(items)
        )

        for index, item in enumerate(items):

            item.amount = each

            if index < extra:

                item.amount += 1