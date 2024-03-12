import json
import csv
import os

for filename in os.listdir("./chunks/"):
    if not filename.endswith(".csv"):
        continue
    with open("./chunks/" + filename, newline="") as csvfile:
        chunk_dict: dict[str, list[tuple[int, int]]] = {}
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        row = 0
        for line in reader:
            for col in range(50):
                group = line[col]
                if group != "0":
                    if group not in chunk_dict:
                        chunk_dict[group] = []
                    chunk_dict[group].append((row, col))
            row += 1
        for key, value in chunk_dict.items():
            chunk_dict[key] = sorted(value)
        filename_json = filename.split(".")[0] + ".json"
        print(filename_json)
        with open("./chunks/" + filename_json, "w") as dictfile:
            json.dump(chunk_dict, dictfile)
