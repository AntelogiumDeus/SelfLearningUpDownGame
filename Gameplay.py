import arcade
from players import PlayerCharacter
import os

#seluruh mapnya 2x
WIDTH = 16 * 2 * 30
HEIGTH = 16 * 2 * 20
TITLE = 'Multiple Screen'

#constant
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
Sound_bg = os.path.join(FILE_PATH,'Assets',"HarvestOst.mp3")

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.sound = arcade.load_sound("Assets/HarvestOst.mp3")
        arcade.play_sound(self.sound, looping=True, volume=0.1)
        self.logo = None
        self.text = ""
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.WHITE)
    def setup(self):
        self.logo = arcade.load_texture('Assets/Title.png')
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(WIDTH/2, (HEIGTH/2) + 170, 250,200, self.logo)
        arcade.draw_text("Start Screen", WIDTH/2, HEIGTH/2, arcade.csscolor.BLACK, font_size=35, anchor_x='center')
        arcade.draw_text("Click here to continue", WIDTH/2, (HEIGTH/2) - 50 , arcade.csscolor.BLACK, font_size=15, anchor_x='center')
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        #object for gamescreen
        Gameview = GameScreen()
        Gameview.setup()
        self.window.show_view(Gameview)

#Class window GameScreen()
class GameScreen(arcade.View):

    def __init__(self):
        super().__init__()
        self.wall = None
        self.home = None
        self.stone = None
        self.items = None
        self.trees = None
        self.apples = None
        self.ground = None
        self.gameMaps = None

        #add the player
        self.player = None
        self.players = None
        self.movement = None

        #total
        self.total_item = 0

        #movement
        self.left_pressed = None
        self.right_pressed = None
        self.up_pressed = None
        self.down_pressed = None
        self.collect = None

        #physic_engine
        self.physic_engine_with_home = None
        self.physic_engine_with_trees = None
        self.physic_engine_with_walls = None
        self.physic_engine_with_stones = None
        self.physic_engine_with_items = None


        #multiple room
        self.current_room = 0
        self.rooms = None

    def setup(self):

        self.gameMaps = arcade.load_tilemap('Maps.JSON', scaling=2)
        self.ground = self.gameMaps.sprite_lists['Ground']
        self.flowers = self.gameMaps.sprite_lists['Flowers']
        self.house = self.gameMaps.sprite_lists['House']
        self.door_house = self.gameMaps.sprite_lists['Door']
        self.house2 = self.gameMaps.sprite_lists['House2']
        self.trees = self.gameMaps.sprite_lists['Trees']
        self.stones = self.gameMaps.sprite_lists['Stones']
        self.apples = self.gameMaps.sprite_lists['Apples']
        self.items = self.gameMaps.sprite_lists['Items']
        self.chicken = self.gameMaps.sprite_lists['Chicken']
        self.wall = self.gameMaps.sprite_lists['Wall']

        #setup player character
        self.players = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.player.center_x = WIDTH // 2
        self.player.center_y = HEIGTH // 2
        self.player.scale = 0.4
        self.players.append(self.player)


        #Collision Player with House
        self.physic_engine_with_home = arcade.PhysicsEngineSimple(
            self.player,
            [self.house,self.house2,self.trees,self.stones,self.wall]
        )






    def on_update(self, delta_time: float):
        self.players.update()
        self.players.update_animation()
        self.physic_engine_with_home.update()
        self.player.change_x = 0
        self.player.change_y = 0
        #condition to move
        if self.left_pressed :
            self.player.change_x = -3
        if self.right_pressed:
            self.player.change_x = 3
        if self.up_pressed:
            self.player.change_y = 3
        if self.down_pressed:
            self.player.change_y = -3
        #collision with items
        collect_item = arcade.check_for_collision_with_list(
            self.player,
            self.items
        )

        if collect_item and self.collect == True:
            for item in collect_item:
                item.remove_from_sprite_lists()

        collide_door = arcade.check_for_collision_with_list(
            self.player,
            self.door_house
        )

        if collide_door:
            print("collide with door")
            Gameview = GameScreen_Interior()
            Gameview.setup()
            self.window.show_view(Gameview)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.E:
            self.collect = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.E:
            self.collect = False

    def on_draw(self):

        self.clear()
        self.ground.draw()
        self.flowers.draw()
        self.house.draw()
        self.house2.draw()
        self.trees.draw()
        self.stones.draw()
        self.apples.draw()
        self.items.draw()
        self.door_house.draw()
        self.chicken.draw()
        self.wall.draw()
        self.players.draw()


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        #object for gameover
        Gameview = GameOverScreen()
        self.window.show_view(Gameview)


