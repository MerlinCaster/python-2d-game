from pythongame.core.common import ItemType, Sprite, UiIconSprite, HeroStat
from pythongame.core.item_inventory import ItemEquipmentCategory
from pythongame.game_data.items.register_items_util import register_stat_modifying_item


def register_molten_axe_item():
    register_stat_modifying_item(
        item_type=ItemType.MOLTEN_AXE,
        ui_icon_sprite=UiIconSprite.ITEM_MOLTEN_AXE,
        sprite=Sprite.ITEM_MOLTEN_AXE,
        image_file_path="resources/graphics/item_molten_axe.png",
        item_equipment_category=ItemEquipmentCategory.MAIN_HAND,
        name="Molten Axe",
        stat_modifiers={HeroStat.PHYSICAL_DAMAGE: 0.25}
    )
