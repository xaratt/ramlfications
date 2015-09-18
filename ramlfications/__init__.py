# -*- coding: utf-8 -*-
# Copyright (c) 2015 Spotify AB

from __future__ import absolute_import, division, print_function

__author__ = "Lynn Root"
__version__ = "0.1.7"
__license__ = "Apache 2.0"

__email__ = "lynn@spotify.com"
__uri__ = "https://ramlfications.readthedocs.org"
__description__ = "A Python RAML parser"

import six

from ramlfications.config import setup_config
from ramlfications.parser import parse_raml

from ramlfications._helpers import load_file, load_string, load_uri


def load(raml_file):
    """
    Module helper function to load a RAML File using \
    :py:class:`.loader.RAMLLoader`.

    :param str raml_file: String path to RAML file
    :return: loaded RAML
    :rtype: dict
    :raises LoadRAMLError: If error occurred trying to load the RAML file
    """
    return load_file(raml_file)


def loads(raml_string):
    """
    Module helper function to load a RAML File using \
    :py:class:`.loader.RAMLLoader`.

    :param str raml_string: String of RAML data
    :return: loaded RAML
    :rtype: dict
    :raises LoadRAMLError: If error occurred trying to load the RAML file
    """
    return load_string(raml_string)

def loadu(raml_uri):
    """
    Module helper function to load a RAML File using \
    :py:class:`.loader.RAMLLoader`.

    :param str raml_uri: String URI to RAML file
    :return: loaded RAML
    :rtype: dict
    :raises LoadRAMLError: If error occurred trying to load the RAML file
    """
    return load_uri(raml_uri)


def parse(raml, config_file=None, loader=None):
    """
    Module helper function to parse a RAML File.  First loads the RAML file
    with defined loader or trying to select it then parses with
    :py:func:`.parser.parse_raml` to return a :py:class:`.raml.RAMLRoot`
    object.

    :param raml: Either string path or URI to the RAML file, a file object, or \
        a string representation of RAML.
    :param str config_file:  String path to desired config file, if any.
    :param func loader:  Preferred RAML loaded, if any.
    :return: parsed API
    :rtype: RAMLRoot
    :raises LoadRAMLError: If error occurred trying to load the RAML file
        (see :py:class:`.loader.RAMLLoader`)
    :raises InvalidRootNodeError: API metadata is invalid according to RAML \
        `specification <http://raml.org/spec.html>`_.
    :raises InvalidResourceNodeError: API resource endpoint is invalid \
        according to RAML `specification <http://raml.org/spec.html>`_.
    :raises InvalidParameterError: Named parameter is invalid \
        according to RAML `specification <http://raml.org/spec.html>`_.
    """
    if not loader:
        loader = load
        # try to select loader based on raml content
        if isinstance(raml, six.text_type) or isinstance(raml, bytes):
            if raml.startswith("#%RAML"):
                loader = loads
            elif raml.startswith("http"):
                loader = loadu
    loaded_data = loader(raml)
    config = setup_config(config_file)
    return parse_raml(loaded_data, config)


def validate(raml, config_file=None):
    """
    Module helper function to validate a RAML File.  First loads \
    the RAML file \
    with :py:class:`.loader.RAMLLoader` then validates with \
    :py:func:`.validate.validate_raml`.

    :param str raml: Either string path to the RAML file, a file object, \or
        a string representation of RAML.
    :param str config_file:  String path to desired config file, if any.
    :return: No return value if successful
    :raises LoadRAMLError: If error occurred trying to load the RAML file
        (see :py:class:`.loader.RAMLLoader`)
    :raises InvalidRootNodeError: API metadata is invalid according to RAML \
        `specification <http://raml.org/spec.html>`_.
    :raises InvalidResourceNodeError: API resource endpoint is invalid \
        according to RAML `specification <http://raml.org/spec.html>`_.
    :raises InvalidParameterError: Named parameter is invalid \
        according to RAML `specification <http://raml.org/spec.html>`_.
    :raises InvalidRAMLError: RAML file is invalid according to RAML \
        `specification <http://raml.org/spec.html>`_.
    """
    loader = load(raml)
    config = setup_config(config_file)
    config["validate"] = True
    parse_raml(loader, config)
