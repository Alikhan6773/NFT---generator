from engine.rule_engine import RuleEngine


rules = {

    "forbidden": [
        {
            "trait": "Clothe.Doctor",
            "with": "Hat & Hair.Army"
        }
    ],

    "required": [
        {
            "trait": "Clothe.Doctor",
            "with": "Eye & Glass.Cyber Eye"
        }
    ]
}


rule_engine = RuleEngine(rules)


# ==========================================
# Test 1 — Valid
# ==========================================

valid_traits = {

    "Clothe": "Doctor",
    "Hat & Hair": "Kings Crown",
    "Eye & Glass": "Cyber Eye"

}

result = rule_engine.validate(
    valid_traits
)

print(
    "Test 1 - Valid:",
    result
)


# ==========================================
# Test 2 — Forbidden
# ==========================================

forbidden_traits = {

    "Clothe": "Doctor",
    "Hat & Hair": "Army",
    "Eye & Glass": "Cyber Eye"

}

result = rule_engine.validate(
    forbidden_traits
)

print(
    "Test 2 - Forbidden:",
    result
)


# ==========================================
# Test 3 — Required
# ==========================================

missing_required_traits = {

    "Clothe": "Doctor",
    "Hat & Hair": "Kings Crown",
    "Eye & Glass": "Bitcoin Eye"

}

result = rule_engine.validate(
    missing_required_traits
)

print(
    "Test 3 - Required:",
    result
)