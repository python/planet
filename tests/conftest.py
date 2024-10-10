import configparser

import planet as planet_module
import pytest


@pytest.fixture(name="config")
def get_config(tmp_path):
    config = configparser.ConfigParser()
    ini_text = f"""\
    [Planet]
    name = Test Planet
    output_dir = {tmp_path}/output
    cache_directory = {tmp_path}/cache

    [https://example.com/rss]
    name = example rss

    [https://example.com/atom]
    name = example atom
    """

    config.read_string(ini_text)
    return config


@pytest.fixture(name="planet")
def get_planet(config):
    return planet_module.Planet(config)


@pytest.fixture(name="rss_channel")
def get_rss_channel(planet):
    return planet_module.Channel(planet, "https://example.com/rss")


@pytest.fixture(name="atom_channel")
def get_atom_channel(planet):
    return planet_module.Channel(planet, "https://example.com/atom")
