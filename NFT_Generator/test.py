from engine.collection_generator import CollectionGenerator
from engine.generator_engine import GeneratorEngine
from engine.dna_engine import DNAEngine
from engine.duplicate_checker import DuplicateChecker
from engine.image_builder import ImageBuilder
from engine.metadata_builder import MetadataBuilder
from engine.rule_engine import RuleEngine


# ==========================================
# Rules
# ==========================================

rules = {

    "forbidden": [
        {
            "trait": "Eye & Glass.Bloody Eye",
            "with": "Mouth & Beard.Cigarettes"
        }
    ],

    "required": [
        {
            "trait": "Clothe.Doctor",
            "with": "Hat & Hair.Army"
        },
        {
            "trait": "Body.Galactic",
            "with": "Eye & Glass.Cyber Eye"
        }
    ]
}


rule_engine = RuleEngine(
    rules
)


# ==========================================
# Collection Generator
# ==========================================

collection_generator = CollectionGenerator(

    assets_folder="assets",

    output_folder="output",

    collection_size=100,

    generator=GeneratorEngine({}),

    dna_engine=DNAEngine(),

    duplicate_checker=DuplicateChecker(),

    image_builder=ImageBuilder(),

    metadata_builder=MetadataBuilder(),

    rule_engine=rule_engine
)


# ==========================================
# Run
# ==========================================

collection_generator.run()