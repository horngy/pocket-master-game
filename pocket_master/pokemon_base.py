"""
This module contains PokeType, TypeEffectiveness and an abstract version of the Pokemon Class
"""

__author__ = "Teh Yee Hong"

from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR
from math import ceil

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.

        Complexity:
            O(1) for best case, it occurs when the file (type_effectiveness.csv) has no lines, the loop would not even start
            O(n) for worst case, it occurs when the file has 16 lines
        """
        table = ArrayR(16)
        with open("type_effectiveness.csv", "r") as file:
            line = 0
            for x in file:
                table.__setitem__(line, x.strip().split(","))
                line += 1
        effectiveness = float(table[attack_type.value + 1][defend_type.value])
        return effectiveness

    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon

        Complexity: O(1)
        """
        return len(PokeType)

class Pokemon(ABC):  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None
        self.max_hp = None

    def set_max_hp(self):
        """
        Set the Pokemon maximum health (this is called when a Pokemon is being made)

        Complexity: O(1)
        """
        self.max_hp = self.health

    def get_max_hp(self):
        """
        Returns the maximum or original health points of a pokemon

        Returns:
            int: The maximum health of the Pokemon

        Complexity: O(1)
        """
        return self.max_hp

    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        """
        return self.health

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    def attack(self, other_pokemon) -> float:
        """
        Calculates and returns the damage that this Pokemon inflicts on the
        other Pokemon during an attack.

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            float: The damage that this Pokemon inflicts on the other Pokemon during an attack.

        Complexity:
            O(n) for both best and worst case. There's only mathematical operation here except for TypeEffectiveness.get_effectiveness(),
            so it is dependent on that function, best case for the function should never happen, so it is O(n).
        """
        if other_pokemon.defence < (self.battle_power / 2):
            damage = self.battle_power - other_pokemon.defence
            effective_damage = damage * TypeEffectiveness.get_effectiveness(self.poketype, other_pokemon.poketype)
        elif other_pokemon.defence < self.battle_power:
            damage = ceil((self.battle_power * 5/8) - (other_pokemon.defence / 4))
            effective_damage = damage * TypeEffectiveness.get_effectiveness(self.poketype, other_pokemon.poketype)
        else:
            damage = ceil(self.battle_power / 4)
            effective_damage = damage * TypeEffectiveness.get_effectiveness(self.poketype, other_pokemon.poketype)

        return effective_damage

    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        """
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.

        Complexity: O(1)
        """
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index(self.name) != len(self.evolution_line)-1:  # check whether there's an evolution
            self._evolve()

    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.

        Complexity: O(1)
        """
        self.battle_power *= 1.5

        self.health *= 1.5
        self.speed *= 1.5
        self.defence *= 1.5
        self.name = self.evolution_line[self.evolution_line.index(self.name) + 1]

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self):
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"

if __name__ == '__main__':
    pass
