from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.max_damage, self.min_damage)


@dataclass
class EquipmentData:
    armors: List[Armor]
    weapons: List[Weapon]

    class Meta:
        unknown = marshmallow.EXCLUDE


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        for i in self.equipment.weapons:
            if i.name == weapon_name:
                return i

    def get_armor(self, armor_name) -> Armor:
        for i in self.equipment.armors:
            if i.name == armor_name:
                return i

    def get_weapons_names(self) -> list:
        weapons_list = []
        for i in self.equipment.weapons:
            weapons_list.append(i.name)
        return weapons_list

    def get_armors_names(self) -> list:
        armors_list = []
        for i in self.equipment.armors:
            armors_list.append(i.name)
        return armors_list

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        equipment_file = open("./data/equipment.json")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
