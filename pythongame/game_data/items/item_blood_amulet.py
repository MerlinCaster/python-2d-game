import random

from pythongame.core.common import ItemType, Sprite
from pythongame.core.damage_interactions import player_receive_healing
from pythongame.core.game_data import UiIconSprite, register_ui_icon_sprite_path, register_item_data, ItemData, \
    register_entity_sprite_initializer, ITEM_ENTITY_SIZE
from pythongame.core.game_state import Event, EnemyDiedEvent, GameState
from pythongame.core.item_effects import register_item_effect, AbstractItemEffect
from pythongame.core.item_inventory import ItemEquipmentCategory
from pythongame.core.view.image_loading import SpriteInitializer

ITEM_TYPE = ItemType.BLOOD_AMULET
HEALTH_ON_KILL_AMOUNT = 5
PROC_CHANCE = 0.3


class ItemEffect(AbstractItemEffect):

    def __init__(self, item_type: ItemType):
        super().__init__(item_type)

    def item_handle_event(self, event: Event, game_state: GameState):
        if isinstance(event, EnemyDiedEvent):
            if random.random() < PROC_CHANCE:
                player_receive_healing(HEALTH_ON_KILL_AMOUNT, game_state)


def register_blood_amulet():
    ui_icon_sprite = UiIconSprite.ITEM_BLOOD_AMULET
    sprite = Sprite.ITEM_BLOOD_AMULET
    image_file_path = "resources/graphics/item_blood_amulet.png"
    register_ui_icon_sprite_path(ui_icon_sprite, image_file_path)
    register_entity_sprite_initializer(sprite, SpriteInitializer(image_file_path, ITEM_ENTITY_SIZE))
    register_item_effect(ITEM_TYPE, ItemEffect(ITEM_TYPE))
    name = "Blood Amulet"
    description = [str(int(PROC_CHANCE * 100)) + "% on kill: gain " + str(HEALTH_ON_KILL_AMOUNT) + " health"]
    item_data = ItemData(ui_icon_sprite, sprite, name, description, ItemEquipmentCategory.NECK)
    register_item_data(ITEM_TYPE, item_data)
