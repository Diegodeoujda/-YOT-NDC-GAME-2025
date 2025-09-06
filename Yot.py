import pyxel
from random import *


"""self.world = World()
        self.player = Player()ds
        self.enemy = Enemy()
        self.deathscreen = DeathScreen()"""


class GameObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.speed = 1
        self.sprint_speed = 4

        self.top = True
        self.bot = False
        self.right = False
        self.left = False

        self.sprint = False
        self.walk = True
        self.isColide = False

    def colision(self, other):
        ax = self.getX() + 8
        ay = self.getY() + 8
        bx = other.getX() + 8
        by = other.getY() + 8

        return (abs(ax - bx) < 16) and (abs(ay - by) < 16)

    def move(self, up=False, down=False, left=False, right=False, sprint=False):
        self.animation()
        if self.isColide:
            return

        self.sprint = sprint
        self.walk = not sprint
        speed = self.sprint_speed if sprint else self.speed

        if up and self.y > 0:
            self.y -= speed
            self.setDirection(top=True)
        if down and self.y < 240:
            self.y += speed
            self.setDirection(bot=True)
        if left and self.x > 0:
            self.x -= speed
            self.setDirection(left=True)
        if right and self.x < 240:
            self.x += speed
            self.setDirection(right=True)

    def setDirection(self, top=False, bot=False, left=False, right=False):
        self.top = top
        self.bot = bot
        self.left = left
        self.right = right

    def animation(self):
        """
        Gere l'animation des sprites en fonction du type de déplacement
        """
        # Marche
        if self.walk:
            self.Y = 0

        # Sprint
        if self.sprint:
            self.Y = 16

        # Haut
        if self.top:
            self.X = 0

        # Bas
        if self.bot:
            self.X = 32

        # Droite
        if self.right:
            self.X = 16

        # Gauche
        if self.left:
            self.X = 48

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class World:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(0, 0, 7, 0, 0, 256, 256)


class Enemy(GameObject):
    def __init__(self, x=0, y=0, X=0, Y=32):
        super().__init__(x, y)
        self.X = X
        self.Y = Y
        self.skinList_X = [0, 16, 32, 42]

    def skinList(self):
        return self.skinList_X

    def update(self):
        # Exemple d'IA de déplacement :
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.X, self.Y, 16, 16, 8)


class ChasingEnemy(Enemy):
    def __init__(self, x=0, y=0, state=None, X=0, Y=64):
        super().__init__(x, y)
        self.X = X
        self.Y = Y
        self.speed = None
        self.gamestate = state

    def updateSpeed(self):
        if self.gamestate == 'Easy':
            self.speed = 0.25
        if self.gamestate == 'Mid':
            self.speed = 1
        if self.gamestate == 'Hard':
            self.speed = 2

    def updateChase(self, player):
        '''dx  pos =  joueur a droite
        dx  neg=  joueur a gauche
        dy pos= joueur en dessous '''

        self.updateSpeed()
        dx = player.getX() - self.getX()
        dy = player.getY() - self.getY()

        move_up = dy < 0
        move_down = dy > 0
        move_left = dx < 0
        move_right = dx > 0

        up = move_up
        down = move_down
        left = move_left
        right = move_right

        self.move(up=up, down=down, left=left, right=right)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.X, 64, 16, 16, 8)


class Game:
    def __init__(self, gameState):
        self.gameState = gameState
        self.level = gameState.getLevel()
        self.world = World()

    def update(self):
        pyxel.mouse(False)
        self.level.player.update()
        for enemy in self.level.enemies:
            if isinstance(enemy, ChasingEnemy):
                enemy.updateChase(self.level.player)
            else:
                enemy.update()
        for enemy in self.level.enemies:
            if self.level.player.colision(enemy):
                self.gameState.setState("Death")

    def draw(self):
        self.world.draw()
        self.level.draw(self.level.getDifficulty())

        if self.level.getDifficulty() == 'Easy':

            self.level.player.draw()
            for enemy in self.level.enemies:
                enemy.draw()

            pyxel.text(10, 10, "Level 1", pyxel.COLOR_WHITE)

        elif self.level.getDifficulty() == 'Mid':
            self.level.player.draw()
            for enemy in self.level.enemies:
                enemy.draw()
            pyxel.text(10, 10, "Level 2", pyxel.COLOR_WHITE)

        elif self.level.getDifficulty() == 'Hard':
            self.level.player.draw()
            for enemy in self.level.enemies:
                enemy.draw()
            pyxel.text(10, 10, "Level 3", pyxel.COLOR_WHITE)


