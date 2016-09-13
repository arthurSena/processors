# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'id': 'icdcm',
        'name': 'ICD-10 Clinical Modification',
        'type': 'other',
        'url': 'https://www.cms.gov/Medicare/Coding/ICD10/index.html',
    }
    return source


def extract_conditions(record):

    # Get all names
    names = []
    names.append(record['desc'])
    names = names + record['terms']

    # Extract conditions
    conditions = []
    for name in names:
        conditions.append({
            'name': name,
            'icdcm_code': record['name'],
        })

    return conditions
