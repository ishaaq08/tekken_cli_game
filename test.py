"""
Imports:
    > inquirer - Collection of common interactive command-line interfaces
    > colored - Alter the colour and attributes of text
    > math - Perform mathematical operations on numerical data types
    > time - 
"""
import inquirer
from termcolor import colored, cprint
import math
import time

class Player():
    """
    Purpose:

        > Definition of player class.
        > Each character created will be an instance of the player class thus acquiring the attributes specified in the Player class
          definition

    Methods:

        > __str__: Returns a human-readable string representation of an object. Without this attribute calling the object will return the
          the class and object id in hexadecimal format which is not useful.
        > select_attack: Enables the user to select which attack, an attribute of the object, they wish to fight with.
        > update_health: After a round has concluded this method calculates the new health of the fighters after opponent attack damage
          has been accounted for.
    """

    def __init__(self, name, health, moves):
    
        self.name = name
        self.health = health
        self.moves = moves

    """
    Purpose:

        > Define the friendly user-friendly representation of an object
        > Otherwise the class and object id would be outputted in hexadecimal form.

    Arguments:

        > self: Allows the method to access the instance/object's properties/attributes

    Returns:

        > The name attribute of the object.
    """
    def __str__(self):
        return f"{self.name}"

    def select_attack(self, opponent):
        """
        Purpose:

            > Produces a prompt enabling the user to select using arrows key from a drop.

        Arguments:

            > self: Allows the method to access the instance/object's properties/attributes
            > opponent: The object associated with player 2's character

        Returns:

            > The damage associated with the characters attack is returned - this value is accessed from the moves attribute of the 
              object which is a dictionary
            > This is used to reduce the opponents health accordingly.
        """

        all_moves = list(self.moves.keys())
        questions = [
            inquirer.List(
                "attack",
                message="Select an attack",
                choices=[all_moves[0], all_moves[1], all_moves[2]],
            ),
        ]

        answers = inquirer.prompt(questions)

        attack = answers["attack"]

        print(colored((f"{self.name} {attack}'s {opponent}!"), "green", attrs=["blink"]))
        print(colored((f"{opponent} incurs a damage of {self.moves[attack]}"), "red", attrs=["bold"]))

        return self.moves[attack]
    
    
    def update_health(self, damage_taken):
        """
        Purpose:

            > Updates and returns the characters health as a number and health bar represented by hashtags
            > Relies on the colored library to print the health bar in green and red - hashtags are green representing life, red 
              hyphens representing lossed life.
            > Relies on the math library to round down the health value for the health bar.
            
        Arguments:

            > self: Allows the method to access the instance/object's properties/attributes
            > damage_taken: Type Integer. Essentially the damage associated with the opponents attack.

        Returns:

            > Nothing is returned - the function directly updates the health attribute of the instance and prints the updated health.
        """
        self.health = self.health - damage_taken
        filled_blocks = "#"*(math.floor(self.health)//10)
        empty_blocks = "-"*(math.ceil(100-self.health)//10)
        print(f"{self.name} Health: [{colored(filled_blocks, "green")}{colored(empty_blocks, "red")}] {str(self.health)}/100")

def select_player(player_name, players_dict):
    """
    Purpose: 
    
        > Enables the user to use the arrow keys to select a character from a list of characters.
        > Selection from a drop down list is facilitated by the 'inquirer' library.
        > The users selection is stored as the value of the dictionary called answers, in which the key is defined as 'player'.
        > The value associated with this key is a characters name. 
        > This name is then used to access the associated key contained in the players_dict dictionary.
        > This then gives the user the access to the relevant player object allowing them to use the character's moves

    Arguments:

        > player_name: This will be either player 1 or 2 depending on in what number the function is invoked
        > player_dict: As defined and returned by the initialize_players() function. 

    Returns:

        > Returns a player object from the players_dict dictionary.
    """

    questions = [
    inquirer.List(
        "player",
        message=f"{player_name} - Select a player",
        choices=list(players_dict.keys()),
    ),
]

    answers = inquirer.prompt(questions)
    return players_dict[answers["player"]]

# # Creating 4 players

def initialize_players():
    """
    Purpose: 
    
        > Instantiates the Player(name, health, moves) class to create 4 player objects
        > moves: defined as a dictionary in which the 'key' is the name of the move and the 'value' is the damage incurred

    Arguments:

        > No arguments required.
    Returns:
        
        > players_dict : Key = Name of player, Value = Reference to the player object
    """

    player_1 = Player("Jin Kazama", 100, {"Punch": 20,\
                                        "Kick": 20,\
                                        "Slap": 20})

    player_2 = Player("Kazuya Mishima", 100, {"Spinning Kick": 40,\
                                            "Upper Cut": 15,\
                                            "Roundhouse Kick": 50})

    player_3 = Player("Heihachi Mishima", 100, {"Atomic Drop": 30,\
                                                "Crouching Dragon Kick": 20,\
                                                "Lightning Hammer": 40})

    player_4 = Player("Eddy Gordo", 100, {"Knee Slicer": 20,\
                                        "Lunging Brush Fire": 30,\
                                            "Perch Flop Kick": 25})
    
    players_dict = {
    "Jin Kazama": player_1,
    "Kazuya Mishima": player_2,
    "Heihachi Mishima": player_3,
    "Eddy Gordo": player_4}
    
    return players_dict

def fight():
    """
    Purpose:

        > Main function invoking above functions.
        > Commences the game, requiring users to select characters and move. 
        > The game is stored in a while loop, repeating until one of the characters health is below 0.

    Arguments:

        > No arguments required.

    Returns:

        > No returns.
        > The main outputs of this argument are print statements.
    """
    players_dict = initialize_players()

    user_1 = select_player("Player 1", players_dict)
    user_2 = select_player("Player 2", players_dict)

    print(f"\n P1: {user_1} vs P2: {user_2}")

    round = 1

    """
    > This loop enables the game to continue so as long as one of the characters health isn't below or equal to 0.
    """

    while user_1.health > 0 and user_2.health > 0:
        print(colored((f"\nFIGHT ROUND {round}"), attrs=["underline"]))
        print("\nPlayer 1 - GET READY TO FIGHT!!!")

        for x in range(0,3):
            print(colored(("."), "yellow", attrs=["bold"]), end = " ", flush=True)
            time.sleep(2)

        damage_to_user_2 = user_1.select_attack(opponent=user_2)
        print("\nPlayer 2 - GET READY TO FIGHT!!!")
        damage_to_user_1 = user_2.select_attack(opponent=user_1)

        if user_1.health > 0 and user_2.health > 0:
            print(colored(("\nHEALTH UPDATE"), "red", "on_yellow"))
            user_1.update_health(damage_to_user_1)
            user_2.update_health(damage_to_user_2)
            round += 1

    """
    > To dictate the winner the program compares the health and the character with the greater health wins.
    """

    if user_1.health > user_2.health:
        print(f"\n{user_1.name} wins !!!!")
    else:
        print(f"\n{user_2.name} wins !!!!")


    """
    > The following statements enable the user the freedom of selecting whether they would like to restart.
    > The variable restart is initially assigned a value of None to ensure the program enters the while loop.
    > The conditional statements detect 3 inputs from the user, "Y/y", "N/n" or anything else, causing the game to restart, end or 
      demand the user to input either y or n respectively.
    """
    
    restart = None
    while restart == None:
        restart = input("Would you like to play again. Please Type in either Y/y or N/n: ")
        if restart.lower() == "y":
            fight()
        elif restart.lower() == "n":
            print("\nThank you for your time. We hope you enjoyed!")
        else:
            restart = None
        
fight()
