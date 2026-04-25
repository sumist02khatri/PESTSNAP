import re


DEFAULT_INFO = {
    "problem": "This pest can reduce rice vigor, damage leaves or stems, and lower yield when infestation is not managed early.",
    "cure": "Confirm the infestation in the field and apply a locally approved pesticide based on agricultural guidance for the detected pest.",
    "prevention": "Monitor the crop regularly, keep the field clean, avoid excessive nitrogen, and follow integrated pest management practices.",
}


def normalize_pest_name(name):
    return re.sub(r"\s+", " ", (name or "").strip().lower())


pest_info = {
    "rice leaf roller": {
        "problem": "Larvae roll and feed on leaves, reducing the green area needed for photosynthesis and weakening plant growth.",
        "cure": "Spray a recommended insecticide such as chlorantraniliprole or emamectin benzoate according to local advisory guidance.",
        "prevention": "Use light traps, remove weed hosts, monitor early leaf damage, and avoid delayed intervention during peak larval activity.",
    },
    "rice leaf caterpillar": {
        "problem": "Leaf-feeding caterpillars scrape and consume foliage, causing defoliation and reduced crop vigor.",
        "cure": "Use a suitable caterpillar control product such as emamectin benzoate or spinosad as advised locally.",
        "prevention": "Scout fields regularly, conserve natural enemies, and manage alternate host weeds near the field.",
    },
    "paddy stem maggot": {
        "problem": "Maggots damage central shoots and can cause dead hearts in young rice plants, reducing tiller survival.",
        "cure": "Apply a recommended systemic insecticide if infestation crosses local threshold levels.",
        "prevention": "Use healthy seedlings, maintain field sanitation, and monitor crop stages that are most vulnerable to stem damage.",
    },
    "asiatic rice borer": {
        "problem": "Stem borers tunnel inside stems, causing dead hearts and white ears that directly reduce grain formation.",
        "cure": "Use stem-borer-targeted granules or sprays approved in your area, especially during early infestation.",
        "prevention": "Destroy crop residues, synchronize planting, use pheromone traps, and avoid leaving stubble that shelters larvae.",
    },
    "yellow rice borer": {
        "problem": "This borer attacks stems and panicles, leading to dead hearts during vegetative stage and white heads later.",
        "cure": "Apply a locally recommended borer management insecticide when early stem damage is observed.",
        "prevention": "Clip seedling tips before transplanting, maintain field hygiene, and monitor moth activity with traps.",
    },
    "rice gall midge": {
        "problem": "The pest forms silver shoots or onion leaf symptoms by damaging the growing point, reducing productive tillers.",
        "cure": "Use a recommended systemic insecticide or granule treatment when infestation appears in the field.",
        "prevention": "Use resistant varieties where available, remove volunteer plants, and avoid staggered planting in nearby fields.",
    },
    "rice stemfly": {
        "problem": "Stemfly larvae mine leaves and affect tillers, leading to weak plants and yield reduction under heavy infestation.",
        "cure": "Use a recommended insecticide after field confirmation and local threshold assessment.",
        "prevention": "Maintain weed-free bunds, monitor leaf symptoms early, and encourage balanced fertilizer use.",
    },
    "brown plant hopper": {
        "problem": "Brown plant hopper sucks sap from rice plants and can cause hopper burn, wilting, and major yield loss.",
        "cure": "Use a recommended hopper management spray such as imidacloprid, buprofezin, or another approved option based on local guidance.",
        "prevention": "Avoid excessive nitrogen, prevent dense planting, drain fields when needed, and conserve natural predators.",
    },
    "rice water weevil": {
        "problem": "Adults and larvae injure leaves and roots, weakening plant establishment and overall crop growth.",
        "cure": "Apply a suitable insecticide if field infestation is confirmed and root or leaf injury is progressing.",
        "prevention": "Manage water carefully, monitor transplanted fields early, and reduce pest carryover from previous crop residues.",
    },
    "rice leafhopper": {
        "problem": "Leafhoppers suck plant sap and may also transmit disease, reducing plant health and productivity.",
        "cure": "Use a recommended insecticide for hopper control after checking pest severity in the field.",
        "prevention": "Use balanced fertilizer, avoid unnecessary sprays that kill beneficial insects, and monitor hopper buildup regularly.",
    },
    "grain spreader thrips": {
        "problem": "Thrips scrape plant tissue and suck sap, causing curling, silvery streaks, and reduced seedling vigor.",
        "cure": "Use a locally recommended thrips control treatment when field infestation is active.",
        "prevention": "Maintain nursery hygiene, avoid moisture stress, and monitor seedlings and early crop stages frequently.",
    },
    "rice shell pest": {
        "problem": "Shell-feeding pests can damage plant surfaces and interfere with healthy growth when left unmanaged.",
        "cure": "Confirm the exact pest stage in the field and use a recommended control product advised by local agriculture experts.",
        "prevention": "Practice routine field scouting, remove hiding places, and integrate cultural and chemical control carefully.",
    },
}


def get_pest_details(name):
    normalized = normalize_pest_name(name)
    details = pest_info.get(normalized, DEFAULT_INFO)
    return {
        "problem": details["problem"],
        "cure": details["cure"],
        "prevention": details["prevention"],
    }


def build_rule_based_response(question, pest_name, confidence, pest_details):
    return (
        f"Detected pest: {pest_name} ({confidence:.2%} confidence).\n\n"
        f"Problem: {pest_details['problem']}\n"
        f"Cure: {pest_details['cure']}\n"
        f"Prevention: {pest_details['prevention']}\n\n"
        f"Question: {question}\n"
        "Guidance: Start with field scouting, confirm infestation severity, and follow locally approved pest-management advice before spraying."
    )
