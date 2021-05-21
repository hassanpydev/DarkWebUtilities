from DarkWebHelpers.initiators.API_Engine import Query
from DarkWebHelpers.FileHandler.FileUtility import write_json
from  random import randint
import argparse
import sys
from os import  path
import os
args = argparse.ArgumentParser()
args.add_argument('-k', type=str, required=True, help="A Keyword to look for")
args.add_argument('-n', type=int, required=True, help="A page number")
parser = args.parse_args()


def main():
    if parser.k and parser.n:
        query_string = Query(query=parser.k,deepScan=False)
        query_string.MakeRequest(int(parser.n))
        file_path = '/tmp'
        name = "{}".format(randint(1,100))
        write_json(path=file_path, data_file=query_string.Result_Json, name=name)
        sys.stdout.write(str(path.join(file_path, name + '.json')))


if __name__ == '__main__':
    main()
