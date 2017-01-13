import os
import csv
import logging

logger = logging.getLogger(__name__)

def write_fail_log(log):
    f = open("/tmp/log_fail_pahse.txt", "a")
    f.write(log)
    f.close()

def build_phase_variation_map(file):
    """
        Receives a path as an input and returns a dict containing
        all normalized phases and their variations

        :param
            file (str): path to the phase variations file
        :return:
            variation map (dict): dict that contains all normalized phases and their variations
    """

    variation_map = {}
    with open(file, 'r') as variations:
        reader = csv.reader(variations, delimiter='|')
        for line in reader:
            variation_map[line[0]] = map(lambda v: v.strip(), line)
    return variation_map

def get_normalized_phase(phase):

    """ Receives a phase as an input and normalizes it if possible.
        Else, returns the unormalized phase.

        :param:
            phase (str): unormalized phase

        :return
            phase_suggested (str): normalized phase
    """

    phase_variation_map = build_phase_variation_map(os.path.join(os.path.dirname(__file__),
                                                 'phases_variations.psv'))
    phase_suggested = None
    for phase_normalized, phase_variations in phase_variation_map.items():
        if phase in phase_variations:
            phase_suggested = phase_normalized

    if phase_suggested:
        logger.debug(
            'Phase "%s" successfully normalized to "%s"',
            phase, phase_suggested)
        return phase_suggested
    else:
        logger.debug(
            'Unsuccessfully phase normalization "%s"',
            phase)
        temp_log = 'Unsuccessfully phase normalization "%s"', phase
        write_fail_log(temp_log)
        return phase
