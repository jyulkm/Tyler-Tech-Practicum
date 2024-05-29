# Auto-tagging System
# Company: Tyler Technology

Auto tagging system that generates tags for dataset based on name and description of dataset.

Members:
- Jiyul Kim
- Jeongyoon Lee
- Shreya Singh

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

## Reproducing Figures Using Trained Models
To reproduce figures from the paper, move to the `scripts/analysis` directory and run the following scripts:
- `1_plot_dataset.py` - Figure 1a
- `2_plot_metrics.py` - Figures 1c, 2a, and 2c
- `3_plot_trajs_fps.py` - Figures 1d, 2b, 2d, and 3a
- `4_plot_eigvals.py` - Figures 3b-e