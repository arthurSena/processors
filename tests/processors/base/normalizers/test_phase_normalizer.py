# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.base.normalizers import get_normalized_phase
import pytest

#Tests
class TestValidateRemoteURL(object):
    @pytest.mark.parametrize('test_input,expected', [ 
            ('Phase 3-4', ['Phase 3', 'Phase 4']),
            ('Phase 3 / Phase 4', ['Phase 3', 'Phase 4']),
            ('Phase III/IV', ['Phase 3', 'Phase 4']),
            ('Phase 2-3', ['Phase 2', 'Phase 3']),
            ('Phase 2 / Phase 3', ['Phase 2', 'Phase 3']),
            ('Phase2/Phase3', ['Phase 2', 'Phase 3']),
            ('Phase II,III', ['Phase 2', 'Phase 3']),
            ('Phase 2/Phase 3', ['Phase 2', 'Phase 3']),
            ('2-3', ['Phase 2', 'Phase 3']),
            ('II-III', ['Phase 2', 'Phase 3']),
            ('Phase 2/3', ['Phase 2', 'Phase 3']),
            ('Phase 1-2', ['Phase 2', 'Phase 1']),
            ('I-IIA', ['Phase 2A', 'Phase 1']),
            ('I-II', ['Phase 2', 'Phase 1']),
            ('Phase I/II', ['Phase 2', 'Phase 1']),
            ('Phase 1/Phase 2', ['Phase 2', 'Phase 1']),
            ('Human pharmacology (Phase I): yes\\nTherapeutic exploratory'+
                ' (Phase II): yes\\nTherapeutic confirmatory - (Phase III):'+
                ' no\\nTherapeutic use (Phase IV): no\\n', ['Phase 2', 'Phase 1']),
            ('Phase 1 / Phase 2', ['Phase 2', 'Phase 1']),
            ('Phase1/Phase2', ['Phase 2', 'Phase 1']),
            ('Phase I,II', ['Phase 2', 'Phase 1']),
            ('1-2', ['Phase 2', 'Phase 1']),
            ('I+II (Phase I+Phase II)', ['Phase 2', 'Phase 1']),
            ('Phase 1/Phase 2', ['Phase 2', 'Phase 1']),
            ('Phase 1/2', ['Phase 2', 'Phase 1']),
            ('Not applicable', ['Not applicable']),
            ('Not Specified', ['Not applicable']),
            ('N/A', ['Not applicable']),
            ('NA', ['Not applicable']),
            ('Not Applicable', ['Not applicable']),
            ('Not entered', ['Not applicable']),
            ('Not selected', ['Not applicable']),
            ('n\\a', ['Not applicable']),
            ('N/', ['Not applicable']),
            ('Phase 2', ['Phase 2']),
            ('2', ['Phase 2']),
            ('Phase2', ['Phase 2']),
            ('IIa', ['Phase 2A']),
            ('IIA', ['Phase 2A']),
            ('Phase 2', ['Phase 2']),
            ('II (Phase II study)', ['Phase 2']),
            ('IIb', ['Phase 2B']),
            ('Phase II', ['Phase 2']),
            ('II', ['Phase 2']),
            ('IIB', ['Phase 2B']),
            ('Phase 3', ['Phase 3']),
            ('Phase 3', ['Phase 3']),
            ('III', ['Phase 3']),
            ('III (Phase III study)', ['Phase 3']),
            ('3', ['Phase 3']),
            ('IIIb', ['Phase 3B']),
            ('Phase3', ['Phase 3']),
            ('Phase III', ['Phase 3']),
            ('IIIB', ['Phase 3B']),
            ('IIIA', ['Phase 3A']),
            ('Phase 0', ['Phase 0']),
            ('0', ['Phase 0']),
            ('0(exploratory trials))', ['Phase 0']),
            ('Phase 1', ['Phase 1']),
            ('I (Phase I study)', ['Phase 1']),
            ('Phase I', ['Phase 1']),
            ('Phase1', ['Phase 1']),
            ('I', ['Phase 1']),
            ('1', ['Phase 1']),
            ('Phase 4', ['Phase 4']),
            ('Post-market', ['Phase 4']),
            ('4', ['Phase 4']),
            ('IV', ['Phase 4']),
            ('Phase IV', ['Phase 4']),
            ('IV (Phase IV study)', ['Phase 4']),
            ('Phase4', ['Phase 4']),
            ('Other', ['Other']),
            ('Pilot study', ['Other']),
            ('Diagnostic New Technique Clincal Study', ['Other']),
            ('Bioequivalence', ['Other']),
            ('New Treatment Measure Clinical Study', ['Other'])
        ])

    def test_phase_normalizer(self, test_input, expected):
        assert get_normalized_phase(test_input) == expected
