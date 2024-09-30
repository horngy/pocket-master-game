"""
This module contains Battle class, which is use for battling within two trainers
"""

from __future__ import annotations

__author__ = "Teh Yee Hong"

from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from math import ceil

class Battle:
    """
    This class represents a battle between two trainers
    """
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion="health") -> None:
        """
        Initializing a new instance of a Battle class

        param arg1: First trainer from Trainer class
        param arg2: Second trainer from Trainer class
        param arg3: the battle_mode of the battle
        param arg4: the criterion of the battle (only available in optimised mode)
        """
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion
        self.team1 = None
        self.team2 = None

    def commence_battle(self) -> Trainer | None:
        """
        This function is used to call a battle between two trainers

        Returns: The trainer that won the battle, if it's a draw, None will be returned

        Complexity:
            Best case O(1), will only happen when both team is empty (impossible)
            Worst case O(n^2), will happen when both team is full of Pokemon (should always happen)
        """
        winning_team = None
        if self.battle_mode.value == 0:
            winning_team = self.set_battle()
        elif self.battle_mode.value == 1:
            winning_team = self.rotate_battle()
        elif self.battle_mode.value == 2:
            winning_team = self.optimise_battle()

        if winning_team == self.team1:
            return self.trainer_1
        elif winning_team == self.team2:
            return self.trainer_2
        else:
            return None

    def _create_teams(self) -> None:
        """
        This function is used to create both trainer's battle_team based on the battle_mode

        Complexity:
            Complexity for .pick_team("Random") is O(1)
            Complexity for .assemble_team(battle_mode: BattleMode, criterion=None) could be O(1) or O(n)
            Best case is O(1), when both trainers already got a team of Pokemon, and when the battle_mode is 0 or 1
            Worst case is O(n), when both trainers do not have a team of Pokemon, and when battle_mode is 2, and after picking randomly it is reversed sorted
        """
        if self.trainer_1.team.team is None:
            self.trainer_1.pick_team("Random")
        self.trainer_1.team.assemble_team(self.battle_mode, self.criterion)
        self.team1 = self.trainer_1.team.battle_team
        if self.trainer_2.team.team is None:
            self.trainer_2.pick_team("Random")
        self.trainer_2.team.assemble_team(self.battle_mode, self.criterion)
        self.team2 = self.trainer_2.team.battle_team

    # Note: These are here for your convenience
    # If you prefer you can ignore them
    def set_battle(self) -> PokeTeam | None:
        """
        When battle_mode is 0, the battle will follow the "King of hill" style

        Returns: The PokeTeam that won the battle

        Complexity:
            Best case is O(1), when one or both team is empty (this would not happen)
            Worst case is O(n^2), when both team is full of Pokemon
        """
        while not (self.team1.is_empty() or self.team2.is_empty()):  # this loop will not end until one of the team is eliminated
            p1 = self.team1.peek()
            p2 = self.team2.peek()
            self.trainer_1.register_pokemon(p2)
            self.trainer_2.register_pokemon(p1)
            p1_alive, p2_alive = self.actual_battle(p1, p2)  # battle between two Pokemon, will return boolean
            if p1_alive is False:
                self.team1.pop()
            if p2_alive is False:
                self.team2.pop()
        if self.team1.is_empty() and self.team2.is_empty():
            return None
        elif self.team1.is_empty():
            return self.team2
        elif self.team2.is_empty():
            return self.team1

    def rotate_battle(self) -> PokeTeam | None:
        """
        When battle_mode is 1, Pokemon will fight a round, then send to the back of the team if they're still alive

        Returns: The PokeTeam that won the battle

        Complexity:
            Best case is O(1), when one or both team is empty (this would not happen)
            Worst case is O(n^2), when both team is full of Pokemon
        """
        while not (self.team1.is_empty() or self.team2.is_empty()):
            p1 = self.team1.serve()
            p2 = self.team2.serve()
            self.trainer_1.register_pokemon(p2)
            self.trainer_2.register_pokemon(p1)
            p1_alive, p2_alive = self.actual_battle(p1, p2)
            if p1_alive is True:
                self.team1.append(p1)
            if p2_alive is True:
                self.team2.append(p2)
        if self.team1.is_empty() and self.team2.is_empty():
            return None
        elif self.team1.is_empty():
            return self.team2
        elif self.team2.is_empty():
            return self.team1

    def optimise_battle(self) -> PokeTeam | None:
        """
        When battle_mode is 2, Pokemon will fight around, then send back to the team, the team will be reorganized,
        then the first pokemon will fight again

        Returns: The PokeTeam that won the battle

        Complexity:
            Best case is O(1), when one or both team is empty (this would not happen)
            Worst case is O(n^2), when both team is full of Pokemon
        """
        while not (self.team1.is_empty() or self.team2.is_empty()):
            p1 = self.team1.peek()
            p2 = self.team2.peek()
            self.trainer_1.register_pokemon(p2)
            self.trainer_2.register_pokemon(p1)
            p1_alive, p2_alive = self.actual_battle(p1, p2)
            if p1_alive is False:
                self.team1.pop()
            if p2_alive is False:
                self.team2.pop()
            self.trainer_1.team.assign_team()
            self.trainer_2.team.assign_team()
        if self.team1.is_empty() and self.team2.is_empty():
            return None
        elif self.team1.is_empty():
            return self.team2
        elif self.team2.is_empty():
            return self.team1

    def actual_battle(self, p1, p2):
        """
        This function is used to battle between two Pokemon

        param arg1: Pokemon by first Trainer
        param arg2: Pokemon by second Trainer

        Returns: Boolean of both Pokemon's life

        Complexity: Both best and worst case is O(n)
        """
        if p1.get_speed() == p2.get_speed():  # when both Pokemon have the same speed
            attack_damage = ceil(p1.attack(p2) * (self.trainer_1.get_pokedex_completion()/self.trainer_2.get_pokedex_completion()))
            p2.defend(attack_damage)
            attack_damage = ceil(p2.attack(p1) * (self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion()))
            p1.defend(attack_damage)
            if p1.is_alive() and p2.is_alive():
                self.both_minus_one(p1, p2)
            else:
                if p1.is_alive() and not p2.is_alive():
                    p1.level_up()
                if p2.is_alive() and not p1.is_alive():
                    p2.level_up()
        else:
            if p1.get_speed() > p2.get_speed():
                self.not_equal_speed(p1, p2, self.trainer_1, self.trainer_2)
            else:
                self.not_equal_speed(p2, p1, self.trainer_2, self.trainer_1)

        return p1.is_alive(), p2.is_alive()

    def not_equal_speed(self, attacker, defender, attacking_dex, defending_dex):
        """
        This function is used to calculate attacking damage and defending it, will check for death, if both is still alive, both_minus_one(p1, p2) will be called

        param arg1: The pokemon that has the faster speed
        param arg2: The pokemon that has the slower speed
        param arg3: The trainer of the faster speed Pokemon
        param arg4: The trainer of the slower speed Pokemon

        Complexity:
            Complexity for .get_pokedex_completion() is guaranteed to be O(n) at this point
            O(n) for both best and worst case
        """
        attack_damage = ceil(attacker.attack(defender) * (attacking_dex.get_pokedex_completion() / defending_dex.get_pokedex_completion()))
        defender.defend(attack_damage)
        if defender.is_alive():
            attack_damage = ceil(defender.attack(attacker) * (defending_dex.get_pokedex_completion() / attacking_dex.get_pokedex_completion()))
            attacker.defend(attack_damage)
            if attacker.is_alive():
                self.both_minus_one(attacker, defender)
            else:
                defender.level_up()
        else:
            attacker.level_up()

    def both_minus_one(self, p1, p2):
        """
        This function is used to deduct both Pokemon's health by 1 after a fight if they're still alive, and will check for death

        param arg1: Pokemon by first trainer
        param arg2: Pokemon by second trainer

        Complexity: O(1) for both cases
        """
        p1.health -= 1
        p2.health -= 1
        if p1.is_alive() and not p2.is_alive():
            p1.level_up()
        if p2.is_alive() and not p1.is_alive():
            p2.level_up()

if __name__ == '__main__':
   pass
