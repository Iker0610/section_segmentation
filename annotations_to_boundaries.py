from collections import defaultdict, namedtuple
from glob import glob as get_files
import json
from pathlib import Path

AnnotatedFile = namedtuple('AnnotatedFile', 'text_file annotation_file')


def convert_file_annotations_to_boundaries(file_path: str, annotations_path: str) -> list[list]:
    with open(annotations_path, encoding='utf-8') as annotation_file:
        annotations = json.load(annotation_file)

    with open(file_path, encoding='utf-8') as file:
        token_num = len([token for line in file.read().splitlines() for token in line.split()])

    boundaries = [list() for _ in range(token_num)]

    for offset, annotation in annotations.items():
        try:
            index = int(offset) - 1
            boundaries[index].append(annotation)
        except:
            print(f"ERROR - {offset} not a number.")

    return boundaries


def convert_annotations_to_boundaries(text_input_folder, annotation_input_folder, output_file):
    files_tuples: dict[str, list] = defaultdict(lambda: [''] * 2)
    for text_file in get_files(f'{text_input_folder}/*'):
        files_tuples[Path(text_file).stem][0] = text_file

    for annotation_file in get_files(f'{annotation_input_folder}/*'):
        files_tuples[Path(annotation_file).stem.split('_')[0]][1] = annotation_file

    boundaries = {file_name: convert_file_annotations_to_boundaries(*annotated_file_paths)
                  for file_name, annotated_file_paths in files_tuples.items()}

    with open(output_file, 'w', encoding='utf-8') as output_file_handler:
        json.dump(boundaries, output_file_handler, ensure_ascii=False)


if __name__ == '__main__':
    text_input = './data'
    annotation_input = './annotations/Maria/schemas'
    output = 'boundaries/boundaries_Maria.json'

    convert_annotations_to_boundaries(text_input, annotation_input, output)
