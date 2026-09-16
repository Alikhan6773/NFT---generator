import json
import os

output_folder = "output"

dna_map = {}
json_count = 0

for filename in sorted(os.listdir(output_folder)):

    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(output_folder, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    dna = data.get("dna")

    json_count += 1

    if dna in dna_map:
        dna_map[dna].append(filename)
    else:
        dna_map[dna] = [filename]


duplicates = {
    dna: files
    for dna, files in dna_map.items()
    if len(files) > 1
}

print("\n========== Duplicate Report ==========")
print("JSON files:", json_count)
print("Unique DNA:", len(dna_map))
print("Duplicate DNA:", len(duplicates))

if duplicates:

    print("\nDuplicates found:")

    for dna, files in duplicates.items():

        print("\nDNA:", dna)

        for filename in files:
            print(" -", filename)

else:

    print("\nNo duplicate DNA found.")

print("\n======================================")