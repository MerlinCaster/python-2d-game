from pythongame.core.buff_effects import AbstractBuffEffect, get_buff_effect, register_buff_effect
from pythongame.core.common import ItemType, Sprite, BuffType, Millis, HeroStat
from pythongame.core.game_data import UiIconSprite
from pythongame.core.game_state import Event, GameState, WorldEntity, \
    NonPlayerCharacter, PlayerBlockedEvent
from pythongame.core.item_effects import StatModifyingItemEffect
from pythongame.core.item_inventory import ItemEquipmentCategory
from pythongame.core.visual_effects import VisualCircle, create_visual_stun_text
from pythongame.game_data.items.register_items_util import register_custom_effect_item

STUN_DURATION = Millis(2500)

BUFF_TYPE_STUNNED = BuffType.STUNNED_BY_AEGIS_ITEM


class ItemEffect(StatModifyingItemEffect):

    def __init__(self, item_type: ItemType, stat_modifiers):
        super().__init__(item_type, stat_modifiers)

    def item_handle_event(self, event: Event, game_state: GameState):
        if isinstance(event, PlayerBlockedEvent):
            event.npc_attacker.gain_buff_effect(get_buff_effect(BUFF_TYPE_STUNNED), STUN_DURATION)

    def get_description(self):
        return super().get_description() + \
               ["On block: stun attacker for " + "{:.1f}".format(STUN_DURATION / 1000) + "s"]


class StunnedFromAegis(AbstractBuffEffect):

    def apply_start_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        visual_effect = VisualCircle((220, 220, 50), buffed_entity.get_center_position(), 9, 16, Millis(250), 2)
        game_state.visual_effects.append(visual_effect)
        game_state.visual_effects.append(create_visual_stun_text(buffed_entity))
        buffed_npc.stun_status.add_one()
        buffed_entity.set_not_moving()

    def apply_end_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        buffed_npc.stun_status.remove_one()

    def get_buff_type(self):
        return BUFF_TYPE_STUNNED


def register_zuls_aegis():
    register_buff_effect(BUFF_TYPE_STUNNED, StunnedFromAegis)

    item_type = ItemType.ZULS_AEGIS
    effect = ItemEffect(item_type, {HeroStat.ARMOR: 3, HeroStat.BLOCK_AMOUNT: 8})
    register_custom_effect_item(
        item_type=item_type,
        ui_icon_sprite=UiIconSprite.ITEM_ZULS_AEGIS,
        sprite=Sprite.ITEM_ZULS_AEGIS,
        image_file_path="resources/graphics/item_zuls_aegis.png",
        item_equipment_category=ItemEquipmentCategory.OFF_HAND,
        name="Zul's Aegis",
        item_effect=effect
    )
