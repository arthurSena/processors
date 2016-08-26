# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'nct',
        'name': 'ClinicalTrials.gov',
        'type': 'register',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['nct_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['brief_title'],
        record['official_title'],
        record['nct_id'])

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Active, not recruiting': ['ongoing', 'not_recruiting'],
        'Approved for marketing': ['other', 'other'],
        'Available': ['ongoing', 'unknown'],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation': ['ongoing', 'recruiting'],
        'No longer available': ['other', 'other'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Suspended': ['suspended', 'not_recruiting'],
        'Temporarily not available': ['other', 'other'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Withdrawn': ['withdrawn', 'not_recruiting'],
        'Withheld': ['other', 'other'],
    }
    status, recruitment_status = statuses[record.get('overall_status')]

    # Get gender
    gender = None
    if (record['eligibility'] or {}).get('gender', None):
        gender = record['eligibility']['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['clinical_results']:
        has_published_results = True

    trial = {
        'identifiers': identifiers,
        'registration_date': record['firstreceived_date'],
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': record['eligibility'],
        'target_sample_size': record['enrollment_anticipated'],
        'first_enrollment_date': record['start_date'],
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': record['phase'],
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    for element in record['conditions'] or []:
        conditions.append({
            'name': element,
        })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['interventions'] or []:
        interventions.append({
            'name': element['intervention_name'],
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['location_countries'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            # ---
            'trial_role': 'recruitment_countries',
        })
    return locations


def extract_organisations(record):
    organisations = []
    for element in record['sponsors'] or []:
        organisations.append({
            'name': element.get('lead_spondor', {}).get('agency', ''),
            # ---
            'trial_role': 'primary_sponsor',
        })
    return organisations


def extract_persons(record):
    persons = []
    for element in record['overall_officials'] or []:
        if element.get('role', None) == 'Principal Investigator':
            persons.append({
                'name': element['last_name'],
                # ---
                'trial_id': record['nct_id'],
                'trial_role': 'principal_investigator',
            })
    return persons
