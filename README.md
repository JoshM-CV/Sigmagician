# Sigmagician

## Overview

Sigmagician is a Python utility for converting Sigma detection rules into hunting queries for various platforms including **KQL (Azure Sentinel / Microsoft 365 Defender)**, **SPL (Splunk)**, and **CarbonBlack**. It supports translating single rules or batch directories of Sigma rules, with options to merge queries into a structured hunting pack and export it as **Markdown** or **PDF**.

## Features

* Translate Sigma rules into **KQL**, **SPL**, or **CarbonBlack** queries.
* Supports **single file** or **batch directory** translation.
* Generates individual query files for each Sigma rule.
* Optionally merge all queries into a **hunting pack** with:

  * Table of Contents
  * Rule metadata (title, description, tags)
  * Properly formatted code blocks per backend
* Optionally export merged hunting pack as **PDF**.

## Requirements

* Python 3.8+
* [Sigma CLI](https://github.com/SigmaHQ/sigma) (`pip install sigma-cli`)
* Optional backend modules:

  * `pysigma-backend-splunk`
  * `pysigma-backend-kql`
  * `pysigma-backend-carbonblack`
* PyYAML (`pip install pyyaml`)
* PyPandoc (`pip install pypandoc`) for PDF export
* Pandoc installed on your system (for PDF export, see [Pandoc installation](https://pandoc.org/installing.html))

## Installation

1. Clone the repository or copy the `sigmagician.py` script.
2. Install required Python packages (On Windows use: py -m pip):

```bash
pip install sigma-cli pyyaml pypandoc
pip install pysigma-backend-splunk pysigma-backend-kql pysigma-backend-carbonblack
```

3. Ensure **Pandoc** is installed on your system for PDF export.

## Usage

Run the script using Python:

```bash
python sigmagician.py
```

### Step-by-step

1. Enter the path to a Sigma rule file or a directory containing multiple Sigma `.yml` or `.yaml` files.
2. Choose the backend for translation:

   * 1: KQL
   * 2: SPL
   * 3: CarbonBlack
3. Choose whether to merge all queries into a **hunting pack** (Markdown).
4. If merging is selected, you can optionally export the hunting pack as a **PDF**.
5. The output is saved in a directory named `sigma_translations_<backend>`.

### Example

```bash
Enter path to Sigma rule file or directory: ./sigma_rules
Select backend:
1. KQL (Azure Sentinel / Microsoft 365 Defender)
2. SPL (Splunk)
3. CarbonBlack
Enter choice (1-3): 2
Do you want to merge all translated queries into one hunting pack? (y/n): y
Do you want to export the hunting pack as PDF? (y/n): y
```

* Individual queries will be saved as `rule_splunk.txt`.
* The merged hunting pack will be saved as `hunting_pack_splunk.md` and `hunting_pack_splunk.pdf`.

## License

GNU V3.0

