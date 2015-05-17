import sys

from harvester import Harvester

if __name__ == "__main__":

    keywords = []
    for arg in sys.argv:
        keywords += str(arg)

    if len(keywords) == 0:
        h = Harvester()
    else:
        h = Harvester(filter_type='keyword', keywords=keywords)

    h.stream()

