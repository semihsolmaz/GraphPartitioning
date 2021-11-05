# GraphPartitioning
Graph partitioning tool with command line interface.

Software reads undirected unweigthed graphs from file and applies graph partitionig algorithm on given graphs.

An edge list labeled with partitons isoutputted to a csv file.

Optionally, a png graphic file displaying orginal graph and the removed edges can be created.

## Usage
```
usage: cli.py [-h] -r input_file_path [-o output_path] [-d] method

A graph partitioning application!

positional arguments:
  method                Name of graph partiton algorithm. Options
                        are:['SpectralBisection']

optional arguments:
  -h, --help            show this help message and exit
  -r input_file_path, --read input_file_path
                        Opens and reads the specified graph file.
  -o output_path, --output output_path
                        output path with filename for output file. Default
                        name is [input_filename]-output.csv and default
                        directory is current directory
  -d, --draw            Draws a graphical representation of graph. Default is
                        false
```                        
