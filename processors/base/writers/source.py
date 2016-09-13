# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import datetime
logger = logging.getLogger(__name__)


# Module API

def write_source(conn, source):
    """Write source to database.

    Args:
        conn (dict): connection dict
        source (dict): normalized source data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Read object
    object = conn['database']['sources'].find_one(id=source['id'])

    # Create object
    if not object:
        object = {}
        object['id'] = source['id']
        object['created_at'] = timestamp
        create = True

    # Update object
    object.update({
        'updated_at': timestamp,
        # ---
        'name': source['name'],
        'type': source.get('type'),
        'url': source.get('url'),
        'terms_and_conditions_url': source.get('terms_and_conditions_url'),
    })

    # Write object
    conn['database']['sources'].upsert(object, ['id'], ensure=False)

    # Log debug
    logger.debug('Source - %s: %s',
        'created' if create else 'updated', source['name'])

    return object['id']
