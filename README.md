# Auto-tagging System - Tyler Technology

Auto tagging system that generates tags for dataset based on name and description of dataset.

## Introduction
This project is 

## System Architecture
![Project Screenshot](images/architecture.png)

## Codebase Structure
- `static` - Source code that defines core dataset generation, model architecture, training, and evaluation functionality
- `templates` - [`hydra`](https://hydra.cc/)-composable config files that define data, model, and training hyperparameters
- `datasets` - Synthetic HDF5 datasets generated using `paper_src.data.ChaoticDataModule`
- `runs` - Checkpoints, training logs, and hyperparameters for models used in paper figures (Note: some files, including Tensorboard logs, have been removed to conserve space)
- `scripts/analysis` - Scripts that generate paper figures using trained models
- `scipts/training` - Scripts that retrain single models or multiple models in parallel using [`ray.tune`](https://docs.ray.io/en/latest/tune/index.html)

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Generating Tags with different Methods
1. Generate tags with openAI
```bash
python3 main.py -method 'openai'
```
2. Generate tags with KeyBert
```bash
python3 main.py -method 'keybert'
```
3. Generate tags with Yake
```bash
python3 main.py -method 'yake'
```
4. Generate tags with TF-IDF
```bash
python3 main.py -method 'tfidf'
```


## Members:
- Jiyul Kim
- Jeongyoon Lee
- Shreya Singh