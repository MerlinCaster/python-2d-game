from pythongame.core.common import ConsumableType, Sprite, UiIconSprite, SoundId
from pythongame.core.consumable_effects import create_potion_visual_effect_at_player, ConsumableWasConsumed, \
    ConsumableFailedToBeConsumed, \
    register_consumable_effect
from pythongame.core.damage_interactions import player_receive_healing
from pythongame.core.game_data import register_entity_sprite_initializer, register_ui_icon_sprite_path, \
    register_consumable_data, ConsumableData, POTION_ENTITY_SIZE, ConsumableCategory
from pythongame.core.game_state import GameState
from pythongame.core.view.image_loading import SpriteInitializer

HEALING_AMOUNT = 100


def _apply_health(game_state: GameState):
    if not game_state.player_state.health_resource.is_at_max():
        create_potion_visual_effect_at_player(game_state)
        player_receive_healing(HEALING_AMOUNT, game_state)
        return ConsumableWasConsumed()
    else:
        return ConsumableFailedToBeConsumed("Already at full health!")


def register_health_potion():
    consumable_type = ConsumableType.HEALTH
    sprite = Sprite.POTION_HEALTH
    ui_icon_sprite = UiIconSprite.POTION_HEALTH

    register_consumable_effect(consumable_type, _apply_health)
    image_path = "resources/graphics/icon_potion_health.png"
    register_entity_sprite_initializer(sprite, SpriteInitializer(image_path, POTION_ENTITY_SIZE))
    register_ui_icon_sprite_path(ui_icon_sprite, image_path)
    description = "Restores " + str(HEALING_AMOUNT) + " health"
    data = ConsumableData(ui_icon_sprite, sprite, "Health potion", description, ConsumableCategory.HEALTH,
                          SoundId.CONSUMABLE_POTION)
    register_consumable_data(consumable_type, data)
