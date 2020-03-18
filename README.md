# RetroRules

* Docker image: [brsynth/retrorules-standalone](https://hub.docker.com/r/brsynth/retrorules-standalone)

Retrieve the reaction rules from retrorules.org

## Input

* **-rule_type**: (string) Valid options: retro, forward, all. Return the rules that are in reverse, forward or both direction
* **-diamters**: (integer list): Valid options: 2, 4, 6, 8, 10, 12, 14, 16. The diameter of the rules to return
* **-output_format**: (string) Valid options: tar, csv. Format output

## Ouput

* **-output**: (string): Path of the output file. Either a TAR (containing a CSV) or CSV list of reaction rules that are in a RetroPath2.0 friendly format 

## Dependencies

* Base docker image: [python:3.7](https://hub.docker.com/layers/python/library/python/3.7/images/sha256-af8fc40f758a1847b87db6c0239f2a5fb70622adc95a68bf1b736fa57ad332bc?context=explore)

## Building the docker

```
docker build -t brsynth/retrorules-standalone:dev .
```

### Running the test

To run the test, run the following command:

```
python run.py -rule_type retro -output rules.tar -diameters 2,8 -output_format tar
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Version

v0.1

## Authors

* **Thomas Duigou**
* Melchior du Lac

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Joan Hérisson

### How to cite RetroRules?
Please cite:

Duigou, Thomas, et al. "RetroRules: a database of reaction rules for engineering biology." Nucleic acids research 47.D1 (2019): D1229-D1235.
