import json
from collections import defaultdict
from pprint import pprint

import jsbeautifier

from segeval.agreement import actual_agreement_linear
from segeval.agreement.bias import artstein_poesio_bias_linear
from segeval.agreement.kappa import fleiss_kappa_linear
from segeval.agreement.pi import fleiss_pi_linear
from segeval.data.jsonutils import input_linear_boundaries_json
from segeval.similarity import boundary_statistics
from segeval.similarity.boundary import boundary_similarity
from segeval.similarity.segmentation import segmentation_similarity
from segeval.similarity.weight import weight_a, weight_s, weight_t

weight_functions = (weight_a, weight_s, weight_t)

if __name__ == '__main__':
    sentence_1 = [frozenset(v) for v in [{1}, {}, {}, {1}, {}, {1}, {}, {}, {1}, {}, {}, {1}, {1}, {}]]
    sentence_2 = [frozenset(v) for v in [{1}, {}, {}, {1}, {1}, {}, {1}, {}, {}, {}, {}, {}, {1}, {}]]
    sentence_3 = [frozenset(v) for v in [{2}, {}, {2}, {}, {2}, {}, {}, {2}, {}, {}, {2}, {2}, {}]]
    sentence_4 = [frozenset(v) for v in [{1}, {}, {1}, {2}, {}, {1}, {}, {}, {}, {}, {}, {1}, {}]]

    dataset = input_linear_boundaries_json('./boundaries/dataset.json')

    stats = defaultdict(dict) | boundary_statistics(
        dataset=dataset,
        weight=weight_functions,
    )

    s = segmentation_similarity(
        dataset=dataset,
        weight=weight_functions,
    )

    b = boundary_similarity(
        dataset=dataset,
        weight=weight_functions,
    )

    for file in stats.keys():
        del stats[file]['boundaries_all']
        del stats[file]['boundary_types']
        del stats[file]['full_misses']
        del stats[file]['matches']
        stats[file]['S'] = s[file]
        stats[file]['B'] = b[file]

    stats['S']['PI'] = str(fleiss_pi_linear(dataset=dataset, fnc_compare=segmentation_similarity, weight=weight_functions))
    stats['B']['PI'] = str(fleiss_pi_linear(dataset=dataset, fnc_compare=boundary_similarity, weight=weight_functions))

    stats['S']['KAPPA'] = str(fleiss_kappa_linear(dataset=dataset, fnc_compare=segmentation_similarity, weight=weight_functions))
    stats['B']['KAPPA'] = str(fleiss_kappa_linear(dataset=dataset, fnc_compare=boundary_similarity, weight=weight_functions))

    stats['S']['BIAS'] = str(artstein_poesio_bias_linear(dataset=dataset, fnc_compare=segmentation_similarity, weight=weight_functions))
    stats['B']['BIAS'] = str(artstein_poesio_bias_linear(dataset=dataset, fnc_compare=boundary_similarity, weight=weight_functions))

    stats['S']['Agreement'] = str(actual_agreement_linear(dataset=dataset, fnc_compare=segmentation_similarity, weight=weight_functions))
    stats['B']['Agreement'] = str(actual_agreement_linear(dataset=dataset, fnc_compare=boundary_similarity, weight=weight_functions))

    stats = {k: v for k, v in sorted(stats.items(), key=lambda item: item[0])}

    pprint(stats, width=20)

    with open('./segmentation_evaluation.json', 'w', encoding='utf-8') as output:
        # json.dump(stats, output, ensure_ascii=False, indent=2)

        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        output.write(jsbeautifier.beautify(json.dumps(stats), opts))

