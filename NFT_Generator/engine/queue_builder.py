import random

from engine.trait_selector import TraitSelector


class QueueBuilder:

    def build(self, plan):

        selectors = {}

        for layer in plan.layers:

            queue = []

            for item in layer.items:

                for _ in range(item.amount):

                    queue.append(item.trait)

            random.shuffle(queue)

            selectors[layer.layer_name] = TraitSelector(queue)

        return selectors