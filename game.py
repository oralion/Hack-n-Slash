from monsters import Dragon, Goblin, Troll
from character import Character
import sys
import os


class Game:

    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def setup(self):
        self.player = Character()
        self.monsters = [
            Goblin(),
            Troll(),
            Dragon()
        ]
        self.monster = self.get_next_monster()

    def get_next_monster(self):
        try:
            return self.monsters.pop(0)
        except IndexError:
            return None

    def cleanup(self):
        if self.monster.hit_points <= 0:
            self.player.experience += self.monster.experience
            print("You killed {}".format(self.monster))
            self.monster = self.get_next_monster()

    def monster_turn(self):
        if self.monster.attack():
            if input("Dodge? Y/n ").lower() != "y":
                if self.player.dodge():
                    print("You have dodged the attack!")
                else:
                    self.player.hit_points -= 1
                    print("You failed to dodge. You lose 1 HP".format(self.monster))
            else:
                self.player.hit_points -= 1
                print("{} has hit you, you lose 1 HP".format(self.monster))
        else:
            print("{} fails his attack".format(self.monster))

    def player_turn(self):
        player_choice = input("[A]ttack, [R]est, [Q]uit? ").lower()
        if player_choice in "arq":
            if player_choice == "a":
                if self.player.attack():
                    print("You are attacking {}".format(self.monster))
                    if self.monster.dodge():
                        print("{} has dodged your attack!".format(self.monster))
                    else:
                        if self.player.lvl_up():
                            self.monster.hit_points -= 2
                        else:
                            self.monster.hit_points -= 1
                        print("You've hit {} with your {}".format(self.monster, self.player.weapon))
                else:
                    print("Your attack has failed")
            elif player_choice == "r":
                self.player.rest()
                print("You rested, HP:{}".format(self.player.hit_points))
            elif player_choice == "q":
                print('Goodbye')
                sys.exit()
        else:
            print("Invalid input")
            self.player_turn()

    def __init__(self):
        self.setup()

        while self.player.hit_points and (self.monster or self.monsters):
            print("\n"+"="*20)
            print(self.player)
            self.monster_turn()
            print("-"*20)
            self.player_turn()
            print("\n" + "=" * 20)
            self.cleanup()

        if self.player.hit_points:
            print("You win!")
        elif self.monsters or self.monster:
            print("You lose!")

        sys.exit()

Game()
