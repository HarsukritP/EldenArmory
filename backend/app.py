from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from weapon import Weapon
from collection import CollectionObjects
import csv
import os

app = Flask(__name__)
CORS(app)

weapons_collection = CollectionObjects()

def load_weapons():
    """Load weapons from CSV file into collection"""
    try:
        weapon_details = {}
        print("Loading weapons metadata...")
        
        # Load weapon details first
        try:
            with open('data/weapons.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for line in reader:
                    weapon_name = line[1]
                    image_url = line[2]
                    description = line[3]
                    weapon_details[weapon_name] = {
                        'image_url': image_url,
                        'description': description
                    }
                print(f"Loaded details for {len(weapon_details)} weapons")
        except Exception as e:
            print(f"Error loading weapons.csv: {str(e)}")
            weapon_details = {}

        print("Loading main weapon stats...")
        with open('data/elden_ring_weapon.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            count = 0
            for line in reader:
                name = line[0]
                weapon_type = line[1]
                physical_dmg = int(line[2]) if line[2] != '-' else 0
                magic_dmg = int(line[3]) if line[3] != '-' else 0
                fire_dmg = int(line[4]) if line[4] != '-' else 0
                light_dmg = int(line[5]) if line[5] != '-' else 0
                holy_dmg = int(line[6]) if line[6] != '-' else 0
                crit_dmg = int(line[7]) if line[7] != '-' else 0
                stamina_dmg = int(line[8]) if line[8] != '-' else 0
                
                scale_dict = {'-': 1.0, 'S': 7.0, 'A': 5.5, 'B': 4.5, 'C': 3.5, 'D': 2.5, 'E': 1.5}
                str_scale = scale_dict[line[9]]
                dex_scale = scale_dict[line[10]]
                int_scale = scale_dict[line[11]]
                fai_scale = scale_dict[line[12]]
                arc_scale = scale_dict[line[13]]
                
                weight = float(line[22]) if line[22] != '-' else 0.0
                upgrade_type = line[23]
                
                details = weapon_details.get(name, {'image_url': '', 'description': ''})
                
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
def home():
    return jsonify({"status": "running"})

@app.route('/api/weapons')
def get_weapons():
    weapons = []
    for key in weapons_collection._object_dictionary:
        for weapon in weapons_collection._object_dictionary[key]:
            weapons.append({
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
    return jsonify(weapons)

@app.route('/api/weapons/<path:name>', methods=['GET'])
def get_weapon(name):
    try:
        level = int(request.args.get('level', 1))
        str_stat = int(request.args.get('strength', 10))
        dex_stat = int(request.args.get('dexterity', 10))
        int_stat = int(request.args.get('intelligence', 10))
        fai_stat = int(request.args.get('faith', 10))
        arc_stat = int(request.args.get('arcane', 10))
        
        print(f"Updating {name} - Level: {level}, STR: {str_stat}, DEX: {dex_stat}")
        
        for weapons in weapons_collection._object_dictionary.values():
            for weapon in weapons:
                if weapon.name().lower() == name.lower():
                    # Create a new weapon instance with updated stats
                    updated_weapon = Weapon(
                        weapon.name(), weapon.type(), 
                        weapon._base_physical, weapon._base_magic, 
                        weapon._base_fire, weapon._base_light, weapon._base_holy,
                        weapon.crit_damage(), weapon.stamina_damage(),
                        weapon.strength_scaling(), weapon.dexterity_scaling(),
                        weapon.intelligence_scaling(), weapon.faith_scaling(),
                        weapon.arcane_scaling(), weapon.weight(),
                        weapon.upgrade_stone(), weapon.image_url(),
                        weapon.description(), level, str_stat, dex_stat,
                        int_stat, fai_stat, arc_stat
                    )
                    
                    return jsonify({
                        'name': updated_weapon.name(),
                        'type': updated_weapon.type(),
                        'physical_damage': updated_weapon.physical_damage(),
                        'magic_damage': updated_weapon.magic_damage(),
                        'fire_damage': updated_weapon.fire_damage(),
                        'light_damage': updated_weapon.light_damage(),
                        'holy_damage': updated_weapon.holy_damage(),
                        'crit_damage': updated_weapon.crit_damage(),
                        'stamina_damage': updated_weapon.stamina_damage(),
                        'strength_scaling': updated_weapon.strength_scaling(),
                        'dexterity_scaling': updated_weapon.dexterity_scaling(),
                        'intelligence_scaling': updated_weapon.intelligence_scaling(),
                        'faith_scaling': updated_weapon.faith_scaling(),
                        'arcane_scaling': updated_weapon.arcane_scaling(),
                        'weight': updated_weapon.weight(),
                        'upgrade_type': updated_weapon.upgrade_stone(),
                        'value': updated_weapon.value(),
                        'image_url': updated_weapon.image_url(),
                        'description': updated_weapon.description()
                    })
        
        return jsonify({'error': 'Weapon not found'}), 404
    except Exception as e:
        print(f"Error in get_weapon: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not load_weapons():
        print("Failed to load weapons, exiting...")
        exit(1)
    print("Weapons loaded successfully")
    app.run(host='127.0.0.1', port=5001, debug=True)