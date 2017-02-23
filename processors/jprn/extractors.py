# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'jprn',
        'name': 'UMIN',
        'type': 'register',
        'source_url': 'http://rctportal.niph.go.jp/en/',
        'terms_and_conditions_url': 'http://rctportal.niph.go.jp/en/agreement',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_identifiers({
        'jprn': base.helpers.safe_prepend('JPRN-', record['unique_trial_number']),
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['title_of_the_study'],
        record['official_scientific_title_of_the_study'],
        record['unique_trial_number'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation(outpatients are not recruited publicly)': ['ongoing', 'recruiting'],
        'Main results already published': ['complete', 'not_recruiting'],
        'No longer recruiting': ['ongoing', 'not_recruiting'],
        'Open public recruiting(outpatients can be recruited publicly)': ['ongoing', 'recruiting'],
        'Preinitiation': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Suspended': ['suspended', 'not_recruiting'],
        'Terminated': ['terminated', 'not_recruiting'],
    }
    status, recruitment_status = statuses[record.get('recruitment_status')]

    # Get gender
    gender = None
    if record['gender'] == 'Male and Female':
        gender = 'both'
    elif record['gender'] == 'Male':
        gender = 'male'
    elif record['gender'] == 'Female':
        gender = 'female'

    # Get has_published_results
    has_published_results = False
    if record['publication_of_results'] in ['Published', 'partially published']:
        has_published_results = True

    # Get study phase
    study_phase = base.normalizers.get_normalized_phase(record['developmental_phase'])

    # Get age_range
    age_range = extract_age_range(record)

    trial = {
        'identifiers': identifiers,
        'registration_date': record['date_of_registration'],
        'public_title': public_title,
        'brief_summary': record['narrative_objectives1'],
        'scientific_title': record['official_scientific_title_of_the_study'],
        'description': record['narrative_objectives1'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'inclusion': record['key_inclusion_criteria'],
            'exclusion': record['key_exclusion_criteria'],
        },
        'target_sample_size': record['target_sample_size'],
        'first_enrollment_date': record['anticipated_trial_start_date'],
        'study_type': record['study_type'],
        'study_design': record['basic_design'],
        'study_phase': study_phase,
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['key_secondary_outcomes'],
        'gender': gender,
        'age_range': age_range,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    conditions.append({
        'name': record['condition'],
    })
    return conditions


def extract_interventions(record):
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    organisations.append({
        'name': record['name_of_primary_sponsor'],
        # ---
        'trial_role': 'primary_sponsor',
    })
    organisations.append({
        'name': record['source_of_funding'],
        # ---
        'trial_role': 'funder',
    })
    return organisations


def extract_persons(record):
    persons = []
    persons.append({
        'name': record.get('research_name_of_lead_principal_investigator', None),
        # ---
        'trial_id': record['unique_trial_number'],
        'trial_role': 'principal_investigator',
    })
    persons.append({
        'name': record.get('public_name_of_contact_person', None),
        # ---
        'trial_id': record['unique_trial_number'],
        'trial_role': 'public_queries',
    })
    return persons


def extract_documents(record):
    documents = []
    results_url = record.get('url_releasing_results')
    if results_url:
        document = {
            'name': 'Results',
            'source_url': results_url,
        }
        documents.append(document)
    return documents


def extract_document_category(record):
    return {
        'id': 22,
        'name': 'Clinical study report',
        'group': 'Results',
    }


def extract_age_range(record):

    def extract_first_number(string_with_int):

        numbers = [int(s) for s in string_with_int.split() if s.isdigit()]

        return numbers[0]

    def correct_age_value(age_string):

        if '=' not in age_string:

            if '<' in age_string:

                age = extract_first_number(age_string)
                corrected_age = int(age) - 1
                corrected_age = str(corrected_age)

                age_string.replace(age, corrected_age)

            elif '>' in age_string:

                age = extract_first_number(age_string)
                corrected_age = int(age) + 1
                corrected_age = str(corrected_age)

                age_string.replace(age, corrected_age)

        return age_string

    def clean(string):
        return string.replace('<', '') \
            .replace('>', '') \
            .replace('=', '') \
            .replace('-old', '') \
            .replace('\n', ' ')

    maximum_age = record['ageupper_limit']
    minimum_age = record['agelower_limit']

    if not maximum_age or 'n/a' in maximum_age.lower():
        maximum_age = 'N/A'

    if not minimum_age or 'n/a' in minimum_age.lower():
        minimum_age = 'N/A'

    if 'Not applicable' in maximum_age:
        maximum_age = 'N/A'
    else:
        maximum_age = correct_age_value(maximum_age)
        maximum_age = clean(maximum_age)
        maximum_age = base.helpers.format_age(maximum_age)

    if 'Not applicable' in minimum_age:
        minimum_age = 'N/A'
    else:
        minimum_age = correct_age_value(minimum_age)
        minimum_age = clean(minimum_age)
        minimum_age = base.helpers.format_age(minimum_age)

    return {'minimum_age': minimum_age, 'maximum_age': maximum_age}
