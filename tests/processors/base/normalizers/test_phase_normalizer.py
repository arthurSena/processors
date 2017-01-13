# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.base.normalizers import get_normalized_phase
import pytest

#Tests


class TestValidateRemoteURL(object):
        @pytest.mark.parametrize("test_input,expected", [
                ('Phase 3-4', 'Phase 3-4'),
                ('Phase 3 / Phase 4', 'Phase 3-4'),
                ('Phase III/IV', 'Phase 3-4'),
                ('Phase 2-3', 'Phase 2-3'),
                ('Phase 2 / Phase 3', 'Phase 2-3'),
                ('Phase2/Phase3', 'Phase 2-3'),
                ('Phase II,III', 'Phase 2-3'),
                ('Phase 2/Phase 3', 'Phase 2-3'),
                ('2-3', 'Phase 2-3'),
                ('II-III', 'Phase 2-3'),
                ('Phase 1-2', 'Phase 1-2'),
                ('I-IIA', 'Phase 1-2'),
                ('I-II', 'Phase 1-2'),
                ('Phase I/II', 'Phase 1-2'),
                ('Phase 1/Phase 2', 'Phase 1-2'),
                ('Human pharmacology (Phase I): yes\\nTherapeutic exploratory '
                '(Phase II): yes\\nTherapeutic confirmatory - (Phase III): no\\nTherapeutic use (Phase IV): no\\n', 'Phase 1-2'),
                ('Phase 1 / Phase 2', 'Phase 1-2'),
                ('Phase1/Phase2', 'Phase 1-2'),
                ('Phase I,II', 'Phase 1-2'),
                ('1-2', 'Phase 1-2'),
                ('I+II (Phase I+Phase II)', 'Phase 1-2'),
                ('Phase 2', 'Phase 2'),
                ('2', 'Phase 2'),
                ('Phase2', 'Phase 2'),
                ('IIa', 'Phase 2'),
                ('IIA', 'Phase 2'),
                ('Phase 2', 'Phase 2'),
                ('II (Phase II study)', 'Phase 2'),
                ('IIb', 'Phase 2'),
                ('Phase II', 'Phase 2'),
                ('II', 'Phase 2'),
                ('IIB', 'Phase 2'),
                ('Phase 3', 'Phase 3'),
                ('Phase 3', 'Phase 3'),
                ('III', 'Phase 3'),
                ('III (Phase III study)', 'Phase 3'),
                ('3', 'Phase 3'),
                ('IIIb', 'Phase 3'),
                ('Phase3', 'Phase 3'),
                ('Phase III', 'Phase 3'),
                ('IIIB', 'Phase 3'),
                ('IIIA', 'Phase 3'),
                ('Phase 0', 'Phase 0'),
                ('0', 'Phase 0'),
                ('0(exploratory trials))', 'Phase 0'),
                ('Phase 1', 'Phase 1'),
                ('I (Phase I study)', 'Phase 1'),
                ('Phase I', 'Phase 1'),
                ('Phase1', 'Phase 1'),
                ('I', 'Phase 1'),
                ('1', 'Phase 1'),
                ('Phase 4', 'Phase 4'),
                ('Post-market', 'Phase 4'),
                ('4', 'Phase 4'),
                ('IV', 'Phase 4'),
                ('Phase IV', 'Phase 4'),
                ('IV (Phase IV study)', 'Phase 4'),
                ('Phase4', 'Phase 4'),
                ('Phase 4', 'Phase 4'),
                ('Not entered', 'Not applicable'),
                ('Pilot study', 'Other'),
                ('Diagnostic New Technique Clincal Study', 'Other'),
                ('Not Applicable', 'Not applicable'),
                ('Bioequivalence', 'Other'),
                ('NA', 'Not applicable'),
                ('New Treatment Measure Clinical Study', 'Other'),
                ('Other', 'Other'),
                ('Not selected', 'Not applicable'),
                ('Not applicable', 'Not applicable'),
                ('Not Specified', 'Not applicable'),
                ('N/A', 'Not applicable')
        ])

        def test_phase_normalizer(self, test_input, expected):
            assert get_normalized_phase(test_input) == expected
