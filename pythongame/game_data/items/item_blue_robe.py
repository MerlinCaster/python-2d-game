from pythongame.core.common import ItemType, Sprite, UiIconSprite
from pythongame.core.game_data import register_ui_icon_sprite_path, register_item_data, ItemData, \
    register_entity_sprite_initializer, SpriteInitializer, ITEM_ENTITY_SIZE
from pythongame.core.game_state import GameState
from pythongame.core.item_effects import register_item_effect, AbstractItemEffect

ITEM_TYPES = [ItemType.BLUE_ROBE_1, ItemType.BLUE_ROBE_2, ItemType.BLUE_ROBE_3]
MANA_AMOUNTS = [10, 20, 30]


class ItemEffect(AbstractItemEffect):

    def __init__(self, mana_amount: int, item_type: ItemType):
        self.mana_amount = mana_amount
        self.item_type = item_type

    def apply_start_effect(self, game_state: GameState):
        game_state.player_state.gain_max_mana(self.mana_amount)

    def apply_end_effect(self, game_state: GameState):
        game_state.player_state.lose_max_mana(self.mana_amount)

    def get_item_type(self):
        return self.item_type


def register_blue_robe_item():
    ui_icon_sprite = UiIconSprite.ITEM_BLUE_ROBE
    sprite = Sprite.ITEM_BLUE_ROBE
    register_ui_icon_sprite_path(ui_icon_sprite, "resources/graphics/item_blue_robe.png")
    register_entity_sprite_initializer(
        sprite, SpriteInitializer("resources/graphics/item_blue_robe.png", ITEM_ENTITY_SIZE))
    for i in range(3):
        item_type = ITEM_TYPES[i]
        health_amount = MANA_AMOUNTS[i]
        register_item_effect(item_type, ItemEffect(health_amount, item_type))
        name = "Blue Robe (" + str(i + 1) + ")"
        description = "Grants +" + str(health_amount) + " max mana"
        register_item_data(item_type, ItemData(ui_icon_sprite, sprite, name, description))