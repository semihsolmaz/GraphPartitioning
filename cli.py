import argparse
import networkx as nx
from graphpartitioning import SpectralBisection
import csv


def cli():
    parser = argparse.ArgumentParser(description="A graph partitioning application!")

    # defining arguments for parser object
    parser.add_argument('method',
                        choices=['SpectralBisection'],
                        type=str,
                        nargs=1,
                        metavar="method",
                        help="Name of graph partiton algorithm. Options are:['SpectralBisection']")

    parser.add_argument("-r", "--read",
                        type=str, nargs=1,
                        metavar="input_file_path",
                        default=None,
                        required=True,
                        help="Opens and reads the specified graph file.")

    parser.add_argument("-o", "--output", type=str, nargs=1,
                        metavar="output_path", default=None,
                        help="output path with filename for output file. "
                             "Default name is [input_filename]-output.csv and default directory is current directory")

    parser.add_argument("-d", "--draw",
                        action='store_true',
                        help="Draws a graphical representation of graph. Default is false")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.read is not None:
        print(args)
        graph = nx.read_edgelist(args.read[0], delimiter=',', nodetype=str)
        graph.name = args.read[0].split('.')[0]

    if args.method is not None:
        if args.method[0] == 'SpectralBisection':
            partitions = SpectralBisection(graph).partition()

        if args.output is not None:
            output_file = args.output[0]
        else:
            output_file = args.read[0].split('.')[0] + '-output.csv'

        headers = ['node', 'node', 'partition']

        with open(output_file, 'w', encoding='UTF8') as f:

            writer = csv.writer(f)
            writer.writerow(headers)

            for index, partition in enumerate(partitions):
                for edge in partition.edges:
                    writer.writerow(list(edge) + [str(index)])

    # elif args.delete != None:
    #     delete(args)
    # elif args.copy != None:
    #     copy(args)
    # elif args.rename != None:
    #     rename(args)


if __name__ == "__main__":
    # calling the main function
    cli()