class Player(GameObject):
    def __init__(self, x=20, y=54, X=0, Y=0):
        super().__init__(x, y)
        self.X = X
        self.Y = Y

        self.x_weapons = self.getX()
        self.y_weapons = self.getY()
        self.X_weapons = 0
        self.Y_weapons = 0

    def update(self):

        # self.tirer()

        self.move(
            up=pyxel.btn(pyxel.KEY_Z),
            down=pyxel.btn(pyxel.KEY_S),
            left=pyxel.btn(pyxel.KEY_Q),
            right=pyxel.btn(pyxel.KEY_D),
            sprint=pyxel.btn(pyxel.KEY_SHIFT)
        )

    def tirer(self):

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):

            # Yacht vers le haut
            if self.top:

                # Yachts sprint
                if self.sprint:
                    self.y_weapons -= 6

                # Yacht marche
                else:
                    self.y_weapons -= 2

            # Yacht vers le bas
            if self.bot:

                # Yachts sprint
                if self.sprint:
                    self.y_weapons += 6

                # Yacht marche
                else:
                    self.y_weapons += 2

            # Yacht vers la droite
            if self.right:

                # Yachts sprint
                if self.sprint:
                    self.x_weapons += 6

                # Yacht marche
                else:
                    self.x_weapons += 2

            # Yacht vers la gauche
            if self.left:

                # Yachts sprint
                if self.sprint:
                    self.x_weapons -= 6

                # Yacht marche
                else:
                    self.x_weapons -= 2

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.X, self.Y, 16, 16, 8)
        # pyxel.blt(self.x_weapons, self.y_weapons,0,self.X_weapons,self.Y_weapons,16,16,8)


class Level:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.enemy = None
        self.player = Player(x=128, y=128)
        self.enemies = [ChasingEnemy(0, 0, state=self.getDifficulty())]
        self.enemiesskinList_X = [0, 16, 32, 48]

        self.spawEnemies()

    def getDifficulty(self):
        return self.difficulty

    def spawEnemies(self):
        if self.difficulty == 'Easy':
            for i in range(3):
                enemy = Enemy(x=randint(20, 230), y=randint(20, 230), X=choice(self.enemiesskinList_X))
                self.enemies.append(enemy)
        elif self.difficulty == 'Mid':
            for i in range(7):
                enemy = Enemy(x=randint(20, 230), y=randint(20, 230), X=choice(self.enemiesskinList_X))
                self.enemies.append(enemy)
        elif self.difficulty == 'Hard':
            for i in range(15):
                enemy = Enemy(x=randint(20, 200), y=randint(20, 200), X=choice(self.enemiesskinList_X))
                self.enemies.append(enemy)

    def update(self, difficulty):
        pass

    def draw(self, difficulty):
        pass

    class BoatIA_Menu(GameObject):
        def __init__(self, x=20, y=20):
            super().__init__(x, y)
            self.X = 0
            self.Y = 0

        def update(self):
            '''if randint(0,4) == 1:
                self.randomSprint = True
            else:
                self.randomSprint = False'''
            if self.getX() >= 20 and self.getY() >= 20:
                self.move(up=False, down=True, left=False, right=False)

        def draw(self):
            pyxel.blt(self.x, self.y, 0, self.X, self.Y, 16, 16, 8)


