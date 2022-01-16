- Download the zip file for your operating system.
- Unzip file.
- cd into the directory that you have unzipped the file.
- Run command (example below)

### CLI help
```
path/to/executable/file >GPcli.exe -h
usage: GPcli.exe [-h] -r input_file_path [-n number_of_partitions]
                 [-o output_path] [-d]
                 method

A graph partitioning application!

positional arguments:
  method                Name of graph partition algorithm. Options
                        are:['SpectralBisection', 'KernighanLin',
                        'EdgeBetweennessCentrality']

optional arguments:
  -h, --help            show this help message and exit
  -r input_file_path, --read input_file_path
                        Opens and reads the specified graph file.
  -n number_of_partitions, --number_of_partitions number_of_partitions
                        Number of partitions to be created by algorithm
  -o output_path, --output output_path
                        output path with filename for output file. Default
                        name is [input_filename]-output.csv and default
                        directory is current directory
  -d, --draw            Draws a graphical representation of graph. Default is
                        false

```
 
 ### Usage example
 ```
path/to/executable/file >GPcli.exe -r soc-karate.csv -n 3 -o karate-edge-betweenness.csv EdgeBetweennessCentrality
Reading soc-karate.csv...
soc-karate.csv is read.
Graph Info:
Name: soc-karate
Type: Graph
Number of nodes: 34
Number of edges: 78
Average degree:   4.5882
Partitioning...
Done.
Creating output file...
karate-edge-betweenness.csv created.

```
