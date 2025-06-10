# FMCooler

**FMCooler** is a Feature Model solver tool that uses the **Simulated Annealing** algorithm to search for valid and optimized feature configurations.

## Functionality

FMCooler explores Feature Models to find optimal or near-optimal configurations by applying heuristic search techniques. It is especially useful for working with complex software product lines and variability management.

## Required Setup

This project is publicly hosted as an open-source repository on GitHub and can be cloned using the following command:

```bash
git clone http://github.com/jdanielescanez/fmcooler
```

## Installation

FMCooler requires Python 3.13. Once the repository has been cloned, navigate into the project directory and install the module along with its dependencies in editable mode:

```bash
cd fmcooler
pip install -e .
```

This will install all necessary dependencies and make the package available for development and use.

## Usage

An example of execution of `fmcooler` gets a feature model (e.g., `tree.uvl`) and a weights file (e.g., `weights.csv`) where we have the data about the impact of each feature for a concrete criteria (e.g., `variable`) that we would like to minimize (i.e., `min`, as `max` is used to maximize) using `100` reads (note that a read refers to one independent run of the annealing algorithm, starting from a initial state and proceeding through the annealing schedule to produce a single sample).

```bash
./fmcooler.py tree.uvl weights.csv variable min 100
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. If you encounter any bugs or have feature requests, please open an issue.

## License

This project is released under an open-source license. See the LICENSE file for more information.