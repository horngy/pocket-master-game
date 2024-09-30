"""
This module contains BattleTower class, which somewhat acts as a Pokemon Gym
"""

__author__ = "Teh Yee Hong"

from poke_team import Trainer, PokeTeam
from battle import Battle
from battle_mode import BattleMode
from data_structures.queue_adt import CircularQueue
from data_structures.sorted_list_adt import ListItem
from typing import Tuple
import random


class BattleTower:
    """
    This class represents a Pokemon Gym, where it is required to defeat every Trainer inside it to get the badge
    """
    MIN_LIVES = 1
    MAX_LIVES = 3

    def __init__(self) -> None:
        """
        Initializing a new instance of the class
        """
        self.the_trainer = None
        self.enemies = None
        self.enemies_defeated_count = 0

    # Hint: use random.randint() for randomisation
    def set_my_trainer(self, trainer: Trainer) -> None:
        """
        This function is used to set the challenger's life

        param arg1: A Trainer class item

        Complexity: O(1)
        """
        lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
        self.the_trainer = ListItem(trainer, lives)

    def generate_enemy_trainers(self, num_teams: int) -> None:
        """
        This function is used to generate total numbers of enemies in the tower and their lives

        param arg1: int: number of enemies inside the tower

        Complexity: O(n) best = worst
        """
        self.enemies = CircularQueue(num_teams)
        count = 0
        while not self.enemies.is_full():
            enemy = Trainer(f"Trainer {count}")
            enemy.pick_team("Random")
            lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            e = ListItem(enemy, lives)
            self.enemies.append(e)
            count += 1

    def battles_remaining(self) -> bool:
        """
        This function is used to determine whether there is still an enemy in the tower
        True when the challenger is still alive and there's still enemies
        False when the challenger is dead or there's no enemy left

        Returns: bool

        Complexity: O(1)
        """
        if self.enemies.is_empty() or self.the_trainer.key == 0:
            return False
        else:
            return True

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        This function is used to call a battle between the challenger and an enemy

        Returns:
            string: the name of the winner or "draw"
            string: the name of the challenger
            string: the name of the enemy
            int: challenger's life
            int: enemy's life

        Complexity:
            O(n^2) for both cases
        """
        current_enemy = self.enemies.serve()
        b = Battle(self.the_trainer.value, current_enemy.value, BattleMode.ROTATE)
        b._create_teams()
        winner = b.commence_battle()

        outcome = None
        if winner is None:
            outcome = "Draw"
            self.the_trainer.key -= 1
            current_enemy.key -= 1
            self.enemies_defeated_count += 1
        elif winner == self.the_trainer.value:
            outcome = self.the_trainer.value.get_name()
            current_enemy.key -= 1
            self.enemies_defeated_count += 1
        elif winner == current_enemy.value:
            outcome = current_enemy.value.get_name()
            self.the_trainer.key -= 1

        if self.the_trainer.key != 0:
            self.the_trainer.value.team.regenerate_team(BattleMode.ROTATE)
        if current_enemy.key != 0:
            current_enemy.value.team.regenerate_team(BattleMode.ROTATE)
            self.enemies.append(current_enemy)
        return outcome, self.the_trainer.value.get_name(), current_enemy.value.get_name(), self.the_trainer.key, current_enemy.key

    def enemies_defeated(self) -> int:
        """
        This is called to return the total number of enemies defeated

        Returns: Integers of enemies defeated
        """
        return self.enemies_defeated_count
