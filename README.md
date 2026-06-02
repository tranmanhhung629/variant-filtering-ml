# variant-filtering-ml
# ML-based Post-processing Filter for Genetic Variant Calling

## Project Title

**Research and Development of a Post-processing Genetic Variant Filter Based on Advanced Machine Learning Models**

## Author

**Tran Manh Hung**
Student ID: **20220068**
Program: **Vietnam-Japan Information Technology, IT-E6**
Supervisor: **Assoc. Prof. Dr. Le Duc Hau**

---

## Overview

This project investigates and develops a post-processing filter for genetic variant calling results using advanced machine learning models. The main goal is to improve the quality of called variants by reducing false positives while maintaining high recall for true variants.

The experiments are conducted on the **HG002 Illumina NovaSeq 250x** dataset and evaluated against the **GIAB benchmark** using **hap.py**. Several filtering approaches are compared, including traditional rule-based and statistical methods, as well as machine learning-based methods.

---

## Methods

The following filtering methods are evaluated:

* **Hard Filter**
* **VQSR** (Variant Quality Score Recalibration)
* **VEF** (Variant Ensemble Filter)
* **TabPFN**
* **Stacking model** combining VEF and TabPFN scores

For the fair comparison experiment, VEF and TabPFN are trained using the same training subset with a maximum of **10,000 variants**. The stacking model uses the prediction scores from VEF and TabPFN as inputs for a meta-learner.

---

## Dataset

The dataset used in this project is:

* Sample: **HG002**
* Sequencing platform: **Illumina NovaSeq**
* Coverage: **250x**
* Benchmark: **GIAB HG002 benchmark**
* Evaluation tool: **hap.py**

Due to the large size of genomic data files, raw sequencing files, reference genomes, and large VCF files are not included in this repository. Only scripts, notebooks, summary results, figures, and reports are provided.

---

## Evaluation Metrics

The methods are evaluated using the following metrics:

* **Recall**
* **Precision**
* **F1-score**
* **False Positives (FP)**
* **False Negatives (FN)**
* **True Positives (TP)**

Results are reported separately for:

* **SNP**
* **INDEL**

---

## Repository Structure

```text
variant-filtering-ml/
│
├── notebooks/
│   └── fair_comparison_vef_tabpfn_stack.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── models.py
│   ├── evaluate.py
│   ├── export_vcf.py
│   └── plot_results.py
│
├── results/
│   ├── snp/
│   │   ├── *.happy.summary.csv
│   │   └── metric tables
│   │
│   └── indel/
│       ├── *.happy.summary.csv
│       └── metric tables
│
├── figures/
│   ├── plot_f1_score_same_scale.png
│   ├── plot_recall_same_scale.png
│   ├── plot_precision_same_scale.png
│   ├── plot_false_positive.png
│   └── plot_false_negative.png
│
├── report/
│   ├── report.tex
│   └── presentation.pdf
│
├── requirements.txt
└── README.md
```

---

## Main Experimental Workflow

The experimental pipeline consists of the following steps:

1. Load candidate variants from VCF files.
2. Load TP/FP labels from hap.py annotated VCF files.
3. Extract variant-level features such as `QUAL`, `DP`, `MQ`, `FS`, `SOR`, and `QD`.
4. Preprocess missing values using a VEF-like strategy.
5. Train VEF and TabPFN under a fair comparison setting.
6. Train a stacking meta-model using prediction scores from VEF and TabPFN.
7. Export filtered VCF files with AI-based scores.
8. Evaluate the filtered VCF files using hap.py.
9. Summarize results by metric and visualize performance.

---

## Key Results

### SNP

For SNP variants, TabPFN achieved the highest F1-score, while the stacking model achieved the lowest number of false positives.

| Metric    | Best Method |
| --------- | ----------- |
| Recall    | TabPFN      |
| Precision | Stack       |
| F1-score  | TabPFN      |
| FP        | Stack       |
| FN        | TabPFN      |
| TP        | TabPFN      |

### INDEL

For INDEL variants, VQSR achieved the highest F1-score and the lowest number of false positives, while VEF achieved the lowest number of false negatives.

| Metric    | Best Method       |
| --------- | ----------------- |
| Recall    | Hard Filter / VEF |
| Precision | VQSR              |
| F1-score  | VQSR              |
| FP        | VQSR              |
| FN        | VEF               |
| TP        | VEF               |

---

## Notes on TabPFN

The experiments use the `tabpfn` Python package. In the Colab environment, the package version was checked as:

```python
import tabpfn
print(tabpfn.__version__)
```

The model checkpoint downloaded during execution was:

```text
tabpfn-v3-classifier-v3_default.ckpt
```

Therefore, the experiments use the TabPFN v3 classifier checkpoint through the installed `tabpfn` package.

---

## Installation

Install the required Python packages:

```bash
pip install numpy pandas scikit-learn scikit-allel xgboost tabpfn torch matplotlib
```

For Google Colab:

```python
!pip install -q scikit-allel tabpfn xgboost
```

TabPFN may require a one-time license acceptance and API key from Prior Labs before downloading the model checkpoint.

---

## Running the Notebook

The main notebook is located at:

```text
notebooks/fair_comparison_vef_tabpfn_stack.ipynb
```

Before running the notebook, update the dataset paths:

```python
BASE = "/content/drive/MyDrive/gr2"
```

Then run the notebook cells in order.

---

## hap.py Evaluation

Example command for evaluating a filtered SNP VCF file:

```bash
hap.py <truth.vcf> test.snp.TabPFN_fair.vcf \
  -f <benchmark.bed> \
  -r <reference.fa> \
  -o happy_snp_tabpfn_fair \
  --pass-only \
  --type SNP
```

Example command for evaluating a filtered INDEL VCF file:

```bash
hap.py <truth.vcf> test.indel.TabPFN_fair.vcf \
  -f <benchmark.bed> \
  -r <reference.fa> \
  -o happy_indel_tabpfn_fair \
  --pass-only \
  --type INDEL
```

---

## Limitations

This project currently focuses mainly on the HG002 sample. Further experiments on additional samples and sequencing platforms are needed to better evaluate the robustness and generalization of the proposed filtering methods.

The stacking model is also an initial experiment and can be further improved by testing different meta-learners, additional features, and more robust validation strategies.

---

## Future Work

Future work may include:

* Extending experiments to more GIAB samples.
* Testing other sequencing platforms and coverage levels.
* Improving stacking with stronger meta-learners such as XGBoost.
* Exploring hard-example sampling for TabPFN.
* Comparing additional machine learning models for variant filtering.
* Building a more automated end-to-end variant filtering pipeline.

