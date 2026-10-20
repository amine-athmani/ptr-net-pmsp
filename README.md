# Pointer networks for parallel machine scheduling

An experiment from my 2019 research internship at the LIST3N lab (UTT): can a pointer network learn to sequence jobs for the unrelated parallel machine scheduling problem with setup times (makespan objective)?

A [pointer network](https://arxiv.org/abs/1506.03134) reads a set of items and outputs a permutation of them, which fits scheduling: the input is the list of jobs, the output is the order in which to dispatch them. The training labels are the best sequences found by metaheuristics on generated instances.

## Data

`data/data.ptr` holds one instance per line, up to 200 jobs. For each job, the input is its processing time on each of the 10 machines and its average setup times, padded to 60 features. After the `output` keyword comes the target job sequence. `data.py` builds this file from the instance files and from metaheuristic logs, keeping the sequence with the lowest makespan. `data/data_100.ptr` is a smaller set.

## Model

- `PointerLSTM.py`: a Keras pointer-network decoder layer (LSTM with attention over the encoder outputs).
- `train.py`: LSTM encoder (64 units) plus pointer decoder, trained with categorical cross-entropy over job positions. The first 1100 instances are used for training and the rest for validation.
- `model_weights.hdf5`: the trained model.

```bash
python train.py
```

The code targets the Keras 2.x API from 2019 (`keras.layers.recurrent`), so it needs an old Keras / TensorFlow 1.x environment to run as is.

## Status

Research prototype, not maintained. My later scheduling work is in [pyscheduling](https://github.com/scheduling-cc/pyscheduling) and in the GECCO 2022 and OLA 2023 papers.
