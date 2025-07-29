from pymatgen.ext.matproj import MPRester
from pymatgen.analysis.structure_analyzer import SpacegroupAnalyzer

API_KEY = "omskIUGlqsV2cSTZxrB5jSG2p76VYM4e"


def get_lowest_entry_for_formula(mpr, formula, space_group=None):
    entries = mpr.get_entries(formula)
    if space_group:
        entries = [e for e in entries if e.structure.get_space_group_info()[1] == space_group]
    if not entries:
        return None
    return min(entries, key=lambda e: e.energy_per_atom)


def get_energy_per_fu(entry):
    """Calculate total energy per formula unit."""
    atoms_per_fu = entry.composition.reduced_composition.num_atoms
    return entry.energy_per_atom * atoms_per_fu


def get_total_energy_per_fu(mpid):
    with MPRester(API_KEY) as mpr:
        entry = mpr.get_entry_by_material_id(mpid)
        if entry is None:
            print(f"No entry found for {mpid}")
            return None

        total_energy = entry.energy
        n_formula_units = entry.composition.get_reduced_composition_and_factor()[1]
        energy_per_fu = total_energy / n_formula_units

        return energy_per_fu


def get_entries(metal, anion, x_target, tolerance):

    with MPRester(API_KEY) as mpr:
        matched = []
        entries = mpr.get_entries_in_chemsys(["Li", metal, anion])
        for entry in entries:
            comp = entry.composition
            el_amt = comp.get_el_amt_dict()

            # Ensure all three elements are present
            if not all(el in el_amt for el in ["Li", metal, anion]):
                continue  # Skip entries missing any of them

            li = el_amt.get("Li", 0)
            mn = el_amt.get(metal, 0)
            o = el_amt.get(anion, 0)

            li_mn_ratio = li / mn
            o_mn_ratio = o / mn

            if abs(li_mn_ratio - x_target) <= tolerance and abs(o_mn_ratio - 2.0) <= 0.1:
                matched.append({

                    "mpid": entry.entry_id,

                })
    return matched


def calculate_voltage_for_metal_anion(metal, anion, x2, x1):
    """Calculate the Li insertion voltage for Li_x2 M X2 -> Li_x1 M X2 across a selected metal and anion."""
    li_x2_formula = f"Li{x2}{metal}{anion}2"
    li_x1_formula = f"Li{x1}{metal}{anion}2"
    if x2 == 1:
        li_x2_formula = f"Li{metal}{anion}2"
    if x1 == 0:
        li_x1_formula = f"{metal}{anion}2"

    with MPRester(API_KEY) as mpr:

        if x2 == 1:
            entry_x22 = get_lowest_entry_for_formula(mpr, li_x2_formula)
            entry_x2 = get_energy_per_fu(entry_x22)

        else:
            results2 = get_entries(metal, anion, x2, tolerance=0.001)
            print(results2)
            energies = []
            for r in results2:
                mpid_clean = r["mpid"].split("-")[0] + "-" + r["mpid"].split("-")[1]
                structure = mpr.get_structure_by_material_id(mpid_clean)
                composition = structure.composition
                reduced_comp, factor = composition.get_reduced_composition_and_factor()
                li_per_fu = reduced_comp["Li"]

                e = get_total_energy_per_fu(mpid_clean) * x2 / li_per_fu
                energies.append(e)

            entry_x2 = max(energies)
            print(energies)

        if x1 == 0:
            entry_x11 = get_lowest_entry_for_formula(mpr, li_x1_formula)
            entry_x1 = get_energy_per_fu(entry_x11)
        else:

            results1 = get_entries(metal, anion, x1, tolerance=0.001)
            energies1 = []
            for r in results1:
                mpid_clean = r["mpid"].split("-")[0] + "-" + r["mpid"].split("-")[1]
                structure = mpr.get_structure_by_material_id(mpid_clean)
                composition = structure.composition
                reduced_comp, factor = composition.get_reduced_composition_and_factor()
                li_per_fu = reduced_comp["Li"]

                e = get_total_energy_per_fu(mpid_clean) * x1 / li_per_fu
                energies1.append(e)

            entry_x1 = max(energies1)

        if not entry_x2:
            print(f"No entry found for {li_x2_formula}.")
            return None
        if not entry_x1:
            print(f"No entry found for {li_x1_formula}.")
            return None

        li_bulk_entry = mpr.get_entry_by_material_id("mp-1018134")  # Bulk Li
        li_bulk_energy = li_bulk_entry.energy_per_atom

        e_x2 = entry_x2
        e_x1 = entry_x1
        print(e_x2)
        print(e_x1)

        delta_x = x2 - x1
        voltage = - (e_x2 - e_x1 - delta_x * li_bulk_energy) / delta_x
        print((x2-x1) * li_bulk_energy)
        print(f"{li_x1_formula} + {(x2-x1)}Li -> {li_x2_formula}")
        print(f"Estimated Voltage: {voltage:.3f} V")
        return voltage


if __name__ == "__main__":
    metal = input("Enter the metal symbol (e.g., Co, Ni, Mn): ").strip()
    anion = input("Enter the anion symbol (e.g., O, S, Se): ").strip()
    x2 = float(input("Enter the starting Li content (x2): ").strip())
    x1 = float(input("Enter the final Li content (x1): ").strip())

    calculate_voltage_for_metal_anion(metal, anion, x2, x1)
