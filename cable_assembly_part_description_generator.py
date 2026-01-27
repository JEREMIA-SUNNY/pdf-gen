
import re

def singl_if_generate_part_description(data):
    part_str = ""
    if data["Part Type"] == "Connector":
        part_str = "Connector"
    

    if data["Part Type"] in ["Connector"]:
        
        # Cable Entry
        cable_entry_map = {
            "Solder Clamp Type": "",
            "Crimp Type": "Crimp Design",
            "Solder Type": "Direct Solder Design",
            "Clamp Type": "Clamp Design",
        }
        cable_entry = cable_entry_map.get(data["Cable Entry"])

        # Specialty logic
        specialty_map = {
            "Standard": part_str,
            "Minibend": f"Minibend {part_str}",
            "Anti-Torque Nut": f"{part_str} with Anti-Torque Nut",
            "Rotary Joint": f"{part_str} with Rotary Joint",
            "Wire Hole": f"{part_str} with Wire Hole",
            "Vent Hole": f"{part_str} with Vent Hole",
            "Field Replaceable": f"Field Replaceable {part_str}",
            "Viton": f"{part_str} with Viton Gasket",
            "Viton Vent Hole": f"{part_str} with Viton Gasket and Vent Hole",
            "Viton Vent Hole with Anti-Torque Nut": f"{part_str} with Viton Gasket, Vent Hole and Anti-torque Nut",
            "Round Contact": f"{part_str} with Round Contact",
            "Solder Cup Contact": f"{part_str} with Solder Cup Contact",
            "Tab Contact": f"{part_str} with Tab Contact",
        }
        specialty_str = specialty_map.get(data["Specialty"], part_str)


        # Mating & Locking Mechanism
        mlm_map = {
            "Standard": "",
            "Snap-On": "Snap-On",
            "Limited Detent": "Limited Detent",
            "Full Detent": "Full Detent",
            "Smooth Bore": "Smooth Bore",
            "Floating": "Floating",
            "2-D Flats": "2-D Flats"
        }
        mlm_str = mlm_map.get(data.get("Mating & Locking Mechanism", ""), "")

        # Suffix
        suffix_str = ""
        if data["Suffix"] == "Ingress Protection IP67":
            suffix_str = "IP67 Mated,"
        elif data["Suffix"] == "Expansion Protection":
            suffix_str = "with Expansion Protection,"
        elif data["Suffix"] == "External Clamp Nut":
            suffix_str = "with External Clamp Nut,"
        elif data["Suffix"] == "No Clamp Nut":
            suffix_str = "without Clamp Nut,"
        elif data["Suffix"] == "Hermetic":
            specialty_str = f"Hermetic {specialty_str}"
        elif data["Suffix"] == "Catchers Mitt":
            specialty_str = f"Catchers Mitt {specialty_str}"
        elif data["Suffix"] == "Tape and Reel":
            specialty_str = f"Tape and Reel {specialty_str}"

        # Final Description
        init_str = (
            f"{data['Connector Series']} {data['Gender']} {data['Style']} {cable_entry}"
            f"{mlm_str} {specialty_str} {suffix_str} "
        ).replace("  ", " ").strip(", ")

        return init_str

    return part_str


def generate_assembly_pn_length(data):
    pn = data["Cable Assembly Part Number"]
    length_val = int(data["Assembly Length"])

    if length_val > 1000:
        length_str = f"{length_val/1000} m"
    else:
        length_str = f"{length_val} mm"

    return f"{pn}, {length_str}"


def generate_assembly_type(data):
    cable_type = data["Cable Type"]
    nk_part = data["NKRF Part Number"]
    outer_jacket = data.get("Outer Jacket")

    if outer_jacket and outer_jacket != "None":
        # Remove bracketed text and add "jacket"
        material = re.sub(r"\s*\(.*?\)", "", outer_jacket).strip()
        material_str = f"{material} jacket"
    else:
        # Extract bracket text from braid and add "braid"
        braid = data.get("Braid", "")
        match = re.search(r"\((.*?)\)", braid)
        braid_material = match.group(1) if match else braid
        material_str = f"{braid_material}"

    return f"{cable_type} RF Cable Assembly with NKRF_{nk_part} cable, {material_str}"


def generate_phase_matched_string(data):
    if data["Phase Match Required"].lower() == "no":
        return "Non-Phase Matched"
    else:
        return (
            f"Phase Matched, DC to {data['Phase Match Frequency']} "
            f"with {data['Phase Match Tolerance']} tolerance "
            f"in a set of {data['Phase Matched Cables per Set']} cables"
        )


# ▶️ Sample input data
sample_data_end_a = {
    "Part Type": "Connector",
    "Connector Series": "N-Type",
    "Gender": "Female (Jack)",
    "Style": "4 Hole Rectangular Panel",
    "Cable Entry": "Solder Type",
    "Cable Group": "2801",
    "Specialty": "Minibend",
    "Mating & Locking Mechanism": "Snap-On",
    "Suffix": "Standard"
}

sample_data_end_b = {
    "Part Type": "Connector",
    "Connector Series": "N-Type",
    "Gender": "Female (Jack)",
    "Style": "4 Hole Rectangular Panel",
    "Cable Entry": "Solder Type",
    "Cable Group": "2801",
    "Specialty": "Minibend",
    "Mating & Locking Mechanism": "Snap-On",
    "Suffix": "Standard"
}

sample_data_cable = {
    "Part Type": "Cable",
    "NKRF Part Number": "T141",
    "Manufacturer": "Insulated Wire",
    "Cable Type": "Low Loss",
    "Outer Jacket": "None",
    "Braid": "TPC (Tin Plated Copper Braid)"
}

sample_data_assembly = {
    "Cable Assembly Part Number": "NPS-T141-1000-NPS",
    "Assembly Length": "500",
    "Phase Match Required": "Yes",
    "Phase Match Tolerance": "+/- 2 degrees",
    "Phase Match Frequency": "18",
    "Phase Matched Cables per Set": "10",
}



# --- Step 1: Connector Descriptions ---
end_a_description = singl_if_generate_part_description(sample_data_end_a)
end_b_description = singl_if_generate_part_description(sample_data_end_b)

# --- Step 2: Assembly PN + Length ---
assembly_pn_length = generate_assembly_pn_length(sample_data_assembly)

# --- Step 3: Assembly Type ---
assembly_type = generate_assembly_type(sample_data_cable)

# --- Step 4: Phase Matched String ---
phase_matched_string = generate_phase_matched_string(sample_data_assembly)

# --- Step 5: Final String ---
final_string = (
    f"{assembly_pn_length}, {assembly_type}. "
    f"{end_a_description} on End A and {end_b_description} on End B. "
    f"{phase_matched_string}"
)

print("Final String:\n", final_string)