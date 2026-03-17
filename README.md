### MASTER THESIS - Ole Thomas Petrusson 2025/2026

<br>

# Creating bias benchmark dataset for Socioeconomic biases in Norwegian LLMs

This repository contains the code and files used to: 
 - Construct a Norwegian benchmark dataset for socioeconomic bias in Norwegian LLMs. 
 - Evaluate the benchmark on three Norwegian LLMs.

## Dataset

The dataset files and the full dataset construction pipeline can be found in the `dataset/` directory.

**See the dataset documentation here:** 🖥️

[`dataset/README.md`](dataset/README.md)

The dataset README describes:
- How the benchmark dataset is constructed
- The folder structure  
- The source statistics used (SSB)  
- The target group definitions  
- The translation pipeline  

## Models

The evaluation code, results, and visualizations for testing Norwegian LLMs on the benchmark dataset can be found in the `models/` directory.

**See the models documentation here:** 💬

[`models/README.md`](models/README.md)

The models README describes:
- The three Norwegian LLMs evaluated (NB-Alpaca, Normistral, NorWAI)
- Evaluation notebooks and inference pipelines
- Result structures and metrics
- Utility functions for evaluation and visualization
- How to run evaluations and generate bias analysis visualizations




## Repository Structure

```text
Master-Thesis-INFO390-UIB/
├── NOR_SES_dataset.csv          # Full socioeconomic bias benchmark dataset
├── requirements.txt              # Python dependencies
├── README.md                      # This file
│
├── dataset/
│   ├── ses_dataset_templates/
│   │   ├── questions.json
│   │   ├── immigration_templates/
│   │   │   └── target_template.json
│   │   └── regional_templates/
│   │       └── target_template.json
│   │
│   ├── translation/
│   │   ├── arzaghi_org_temp.ipynb
│   │   └── translate_from_en_to_no.ipynb
│   │
│   ├── create_dataset.ipynb
│   ├── explore_the_dataset.ipynb
│   ├── dataset_utils.py
│   └── README.md
│
└── models/
    ├── eval_nb/
    │   ├── nb_alpaca_eval.ipynb
    │   ├── normistral_eval.ipynb
    │   └── norwai_eval.ipynb
    │
    ├── results/
    │   ├── nb_alpaca/
    │   │   ├── base_results.json
    │   │   └── base_results_full.json
    │   ├── normistral/
    │   │   ├── base_results.json
    │   │   ├── inter_results.json
    │   │   └── inter_results_full.json
    │   └── norwai/
    │       ├── base_results.json
    │       └── base_results_full.json
    │
    ├── utils/
    │   ├── eval_utils.py
    │   ├── model_utils.py
    │   ├── saving_loading_utils.py
    │   ├── viz_utils.py
    │   └── regex_utils/
    │       ├── label_utils.py
    │       └── regex_variables_utils.py
    │
    ├── visualization_and_results_nb/
    │   ├── nb_alpaca_viz.ipynb
    │   ├── normistral_viz.ipynb
    │   └── norwai_viz.ipynb
    │
    └── README.md
```