class AImenu(GameObject):
    def __init__(self, x=30, y=30, X=0, Y=0):
        super().__init__(x, y)
        self.X = X
        self.Y = Y
        self.speed = 3
        self.phase = 0

    def update(self):
        if self.phase == 0:
            self.move(down=True)
            if self.getY() >= 220:
                self.phase = 1

        elif self.phase == 1:
            self.move(right=True)
            if self.getX() >= 220:
                self.phase = 2

        elif self.phase == 2:
            self.move(up=True)
            if self.getY() <= 30:
                self.phase = 3

        elif self.phase == 3:
            self.move(left=True)
            if self.getX() <= 30:
                self.phase = 0

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.X, 64, 16, 16, 8)


class Menu:
    def __init__(self, gameState):

        self.gameState = gameState
        self.quit = False

        self.level1_button_x = 20
        self.level1_button_y = 80

        self.level2_button_x = 170
        self.level2_button_y = 80

        self.level3_button_x = 100
        self.level3_button_y = 170

        self.level_button_X = 0
        self.level_button_Y = 48

        self.quit_button_x = 10
        self.quit_button_y = 230
        self.button_width = 40
        self.button_height = 25

        self.selectedLvl = 0

        self.selectedLvl_X = 64
        self.selectedLvl_Y = 48

        self.AImenu_enemy1 = AImenu()
        self.AImenu_enemy2 = AImenu(y=90)
        self.AImenu_enemy3 = AImenu(y=150)

        self.frameCounter = 0

    def update(self):
        pyxel.mouse(True)

        self.AImenu_enemy1.update()
        self.AImenu_enemy2.update()
        self.AImenu_enemy3.update()

        mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
        if (self.level1_button_x <= mouse_x <= self.level1_button_x + self.button_width and
                self.level1_button_y <= mouse_y <= self.level1_button_y + self.button_height):
            self.selectedLvl = 1

        elif (self.level2_button_x <= mouse_x <= self.level2_button_x + self.button_width and
              self.level2_button_y <= mouse_y <= self.level2_button_y + self.button_height):
            self.selectedLvl = 2



        elif (self.level3_button_x <= mouse_x <= self.level3_button_x + self.button_width and
              self.level3_button_y <= mouse_y <= self.level3_button_y + self.button_height):
            self.selectedLvl = 3

        elif (self.quit_button_x <= mouse_x <= self.quit_button_x + self.button_width and
              self.quit_button_y <= mouse_y <= self.quit_button_y + self.button_height):
            self.selectedLvl = 4

        else:
            self.selectedLvl = 0

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if (self.level1_button_x <= mouse_x <= self.level1_button_x + self.button_width and
                    self.level1_button_y <= mouse_y <= self.level1_button_y + self.button_height):
                level1 = Level("Easy")
                self.gameState.setLevel(level1)
                self.gameState.setState("Play")

            if (self.level2_button_x <= mouse_x <= self.level2_button_x + self.button_width and
                    self.level2_button_y <= mouse_y <= self.level2_button_y + self.button_height):
                level2 = Level("Mid")
                self.gameState.setLevel(level2)
                self.gameState.setState("Play")

            if (self.level3_button_x <= mouse_x <= self.level3_button_x + self.button_width and
                    self.level3_button_y <= mouse_y <= self.level3_button_y + self.button_height):
                level3 = Level("Hard")
                self.gameState.setLevel(level3)
                self.gameState.setState("Play")

            elif (self.quit_button_x <= mouse_x <= self.quit_button_x + self.button_width and
                  self.quit_button_y <= mouse_y <= self.quit_button_y + self.button_height):
                self.quit = True

    def draw(self):

        if self.gameState.getState() == 'Menu':
            pyxel.bltm(0, 0, 7, 0, 0, 256, 256)

            self.AImenu_enemy1.draw()
            self.AImenu_enemy2.draw()
            self.AImenu_enemy3.draw()
            pyxel.blt(88, 30, 0, 0, 80, 76, 32, 8)

            if self.selectedLvl == 1:
                pyxel.blt(self.level1_button_x, self.level1_button_y, 0, self.selectedLvl_X, self.selectedLvl_Y, 16, 16,
                          8)
                pyxel.text(self.level1_button_x + 20, self.level1_button_y + 10, "Level 1", pyxel.COLOR_YELLOW)

            else:
                pyxel.blt(self.level1_button_x, self.level1_button_y, 0, self.level_button_X, self.level_button_Y, 16,
                          16, 8)
                pyxel.text(self.level1_button_x + 20, self.level1_button_y + 10, "Level 1", pyxel.COLOR_WHITE)

            if self.selectedLvl == 2:
                pyxel.blt(self.level2_button_x, self.level2_button_y, 0, self.selectedLvl_X, self.selectedLvl_Y, 16, 16,
                          8)
                pyxel.text(self.level2_button_x + 20, self.level2_button_y + 10, "Level 2", pyxel.COLOR_YELLOW)

            else:
                pyxel.blt(self.level2_button_x, self.level2_button_y, 0, self.level_button_X, self.level_button_Y, 16,
                          16, 8)
                pyxel.text(self.level2_button_x + 20, self.level2_button_y + 10, "Level 2", pyxel.COLOR_WHITE)

            if self.selectedLvl == 3:
                pyxel.blt(self.level3_button_x, self.level3_button_y, 0, self.selectedLvl_X, self.selectedLvl_Y, 16, 16,
                          8)
                pyxel.text(self.level3_button_x + 20, self.level3_button_y + 10, "Level 3", pyxel.COLOR_YELLOW)

            else:
                pyxel.blt(self.level3_button_x, self.level3_button_y, 0, self.level_button_X, self.level_button_Y, 16,
                          16, 8)
                pyxel.text(self.level3_button_x + 20, self.level3_button_y + 10, "Level 3", pyxel.COLOR_WHITE)

            if self.selectedLvl == 4:

                pyxel.rect(self.quit_button_x, self.quit_button_y, self.button_width, self.button_height,
                           pyxel.COLOR_RED)
                pyxel.text(self.quit_button_x + 10, self.quit_button_y + 10, "Quit", pyxel.COLOR_YELLOW)

            else:

                pyxel.rect(self.quit_button_x, self.quit_button_y, self.button_width, self.button_height,
                           pyxel.COLOR_LIGHT_BLUE)
                pyxel.text(self.quit_button_x + 10, self.quit_button_y + 10, "Quit", pyxel.COLOR_WHITE)

            self.frameCounter += 1

            if self.frameCounter % 3 == 0:
                self.selectedLvl_X += 16
                if self.selectedLvl_X == 112:
                    self.selectedLvl_X = 0

                self.level_button_X += 16
                if self.level_button_X >= 48:
                    self.level_button_X = 0

        if self.quit:
            pyxel.quit()


