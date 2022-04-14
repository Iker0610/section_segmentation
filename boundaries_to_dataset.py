import json
from collections import defaultdict
from functools import cache
import re
from glob import glob as get_files
from pathlib import Path

annotator_from_filename_regex = re.compile(r'^boundaries_(.*?).json$')


def get_unique_annotations(annotations: list[list[str]]) -> set[str]:
    return set((item for annotation in annotations for item in annotation))


@cache
def get_annotator_from_file_path(path: str):
    return annotator_from_filename_regex.match(Path(path).name).groups()[0]


def generate_dataset_from_boundaries(boundaries_folder: str, output_file: str):
    unique_annotations: set[str] = set()

    file_boundaries: dict[str, dict[str, list]] = defaultdict(dict)

    for file_path in get_files(f'{boundaries_folder}/boundaries_*.json'):
        annotator = get_annotator_from_file_path(file_path)
        with open(file_path, encoding='utf-8') as f:
            annotator_boundaries_per_file: dict[str, list] = json.load(f)

        for file, annotator_boundaries in annotator_boundaries_per_file.items():
            file_boundaries[file][annotator] = annotator_boundaries
            unique_annotations |= get_unique_annotations(annotator_boundaries)

    dataset = {
        "segmentation_type": "linear",
        "boundary_format": "sets",
        "boundary_types": list(unique_annotations),
        "items": file_boundaries,
    }

    with open(output_file, 'w', encoding='utf-8') as dataset_file:
        json.dump(dataset, dataset_file, ensure_ascii=False, indent=2, sort_keys=False)


if __name__ == '__main__':
    boundaries = './boundaries'
    output = './boundaries/dataset.json'
    generate_dataset_from_boundaries(boundaries, output)
