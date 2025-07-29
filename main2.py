from pymatgen.ext.matproj import MPRester
from pymatgen.core import Composition
import os

API_KEY = os.getenv("MP_API_KEY")


def get_lowest_entry_for_formula(mpr, formula):
    """Get the lowest energy entry for a given formula."""
    entries = mpr.get_entries(formula)
    if not entries:
        print(f"No entries found for: {formula}")
        return None
    return min(entries, key=lambda e: e.energy_per_atom)


def get_energy_per_fu(entry):
    """Energy per formula unit = energy/atom × atoms per reduced formula unit"""
    return entry.energy_per_atom * entry.composition.reduced_composition.num_atoms


def calculate_voltage(cathode_formula, anode_formula):
    li_cathode_formula = "Li" + cathode_formula

    with MPRester(API_KEY) as mpr:
        # Look up all entries
        cathode_entry = get_lowest_entry_for_formula(mpr, cathode_formula)
        li_cathode_entry = get_lowest_entry_for_formula(mpr, li_cathode_formula)
        anode_entry = get_lowest_entry_for_formula(mpr, anode_formula)

        if not all([cathode_entry, li_cathode_entry, anode_entry]):
            print("Could not retrieve one or more required entries.")
            return None

        # Determine if anode is lithiated (like LiC6, LiSi)
        anode_comp = Composition(anode_formula)
        if "Li" in anode_comp and len(anode_comp) > 1:
            # Remove Li to get delithiated anode
            delith_dict = anode_comp.as_dict()
            delith_dict["Li"] -= delith_dict["Li"]  # remove all Li
            if delith_dict["Li"] <= 0:
                del delith_dict["Li"]
            if not delith_dict:
                print("Delithiated anode would be empty. Invalid setup.")
                return None
            delith_formula = "".join(f"{el}{int(amt) if amt != 1 else ''}" for el, amt in delith_dict.items())
            delith_anode_comp = Composition(delith_formula)
            num_atoms = delith_anode_comp.num_atoms
            delith_entry = get_lowest_entry_for_formula(mpr, delith_formula)
            if not delith_entry:
                print(f"Could not find delithiated anode: {delith_formula}")
                return None

            energy_delith_anode = (get_energy_per_fu(delith_entry)) * num_atoms
            # Reaction: MX2 + LiX → LiMX2 + X
            E_reactants = get_energy_per_fu(cathode_entry) + get_energy_per_fu(anode_entry)
            E_products = get_energy_per_fu(li_cathode_entry) + energy_delith_anode
            reaction = f"{cathode_formula} + {anode_formula} → {li_cathode_formula} + {delith_formula}"

        else:
            # Simple lithium metal reaction: MX2 + Li → LiMX2
            E_reactants = get_energy_per_fu(cathode_entry) + get_energy_per_fu(anode_entry)
            E_products = get_energy_per_fu(li_cathode_entry)
            reaction = f"{cathode_formula} + {anode_formula} → {li_cathode_formula}"

        voltage = -(E_products - E_reactants)

        print(f"\nReaction: {reaction}")
        print(f"Estimated Voltage: {voltage:.3f} V")
        return voltage


if __name__ == "__main__":
    cathode = input("Enter cathode formula: ").strip()
    anode = input("Enter anode formula: ").strip()
    calculate_voltage(cathode, anode)
