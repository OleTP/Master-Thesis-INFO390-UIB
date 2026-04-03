# Models Folder


This folder contains all files to evaluate three Norwegian LLMs on the socioeconomic bias benchmark dataset. It includes evaluation notebooks, utility functions, results, and comprehensive visualizations for analyzing model performance and bias patterns.

The three models evaluated are:
- **nb-gpt-j-6B-alpaca (NB-Alpaca)** [Link to the model](https://huggingface.co/NbAiLab/nb-gpt-j-6B-alpaca)
- **Normistral-7b-warm-instruct (Normistral)** [Link to the model](https://huggingface.co/norallm/normistral-7b-warm-instruct)
- **NorwAI-Mistral-7B-instruct (NorwAI)** [Link to the model](https://huggingface.co/NorwAI/NorwAI-Mistral-7B-instruct)

## Folder Structure

### `/eval_nb`
Contains Jupyter notebooks for evaluating different models:
- `nb_alpaca_eval.ipynb` - Evaluation notebook for NB-Alpaca model
- `normistral_eval.ipynb` - Evaluation notebook for Normistral model
- `norwai_eval.ipynb` - Evaluation notebook for NorwAI model

### `/results`
Stores evaluation results for each model in JSON format:
- `nb_alpaca/` - Results from NB-Alpaca model evaluation
- `normistral/` - Results from Normistral model evaluation
- `norwai/` - Results from NorwAI model evaluation

Each model folder contains:
- `base_results.json` - Core evaluation metrics
- `base_results_full.json` - Comprehensive evaluation results with model output.
- `inter_results.json` / `inter_results_full.json` - Intersectional answers

### `/utils`
Contains utility functions for model evaluation and data handling:
- `eval_utils.py` - Evaluation metrics and scoring functions
- `model_utils.py` - Model loading and inference utilities
- `saving_loading_utils.py` - Functions for saving and loading models/results
- `viz_utils.py` - Visualization and plotting utilities
- `regex_utils/` - Regex-based utilities for label processing
  - `label_utils.py` - Label extraction and processing
  - `regex_variables_utils.py` - Regex pattern definitions

### `/visualization_and_results_nb`
Contains Jupyter notebooks for visualizing results and generating figures:
- `nb_alpaca_viz.ipynb` - Visualization notebook for NB-Alpaca results
- `normistral_viz.ipynb` - Visualization notebook for Normistral results
- `norwai_viz.ipynb` - Visualization notebook for NorwAI results

## Usage

1. Run evaluation notebooks in `/eval_nb` to test models on the dataset
2. Results are automatically saved to `/results`
3. Use notebooks in `/visualization_and_results_nb` to analyze and visualize results
4. Import utilities from `/utils` for common evaluation and processing tasks