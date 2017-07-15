# pybind11 compiler benchmarking tools

Tools for benchmarking [pybind11](https://github.com/pybind/pybind11) test
suite compilations.

## Generating test data

Usage (from a pybind11 checkout):

    N=50 # How many times to build the test suite
    mkdir build-gcc && cd build-gcc
    CXX='/path/to/pybind11-compiler-bench/timec++ g++' cmake ..
    for ((i = 0; i < $N; i++)); do make clean && make; done
    # (wait patiently for $N builds to complete)
    mv tests/timings.txt /path/to/pybind11-compiler-bench/timings1.txt

Repeat this to generate different `timings*.txt` files for different compilers
and/or different modifications.

## Comparing test data

    cd /path/to/pybind11-compiler-bench
    python3 compare-timings.py timings1.txt timings2.txt [...]

which will give you the mean and standard deviation of compiler user CPU time
and maximum memory for the compilation of each test suite object.  For any
input files beyond the first (e.g. `timings2.txt` above) you also get a
relative difference of the mean values relative to the mean values of the first
file.
