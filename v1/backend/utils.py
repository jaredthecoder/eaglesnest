# Python Standard Library assets
import argparse

# Setup the command line parser
def setup_argparser():

    parser = argparse.ArgumentParser(description='Viz',
                                     version='0.0.0',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('--filter_type', dest='filter_type', required=False, type=str, default='location', help='[location/keyword] What type of filter to put on the twitter stream. Default is location.')
    parser.add_argument('--keywords', dest='keywords', required=False, type=[], nargs='+', help='Keywords to filter by. Only used if filter_type is keywords.')
    return parser

