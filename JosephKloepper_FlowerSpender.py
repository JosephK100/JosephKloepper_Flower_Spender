#Joseph Kloepper
#11/25/25
#CS - 100 (Final Game)
#The idea is to play a flower gardener type game, where you click for points.
#As you gain points, you hit milestones and unlock new flower colors.

import simpleGE, pygame, random

def random_color(score):
    """
    Generates a random flower based on the player's score.
    My random_color function unlocks new color palettes at specific score milestones (30, 60, 90, 120)
    Basic RGB colors are always an option.
    From 30 points on up pastels are added to the mix.
    From 60 on up neon colors are added.
    From 90 on up the more earthy colors are added.
    From 120 on up I added "rare" colors, which is really just silver, gold, and purple.
    Uses the player's score to determine what colors can be generated and returns an RGB from the unlocked colors.
    """
    #I used a list to hold the unlockable colors.
    choices = []

    #Basic colors (Always available)
    choices.append((random.randint(0,255),
                    random.randint(0,255),
                    random.randint(0,255)))

    #Pastel colors - unlocked at 30.
    if score >= 30:
        choices.append((random.randint(100,255),
                        random.randint(100,255),
                        random.randint(100,255)))

    #Neon colors - unlocked at 60.
    if score >= 60:
        neon_choices = [
            (255,0,255), (0,255,255), (255,255,0), (0,255,0),
            (255,128,0), (0,128,255), (255,0,128)
        ]
        choices.append(random.choice(neon_choices))

    #Earthy colors - unlocked at 90.
    if score >= 90:
        earth_choices = [
            (139,69,19),
            (160,82,45),
            (210,180,140),
            (34,139,34)
        ]
        choices.append(random.choice(earth_choices))

    #"Rare colors" - unlocked at 120.
    if score >= 120:
        rare_choices = [
            (255,215,0),
            (192,192,192),
            (128,0,128)
        ]
        choices.append(random.choice(rare_choices))

    return random.choice(choices)


class Intro(simpleGE.Scene):
    """
    Here is the intro scene for my flower garden simulator.
    It's fairly basic, it displays the game instructions, play, and exit buttons.
    """
    def __init__(self):
        super().__init__()

        #Title/Instructions.
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
            "~Flower Garden Simulator~",
            "Click anywhere to plant new flowers.",
            "Earn points to unlock rarer colors.",
            "Click Play to start or Exit to quit."
        ]
        self.instructions.center = (320, 100)
        self.instructions.size = (560, 200)
        self.instructions.bgColor = (173, 216, 230)
        self.instructions.fgColor = (0, 100, 0)

        #Play button.
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (320, 250)

        #Exit button.
        self.btnExit = simpleGE.Button()
        self.btnExit.text = "Exit"
        self.btnExit.center = (320, 300)

        #Add UI elements to the intro screen.
        self.sprites = [self.instructions, self.btnPlay, self.btnExit]
        self.status = None
        
        
    def update(self):
        """
        Handles button clicks in the intro scene.
        If the user presses "play" - Go to the game scene.
        If the user presses "exit" - Close the game.
        """
        if self.btnPlay.clicked:
            self.status = "play"
            self.stop()
        if self.btnExit.clicked:
            self.status = "exit"
            self.stop()


class Game(simpleGE.Scene):
    """
    Here's the main function for my game.
    It sets the background.
    Shows and tracks the player's score.
    Plants the "flowers."
    Displays the unlock notifications when the player reaches a milestone.
    Resets the score. (Was originally meant to clear the garden.)
    Contains the placeholder store button.
    """
    def __init__(self):
        super().__init__()
        self.setImage("environment_forestbackground1-1.png") 
        
        
        #Label for user score.
        self.score = 0
        self.scoreLabel = simpleGE.Label()
        self.scoreLabel.text = "Score: 0"
        self.scoreLabel.center = (80, 20)
        

        #Store button. (It's currently just for show)
        self.btnStore = simpleGE.Button()
        self.btnStore.text = "Store"
        self.btnStore.center = (555, 20)
        self.btnStore.bgColor = (173, 216, 230)


        #Sizing and position for the inital flower 
        self.flower_color = random_color(self.score)
        self.flower_pos = (320, 240)
        self.flower_radius = 15

        #Here's my mini label that notifies the user when they unlock new colors or reset the score counter.        
        self.unlockLabel = simpleGE.Label()
        self.unlockLabel.text = ""
        self.unlockLabel.center = (520, 460)
        self.unlockLabel.size = (250, 30)
        self.sprites.append(self.unlockLabel)
        
        #Reset button. 
        self.btnReset = simpleGE.Button()
        self.btnReset.text = "Reset"
        self.btnReset.center = (555, 80)
        self.btnReset.bgColor = (173, 216, 230)
        
        #Add UI elements.
        self.sprites = [self.scoreLabel, self.btnStore, self.btnReset, self.unlockLabel]
        

    
    def update(self):
        """
        Main update loop for the game scene.
        It lets the user know if the store button was pressed.
        Manages the unlock notifications when score milestones are hit.
        Manages the reset button to clear the score.
        Draws the flowers onto the scene.
        """
        if self.btnStore.clicked:
            print("Store button pressed")
        
        
        #Generates a flower when the user presses the left-clicks.
        if pygame.mouse.get_pressed()[0]:
            #Add 1 point per click.
            self.score += 1
            self.scoreLabel.text = f"Score: {self.score}"
            #New random color + location
            self.flower_color = random_color(self.score)
            self.flower_pos = (random.randint(50, 590), random.randint(100, 430))
            #I added a small pause between clicks.
            pygame.time.wait(200)
        
        if self.score == 30:
            self.unlockLabel.text = "Unlocked pastel flowers!"
        if self.score == 60:
            self.unlockLabel.text = "Unlocked neon flowers!"
        if self.score == 90:
            self.unlockLabel.text = "Unlocked earth flowers!"
        if self.score == 120:
            self.unlockLabel.text = "Unlocked rare flowers!"
        
        if self.btnReset.clicked:
            self.score = 0
            self.scoreLabel.text = "Score: 0"
            self.unlockLabel.text = "~Score Cleared~"
            return

        #Drawing the flower
        pygame.draw.circle(self.screen, self.flower_color, self.flower_pos, self.flower_radius,)


def main():
    """
    Main loop for the game.
    It shows the intro scene.
    Can transfer the player to the game scene.
    If play is selected, move to game scene.
    If exit is selected, close the game.
    """
    keepGoing = True
    while keepGoing:
        intro = Intro()
        intro.start()
        if intro.status == "play":
            garden = Game()
            garden.start()
        else:
            keepGoing = False

if __name__ == "__main__":
    main()