# flagser

## Modifications

This fork of `flagser` adds one new operation to the math parser, called `maxabs`.
This outputs the maximum of the absolute values of the filtration times of the faces.
The purpose of this operation is so that some edges can be marked with a negative values; these edges will all appear before `t=0` but higher simplices arrive at the same time.
This allows the computation of grounded persistent directed flag complex homology (GrPdFlH).
To facilitate this application, we include a small Python wrapper in `GrPdFlH.py`.

The Python wrapper exports a single function `GrPdFlH(digraph, flagser_path)`.
The first input should be a weighted `networkx.DiGraph` and the second input should be the path to the compiled `flagser` binary from this fork.
The example A.13 from the paper is included to illustrate usage of the wrapper.

In order to run the test, follow the build instructions as below.
Then move back into the root directory and run the example
```
cd ..
python example_a13.py
```
You should see the output
```
[[0.0, 21.0]]
[[0.0, 30.0]]
```

A new software package, designed specifically for computing GrPdFlH and GrPPH is available [here](https://github.com/tomchaplin/grpphati).
For the associated article, please see [the arXiv preprint](https://arxiv.org/abs/2210.11274).

## Original README

Copyright © 2017–2021 Daniel Lütgehetmann.

### Description

flagser computes the homology of directed flag complexes. For a more detailed
description consult the documentation under `docs/documentation_flagser.pdf`.

### Building

Flagser requires a C++14 compiler and cmake. Here is how to obtain, build, and
run flagser:

```sh
git clone git@gitlab.com:luetge/flagser.git
cd flagser
(mkdir -p build && cd build && cmake .. && make -j)
./test/run
```

### Running

To call flagser you run

```sh
./flagser --out example.homology test/medium-test-data.flag
```

For more detailed instructions, see `docs/documentation_flagser.pdf`. 

You can run `flagser` with the argument `--in-memory` which changes `flagser` 
internals storing the full directed flag complex in memory, speeding up parts 
of the computation but requiring more memory.

Included in this package is also the original program `ripser`, modified only
in that the features of `flagser` are supported.

### Euler characteristic and cell counts

To only compute the Euler characteristic and cell counts, run

```sh
./flagser-count example.flag
```

### Online Version

An online version is available here (thanks to [JasonPSmith]( https://github.com/JasonPSmith )): https://homepages.abdn.ac.uk/neurotopology/flagser.html

### License

flagser is licensed under the MIT license (COPYING.txt), with an extra clause (CONTRIBUTING.txt) clarifying the license for modifications released without an explicit written license agreement. Please contact the author if you want to use Ripser in your software under a different license.
