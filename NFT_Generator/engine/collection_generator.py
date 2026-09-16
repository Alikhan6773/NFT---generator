from engine.layer_loader import load_collection
from engine.validation_engine import ValidationEngine
from engine.planner_engine import PlannerEngine
from engine.queue_builder import QueueBuilder
from engine.trait_config_loader import TraitConfigLoader
from engine.verification_engine import VerificationEngine


class CollectionGenerator:

    def __init__(
        self,
        assets_folder,
        output_folder,
        collection_size,
        generator,
        dna_engine,
        duplicate_checker,
        image_builder,
        metadata_builder,
        rule_engine=None,
        config_path="config/traits.json"
    ):

        self.assets_folder = assets_folder
        self.output_folder = output_folder
        self.collection_size = collection_size

        self.generator = generator
        self.dna_engine = dna_engine
        self.duplicate_checker = duplicate_checker
        self.image_builder = image_builder
        self.metadata_builder = metadata_builder

        self.rule_engine = rule_engine

        self.config_path = config_path
        self.config_loader = TraitConfigLoader()

    # ==========================================
    # Load Collection
    # ==========================================

    def load_collection(self):

        return load_collection(
            self.assets_folder
        )

    # ==========================================
    # Configure Traits
    # ==========================================

    def configure_traits(self, collection):

        config = self.config_loader.load(
            self.config_path
        )

        self.config_loader.apply(
            collection,
            config
        )

    # ==========================================
    # Validation
    # ==========================================

    def validate(self, collection):

        validator = ValidationEngine()

        validator.validate_assets_folder(
            self.assets_folder
        )

        validator.validate_layers(
            collection
        )

        validator.validate_rarity(
            collection,
            self.collection_size
        )

        validator.print_report()

        if validator.errors:

            raise ValueError(
                "Validation failed. "
                "Generation stopped."
            )

    # ==========================================
    # Create Plan
    # ==========================================

    def create_plan(self, collection):

        planner = PlannerEngine()

        return planner.create_plan(
            collection,
            self.collection_size
        )

    # ==========================================
    # Build Queues
    # ==========================================

    def build_queues(self, plan):

        queue_builder = QueueBuilder()

        return queue_builder.build(
            plan
        )

    # ==========================================
    # Generate Collection
    # ==========================================

    def generate(self, collection_size):

        print(
            "\nGenerating Collection...\n"
        )

        for i in range(collection_size):

            nft = self.generator.find_next_valid(
                self.dna_engine,
                self.duplicate_checker
            )

            if nft is None:

                raise Exception(
                    "No valid NFT combination found."
                )

            self.duplicate_checker.add(
                nft.dna
            )

            self.generator.commit()

            self.image_builder.build(
                nft.image_paths,
                f"{self.output_folder}/"
                f"{i + 1:04}.png"
            )

            self.metadata_builder.build(
                nft_number=i + 1,
                selected_traits=nft.attributes,
                dna=nft.dna,
                output_folder=self.output_folder
            )

            print(
                f"{i + 1:04} -> {nft.dna}"
            )

        print(
            "\nCollection generated successfully."
        )

    # ==========================================
    # Verification
    # ==========================================

    def verify_collection(self):

        verification_engine = VerificationEngine(
            self.generator.collection
        )

        verification_engine.run(

            expected_size=self.collection_size,

            rule_engine=self.rule_engine,

            trait_expectations=[
                {
                    "layer": "Clothe",
                    "trait": "Doctor",
                    "count": 5
                },
                {
                    "layer": "Background",
                    "trait": "Purple",
                    "count": 40
                },
                {
                    "layer": "Background",
                    "trait": "Pink Red",
                    "count": 30
                },
                {
                    "layer": "Background",
                    "trait": "Light Green",
                    "count": 15
                },
                {
                    "layer": "Background",
                    "trait": "Vibrant Yellow",
                    "count": 15
                }
            ]
        )

    # ==========================================
    # Run Pipeline
    # ==========================================

    def run(self):

        # --------------------------------------
        # Load
        # --------------------------------------

        collection = self.load_collection()

        # --------------------------------------
        # Config
        # --------------------------------------

        self.configure_traits(
            collection
        )

        # --------------------------------------
        # Validation
        # --------------------------------------

        self.validate(
            collection
        )

        # --------------------------------------
        # Plan
        # --------------------------------------

        plan = self.create_plan(
            collection
        )

        # --------------------------------------
        # Queues
        # --------------------------------------

        queues = self.build_queues(
            plan
        )

        self.generator.queues = queues

        # --------------------------------------
        # Rule Engine
        # --------------------------------------

        self.generator.rule_engine = (
            self.rule_engine
        )

        # --------------------------------------
        # Debug
        # --------------------------------------

        print(
            "\n===== RULE DEBUG ====="
        )

        for layer_name, selector in queues.items():

            print(
                f"\nLayer: {layer_name}"
            )

            for item in selector.traits:

                print(
                    f"{item['trait'].name} "
                    f"-> {item['remaining']}"
                )

        print(
            "\n===== END RULE DEBUG ====="
        )

        # --------------------------------------
        # Generate
        # --------------------------------------

        self.generate(
            plan.collection_size
        )

        # --------------------------------------
        # Verify
        # --------------------------------------

        self.verify_collection()