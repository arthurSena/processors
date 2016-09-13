# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'id': 'fdadl',
        'name': 'FDA Drug Labels',
        'type': 'other',
        'url': 'https://open.fda.gov',
        'terms_and_conditions_url': 'https://open.fda.gov/terms/',
    }
    return source


def extract_interventions(record):

    # Get all names
    names = []
    names.append(record['generic_name'])
    names.append(record['brand_name'])

    # Extract interventions
    interventions = []
    for name in names:
        interventions.append({
            'name': name,
            'type': 'drug',
            'description': record['product_type'],
            'ndc_code': record['product_ndc'],
            'fda_application_id': record.get('fda_application_number'),
        })

    return interventions
