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

FMCooler requires Python >= 3.11. Once the repository has been cloned, navigate into the project directory and install the module along with its dependencies in editable mode:

```bash
cd fmcooler
pip install -e .
```

This will install all necessary dependencies and make the package available for development and use. You can see the dependencies inside the `pyproject.toml` file.

FMCooler was also tested succesfully on the cloud-based Google Colab, so users could upload it to the session and use a notebook to install the dependencies and launch the tool.

Windows users, that want to run it locally, will require to install extra software for a succesful installation, such as Microsoft C++ Build Tools (e.g., the qubovert dependency is not precompiled so its C++ parts will require to be compiled in your computer).


## Usage

A generic example of execution of `fmcooler` gets a feature model (e.g., `tree.uvl`) and a weights file (e.g., `weights.csv`) where we have the data about the impact of each feature for a concrete criteria (e.g., $\sum_i \text{weight}(\text{var}_i) \cdot \text{rate}_i$, defined by `vars:rates:min`, where the elements of `vars`, `rates` and `min` are separated by commas. The latter has `min` and `max` for each variable, making that when `max`, the corresponding weight is multiplied by -1), using `100` reads. A read, in the SA terminology, refers to one independent run of the annealing algorithm, starting from an initial state and proceeding through the annealing schedule to produce a single sample. The final result will be the best result among the independent reads. An example of multi-criteria execution can be seen below, for the minimisation of Battery with the rate of `0.4` and the maximisation of Usability with the rate of `0.6`.

```bash
./fmcooler.py tree.uvl weights.csv Battery,Usability:0.4,0.6:min,max 100
```

## Execution Examples

### Mono-criteria

An example of execution of `fmcooler` runs `1000` independent annealing-based optimization processes on the feature model specified in `examples/mobile_media.uvl`, using the impact data from `examples/mobile_media.csv`. The goal is to **minimize** the weighted influence of the `Battery` feature with a coefficient of `1.0`. Each run starts from a different initial state and follows an annealing schedule to explore possible configurations, producing samples that seek to reduce the total impact of the `Battery` feature as much as possible.

```bash
./fmcooler.py examples/mobile_media.uvl examples/mobile_media.csv Battery:1.0:min 1000
```

### Multi-criteria
The last example of `fmcooler` execution runs `10000` processes on the same feature model and using the same impact data. The goal is to **maximize** the combined weighted influence of `Battery` and `Usability` features, each weighted with a coefficient of `0.5`.

```bash
./fmcooler.py examples/mobile_media.uvl examples/mobile_media.csv Battery,Usability:0.5,0.5:max,max 10000
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests. If you encounter any bugs or have feature requests, please open an issue.

## License

This project is released under an open-source license. See the LICENSE file for more information.
