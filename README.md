# FMCooler

**FMCooler** is a tool that uses the **Simulated Annealing** algorithm to search for valid and optimized feature configurations within feature models.

https://github.com/user-attachments/assets/12e87894-fa4b-44bb-a43b-b1776ef972ce

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

A generic example of execution of `fmcooler` gets a feature model (e.g., `tree.uvl`) and a weights file (e.g., `weights.csv`) where we have the data about the impact of each feature for a concrete criteria (e.g., $\sum_i$ `variable`$_i \cdot$ `rate`$_i$) that we would like to minimize (i.e., `min`, as `max` is used to maximize) using `100` reads (note that a read refers to one independent run of the annealing algorithm, starting from a initial state and proceeding through the annealing schedule to produce a single sample).

```bash
./fmcooler.py tree.uvl weights.csv variable1,...,variableN:rate1,...,rateN min 100
```

## Execution Examples

### Mono-criteria

An example of execution of `fmcooler` runs `1000` independent annealing-based optimization processes on the feature model specified in `examples/mobile_media.uvl`, using the impact data from `examples/mobile_media.csv`. The goal is to **minimize** the weighted influence of the `Battery` feature with a coefficient of `1.0`. Each run starts from a different initial state and follows an annealing schedule to explore possible configurations, producing samples that seek to reduce the total impact of the `Battery` feature as much as possible.

```bash
./fmcooler.py examples/mobile_media.uvl examples/mobile_media.csv Battery:1.0 min 1000
```

### Multi-criteria
The last example of `fmcooler` execution runs `10000` processes on the same feature model and using the same impact data. The goal is to **maximize** the combined weighted influence of `Battery` and `Usability` features, each weighted with a coefficient of `0.5`.

```bash
./fmcooler.py examples/mobile_media.uvl examples/mobile_media.csv Battery,Usability:0.5,0.5 max 10000
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. If you encounter any bugs or have feature requests, please open an issue.

## License

This project is released under an open-source license. See the LICENSE file for more information.
