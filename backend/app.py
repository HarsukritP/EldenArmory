from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from weapon import Weapon
from collection import CollectionObjects
import csv
import os

app = Flask(__name__)

# Define BASE_DIR based on the current working directory
BASE_DIR = os.getcwd()

CORS(app, resources={
    r"/*": {
        "origins": ["https://eldenarmory.vercel.app", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize weapons collection globally
weapons_collection = CollectionObjects()

def load_weapons():
    """Load weapons from CSV file into collection"""
    try:
        # Create a dictionary to store image URLs and descriptions
        weapon_details = {}
        weapons_csv_path = os.path.join(BASE_DIR, 'data', 'weapons.csv')
        elden_ring_weapon_csv_path = os.path.join(BASE_DIR, 'data', 'elden_ring_weapon.csv')
        
        print(f"Looking for weapons CSV at: {weapons_csv_path}")
        print(f"Looking for elden ring CSV at: {elden_ring_weapon_csv_path}")
        
        # First, load the weapon details from weapons.csv
        try:
            with open(weapons_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for line in reader:
                    weapon_name = line[1].strip()  # name column, strip whitespace
                    image_url = line[2]    # image column
                    description = line[3]   # description column
                    # Store with lowercase key for case-insensitive matching
                    weapon_details[weapon_name.lower()] = {
                        'image_url': image_url,
                        'description': description
                    }
                print(f"Loaded details for {len(weapon_details)} weapons")
        except Exception as e:
            print(f"Error loading weapons.csv: {str(e)}")
            weapon_details = {}

        print("Loading main weapon stats...")
        with open(elden_ring_weapon_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            count = 0
            for line in reader:
                name = line[0].strip()  # Strip whitespace
                weapon_type = line[1]
                # Directly use the values from CSV - they're already the correct numbers
                physical_dmg = int(line[2]) if line[2] != '-' else 0
                magic_dmg = int(line[3]) if line[3] != '-' else 0
                fire_dmg = int(line[4]) if line[4] != '-' else 0
                light_dmg = int(line[5]) if line[5] != '-' else 0
                holy_dmg = int(line[6]) if line[6] != '-' else 0
                crit_dmg = int(line[7]) if line[7] != '-' else 0
                stamina_dmg = int(line[8]) if line[8] != '-' else 0
                
                # Parse scaling values
                scale_dict = {'-': 0, 'S': 7.0, 'A': 5.5, 'B': 4.5, 'C': 3.5, 'D': 2.5, 'E': 1.5}
                str_scale = scale_dict[line[9]]
                dex_scale = scale_dict[line[10]]
                int_scale = scale_dict[line[11]]
                fai_scale = scale_dict[line[12]]
                arc_scale = scale_dict[line[13]]
                
                weight = float(line[22]) if line[22] != '-' else 0.0
                upgrade_type = line[23]
                
                # Case-insensitive lookup for weapon details
                details = weapon_details.get(name.lower(), {'image_url': '', 'description': ''})
                
                weapon = Weapon(
                    name, weapon_type, physical_dmg, magic_dmg, fire_dmg, 
                    light_dmg, holy_dmg, crit_dmg, stamina_dmg, 
                    str_scale, dex_scale, int_scale, fai_scale, arc_scale,
                    weight, upgrade_type, details['image_url'], details['description']
                )
                weapons_collection.add_object(weapon, weapon_type)
                count += 1
            print(f"Successfully loaded {count} weapons")
            return True
    except Exception as e:
        print(f"Error loading weapons: {str(e)}")
        return False

@app.route('/')
def index():
    return "Elden Ring Weapons API is running!"

@app.route('/api/weapons', methods=['GET'])
def get_weapons():
    try:
        weapons = []
        if not weapons_collection or not hasattr(weapons_collection, '_object_dictionary'):
            print("Warning: weapons_collection is not properly initialized")
            return jsonify([]), 500
            
        print(f"Collection has {len(weapons_collection._object_dictionary)} weapon types")
        for key in weapons_collection._object_dictionary:
            for weapon in weapons_collection._object_dictionary[key]:
                weapons.append({
                    'name': weapon.name(),
                    'type': weapon.type(),
                    'physical_damage': weapon._base_physical if hasattr(weapon, '_base_physical') else weapon.physical_damage(),
                    'magic_damage': weapon._base_magic if hasattr(weapon, '_base_magic') else weapon.magic_damage(),
                    'fire_damage': weapon._base_fire if hasattr(weapon, '_base_fire') else weapon.fire_damage(),
                    'light_damage': weapon._base_light if hasattr(weapon, '_base_light') else weapon.light_damage(),
                    'holy_damage': weapon._base_holy if hasattr(weapon, '_base_holy') else weapon.holy_damage(),
                    'crit_damage': weapon.crit_damage(),
                    'stamina_damage': weapon.stamina_damage(),
                    'strength_scaling': weapon.strength_scaling(),
                    'dexterity_scaling': weapon.dexterity_scaling(),
                    'intelligence_scaling': weapon.intelligence_scaling(),
                    'faith_scaling': weapon.faith_scaling(),
                    'arcane_scaling': weapon.arcane_scaling(),
                    'weight': weapon.weight(),
                    'upgrade_type': weapon.upgrade_stone(),
                    'value': weapon.value(),
                    'image_url': weapon.image_url(),
                    'description': weapon.description()
                })
        return jsonify(weapons)
    except Exception as e:
        print(f"Error in get_weapons: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/weapons/<path:name>', methods=['GET'])
def get_weapon(name):
    try:
        level = int(request.args.get('level', 1))  # Default level 1
        str_stat = int(request.args.get('strength', 10))
        dex_stat = int(request.args.get('dexterity', 10))
        int_stat = int(request.args.get('intelligence', 10))
        fai_stat = int(request.args.get('faith', 10))
        arc_stat = int(request.args.get('arcane', 10))
        
        # Case-insensitive weapon lookup
        name_lower = name.lower().strip()
        for weapons in weapons_collection._object_dictionary.values():
            for base_weapon in weapons:
                if base_weapon.name().lower().strip() == name_lower:
                    # Create a new weapon instance for scaling
                    weapon = Weapon(
                        base_weapon.name(),
                        base_weapon.type(),
                        base_weapon._base_physical if hasattr(base_weapon, '_base_physical') else base_weapon.physical_damage(),
                        base_weapon._base_magic if hasattr(base_weapon, '_base_magic') else base_weapon.magic_damage(),
                        base_weapon._base_fire if hasattr(base_weapon, '_base_fire') else base_weapon.fire_damage(),
                        base_weapon._base_light if hasattr(base_weapon, '_base_light') else base_weapon.light_damage(),
                        base_weapon._base_holy if hasattr(base_weapon, '_base_holy') else base_weapon.holy_damage(),
                        base_weapon.crit_damage(),
                        base_weapon.stamina_damage(),
                        base_weapon.strength_scaling(),
                        base_weapon.dexterity_scaling(),
                        base_weapon.intelligence_scaling(),
                        base_weapon.faith_scaling(),
                        base_weapon.arcane_scaling(),
                        base_weapon.weight(),
                        base_weapon.upgrade_stone(),
                        base_weapon.image_url(),
                        base_weapon.description(),
                        level,
                        str_stat,
                        dex_stat,
                        int_stat,
                        fai_stat,
                        arc_stat
                    )
                    
                    return jsonify({
                        'name': weapon.name(),
                        'type': weapon.type(),
                        'physical_damage': weapon.physical_damage(),
                        'magic_damage': weapon.magic_damage(),
                        'fire_damage': weapon.fire_damage(),
                        'light_damage': weapon.light_damage(),
                        'holy_damage': weapon.holy_damage(),
                        'crit_damage': weapon.crit_damage(),
                        'stamina_damage': weapon.stamina_damage(),
                        'strength_scaling': weapon.strength_scaling(),
                        'dexterity_scaling': weapon.dexterity_scaling(),
                        'intelligence_scaling': weapon.intelligence_scaling(),
                        'faith_scaling': weapon.faith_scaling(),
                        'arcane_scaling': weapon.arcane_scaling(),
                        'weight': weapon.weight(),
                        'upgrade_type': weapon.upgrade_stone(),
                        'value': weapon.value(),
                        'image_url': weapon.image_url(),
                        'description': weapon.description()
                    })
                    
        return jsonify({'error': 'Weapon not found'}), 404
    except Exception as e:
        print(f"Error in get_weapon: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
@app.route('/debug', methods=['GET'])
def debug():
    import sys
    debug_info = {
        "status": "online",
        "base_dir": BASE_DIR,
        "python_version": sys.version,
        "weapons_loaded": hasattr(weapons_collection, '_object_dictionary')
    }
    
    # Check if data directory exists and list its contents
    data_dir = os.path.join(BASE_DIR, 'data')
    debug_info["data_dir_exists"] = os.path.exists(data_dir)
    
    if os.path.exists(data_dir):
        debug_info["data_dir_contents"] = os.listdir(data_dir)
        
        # Check CSV files specifically
        weapons_csv_path = os.path.join(data_dir, 'weapons.csv')
        elden_ring_csv_path = os.path.join(data_dir, 'elden_ring_weapon.csv')
        
        debug_info["weapons_csv_exists"] = os.path.exists(weapons_csv_path)
        debug_info["elden_ring_csv_exists"] = os.path.exists(elden_ring_csv_path)
    
    # Check weapons collection
    if hasattr(weapons_collection, '_object_dictionary'):
        debug_info["weapon_types"] = list(weapons_collection._object_dictionary.keys())
        debug_info["total_weapons"] = sum(len(weapons) for weapons in weapons_collection._object_dictionary.values())
    
    return jsonify(debug_info)

# Load weapons when the application is initialized
print("Loading weapons on initialization...")
load_weapons()
print("Weapons loading completed")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)