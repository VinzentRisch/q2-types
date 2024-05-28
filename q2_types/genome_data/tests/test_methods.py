# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os

from qiime2.plugin.testing import TestPluginBase

from q2_types.genome_data import SeedOrthologDirFmt, collate_orthologs, \
    partition_orthologs


class TestOrthologsPartitionCollating(TestPluginBase):
    package = "q2_types.genome_data.tests"

    def test_collate_orthologs(self):
        p1 = self.get_data_path("partitioned_orthologs/ortholog_1")
        p2 = self.get_data_path("partitioned_orthologs/ortholog_2")
        orthologs = [
            SeedOrthologDirFmt(p1, mode="r"),
            SeedOrthologDirFmt(p2, mode="r")
        ]

        collated_orthologs = collate_orthologs(orthologs)
        self.assertTrue(os.path.exists(
            collated_orthologs.path / "1.emapper.seed_orthologs")
        )
        self.assertTrue(os.path.exists(
            collated_orthologs.path / "2.emapper.seed_orthologs")
        )

    def test_partition_orthologs(self):
        p = self.get_data_path("collated_orthologs")
        orthologs = SeedOrthologDirFmt(path=p, mode="r")
        obs = partition_orthologs(orthologs, 2)

        self.assertTrue(os.path.exists(
            obs["1"].path / "1.emapper.seed_orthologs")
        )
        self.assertTrue(os.path.exists(
            obs["1"].path / "1.emapper.seed_orthologs")
        )

    def test_partition_orthologs_warning_message(self):
        path = self.get_data_path("collated_orthologs")
        orthologs = SeedOrthologDirFmt(path=path, mode="r")

        with self.assertWarnsRegex(
            UserWarning, "You have requested a number of.*5.*2.*2"
        ):
            partition_orthologs(orthologs, 5)