class GameScreen_Interior(arcade.View):
    def __init__(self):
        super().__init__()
        #movement
        self.left_pressed = None
        self.right_pressed = None
        self.up_pressed = None
        self.down_pressed = None
        self.collect = None

        #collision interior
        self.collide_wall_interior = None
        self.collide_mattress_interior = None
        self.collide_props_interior = None


    def setup(self):
        self.gameMaps2 = arcade.load_tilemap('Map_House1.json', scaling=2)
        self.ground2 = self.gameMaps2.sprite_lists['Ground']
        self.wall2 = self.gameMaps2.sprite_lists['Wall']
        self.window2 = self.gameMaps2.sprite_lists['Window']
        self.props = self.gameMaps2.sprite_lists['Props']
        self.door2 = self.gameMaps2.sprite_lists['House1_IN']
        self.mattress2 = self.gameMaps2.sprite_lists['Mattress']
        self.exit = self.gameMaps2.sprite_lists['Exit']


        self.players = arcade.SpriteList()
        self.player = PlayerCharacter()
        self.player.center_x = WIDTH // 4 + 50
        self.player.center_y = HEIGTH // 5 + 40
        self.player.scale = 0.4
        self.players.append(self.player)

        #Collide with interior
        self.collide_wall_interior = arcade.PhysicsEngineSimple(
            self.player,
            [self.wall2,self.mattress2, self.props]
        )


    def on_draw(self):
        self.clear()
        self.ground2.draw()
        self.wall2.draw()
        self.window2.draw()
        self.door2.draw()
        self.mattress2.draw()
        self.props.draw()
        self.exit.draw()
        self.players.draw()

    def on_update(self, delta_time: float):
        self.players.update()
        self.players.update_animation()
        self.collide_wall_interior.update()
        # self.collide_mattress_interior.update()
        # self.collide_props_interior.update()
        self.player.change_x = 0
        self.player.change_y = 0
        if self.left_pressed :
            self.player.change_x = -2
        if self.right_pressed:
            self.player.change_x = 2
        if self.up_pressed:
            self.player.change_y = 2
        if self.down_pressed:
            self.player.change_y = -2

        exit_room = arcade.check_for_collision_with_list(
            self.player,
            self.exit
        )
        if exit_room:
            gameview = GameScreen()
            gameview.setup()
            self.window.show_view(gameview)





    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.E:
            self.collect = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.E:
            self.collect = False




class GameOverScreen(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_RED)
    def on_draw(self):
        self.clear()
        arcade.draw_text("Game Over", WIDTH/2, HEIGTH/2, arcade.csscolor.WHITE, font_size=35, anchor_x='center')
        arcade.draw_text("(R) Restart, (Q) Quit", WIDTH/2, (HEIGTH/2) - 50, arcade.csscolor.WHITE, font_size=15, anchor_x='center')
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            #object
            gameview = GameScreen()
            gameview.setup()
            self.window.show_view(gameview)
        if symbol == arcade.key.Q:
            self.window.show_view(Confirm_Screen())

class Confirm_Screen(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Are you sure want to Quit?", WIDTH/2, (HEIGTH/2), arcade.csscolor.BLACK, font_size=35, anchor_x='center' )
        arcade.draw_text("(Y) Quit, (N) No", WIDTH/2, (HEIGTH/2) - 50, arcade.csscolor.BLACK, font_size=15, anchor_x='center' )
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Y:
            arcade.close_window()
        if symbol ==  arcade.key.N:
            self.window.show_view(GameOverScreen())

#define function
def main():
    window = arcade.Window(WIDTH,HEIGTH,TITLE)
    Gameview = StartScreen()
    Gameview.setup()
    window.show_view(Gameview)
    arcade.run()

main()