"""
This module contains PokeTeam and Trainer
"""

__author__ = "Teh Yee Hong"

from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.array_sorted_list import ArraySortedList
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.sorted_list_adt import ListItem
from data_structures.referential_array import ArrayR

class PokeTeam:
    """
    Represents a team of Pokemon
    """
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]
    random.seed(20)

    def __init__(self):
        """
        initialize a new instance of PokeTeam class
        team and battle_team is different in my code,
        team is just used to store all the pokemon own by a trainer,
        battle_team is the team used for battling
        """
        self.team = None
        self.team_count = 0
        self.battle_team = None
        self.criterion = None

    def choose_manually(self):
        """
        Use to choose Pokemon manually (based on index), will be asked to choose until it reaches TEAM_LIMIT or 'done'

        Complexity:
            Best case is O(1), if user input 'done' straight away the loop will break
            Worst case is O(n), n is when it reaches TEAM_LIMIT
        """
        self.team = ArrayR(self.TEAM_LIMIT)
        self.team_count = self.__len__()
        while self.team_count != self.TEAM_LIMIT:
            p = input("Choose your pokemon ('done' to end): ")
            if p == "done":
                break
            else:
                choice = self.POKE_LIST[int(p)]()
                choice.set_max_hp()
                self.team[self.team_count] = choice
                self.team_count += 1
        self.battle_team = self.team
        print("done")

    def choose_randomly(self) -> None:
        """
        Use to choose Pokemon randomly, will choose until it reaches TEAM_LIMIT

        Complexity:
            O(n) for both best and worst case
        """
        self.team = ArrayR(self.TEAM_LIMIT)
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            choice = all_pokemon[rand_int]()
            choice.set_max_hp()
            self.team[i] = choice
            self.team_count += 1
        self.battle_team = self.team

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        Will regenerate the health of all the Pokemon in the battle_team to their maximum health,
        will also assemble their team again

        param arg1: the battle_mode of the battle
        param arg2: the criterion of the battle (only available in optimised mode)

        Complexity:
            best and worst case is both O(n), the first for loop is O(n), self.assemble_team is either O(1) or O(n)
        """
        for x in self.team:
            x.health = x.max_hp
        self.assemble_team(battle_mode, criterion)

    def assign_team(self) -> None:
        """
        Will reassign the battle_team based on the criterion of the battle (only available in optimised mode)

        Complexity:
            Best case is O(n), when all the Pokemon are already sorted based on the criterion, so no sorting is needed, it will be faster
            Worst case is O(n * log n) = O(n), when all the Pokemon are reverse sorted, max arrangement is needed, sorting will be slower
        """
        temp = ArraySortedList(6)
        count = 0
        team_count = len(self.battle_team)
        while count != team_count:  
            x = self.battle_team.pop()
            if x is not None:
                if self.criterion == "health":
                    p = ListItem(x, x.get_health())
                    temp.add(p)
                elif self.criterion == "defence":
                    p = ListItem(x, x.get_defence())
                    temp.add(p)
                elif self.criterion == "battle_power":
                    p = ListItem(x, x.get_battle_power())
                    temp.add(p)
                elif self.criterion == "speed":
                    p = ListItem(x, x.get_speed())
                    temp.add(p)
                elif self.criterion == "level":
                    p = ListItem(x, x.get_level())
                    temp.add(p)
            count += 1
        for i in range(len(temp) - 1, -1, -1):  # reversed
            self.battle_team.push(temp[i].value)

    def assemble_team(self, battle_mode: BattleMode, criterion=None) -> None:
        """
        Will assemble a battle_team, the data structure of battle_team is different based on the battle_mode

        param arg1: the battle_mode of the battle
        param arg2: the criterion of the battle (only available in optimised mode)

        Complexity:
            best case is O(1), occurs when mode is either 0 or 1
            worst case is O(n * log n) = O(n), when mode is 2 and all Pokemon are reverse sorted
        """
        mode = battle_mode.value
        self.criterion = criterion

        if mode == 0:
            self.battle_team = ArrayStack(6)
            count = 0
            while count != 6:
                if self.team[count] is not None:
                    self.battle_team.push(self.team[count])
                count += 1

        elif mode == 1:
            self.battle_team = CircularQueue(6)
            count = 0
            while count != 6:
                if self.team[count] is not None:
                    self.battle_team.append(self.team[count])
                count += 1

        elif mode == 2:
            temp = ArraySortedList(6)  # an ArraySortedList will be used to sort all the Pokemon first, then only push to an ArrayStack
            count = 0
            while count != 6:
                if self.criterion == "health":
                    p = ListItem(self.team[count], self.team[count].get_health())
                    temp.add(p)
                elif self.criterion == "defence":
                    p = ListItem(self.team[count], self.team[count].get_defence())
                    temp.add(p)
                elif self.criterion == "battle_power":
                    p = ListItem(self.team[count], self.team[count].get_battle_power())
                    temp.add(p)
                elif self.criterion == "speed":
                    p = ListItem(self.team[count], self.team[count].get_speed())
                    temp.add(p)
                elif self.criterion == "level":
                    p = ListItem(self.team[count], self.team[count].get_level())
                    temp.add(p)
                count += 1
            self.battle_team = ArrayStack(6)
            for i in range(len(temp) - 1, -1, -1):
                self.battle_team.push(temp[i].value)

    def special(self, battle_mode: BattleMode) -> None:
        """
        will change the battle_team formation based on the battle_mode

        param arg1: the battle_mode of the battle

        Complexity:
            Best case is O(1), when mode is 0
            Worst case is O(n), when mode is 2
        """
        mode = battle_mode.value
        if mode == 0:
            self.special_set()
        elif mode == 1:
            self.special_rotate()
        elif mode == 2:
            self.special_optimise()

    def special_set(self):
        """
        Reverse the first half of the team, when battle_mode is 0

        Complexity: O(1)
        """
        temp1 = self.battle_team.pop()
        temp2 = self.battle_team.pop()
        temp3 = self.battle_team.pop()
        self.battle_team.push(temp1)
        self.battle_team.push(temp2)
        self.battle_team.push(temp3)

    def special_rotate(self):
        """
        Reverse the bottom half of the team, when battle_mode is 1

        Complexity: O(1)
        """
        temp1 = self.battle_team.serve()
        temp2 = self.battle_team.serve()
        temp3 = self.battle_team.serve()
        temp4 = self.battle_team.serve()
        temp5 = self.battle_team.serve()
        temp6 = self.battle_team.serve()
        self.battle_team.append(temp1)
        self.battle_team.append(temp2)
        self.battle_team.append(temp3)
        self.battle_team.append(temp6)
        self.battle_team.append(temp5)
        self.battle_team.append(temp4)

    def special_optimise(self):
        """
        Reverse the whole team, when battle_mode is 2

        Complexity: Best and worst are both O(n), this will only be called after the team is in sorted order,
                    so just reversing when adding into the battle_team
        """
        temp = ArraySortedList(6)
        count = 0
        team_count = len(self.battle_team)
        while count != team_count:
            x = self.battle_team.pop()
            if x is not None:
                if self.criterion == "health":
                    p = ListItem(x, x.get_health())
                    temp.add(p)
                elif self.criterion == "defence":
                    p = ListItem(x, x.get_defence())
                    temp.add(p)
                elif self.criterion == "battle_power":
                    p = ListItem(x, x.get_battle_power())
                    temp.add(p)
                elif self.criterion == "speed":
                    p = ListItem(x, x.get_speed())
                    temp.add(p)
                elif self.criterion == "level":
                    p = ListItem(x, x.get_level())
                    temp.add(p)
            count += 1
        for i in range(len(temp)):
            self.battle_team.push(temp[i].value)

    def temp_copy(self):
        """
        this function convert the battle_team into an ArrayR temporary, purposes to get the length, string and item of the class
        ArrayStack and CircularQueue works differently, so in order for all of them to work the same, converting all into an ArrayR works

        Returns:
            An ArrayR containing battle_team

        Complexity:
            Best case is O(1), when battle_team is already an ArrayR
            Worst case is O(n), when battle_team is not an ArrayR, and all the Pokemon are alive
        """
        temp = ArrayR(6)
        count = 0
        if isinstance(self.battle_team, ArrayStack):
            temp_stack = ArrayStack(len(self.battle_team))
            for i in range(len(self.battle_team)):
                x = self.battle_team.pop()
                temp_stack.push(x)
                if x.is_alive():
                    temp[count] = x
                    count += 1
            for i in range(len(temp_stack)):
                x = temp_stack.pop()
                self.battle_team.push(x)
        elif isinstance(self.battle_team, CircularQueue):
            for i in range(len(self.battle_team)):
                x = self.battle_team.serve()
                self.battle_team.append(x)
                if x.is_alive():
                    temp[count] = x
                    count += 1
        else:
            temp = self.battle_team
        return temp

    def __getitem__(self, index: int):
        """
        Get you the item based on index

        param arg1: index in the form of integer

        Returns: the item on the index

        Complexity: Depending on self.temp_copy()
        """
        temp = self.temp_copy()
        return temp[index]

    def __len__(self):
        """
        Get you the length of the battle_team

        Returns: length in the form of integer

        Complexity: O(n) for best and worst case, as self.temp_copy() could be O(1) or O(n)
        """
        temp = self.temp_copy()
        count = 0
        for x in temp:
            if x is not None:
                count += 1
        return count

    def __str__(self):
        """
        Return a string presentation of the battle_team in Pokemon's name format

        Returns: A string

        Complexity: O(n) for best and worst case, as self.temp_copy() could be O(1) or O(n)
        """
        temp = self.temp_copy()
        string = ""
        for i in temp:
            if i is not None:
                string += i.name + " "
        return string

class Trainer:
    """
    This class contains the name, battle_team and poketypedex of a trainer
    """

    def __init__(self, name) -> None:
        """
        Initialize a new instance of trainer class

        param arg1: name of the trainer in string form
        """
        self.name = name
        self.team = PokeTeam()
        self.poketypedex = ArrayR(len(PokeType))

    def pick_team(self, method: str) -> None:
        """
        This will pick the trainer's team base on method choosen, then register all the pokemon into poketypedex

        param arg1: either "Random" or "Manual" in string form

        Complexity:
            Best case is O(1) when "Random" is choosen and the Pokemon's type is first in poketypedex
            Worst is O(n) when "Manual" is choosen and the Pokemon's type is not in it, and there's already len(PokeType) - 1 element in the poketypedex
        """
        if method == "Random":
            self.team.choose_randomly()
        elif method == "Manual":
            self.team.choose_manually()
        else:
            raise Exception("Error")
        for x in self.team:
            self.register_pokemon(x)

    def get_team(self) -> PokeTeam:
        """
        This will return the trainer's PokeTeam

        Returns: Trainer's PokeTeam in string form

        Complexity: O(1)
        """
        return self.team

    def get_name(self) -> str:
        """
        This will return the name of Trainer

        Returns: name in the form of string

        Complexity: O(1)
        """
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        This will register Pokemon's type that are not in the poketypedex

        param arg1: a Pokemon class (son class)

        Complexity:
            Best case is O(1), when the Pokemon's type is already inside poketypedex, and it is the first one
            Worst case is O(n), when the Pokemon's type is not in it, and there's already len(PokeType) - 1 element in the poketypedex
        """
        if pokemon is not None:
            try:
                self.poketypedex.index(pokemon.get_poketype())  # check whether the pokemon's type is already in it, if it's not, ValueError will be returned
            except ValueError:  # ValueError returned so it will be added into it
                self.poketypedex[self.poketypedex.index(None)] = pokemon.get_poketype()

    def get_pokedex_completion(self) -> float:
        """
        This will calculate poketypedex completion

        Returns: float of the percentage completed

        Complexity:
            Best case is O(1) when there are no nothing inside poketypedex
            Worst case is O(n) when the poketypedex is full
        """
        count = 0
        for x in self.poketypedex:
            if x is not None:
                count += 1
            else:
                break
        return round((count / len(self.poketypedex)), 2)

    def __str__(self) -> str:
        """
        This will return a string representation of the Trainer class

        Returns: a string representing the Class

        Complexity: O(1)
        """
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"

if __name__ == '__main__':
    pass
