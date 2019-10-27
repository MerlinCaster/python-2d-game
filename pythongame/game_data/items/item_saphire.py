from pythongame.core.common import ItemType, Sprite, UiIconSprite
from pythongame.core.game_data import register_ui_icon_sprite_path, register_item_data, ItemData, \
    register_entity_sprite_initializer, ITEM_ENTITY_SIZE
from pythongame.core.item_effects import register_item_effect, AbstractItemEffect
from pythongame.core.view.image_loading import SpriteInitializer

ITEM_TYPE = ItemType.SAPHIRE


class ItemEffect(AbstractItemEffect):
    def get_item_type(self):
        return ITEM_TYPE


def register_saphire():
    ui_icon_sprite = UiIconSprite.ITEM_SAPHIRE
    sprite = Sprite.ITEM_SAPHIRE
    image_file_path = "resources/graphics/item_saphire.png"
    register_item_effect(ITEM_TYPE, ItemEffect())
    register_ui_icon_sprite_path(ui_icon_sprite, image_file_path)
    register_entity_sprite_initializer(sprite, SpriteInitializer(image_file_path, ITEM_ENTITY_SIZE))
    description = ["It looks expensive..."]
    register_item_data(ITEM_TYPE, ItemData(ui_icon_sprite, sprite, "Saphire", description))