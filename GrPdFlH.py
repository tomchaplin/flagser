import os, tempfile, subprocess
import networkx as nx
import re
import numpy as np
from math import floor

# In all of these functions digraph is a NetworkX.DiGraph
# Assumed to be weighted

def reg_path(digraph):
    return False

def _build_flag_file_str(digraph):
    strings = []
    nn = digraph.number_of_nodes()
    sp_iter = nx.shortest_path_length(digraph, weight='weight')

    # Add the 1-simplices and figure out the most negative entry
    lowest_entry = 0
    strings.append('dim 1:')
    for source, sp_dict in sp_iter:
        for target, length in sp_dict.items():
            if source == target:
                continue
            # Mark underlying edges by giving them negative weight
            is_underlying_edge = digraph.has_edge(source, target)
            weight = -length if is_underlying_edge else length
            lowest_entry = weight if weight < lowest_entry else lowest_entry
            # strings.append(f"%d %d %f" % (source, target, weight))
            string = str(source) + ' ' + str(target) + ' ' + f"{weight:.3f}"
            strings.append(string)

    # Now go back and add the 0-simplices
    zero_entry = floor(lowest_entry-1)
    strings.insert(0, ' '.join([str(zero_entry) for i in range(nn)]))
    strings.insert(0, 'dim 0:')
    return "\n".join(strings)

def _parse_single_flagser_line(line):
    # This regex allows for positive/negative numbers and exponential notation
    bar = list(map(float, re.findall(r'[\+\-\d.e]+', line)))
    bar[0] = max(bar[0], 0.0) # Make birth times 0 since artifically negative
    # Infinity bars are in the format [t, ) so bar wil be a singleton [t]
    if len(bar)<2:
        bar.append(np.inf)
    return bar


def _parse_flagser_output(flagser_output):
    lines = list(flagser_output.splitlines())
    start = 1;
    end = lines.index('')
    return list(map(_parse_single_flagser_line, lines[start:end]))

def GrPdFlH(digraph, flagser_path):
    # Flagser expects nodes to be labelled 0 through n
    digraph = nx.convert_node_labels_to_integers(digraph, first_label=0)
    # Build string that flagser expects in file
    flag_file_str = _build_flag_file_str(digraph)
    # Build up the OS command to run
    tmp_in = tempfile.NamedTemporaryFile(delete=False, mode="w")
    tmp_out_name = next(tempfile._get_candidate_names())
    tmp_dir = tempfile._get_default_tempdir()
    tmp_out_path = tmp_dir+"/tmp"+tmp_out_name
    cmd = [flagser_path,
            '--out', tmp_out_path,
            '--max-dim', str(1),
            '--min-dim', str(1),
            '--filtration', 'maxabs',
            tmp_in.name]
    # Write flagser input to file
    try:
        tmp_in.write(flag_file_str)
    finally:
        tmp_in.close()
    # Run flagser
    proc = subprocess.run(cmd, capture_output=True)
    # Read flagser output from file
    with open(tmp_out_path, "r") as tmp_out:
        output = tmp_out.read()
    # Get rid of temp files
    os.unlink(tmp_in.name)
    os.unlink(tmp_out_path)
    # Parse flagser output and return to user
    parsed = _parse_flagser_output(output)
    return parsed
