# Li-Intercalation-Voltage
Python scripts and utilities for Li intercalation voltage estimation from DFT data from Materials Project Library

[Badges: optional – tests, license, Python version]

## Table of contents
- [Background theory](#background-theory)
- [Formulae](#formulae)
- [Implementation with PyMatGen](#implementation-with-pymatgen)
- [Installation](#installation)
- [Set up your Materials Project API key](#set-up-your-materials-project-api-key)
- [Examples](#examples)
- [Assumptions & caveats](#assumptions--caveats)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Citation](#citation)

---

## Background Theory

Lithium intercalation compounds, especially lithium-metal oxides and dichalcogenides, are key materials for rechargeable lithium-ion batteries. These compounds allow **reversible insertion and removal of Li⁺ ions** without significant structural changes, a process called **topotactic intercalation**.

- **Electrochemical Cell:**  
  A lithium-ion cell consists of a **cathode** and **anode** separated by an electrolyte that allows Li⁺ transport. The open-circuit voltage (OCV) of the cell is determined by the difference in **Li chemical potential** between the electrodes:

V = (μ_Li^cathode - μ_Li^anode) / zF

where:
- μ_Li = chemical potential of lithium  
- z = number of electrons transferred (z = 1 for Li)  
- F = Faraday constant  

- **Intercalation Voltage:**  
The average voltage for lithium insertion/removal is directly related to the change in **Gibbs free energy**:

V = -ΔG / (nF)

In ab initio studies, ΔG is approximated by the total energy difference (ΔE) between the **lithiated** and **delithiated** phases:

V ≈ - (E_LiMO2 - E_MO2 - E_Li) / nF

This requires three total energies:
1. **LiMO2:** Lithiated cathode
2. **MO2:** Delithiated cathode (Li removed)
3. **Li:** Metallic lithium (reference)

### **Role of Anion Chemistry**

The intercalation voltage depends strongly on the **anion (X)**:

- Oxides (O²⁻) → Highest voltages (~3.7–4.2 V)
- Sulfides (S²⁻) → Moderate voltages (~2.0 V)
- Selenides (Se²⁻) → Lower voltages (~1.5 V)

**Reason:** A significant fraction of the electron from Li⁺ is transferred to the anion. Oxygen, being more electronegative, stabilizes the additional charge better, resulting in a higher voltage.

- **Structural Effects:**  
While the metal chemistry and anion type largely determine the voltage, the **crystal structure** can influence ionic relaxation and band structure changes upon intercalation.

### **Electronic Effects & Charge Transfer**

- Li is fully ionized (Li⁺) upon intercalation.
- Its electron is donated to:
  - **Transition metal cations:** Reducing their oxidation state (e.g., Co³⁺ → Co²⁺)
  - **Anion framework:** Oxygen gains partial negative charge  

This charge transfer modifies the **band structure**:
- Antibonding **eg\*** (metal d) bands shift downward
- Bonding **eg_b** (oxygen p) bands shift upward
- **t₂g bands** (nonbonding d) remain largely unaffected  

As we go across the periodic table (Ti → Zn):
- Metal d bands lower in energy  
- M–O bond length decreases (until Co), increasing voltage 

### **Trends and Key Findings**

- **Anion effect is dominant:** Oxides > sulfides > selenides in voltage  
- **Late transition metals (Co, Ni, Zn, Al)** give higher voltages  
- Fully optimized geometries are essential: ignoring relaxation leads to significant errors  
- Intercalation voltage trends can be predicted accurately using ab initio pseudopotential methods

### **Upper Voltage Limit**

- Oxygen-centered charge transfer leads to the highest voltages.
- Predicted maximum intercalation voltage for **LiAlO₂:** ~4.7 V  
- Hypothetical pure O₂-based solid could reach **~5.3 V**, but is not practically feasible.


### **Key Insight:**  

Ab initio pseudopotential methods, combined with thermodynamics, enable prediction of average intercalation voltages **without experimental data**, allowing screening of new electrode materials for improved energy density.

---

## Formulae

1. General thermodynamic formula
The open‑circuit voltage **V** is related to the Gibbs free energy change **ΔG**:
- V = - ΔG / (nF)

- **ΔG** = change in Gibbs free energy of the reaction (J/mol)  
- **n** = number of electrons (or Li⁺) transferred  
- **F** = Faraday constant = 96,485 C/mol  

---

### Approximation using DFT energies

In DFT-based approaches:

ΔG ≈ ΔE = E_products - E_reactants

So, V ≈ - ΔE / (nF)

If **ΔE** is in **eV per Li atom**, the Faraday constant cancels out:

V (V) ≈ - ΔE (eV)

V = - [ E(Li–Cathode) - E(Cathode) - E(Li) ]

For lithium intercalation between MO₂ and LiMO₂:

V ≈ - (E_LiMO2 - E_MO2 - E_Li) / F

where:
1. **E_LiMO2:** Total energy of the lithiated compound  
2. **E_MO2:** Total energy of the delithiated compound  
3. **E_Li:** Total energy per atom of metallic Li (reference)

---

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

---

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

#### C) IDE Setup
1. Set `MP_API_KEY` inside your IDE so the script picks it up automatically.
2. For example, in PyCharm,
3. Go to Run → Edit Configurations…
4. Select your script (or add one).
5. Under Environment variables, add: `MP_API_KEY=your_api_key_here`
6. Click OK and run the script.

---

### Option 3 — `.env` file (with `python-dotenv`)

You can keep your Materials Project API key in a `.env` file. The project will read it automatically.

1. **Copy the template**
   - Find the file named `.env.example` in the project.
   - Make a copy and rename it to **`.env`** (just `.env`, no extra name).
2. **Add your API key**
   - Open the new `.env` file.
   - Replace `your_api_key_here` with your real Materials Project API key:
     ```
     MP_API_KEY=your_real_api_key
     ```
3. **Run the script**
   - You don’t need to edit the code. When you run the script, it will automatically load the key from the `.env` file.

### Keep it private

- **Do not commit your `.env` file** to the repository.  
- It’s already listed in `.gitignore` so you can safely keep it local.

---

## Implementation with PyMatGen

This script estimates an average intercalation voltage for a simple “cathode ↔ anode” reaction using formation energies from the [Materials Project] via pymatgen.

What the script does:
1. Loads your Materials Project API key robustly (local file → env var → .env), then creates an MPRester client.
2. Fetches energies for three compositions:
- the cathode host (e.g., FePO4)
- the lithiated cathode (e.g., LiFePO4)
- the anode (e.g., Li or a lithiated anode like LiC6)
3. Forms a notional reaction and computes Voltage through the formula.
4. Prints the reaction and the estimated voltage.

---

Core functions

1. `get_lowest_entry_for_formula(mpr, formula)`
- Queries Materials Project for all entries matching a chemical formula and returns the one with lowest energy per atom (a simple proxy for stability).
2. `get_energy_per_fu(entry)`
- Converts entry.energy_per_atom (eV/atom) to eV per reduced formula unit (FU) by multiplying by entry.composition.reduced_composition.num_atoms.
3. `calculate_voltage(cathode_formula, anode_formula)`
- Builds the lithiated cathode formula as "Li" + cathode_formula.
- Fetches lowest-energy entries for: cathode, lithiated cathode, and anode.
- Computes the Voltage
- Reports the reaction string and estimated voltage

---


## Installation

Follow these steps to set up the project and install dependencies.

---

### 1) Clone the repository
```bash
git clone https://github.com/<goob-gooberson>/<Li-Intercalation-Volatge>.git
cd <Li-Intercalation-Volatge>
```

### 2) Install Dependencies

Key packages:
- pymatgen – for Materials Project API access and structure handling
- python-dotenv – to support loading .env files automatically (optional)

### 3) Set your Materials Project API Key

You must provide your MP API key before running. See [Set up your Materials Project API key](#set-up-your-materials-project-api-key):

### 4) Run the script

---

## Examples

### 1) Lithium metal anode
- Interactive run:
- Enter cathode formula: FePO4
- Enter anode formula: Li
---
- Reaction: FePO4 + Li → LiFePO4
- Estimated Voltage: 3.420 V

### 2) Graphite anode (lithiated anode → delithiated product)
- Enter cathode formula: FePO4
- Enter anode formula: LiC6
---
- Reaction: FePO4 + LiC6 → LiFePO4 + C6
- Estimated Voltage: 3.410 V

### 3) Silicon anode (lithiated → delithiated)
- Enter cathode formula: TiS2
- Enter anode formula: LiSi
---
- Reaction: TiS2 + LiSi → LiTiS2 + Si
- Estimated Voltage: 2.220 V

### 4) Another cathode example
- Enter cathode formula: CoO2
- Enter anode formula: Li
---
- Reaction: CoO2 + Li → LiCoO2
- Estimated Voltage: 3.900 V

---

Examples (multi‑composition voltage, `calculate_voltage_for_metal_anion`)

The script prompts you for:
- **metal** (e.g., `Co`, `Ni`, `Mn`)
- **anion** (e.g., `O`, `S`, `Se`)
- **x2** = higher Li content (final composition on the right)
- **x1** = lower Li content (initial composition on the left)

It evaluates the reaction:
Li_x1 M X2 + (x2 − x1) Li → Li_x2 M X2

### 1) Classic layered oxide (Co/O): from `x1 = 0` to `x2 = 1`
- Enter the metal symbol (e.g., Co, Ni, Mn): Co
- Enter the anion symbol (e.g., O, S, Se): O
- Enter the starting Li content (x2): 1
- Enter the final Li content (x1): 0
---
- CoO2 + 1.0Li -> LiCoO2
- Estimated Voltage: 3.900 V

### 2) Half‑lithiated step (Co/O): from `x1 = 0` to `x2 = 0.5`
- Enter the metal symbol (e.g., Co, Ni, Mn): Co
- Enter the anion symbol (e.g., O, S, Se): O
- Enter the starting Li content (x2): 0.5
- Enter the final Li content (x1): 0
---
- CoO2 + 0.5Li -> Li0.5CoO2
- Estimated Voltage: 3.650 V

### 3) Nickel oxide (Ni/O): from `x1 = 0.5` to `x2 = 1.0
- Enter the metal symbol (e.g., Co, Ni, Mn): Ni
- Enter the anion symbol (e.g., O, S, Se): O
- Enter the starting Li content (x2): 1
- Enter the final Li content (x1): 0.5
---
- Li0.5NiO2 + 0.5Li -> LiNiO2
- Estimated Voltage: 3.700 V

### 4) Sulfide example (Mn/S): from `x1 = 0` to `x2 = 1`
- Enter the metal symbol (e.g., Co, Ni, Mn): Mn
- Enter the anion symbol (e.g., O, S, Se): S
- Enter the starting Li content (x2): 1
- Enter the final Li content (x1): 0
---
- MnS2 + 1.0Li -> LiMnS2
- Estimated Voltage: 2.400 V

---

### Notes

- The code uses Materials Project entries within the chemical system `{Li, M, X}` and a tolerance
  around your target `x` to estimate energies when exact `Li{x}MX2` formulas are not directly available.
- Bulk Li reference is taken from Materials Project ID `mp-1018134`.
- If any required entry is missing, the script will print a message and skip the calculation.

---

## Assumptions & caveats

The intercalation voltage calculations and ab initio predictions are subject to several key assumptions and limitations:

---

### **1. Thermodynamic Assumptions**

- **ΔG ≈ ΔE:**  
  Gibbs free energy change is approximated by the total internal energy difference from DFT:

Entropy (**TΔS**) and pressure-volume (**PΔV**) contributions are neglected.  
- Valid at **0 K** and can introduce small errors (~0.1–0.2 V) at room temperature.

- **Average voltage only:**  
Voltage is calculated for the **end-member compositions** (x = 0 and x = 1) and reported as an **average voltage**.  
- Does not capture intermediate phase transitions or the full V(x) curve.

---

### **2. Structural Assumptions**

- **Topotactic Li removal:**  
It is assumed that removing Li from **LiMO₂** does not drastically change the host structure (MO₂).  
- In reality, some materials undergo cation migration or structural collapse (e.g., LiNiO₂).

- **Fully relaxed vs unrelaxed:**  
The reported voltages are typically for **fully relaxed structures**.  
- Neglecting relaxation can lead to differences of up to **0.5 V** (see hR4 vs tI16 structure in Table V).

- **No configurational disorder:**  
Disordered Li/vacancy arrangements are ignored; only fully lithiated and fully delithiated phases are considered.

---

### **3. Electronic & Chemical Assumptions**

- **Full ionization of Li:**  
Li is assumed to be completely ionized to Li⁺, donating its electron to the host lattice.

- **Electron transfer distribution:**  
Electron donation is considered to occur to both the transition metal and anion framework.  
- Exact partitioning may vary with chemistry and is not directly measured.

- **No rigid-band approximation:**  
Nonrigid-band effects (changes in band structure upon intercalation) are important and included, but DFT may not capture all subtleties.

---

### **4. Reference and Methodological Limitations**

- **Reference to metallic Li:**  
The anode reference is **Li metal**, which simplifies voltage predictions.  
- Practical anodes (e.g., LiC₆) would shift the absolute voltage slightly.

- **DFT functional limitations:**  
- Local Density Approximation (LDA) and Generalized Gradient Approximation (GGA) tend to **overbind metallic Li**, leading to underprediction of voltage by ~0.2 V.  
- Correlation effects in transition metal d-electrons are not fully captured without advanced corrections (e.g., +U or hybrid functionals).

- **Phase metastability:**  
Calculations may consider hypothetical or metastable structures that have not been synthesized.

---

### **5. Scope and Predictive Use**

- **Screening tool, not exact voltages:**  
While trends are robust, absolute voltages can deviate from experiments by ~0.2–0.3 V.  

- **Other properties not considered:**  
- Li diffusion kinetics, electronic conductivity, and stability at high voltage are **not addressed**.  
- High predicted voltage does not guarantee practical battery performance.

---

## Troubleshooting

1. “No entries found for …”
- Check the formula spelling and capitalisation (LiFePO4, not lifePO4). Try a simpler or reduced formula.
2. API errors
- Ensure MP_API_KEY is valid and your network allows HTTPS.
3. Unexpected voltages
- The script only considers the lowest energy formations, which may not be the ones participating in the reactions.
- Sometimes there are multiple or old entries in the MP library.

--- 

## License

MIT License

Copyright (c) [2025] [VIPUL]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Citation

If you use this code in your research, please cite:

## This repository

> **[VIPUL]**, *Voltage Calculation Tools using Materials Project API (PyMatGen)*,  
> GitHub repository: [https://github.com/<goob-gooberson>/<Li-Intercalation_Voltage>](https://github.com/goob-gooberson/Li-Intercalation-Voltage)  

This project builds on the pymatgen library. Please also cite:

Ong, S. P. et al., Python Materials Genomics (pymatgen): A robust, open-source python library for materials analysis,
Computational Materials Science, 68, 314–319 (2013). https://doi.org/10.1016/j.commatsci.2012.10.028

---