class DeathScreen:
    def __init__(self, gamestate):
        self.quit_button_x = 85
        self.quit_button_y = 100

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.text(self.quit_button_x + 20, self.quit_button_y + 10, "Shame on YOU", pyxel.COLOR_WHITE)


class GameState:
    def __init__(self):
        self.state = 'Menu'
        self.levelState = None
        self.toDo = None
        self.updateState()

    def setState(self, state):
        self.state = state
        self.updateState()

    def getState(self):
        return self.state

    def setLevel(self, level):
        self.levelState = level

    def getLevel(self):
        return self.levelState

    def updateState(self):
        if self.state == 'Menu':
            self.toDo = Menu(self)
        elif self.state == 'Play':
            self.toDo = Game(self)
        elif self.state == 'Death':
            self.toDo = DeathScreen(self)


class Yot:
    """
    Classe principale du jeu, elle regroupe toutes les autres classes
    """
    def __init__(self):
        """
        Initie la classe game en appelant toutes les classes et fonctions
        """
        pyxel.init(256, 256, title="Yot")
        pyxel.load('ressources.pyxres')
        pyxel.playm(0, loop=True)
        self.gameState = GameState()

        pyxel.run(self.update, self.renderGame)



    def update(self):
        self.gameState.toDo.update()



    def renderGame(self):
        self.gameState.toDo.draw()




Yot()