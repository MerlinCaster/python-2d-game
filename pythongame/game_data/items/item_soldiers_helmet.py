from pythongame.core.common import ItemType, Sprite
from pythongame.core.game_data import UiIconSprite, register_ui_icon_sprite_path, register_item_data, ItemData, \
    register_entity_sprite_initializer, SpriteInitializer, ITEM_ENTITY_SIZE
from pythongame.core.game_state import GameState
from pythongame.core.item_effects import register_item_effect, AbstractItemEffect

ITEM_TYPES = [ItemType.SOLDIERS_HELMET_1, ItemType.SOLDIERS_HELMET_2, ItemType.SOLDIERS_HELMET_3]
HEALTH_AMOUNTS = [10, 20, 30]


class ItemEffect(AbstractItemEffect):

    def __init__(self, health_amount: int, item_type: ItemType):
        self.health_amount = health_amount
        self.item_type = item_type

    def apply_start_effect(self, game_state: GameState):
        game_state.player_state.gain_max_health(self.health_amount)

    def apply_end_effect(self, game_state: GameState):
        game_state.player_state.lose_max_health(self.health_amount)

    def get_item_type(self):
        return self.item_type


def register_soldiers_helmet_item():
    ui_icon_sprite = UiIconSprite.ITEM_SOLDIERS_HELMET
    sprite = Sprite.ITEM_SOLDIERS_HELMET
    register_ui_icon_sprite_path(ui_icon_sprite, "resources/graphics/item_soldiers_helmet.png")
    register_entity_sprite_initializer(
        sprite, SpriteInitializer("resources/graphics/item_soldiers_helmet.png", ITEM_ENTITY_SIZE))
    for i in range(3):
        item_type = ITEM_TYPES[i]
        health_amount = HEALTH_AMOUNTS[i]
        register_item_effect(item_type, ItemEffect(health_amount, item_type))
        name = "Soldier's Helmet (" + str(i + 1) + ")"
        description = "Grants +" + str(health_amount) + " max health"
        register_item_data(item_type, ItemData(ui_icon_sprite, sprite, name, description))