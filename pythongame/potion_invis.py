from pythongame.buffs import AbstractBuff, register_buff_effect
from pythongame.common import PotionType, BuffType, Millis
from pythongame.game_data import register_ui_icon_sprite_path, UiIconSprite, register_potion_icon_sprite, \
    register_buff_text
from pythongame.game_state import GameState
from pythongame.potions import create_potion_visual_effect_at_player, PotionWasConsumed, register_potion_effect
from pythongame.visual_effects import VisualRect


def _apply_invis(game_state: GameState):
    create_potion_visual_effect_at_player(game_state)
    game_state.player_state.gain_buff(BuffType.INVISIBILITY, Millis(5000))
    return PotionWasConsumed()


class Invisibility(AbstractBuff):
    def __init__(self):
        self._time_since_graphics = 0

    def apply_start_effect(self, game_state: GameState):
        game_state.player_state.is_invisible = True

    def apply_middle_effect(self, game_state: GameState, time_passed: Millis):
        self._time_since_graphics += time_passed
        if self._time_since_graphics > 320:
            self._time_since_graphics = 0
            game_state.visual_effects.append(
                VisualRect((0, 0, 250), game_state.player_entity.get_center_position(), 60, Millis(400),
                           game_state.player_entity))

    def apply_end_effect(self, game_state: GameState):
        game_state.player_state.is_invisible = False


def register_invis_potion():
    register_potion_effect(PotionType.INVISIBILITY, _apply_invis)
    register_buff_effect(BuffType.INVISIBILITY, Invisibility())
    register_buff_text(BuffType.INVISIBILITY, "Invisibility")
    register_potion_icon_sprite(PotionType.INVISIBILITY, UiIconSprite.INVISIBILITY_POTION)
    register_ui_icon_sprite_path(UiIconSprite.INVISIBILITY_POTION, "resources/invis_potion.png")
