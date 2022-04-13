from pprint import pprint

from segeval.similarity.segmentation import segmentation_similarity
from segeval import util, similarity, window, data, agreement, format

if __name__ == '__main__':
    sentence_1 = [frozenset(v) for v in [{1}, {}, {1}, {}, {1}, {}, {}, {1}, {}, {}, {1}, {1}, {}]]
    sentence_2 = [frozenset(v) for v in [{1}, {}, {1}, {1}, {}, {1}, {}, {}, {}, {}, {}, {1}, {}]]
    sentence_3 = [frozenset(v) for v in [{2}, {}, {2}, {}, {2}, {}, {}, {2}, {}, {}, {2}, {2}, {}]]
    sentence_4 = [frozenset(v) for v in [{1}, {}, {1}, {2}, {}, {1}, {}, {}, {}, {}, {}, {1}, {}]]

    sentence_1_1 = [6, 8]
    sentence_1_2 = [7, 7]

    pprint(similarity.boundary_statistics(sentence_1, sentence_2, boundary_format=format.BoundaryFormat.sets, ), sort_dicts=False)
    print(
        similarity.segmentation.segmentation_similarity(
            sentence_1, sentence_2,
            boundary_format=format.BoundaryFormat.sets,

            weight=(similarity.weight.weight_a, similarity.weight.weight_s, similarity.weight.weight_t),
            # weight=(similarity.weight.weight_a, similarity.weight.weight_s, similarity.weight.weight_t_scale),
        )
    )
