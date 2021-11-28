import argparse
import networkx as nx
from graphpartitioning import SpectralBisection, KernighanLin
import csv
from colorama import init, deinit


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cli():
    parser = argparse.ArgumentParser(description="A graph partitioning application!")

    # defining arguments for parser object
    parser.add_argument('method',
                        choices=['SpectralBisection', 'KernighanLin'],
                        type=str,
                        nargs=1,
                        metavar="method",
                        help="Name of graph partition algorithm. "
                             "Options are:['SpectralBisection', 'KernighanLin', 'EdgeBetweennessCentrality']")

    parser.add_argument("-r", "--read",
                        type=str, nargs=1,
                        metavar="input_file_path",
                        default=None,
                        required=True,
                        help="Opens and reads the specified graph file.")

    parser.add_argument("-n", "--number_of_partitions",
                        type=int, nargs=1,
                        metavar="number_of_partitions",
                        default=2,
                        help="Number of partitions to be created by algorithm")

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
        print(f"{bcolors.BOLD}Reading {args.read[0]}...{bcolors.ENDC}")
        graph = nx.read_edgelist(args.read[0], delimiter=',', nodetype=str)
        graph.name = args.read[0].split('.')[0]
        print(f"{bcolors.OKGREEN}{args.read[0]} is read.{bcolors.ENDC}")
        print(f"Graph Info:\n{nx.info(graph)}")

    # todo: add controls for directed and weighted graphs
    if args.method is not None:
        if args.method[0] == 'SpectralBisection':
            print(f"{bcolors.BOLD}Partitioning...{bcolors.ENDC}")
            parted_graph = SpectralBisection(graph)
            partitions = parted_graph.partition(args.number_of_partitions[0])
            print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")
        elif args.method[0] == 'KernighanLin':
            print(f"{bcolors.BOLD}Partitioning...{bcolors.ENDC}")
            parted_graph = KernighanLin(graph)
            partitions = parted_graph.partition(args.number_of_partitions[0])
            print(f"{bcolors.OKGREEN}Done.{bcolors.ENDC}")
        elif args.method[0] == 'EdgeBetweennessCentrality':
            print('EdgeBetweennessCentrality')

        if args.output is not None:
            output_file = args.output[0]
        else:
            output_file = args.read[0].split('.')[0] + '-output.csv'

        headers = ['node', 'node', 'partition']

        print(f"{bcolors.BOLD}Creating output file...{bcolors.ENDC}")
        with open(output_file, 'w', encoding='UTF8') as f:

            writer = csv.writer(f)
            writer.writerow(headers)

            for index, partition in enumerate(partitions):
                for edge in partition.edges:
                    writer.writerow(list(edge) + [str(index)])

        print(f"{bcolors.OKGREEN}{output_file} created.{bcolors.ENDC}")

        if args.draw:
            print(f"{bcolors.BOLD}Drawing graph...{bcolors.ENDC}")
            parted_graph.drawInitialWithColor(args.read[0].split('.')[0] + '.png')
            print(f"{bcolors.OKGREEN}{args.read[0].split('.')[0] + '.png'} created.{bcolors.ENDC}")
    # elif args.delete != None:
    #     delete(args)
    # elif args.copy != None:
    #     copy(args)
    # elif args.rename != None:
    #     rename(args)


if __name__ == "__main__":
    # calling the main function
    init()
    cli()
    deinit()
