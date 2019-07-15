import random

from pythongame.core.common import NpcType, Sprite, Direction, Millis, get_all_directions, ConsumableType, \
    PortraitIconSprite
from pythongame.core.game_data import register_npc_data, NpcData, SpriteSheet, register_entity_sprite_map, \
    NpcDialog, register_portrait_icon_sprite_path
from pythongame.core.game_state import GameState, NonPlayerCharacter, WorldEntity
from pythongame.core.npc_behaviors import register_npc_behavior, AbstractNpcMind, AbstractNpcAction, register_npc_action
from pythongame.core.pathfinding.grid_astar_pathfinder import GlobalPathFinder


class NpcMind(AbstractNpcMind):
    def __init__(self, global_path_finder: GlobalPathFinder):
        super().__init__(global_path_finder)
        self._update_path_interval = 900
        self._time_since_updated_path = self._update_path_interval

    def control_npc(self, game_state: GameState, npc: NonPlayerCharacter, player_entity: WorldEntity,
                    is_player_invisible: bool, time_passed: Millis):
        self._time_since_updated_path += time_passed
        if self._time_since_updated_path > self._update_path_interval:
            self._time_since_updated_path = 0
            if random.random() < 0.8:
                npc.world_entity.set_not_moving()
            else:
                direction = random.choice(get_all_directions())
                npc.world_entity.set_moving_in_dir(direction)


class NpcAction(AbstractNpcAction):

    def act(self, game_state: GameState):
        cost = 5
        player_state = game_state.player_state
        can_afford = player_state.money >= cost
        empty_consumable_slot = player_state.find_first_empty_consumable_slot()
        if not can_afford:
            return "Not enough gold!"
        if not empty_consumable_slot:
            return "Not enough space!"
        player_state.money -= cost
        player_state.consumable_slots[empty_consumable_slot] = ConsumableType.MANA_LESSER
        return "Bought mana potion!"


def register_ninja_npc():
    size = (30, 30)  # Must not align perfectly with grid cell size (pathfinding issues)
    sprite = Sprite.NEUTRAL_NPC_NINJA
    npc_type = NpcType.NEUTRAL_NINJA
    movement_speed = 0.03
    health = 6
    dialog = NpcDialog(
        "Ah.. You're new here, aren't you? Interested in my stock of mana potions?",
        "Buy mana potion for 5 gold")
    register_npc_data(npc_type, NpcData(sprite, size, health, 0, movement_speed, 4, False, True, dialog,
                                        PortraitIconSprite.NINJA, None))
    register_npc_behavior(npc_type, NpcMind)
    register_npc_action(npc_type, NpcAction())
    sprite_sheet = SpriteSheet("resources/graphics/enemy_sprite_sheet_3.png")
    original_sprite_size = (32, 32)
    scaled_sprite_size = (48, 48)
    x = 6
    indices_by_dir = {
        Direction.DOWN: [(x, 0), (x + 1, 0), (x + 2, 0)],
        Direction.LEFT: [(x, 1), (x + 1, 1), (x + 2, 1)],
        Direction.RIGHT: [(x, 2), (x + 1, 2), (x + 2, 2)],
        Direction.UP: [(x, 3), (x + 1, 3), (x + 2, 3)]
    }
    register_entity_sprite_map(sprite, sprite_sheet, original_sprite_size, scaled_sprite_size, indices_by_dir,
                               (-8, -16))
    register_portrait_icon_sprite_path(PortraitIconSprite.NINJA, 'resources/graphics/ninja_portrait.png')