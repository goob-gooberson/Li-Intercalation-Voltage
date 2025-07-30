# Li-Intercalation-Voltage
Python scripts and utilities for Li intercalation voltage estimation from DFT data from Materials Project Library

[Badges: optional – tests, license, Python version]

## Table of contents
- [Background theory](#background-theory)
- [Formulae](#formulae)
- [Implementation with PyMatGen](#implementation-with-pymatgen)
- [Install](#install)
- [Set up your Materials Project API key](#set-up-your-materials-project-api-key)
- [Quick start](#quick-start)
- [Examples](#examples)
- [Input data formats](#input-data-formats)
- [Assumptions & caveats](#assumptions--caveats)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Citation](#citation)

---

## Background theory

## Set up your Materials Project API key
This project accepts your API key in **any one** of these ways:
**Priority order used by the code:**  
1) `local_settings.py` (simple local file)  
2) Environment variable `MP_API_KEY` (includes Codespaces/GitHub Actions/OS/IDE)  
3) `.env` file (with `python-dotenv`)

 Do **only one** method. Never commit real keys to the repo.

 ---

### Option 1 — Local file (easiest, no terminal)

1. In the **same folder as the Python script**, create a file named **`local_settings.py`**.
2. Put your key inside:
   ```python
   MP_API_KEY = "paste_your_materials_project_key_here"
3. Do not commit this file. (Create through Codespaces if you're doing it on Website)

### Option 2 — Environment variable `MP_API_KEY`

#### A) GitHub Codespaces
1. Go to **Settings → Secrets and variables → Codespaces → New repository secret**.
2. Name the secret **`MP_API_KEY`** and paste your API key as the value.
3. Click **Add secret**.
4. Open a Codespace (**Code → Create codespace on main**) and run the script.  
   Your key will be available automatically.

---

#### B) GitHub Actions (CI)
1. Go to **Settings → Secrets and variables → Actions → New repository secret**.
2. Name it **`MP_API_KEY`** and paste your key.
3. In your workflow YAML, expose it like this:
   ```yaml
   env:
     MP_API_KEY: ${{ secrets.MP_API_KEY }}

---


