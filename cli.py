import argparse
import networkx as nx
from graphpartitioning import SpectralBisection
import csv


@click.group()
# @click.option('--debug/--no-debug', default=False)
@click.option("--in", "-i", "in_file", required=True, help="Path to graph file to be processed.",)
@click.pass_context
def cli(ctx, in_file):
    ctx.ensure_object(dict)
    ctx.obj['in_file'] = [in_file]
    click.echo(in_file)


@cli.command()  # @cli, not @click!
# @click.argument('filename')
# @click.option("--in", "-i", "in_file", required=True, help="Path to graph file to be processed.",)
# @click.option("--out-file", "-o", default="./output.xlsx", help="Path to output file for partitions.")
# @click.option("--delimiter", "-del", default=" ", help="Delimiter for edge list file.")
# @click.option('--draw', '-d', default='',
#               type=click.Choice(['', 'kamada-kawai', 'circular'], case_sensitive=False),
#               help="Layout for graphic output.")
@click.pass_context
def SpectralBisection(ctx):
    filename = ctx.obj['in_file']
    click.echo('Loading ' + filename[0] + '...')
    graph = nx.read_edgelist(filename[0], delimiter=',', nodetype=str)
    graph.name = filename[0].split('.')[0]
    click.echo(filename[0] + ' read:\n' + nx.info(graph))

    click.echo('Partitioning...')
    bisection = SpectralBisection(graph)
    click.echo('hre...')
    partitions = bisection.partition()
    click.echo('hre...')
    header = ['node', 'node', 'partition']
    click.echo('hre...')
    with open(filename[0].split('.')[0] + '-output.csv', 'w', encoding='UTF8') as f:
        click.echo('hre...')
        writer = csv.writer(f)
        writer.writerow(header)

        for index, partition in enumerate(partitions):
            for edge in partition.edges:
                writer.writerow(list(edge) + [str(index)])

    # if len(draw) > 0:
    #     print('drawing')


if __name__ == "__main__":
    cli(obj={})
