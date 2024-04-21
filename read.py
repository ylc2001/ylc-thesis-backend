from utils.read_binary import BinaryResultReader

file_path = "./files/ylc-P40-Pro/2024-01-08-Blendshapes.bin"
reader = BinaryResultReader(file_path)
blendshapes_results = reader.read_face_blendshapes_result()

for i, result in enumerate(blendshapes_results, start=1):
    print(f"Result {i}:")
    print(f"  Timestamp: {result['timestamp']}")
    print("  Blendshapes:")
    for id, score in result['blendshapes'].items():
        print(f"    ID: {id}-{result['blendshape_names'].get(id, 'unknown feature')}, Score: {score}")
    print()