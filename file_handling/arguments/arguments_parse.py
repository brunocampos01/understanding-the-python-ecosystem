"""
python [file].py [command] [options] NAME
python argparse/commands.py --help

https://docs.python.org/3/howto/argparse.html
"""
import argparse


def execute_process(options):
    pass

    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Execute SQL")
    parser.add_argument('-f','--fileName', metavar='fileName', type=str, help='')
    parser.add_argument('-e','--schemaExadata', metavar='schemaExadata', type=str, help='')
    parser.add_argument('-a','--schemaExadataAux', metavar='schemaExadataAux', type=str, help='')
    parser.add_argument('-i','--impalaHost', metavar='impalaHost', type=str, help='')
    parser.add_argument('-o','--impalaPort', metavar='impalaPort', type=str, help='')
    args = parser.parse_args()

    options = {
                    'file_name': args.fileName,
                    'schema_exadata': args.schemaExadata, 
                    'schema_exadata_aux': args.schemaExadataAux,
                    'impala_host' : args.impalaHost,
                    'impala_port' : args.impalaPort
                }

    execute_process(options)
