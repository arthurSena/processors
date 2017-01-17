import os
import csv
import logging
import json

logger = logging.getLogger(__name__)

def build_phase_variation_map(file):
    """
        Receives a path as an input and returns a dict containing
        all normalized phases and their variations

        :param
            file (str): path to the phase variations file
        :return:
            variation map (dict): dict that contains all normalized phases and
                                    their variations
    """
    variation_map = {}
    with open(file, 'r') as variations:
        reader = csv.reader(variations, quotechar='"', delimiter=',')
        for line in reader:
            variation, target = line[0], line[1]
            if target in variation_map.keys():
                variation_map[target].append(variation)
            else:
                variation_map[target] = [target, variation]
    return variation_map

def array_to_json(phases_list):
    """ Receives a list containing normalized phases of an study
        and returns its json representation as a string.

        :param:
            phases_array (list): normalized phases

        :return:
            normalized_json (str): json containing phase normalization

    """
    study_phases = {}
    study_phases["Phases"] = phases_array
    normalized_json = json.dumps(study_phases)
    return normalized_json

def get_normalized_phase(phase):
    """ Receives a phase as an input and normalizes it if possible.
        Else, returns the unormalized phase.

        :param:
            phase (str): unormalized phase

        :return:
            phase_suggestions (str): normalized phase suggestions
    """
    if not phase:
        logger.debug('Unsuccessfully phase normalization \'None\'')
        return phase
    phase_variation_map = build_phase_variation_map\
                        (os.path.join(os.path.dirname(__file__),
                                      'phases_variations.csv'))
    phase_suggestions = []
    for phase_normalized, phase_variations in phase_variation_map.items():
        if phase in phase_variations:
            phase_suggestions.append(phase_normalized)
    if phase_suggestions:
        logger.debug(
            'Phase \'%s\' successfully normalized to \'%s\'',
            phase, phase_suggestions)
        return array_to_json(phase_suggestions)
    else:
        logger.debug(
            'Unsuccessfully phase normalization \'%s\'',
            phase)
        return array_to_json(phase)
