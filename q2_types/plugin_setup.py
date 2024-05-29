# ----------------------------------------------------------------------------
# Copyright (c) 2016-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
import qiime2.plugin
import qiime2.sdk
from qiime2.core.type import Int, Range, Collection, List

import q2_types
from q2_types import __version__

from q2_types.feature_data_mag import MAG, NOG
# from q2_types.genome_data import
from q2_types.per_sample_sequences import MAGs
from q2_types.feature_data import FeatureData
from q2_types.genome_data import BLAST6
from q2_types.sample_data import SampleData


citations = qiime2.plugin.Citations.load('citations.bib', package='q2_types')
plugin = qiime2.plugin.Plugin(
    name='types',
    version=__version__,
    website='https://github.com/qiime2/q2-types',
    package='q2_types',
    description=('This QIIME 2 plugin defines semantic types and '
                 'transformers supporting microbiome analysis.'),
    short_description='Plugin defining types for microbiome analysis.'
)

plugin.register_views(pd.Series, pd.DataFrame,
                      citations=[citations['mckinney-proc-scipy-2010']])

# __init__.py loads first and imports all of the subpackages.

plugin.methods.register_function(
    function=q2_types.per_sample_sequences.partition_sample_data_mags,
    inputs={"mags": SampleData[MAGs]},
    parameters={"num_partitions": Int % Range(1, None)},
    outputs={"partitioned_mags": Collection[SampleData[MAGs]]},
    input_descriptions={"mags": "The MAGs to partition."},
    parameter_descriptions={
        "num_partitions": "The number of partitions to split the MAGs"
        " into. Defaults to partitioning into individual"
        " MAGs."
    },
    name="Partition MAGs",
    description="Partition a SampleData[MAGs] artifact into smaller "
                "artifacts containing subsets of the MAGs",
)

plugin.methods.register_function(
    function=q2_types.genome_data.partition_orthologs,
    inputs={"orthologs": SampleData[BLAST6]},
    parameters={"num_partitions": Int % Range(1, None)},
    outputs={"partitioned_orthologs": Collection[SampleData[BLAST6]]},
    input_descriptions={"orthologs": "The orthologs to partition."},
    parameter_descriptions={
        "num_partitions": "The number of partitions to split the MAGs"
        " into. Defaults to partitioning into individual"
        " MAGs."
    },
    name="Partition orthologs",
    description="Partition a SampleData[BLAST6] artifact into smaller "
                "artifacts containing subsets of the BLAST6 reports.",
)

plugin.methods.register_function(
    function=q2_types.per_sample_sequences.collate_sample_data_mags,
    inputs={"mags": List[SampleData[MAGs]]},
    parameters={},
    outputs={"collated_mags": SampleData[MAGs]},
    input_descriptions={"mags": "A collection of MAGs to be collated."},
    name="Collate mags",
    description="Takes a collection of SampleData[MAGs]'s "
                "and collates them into a single artifact.",
)

plugin.methods.register_function(
    function=q2_types.feature_data_mag.partition_feature_data_mags,
    inputs={"mags": FeatureData[MAG]},
    parameters={"num_partitions": Int % Range(1, None)},
    outputs={"partitioned_mags": Collection[FeatureData[MAG]]},
    input_descriptions={"mags": "MAGs to partition."},
    parameter_descriptions={
        "num_partitions": "The number of partitions to split the MAGs"
        " into. Defaults to partitioning into individual"
        " MAGs."
    },
    name="Partition MAGs",
    description="Partition a FeatureData[MAG] artifact into smaller "
                "artifacts containing subsets of the MAGs",
)

plugin.methods.register_function(
    function=q2_types.feature_data_mag.collate_feature_data_mags,
    inputs={"mags": List[FeatureData[MAG]]},
    parameters={},
    outputs={"collated_mags": FeatureData[MAG]},
    input_descriptions={"mags": "A collection of MAGs to be collated."},
    name="Collate mags",
    description="Takes a collection of FeatureData[MAG]'s "
                "and collates them into a single artifact.",
)

plugin.methods.register_function(
    function=q2_types.genome_data.collate_orthologs,
    inputs={"orthologs": List[SampleData[BLAST6]]},
    parameters={},
    outputs={"collated_orthologs": SampleData[BLAST6]},
    input_descriptions={"orthologs": "Orthologs to collate"},
    parameter_descriptions={},
    name="Collate Orthologs",
    description="Takes a collection SampleData[BLAST6] artifacts "
                "and collates them into a single artifact.",
)

plugin.methods.register_function(
    function=q2_types.feature_data_mag.collate_ortholog_annotations,
    inputs={'ortholog_annotations': List[FeatureData[NOG]]},
    parameters={},
    outputs=[('collated_ortholog_annotations', FeatureData[NOG])],
    input_descriptions={
        'ortholog_annotations': "Collection of ortholog annotations."
    },
    output_descriptions={
        'collated_ortholog_annotations': "Collated ortholog annotations."
    },
    name='Collate ortholog annotations.',
    description="Takes a collection of FeatureData[NOG]'s "
                "and collates them into a single artifact.",
)

