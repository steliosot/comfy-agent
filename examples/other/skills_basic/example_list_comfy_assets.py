from pprint import pprint

from skills.list_comfy_assets.skill import run


result = run(include_files=True)

print("server:", result["server"])
print("counts:")
pprint(result["counts"])

print("\ncheckpoints (first 10):")
for item in result["assets"]["checkpoints"][:10]:
    print("-", item)

print("\ninput files (first 10):")
for item in result["assets"]["input_files"][:10]:
    print("-", item)
