# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'pfizer',
        'name': 'Pfizer',
        'type': 'register',
        'source_url': 'http://www.pfizer.com/research/clinical_trials',
        'terms_and_conditions_url': 'http://www.pfizer.com/general/terms',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_identifiers({
        'nct': record['nct_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['title'],
        record['nct_id'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Active, not recruiting': ['ongoing', 'not_recruiting'],
        'Available': ['ongoing', 'unknown'],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation': ['ongoing', 'recruiting'],
        'No longer available': ['other', 'other'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Unknown': ['unknown', 'unknown'],
        'Withdrawn': ['withdrawn', 'other'],
    }
    status, recruitment_status = statuses[record.get('status')]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = None

    # Get age_range
    age_range = extract_age_range(record)

    trial = {
        'identifiers': identifiers,
        'public_title': public_title,
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'first_enrollment_date': record['study_start_date'],
        'study_type': record['study_type'],
        'gender': gender,
        'age_range': age_range,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    return conditions


def extract_interventions(record):
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    return organisations


def extract_persons(record):
    persons = []
    return persons

def extract_age_range(record):

    age_info = record['age_range']

    cleaner = lambda x: ' '.join(x.lower().replace('and older', '').split())

    if 'and older' in age_info.lower():
        minimum_age = cleaner(age_info)
        minimum_age = base.helpers.format_age(minimum_age)
        maximum_age = 'N/A'

    else:
        minimum_age, maximum_age = age_info.split('-')

        minimum_age = cleaner(minimum_age)
        maximum_age = cleaner(maximum_age)

        minimum_age = base.helpers.format_age(minimum_age)
        maximum_age = base.helpers.format_age(maximum_age)

    return {'maximum_age': maximum_age, 'minimum_age': minimum_age}
