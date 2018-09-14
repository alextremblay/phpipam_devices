#!/usr/bin/env python3
"""
    NAME
        phpipam_dev -- phpIPAM Devices tool

    SYNOPSIS
        phpipam_dev -h
        phpipam_dev -r
        phpipam_dev get [search_word]
        phpipam_dev create
        phpipam_dev update

    DESCRIPTION
        This tool allows you to retireve information about devices in a phpIPAM
        installation and create / update devices.

    COMMAND LINE OPTIONS
        -h, --help
            Print this help message and exit
        -r, --reset
            Delete stored application data and exit

    AUTHOR
        Alex Tremblay

"""
# Local imports
import config
import phpipam_dev

# Std Lib imports
import sys

# External imports
import click


settings = config.get(name='phpipam', values=[
                          {
                              'value': 'url',
                              'prompt': "Please enter the full URL of your "
                                        "phpIPAM installation including the API"
                                        " app_id \nex. https://phpipam."
                                        "mycompanyserver.com/api/app_id/ \n"
                                        "URL> ",
                              'optional': False,
                              'sensitive': False
                          },
                          {
                              'value': 'username',
                              'prompt': "Please enter your phpIPAM username: \n"
                                        "Username> ",
                              'optional': True,
                              'sensitive': False
                          },
                          {
                              'value': 'password',
                              'prompt': "Please enter your phpIPAM password: \n"
                                        "Password> ",
                              'optional': True,
                              'sensitive': True
                          },
                      ])


@click.group()
@click.option('--reset', is_flag=True)
def main(reset=False):
    if reset:
        config.reset()
        sys.exit()


@main.command()
@click.option('--csv-mode', '-c', is_flag=True)
@click.argument('search_word', required=False)
def get(csv_mode=False, search_word=None):
    phpipam_dev.get(**settings, csv_mode=csv_mode, search_word=search_word)


@main.command()
@click.argument('hostname')
@click.argument('ip', required=False)
@click.argument('Building', required=False)
@click.argument('Closet', required=False)
@click.argument('Serial', required=False)
@click.argument('model', required=False)
@click.argument('vendor', required=False)
@click.argument('version', required=False)
@click.argument('description', required=False)
def create(hostname, *optionals ):
    test = phpipam_dev.Device(hostname, *optionals)
    print(test.asdict())
    phpipam_dev.create(**settings, device=test)


if __name__ == "__main__":
    main()
