import random

from pythongame.core.ability_effects import register_ability_effect
from pythongame.core.buff_effects import get_buff_effect, AbstractBuffEffect, register_buff_effect
from pythongame.core.common import AbilityType, Millis, BuffType, UiIconSprite
from pythongame.core.damage_interactions import deal_player_damage_to_enemy
from pythongame.core.game_data import register_ability_data, AbilityData, register_ui_icon_sprite_path, \
    register_buff_text
from pythongame.core.game_state import GameState, WorldEntity, NonPlayerCharacter
from pythongame.core.visual_effects import VisualRect, VisualCircle

STUN_DURATION = Millis(3500)
CHANNELING_STOMP = BuffType.CHANNELING_STOMP
STUNNED_BY_STOMP = BuffType.STUNNED_BY_STOMP

MIN_DMG = 6
MAX_DMG = 8


def _apply_ability(game_state: GameState) -> bool:
    game_state.player_state.gain_buff_effect(get_buff_effect(CHANNELING_STOMP), Millis(500))
    return True


class ChannelingStomp(AbstractBuffEffect):

    def __init__(self):
        self.time_since_graphics = 0
        self.graphics_size = 40

    def apply_start_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        game_state.player_state.add_stun()
        game_state.player_entity.set_not_moving()

    def apply_middle_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter,
                            time_passed: Millis) -> bool:

        self.time_since_graphics += time_passed

        if self.time_since_graphics > 80:
            self.time_since_graphics = 0
            visual_effect = VisualCircle(
                (250, 250, 250), buffed_entity.get_center_position(), self.graphics_size, self.graphics_size + 10,
                Millis(70), 2, None)
            self.graphics_size -= 7
            game_state.visual_effects.append(visual_effect)
        return False

    def apply_end_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        game_state.player_state.remove_stun()
        hero_center_pos = game_state.player_entity.get_center_position()
        distance = 80
        affected_enemies = game_state.get_enemies_within_x_y_distance_of(distance, hero_center_pos)
        game_state.visual_effects.append(
            VisualRect((50, 50, 50), hero_center_pos, distance * 2, int(distance * 2.1), Millis(200), 2, None))
        game_state.visual_effects.append(
            VisualRect((150, 150, 0), hero_center_pos, distance, distance * 2, Millis(150), 3, None))
        game_state.visual_effects.append(
            VisualRect((250, 250, 0), hero_center_pos, distance, distance * 2, Millis(100), 4, None))
        for enemy in affected_enemies:
            damage: float = MIN_DMG + random.random() * (MAX_DMG - MIN_DMG)
            deal_player_damage_to_enemy(game_state, enemy, damage)
            enemy.gain_buff_effect(get_buff_effect(STUNNED_BY_STOMP), STUN_DURATION)
        game_state.player_state.gain_buff_effect(get_buff_effect(BuffType.RECOVERING_AFTER_ABILITY), Millis(300))

    def get_buff_type(self):
        return CHANNELING_STOMP


class StunnedFromStomp(AbstractBuffEffect):

    def apply_start_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        buffed_npc.add_stun()
        buffed_entity.set_not_moving()

    def apply_end_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        buffed_npc.remove_stun()

    def get_buff_type(self):
        return STUNNED_BY_STOMP


def register_stomp_ability():
    ability_type = AbilityType.STOMP
    ui_icon_sprite = UiIconSprite.ABILITY_STOMP

    register_ability_effect(ability_type, _apply_ability)
    description = "Damages and stuns enemies around you (" + str(MIN_DMG) + "-" + str(MAX_DMG) + ")"
    register_ability_data(
        ability_type,
        AbilityData("War Stomp", ui_icon_sprite, 12, Millis(7000), description, None))
    register_ui_icon_sprite_path(ui_icon_sprite, "resources/graphics/warstomp_icon.png")
    register_buff_effect(CHANNELING_STOMP, ChannelingStomp)
    register_buff_text(CHANNELING_STOMP, "Channeling")
    register_buff_effect(STUNNED_BY_STOMP, StunnedFromStomp)