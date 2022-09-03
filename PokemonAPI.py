import requests
from jinja2 import *
class PokemonAPI:
    def __init__(self,pokemon_name):
        self.pokemon_name = pokemon_name

    def get_pokemon(self):
        name = self.pokemon_name
        if str(name).lower() == "mimikyu":
            full_path = "https://pokeapi.co/api/v2/pokemon/778"
        else:
            full_path = "https://pokeapi.co/api/v2/pokemon/" + str(name).lower()
        response = requests.get(full_path)
        json = response.json()
        return json

    def get_id(self,json):
        id = json["id"]
        return str(id)

    def get_name(self,json):
        if(json["name"] == "mimikyu-disguised"):
            name = "mimikyu"
        else:
            name = json["name"]
        return str(name)

    def get_types(self,json):
        all_type_info = []
        pokemon_types = []
        quarter_damage_types = []
        half_damage_types = []
        double_damage_types = []
        quad_damage_types = []
        no_damage_types = []
        for types in json["types"]:
            type = types.get('type').get('name')
            pokemon_types.append(type)
        all_type_info.append(pokemon_types)
        for type in pokemon_types:
            link = "https://pokeapi.co/api/v2/type/" + type
            type_response = requests.get(link).json()
            damage_relations = type_response.get("damage_relations")
            for half_damage in damage_relations.get("half_damage_from"):
                if half_damage.get("name") in half_damage_types:
                    half_damage_types.remove(half_damage.get("name"))
                    quarter_damage_types.append(half_damage.get("name"))
                else:
                    half_damage_types.append(half_damage.get("name"))
            for double_damage in damage_relations.get("double_damage_from"):
                if double_damage.get("name") in double_damage_types:
                    double_damage_types.remove(double_damage.get("name"))
                    quad_damage_types.apppend(double_damage.get("name"))
                else:
                    double_damage_types.append(double_damage.get("name"))
            for no_damage in damage_relations.get("no_damage_from"):
                if no_damage.get("name") not in no_damage_types:
                    no_damage_types.append(no_damage.get("name"))
        all_type_info.append(no_damage_types) #1
        all_type_info.append(quarter_damage_types) #2
        all_type_info.append(half_damage_types) #3
        all_type_info.append(double_damage_types) #4
        all_type_info.append(quad_damage_types) #5
        print(all_type_info)
        return all_type_info

    def get_stats(self,json):
        # 0 = hp 1 = atk 2 = def 3 = sp ak 4 = sp def & 5 = spd_stat
        stat_json = json["stats"]
        stats = []
        for index in range(6):
            stats.append(stat_json[index].get('base_stat'))
        return stats
    
    def get_damage_multiplier(self,damage_response, input_list):
        damages = []
        for damage in input_list:
            damage_type = []
            if damage_response.get(damage):
                for entry in damage_response.get(damage):
                    damage_type.append(entry.get("name"))
                damages.append(damage_type)
        return damages

    def get_move_names(self,json):
        all_move_names = []
        move_json = json["moves"]
        for i,move in enumerate(move_json,start = 0):
             move_name = move_json[i].get("move").get("name")
             all_move_names.append(move_name)
        return all_move_names

    def get_move_info(self,move_name): 
        link = "https://pokeapi.co/api/v2/move/" + move_name
        move_response = requests.get(link).json()
        move_info = {
            "name": move_name,
            "description": move_response.get("effect_entries")[0].get('effect'),
            "accuracy": move_response.get("accuracy"),
            "power": move_response.get("power"),
            "pp": move_response.get("pp"),
            "type": move_response.get("type").get("name")
        }
        return move_info

    def get_abilities(self,json):
        abilities = {}
        for ability in json["abilities"]:
            ability_name = ability.get('ability').get('name')
            description_path = "https://pokeapi.co/api/v2/ability/" + ability_name
            description_response = requests.get(description_path).json()
            possible_abilities = list(description_response['effect_entries'])
            for ability in possible_abilities:
                if 'en' in ability.get('language').get('name'):
                    abilities[ability_name] = ability.get('short_effect')
        return abilities

    def get_sprite(self,json):
        id_ = self.get_id(json)
        if(len(id_) == 1):
            id_ = "00" + id_
        elif(len(id_) == 2):
            id_ = "0" + id_
        sprite_link = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/" + \
            id_ + ".png"
        return sprite_link
    
    def confirm_legit(self,json):
        try:
            pokemon_json = self.get_pokemon()
            pokemon_name = self.get_name(pokemon_json)
            return(pokemon_name)
        except:
            return("404")