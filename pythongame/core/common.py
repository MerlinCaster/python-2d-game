import random
from enum import Enum
from typing import NewType, Optional, Any, List, Callable

Millis = NewType('Millis', int)

PLAYER_ENTITY_SIZE = (30, 30)


class Observable:
    def __init__(self):
        self._observers: List[Callable[[Any], Any]] = []

    def register_observer(self, observer: Callable[[Any], Any]):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            # print("DEBUG Notifying observer " + str(observer) + ": " + str(event))
            observer(event)


class SceneId(Enum):
    STARTING_PROGRAM = 1
    PICKING_HERO = 2
    CREATING_GAME_WORLD = 3
    PLAYING = 4
    PAUSED = 5
    VICTORY_SCREEN = 6
    CHALLENGE_COMPLETE_SCREEN = 7


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


def get_all_directions():
    return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


class HeroUpgradeId(Enum):
    ARMOR = 1
    DAMAGE = 2
    MAX_HEALTH = 3
    MAX_MANA = 4
    HEALTH_REGEN = 5
    MANA_REGEN = 6
    ABILITY_WHIRLWIND_STUN = 10
    ABILITY_FIREBALL_BURN = 11
    ABILITY_ENTANGLING_ROOTS_COOLDOWN = 12
    ABILITY_FIREBALL_MANA_COST = 13
    ABILITY_ARCANE_FIRE_COOLDOWN = 14
    ABILITY_STEALTH_MANA_COST = 20
    ABILITY_SHIV_SNEAK_BONUS_DAMAGE = 21
    ABILITY_DASH_KILL_RESET = 22
    ABILITY_SHIV_FULL_HEALTH_BONUS_DAMAGE = 23
    ABILITY_STEALTH_MOVEMENT_SPEED = 24
    ABILITY_DASH_MOVEMENT_SPEED = 25
    ABILITY_CHARGE_MELEE = 30
    ABILITY_SLASH_AOE_BONUS_DAMAGE = 31
    ABILITY_BLOODLUST_DURATION = 32
    ABILITY_SLASH_CD = 33
    ABILITY_CHARGE_RESET_STOMP_COOLDOWN = 34
    MAGE_LIGHT_FOOTED = 50
    WARRIOR_RETRIBUTION = 51


class ConsumableType(Enum):
    HEALTH_LESSER = 1
    HEALTH = 2
    MANA_LESSER = 11
    MANA = 12
    SPEED = 21
    INVISIBILITY = 22
    POWER = 23
    BREW = 50
    WARP_STONE = 60
    SCROLL_SUMMON_DRAGON = 101


class NpcType(Enum):
    NECROMANCER = 3
    WARRIOR = 4
    RAT_1 = 5
    RAT_2 = 6
    DARK_REAPER = 7
    GOBLIN_WARLOCK = 8
    MUMMY = 9
    GOBLIN_WORKER = 10
    GOBLIN_SPEARMAN = 11
    GOBLIN_SPEARMAN_ELITE = 12
    GOBLIN_WARRIOR = 13
    ZOMBIE = 14
    VETERAN = 15
    ICE_WITCH = 16
    WARRIOR_KING = 17
    NEUTRAL_DWARF = 100
    NEUTRAL_NOMAD = 101
    NEUTRAL_NINJA = 102
    NEUTRAL_SORCERER = 103
    NEUTRAL_YOUNG_SORCERESS = 104
    NEUTRAL_WARPSTONE_MERCHANT = 105
    NEUTRAL_CHALLENGE_STARTER = 107
    PLAYER_SUMMON_DRAGON = 200


class WallType(Enum):
    WALL = 1
    STATUE = 2
    WALL_DIRECTIONAL_N = 11
    WALL_DIRECTIONAL_NE = 12
    WALL_DIRECTIONAL_E = 13
    WALL_DIRECTIONAL_SE = 14
    WALL_DIRECTIONAL_S = 15
    WALL_DIRECTIONAL_SW = 16
    WALL_DIRECTIONAL_W = 17
    WALL_DIRECTIONAL_NW = 18
    WALL_DIRECTIONAL_POINTY_NE = 19
    WALL_DIRECTIONAL_POINTY_SE = 20
    WALL_DIRECTIONAL_POINTY_SW = 21
    WALL_DIRECTIONAL_POINTY_NW = 22
    WALL_CHAIR = 30
    ALTAR = 31
    SHELF_EMPTY = 40
    SHELF_HELMETS = 41
    SHELF_ARMORS = 42
    BARREL_1 = 50
    BARREL_2 = 51
    BARREL_3 = 52
    BARREL_4 = 53
    BARREL_5 = 54
    BARREL_6 = 55


class AbilityType(Enum):
    HEAL = 1
    FIREBALL = 2
    ARCANE_FIRE = 4
    TELEPORT = 5
    FROST_NOVA = 6
    WHIRLWIND = 7
    ENTANGLING_ROOTS = 8
    SWORD_SLASH = 10
    BLOOD_LUST = 11
    CHARGE = 12
    STOMP = 13
    SHIV = 14
    STEALTH = 15
    INFUSE_DAGGER = 16
    DASH = 17
    KILL_EVERYTHING = 18


class Sprite(Enum):
    NONE = 0
    EFFECT_ABILITY_FROST_NOVA = 3
    PROJECTILE_PLAYER_FIREBALL = 11
    PROJECTILE_PLAYER_ARCANE_FIRE = 12
    PROJECTILE_PLAYER_WHIRLWIND = 13
    PROJECTILE_ENEMY_GOBLIN_WARLOCK = 14
    PROJECTILE_PLAYER_ENTANGLING_ROOTS = 15
    POTION_HEALTH = 101
    POTION_HEALTH_LESSER = 102
    POTION_MANA = 103
    POTION_MANA_LESSER = 104
    CONSUMABLE_SCROLL_SUMMON_DRAGON = 105
    POTION_INVIS = 106
    POTION_SPEED = 107
    POTION_BREW = 108
    CONSUMABLE_WARPSTONE = 109
    ELIXIR_POWER = 110
    ENEMY_NECROMANCER = 201
    ENEMY_RAT_1 = 202
    ENEMY_RAT_2 = 203
    ENEMY_DARK_REAPER = 204
    ENEMY_GOBLIN_WARLOCK = 205
    ENEMY_MUMMY = 206
    ENEMY_WARRIOR = 207
    ENEMY_GOBLIN_WORKER = 209
    ENEMY_GOBLIN_SPEARMAN = 210
    ENEMY_GOBLIN_SPEARMAN_ELITE = 211
    ENEMY_GOBLIN_WARRIOR = 212
    ENEMY_ZOMBIE = 213
    ENEMY_VETERAN = 214
    ENEMY_ICE_WITCH = 215
    ENEMY_WARRIOR_KING = 216
    PLAYER_SUMMON_DRAGON = 250
    NEUTRAL_NPC_DWARF = 260
    NEUTRAL_NPC_NOMAD = 261
    NEUTRAL_NPC_NINJA = 262
    NEUTRAL_NPC_SORCERER = 263
    NEUTRAL_NPC_YOUNG_SORCERESS = 264
    NEUTRAL_WARPSTONE_MERCHANT = 265
    NEUTRAL_NPC_CHALLENGE_STARTER = 267
    ITEM_AMULET_OF_MANA = 301
    ITEM_MESSENGERS_HAT = 302
    ITEM_ROD_OF_LIGHTNING = 303
    ITEM_SKULL_STAFF = 304
    ITEM_SOLDIERS_HELMET = 305
    ITEM_BLESSED_SHIELD = 306
    ITEM_STAFF_OF_FIRE = 307
    ITEM_BLUE_ROBE = 308
    ITEM_ORB_OF_THE_MAGI = 309
    ITEM_WIZARDS_COWL = 310
    ITEM_ZULS_AEGIS = 311
    ITEM_KNIGHTS_ARMOR = 312
    ITEM_GOATS_RING = 313
    ITEM_BLOOD_AMULET = 314
    ITEM_WOODEN_SHIELD = 315
    ITEM_ELVEN_ARMOR = 316
    ITEM_GOLD_NUGGET = 317
    ITEM_SAPHIRE = 318
    ITEM_LEATHER_COWL = 319
    ITEM_WINGED_HELMET = 320
    ITEM_ELITE_ARMOR = 321
    ITEM_RING_OF_POWER = 322
    ITEM_LEATHER_ARMOR = 323
    ITEM_FREEZING_GAUNTLET = 324
    ITEM_ROYAL_DAGGER = 325
    ITEM_ROYAL_SWORD = 326
    ITEM_MOLTEN_AXE = 327
    ITEM_ORB_OF_WISDOM = 328
    ITEM_ORB_OF_LIFE = 329
    ITEM_WAND = 330
    ITEM_GLADIATOR_ARMOR = 331
    ITEM_NOBLE_DEFENDER = 332
    ITEM_FROG = 333
    ITEM_HATCHET = 334
    ITEM_ELITE_HELMET = 335
    ITEM_STONE_AMULET = 336
    ITEM_TORN_DOCUMENT = 337
    ITEM_KEY = 338
    ITEM_WOODEN_SWORD = 339
    ITEM_DRUIDS_RING = 340
    ITEM_WARLOCKS_COWL = 341
    ITEM_LICH_ARMOR = 342
    ITEM_WARLORDS_ARMOR = 343
    ITEM_HEALING_WAND = 344
    ITEM_SKULL_SHIELD = 345
    ITEM_THIEFS_MASK = 346
    ITEM_SERPENT_SWORD = 347
    ITEM_WHIP = 348
    ITEM_CLEAVER = 349
    ITEM_DESERT_BLADE = 350
    ITEM_PRACTICE_SWORD = 351
    ITEM_NOVICE_WAND = 352
    ITEM_SORCERESS_ROBE = 353
    ITEM_BLESSED_CHALICE = 354
    ITEM_NECKLACE_OF_SUFFERING = 355
    ITEM_FIRE_WAND = 356
    COINS_1 = 400
    COINS_2 = 401
    COINS_5 = 402
    DECORATION_GROUND_STONE = 450
    DECORATION_GROUND_STONE_GRAY = 451
    DECORATION_PLANT = 452
    DECORATION_ENTANGLING_ROOTS_EFFECT = 453
    WALL = 501
    WALL_STATUE = 502
    WALL_ALTAR = 503
    WALL_DIRECTIONAL_N = 511
    WALL_DIRECTIONAL_NE = 512
    WALL_DIRECTIONAL_E = 513
    WALL_DIRECTIONAL_SE = 514
    WALL_DIRECTIONAL_S = 515
    WALL_DIRECTIONAL_SW = 516
    WALL_DIRECTIONAL_W = 517
    WALL_DIRECTIONAL_NW = 518
    WALL_DIRECTIONAL_POINTY_NE = 519
    WALL_DIRECTIONAL_POINTY_SE = 520
    WALL_DIRECTIONAL_POINTY_SW = 521
    WALL_DIRECTIONAL_POINTY_NW = 522
    WALL_CHAIR = 530
    WALL_SHELF_EMPTY = 540
    WALL_SHELF_HELMETS = 541
    WALL_SHELF_ARMORS = 542
    WALL_BARREL_1 = 550
    WALL_BARREL_2 = 551
    WALL_BARREL_3 = 552
    WALL_BARREL_4 = 553
    WALL_BARREL_5 = 554
    WALL_BARREL_6 = 555
    PORTAL_DISABLED = 600
    PORTAL_BLUE = 601
    PORTAL_GREEN = 602
    PORTAL_RED = 603
    PORTAL_DARK = 604
    WARP_POINT = 650
    HERO_MAGE = 700
    HERO_WARRIOR = 701
    HERO_ROGUE = 702
    HERO_GOD = 703
    CHEST = 800
    MAP_EDITOR_SMART_FLOOR_1 = 900
    MAP_EDITOR_SMART_FLOOR_2 = 901
    MAP_EDITOR_SMART_FLOOR_3 = 902
    MAP_EDITOR_SMART_FLOOR_4 = 903


class BuffType(Enum):
    HEALING_OVER_TIME = 1
    INCREASED_MOVE_SPEED = 3
    INVISIBILITY = 4
    CHANNELING_ARCANE_FIRE = 5
    REDUCED_MOVEMENT_SPEED = 6
    INVULNERABILITY = 7
    STUNNED_BY_WHIRLWIND = 8
    ENEMY_GOBLIN_WARLOCK_BURNT = 9
    ROOTED_BY_ENTANGLING_ROOTS = 10
    SUMMON_DIE_AFTER_DURATION = 11
    BLOOD_LUST = 13
    CHARGING = 14
    STUNNED_FROM_CHARGE_IMPACT = 15
    RECOVERING_AFTER_ABILITY = 17
    CHANNELING_STOMP = 18
    STUNNED_BY_STOMP = 19
    STEALTHING = 20
    AFTER_STEALTHING = 21
    STUNNED_BY_AEGIS_ITEM = 22
    DEBUFFED_BY_GOATS_RING = 23
    DAMAGED_BY_INFUSED_DAGGER = 26
    AFTER_DASH = 27
    RESTORING_HEALTH_FROM_BREW = 28
    DEBUFFED_BY_FREEZING_GAUNTLET = 29
    SLOWED_BY_ICE_WITCH = 30
    SLOWED_FROM_NOBLE_DEFENDER = 31
    TELEPORTING_WITH_PORTAL = 32
    TELEPORTING_WITH_WARP_STONE = 33
    TELEPORTING_WITH_WARP_POINT = 34
    BEING_SPAWNED = 35
    BURNT_BY_FIREBALL = 36
    PROTECTED_BY_STONE_AMULET = 37
    ELIXIR_OF_POWER = 38
    BUFFED_BY_HEALING_WAND = 39
    ENEMY_GOBLIN_SPEARMAN_SPRINT = 40
    BLEEDING_FROM_CLEAVER_WEAPON = 41
    SPEED_BUFF_FROM_DASH = 42
    BUFFED_FROM_RETRIBUTION_TALENT = 43
    INCREASED_DAMAGE_FROM_NECKLACE_OF_SUFFERING = 44


class ItemType(Enum):
    MESSENGERS_HAT = 1
    SKULL_STAFF = 3
    ROD_OF_LIGHTNING = 4
    STAFF_OF_FIRE = 7
    AMULET_OF_MANA_1 = 10
    AMULET_OF_MANA_2 = 11
    AMULET_OF_MANA_3 = 12
    BLESSED_SHIELD_1 = 20
    BLESSED_SHIELD_2 = 21
    BLESSED_SHIELD_3 = 22
    SOLDIERS_HELMET_1 = 30
    SOLDIERS_HELMET_2 = 31
    SOLDIERS_HELMET_3 = 32
    BLUE_ROBE_1 = 40
    BLUE_ROBE_2 = 41
    BLUE_ROBE_3 = 42
    ORB_OF_THE_MAGI_1 = 50
    ORB_OF_THE_MAGI_2 = 51
    ORB_OF_THE_MAGI_3 = 52
    ORB_OF_WISDOM_1 = 53
    ORB_OF_WISDOM_2 = 54
    ORB_OF_WISDOM_3 = 55
    ORB_OF_LIFE_1 = 56
    ORB_OF_LIFE_2 = 57
    ORB_OF_LIFE_3 = 58
    WIZARDS_COWL = 60
    ZULS_AEGIS = 70
    KNIGHTS_ARMOR = 71
    GOATS_RING = 72
    BLOOD_AMULET = 73
    WOODEN_SHIELD = 74
    ELVEN_ARMOR = 75
    GOLD_NUGGET = 76
    SAPHIRE = 77
    LEATHER_COWL = 78
    WINGED_HELMET = 79
    ELITE_ARMOR = 80
    RING_OF_POWER = 81
    LEATHER_ARMOR = 82
    FREEZING_GAUNTLET = 83
    ROYAL_DAGGER = 84
    ROYAL_SWORD = 85
    MOLTEN_AXE = 86
    WAND = 87
    GLADIATOR_ARMOR = 88
    NOBLE_DEFENDER = 89
    FROG = 90
    HATCHET = 91
    ELITE_HELMET = 92
    STONE_AMULET = 93
    TORN_DOCUMENT = 94
    KEY = 95
    WOODEN_SWORD = 96
    DRUIDS_RING = 97
    WARLOCKS_COWL = 98
    LICH_ARMOR = 99
    WARLORDS_ARMOR = 100
    HEALING_WAND = 101
    SKULL_SHIELD = 102
    THIEFS_MASK = 103
    SERPENT_SWORD = 104
    WHIP = 105
    CLEAVER = 106
    DESERT_BLADE = 107
    PRACTICE_SWORD = 108
    NOVICE_WAND = 109
    SORCERESS_ROBE = 110
    BLESSED_CHALICE = 111
    NECKLACE_OF_SUFFERING = 112
    FIRE_WAND = 113


class ProjectileType(Enum):
    PLAYER_FIREBALL = 1
    PLAYER_ARCANE_FIRE = 2
    PLAYER_WHIRLWIND = 3
    PLAYER_ENTANGLING_ROOTS = 4
    ENEMY_GOBLIN_WARLOCK = 101
    ENEMY_NECROMANCER = 102


class SoundId(Enum):
    ABILITY_FIREBALL = 1
    ABILITY_WHIRLWIND = 2
    ABILITY_TELEPORT = 3
    ABILITY_ENTANGLING_ROOTS = 4
    ABILITY_CHARGE = 5
    ABILITY_SHIV = 6
    ABILITY_STEALTH = 7
    ABILITY_INFUSE_DAGGER = 8
    ABILITY_DASH = 9
    ABILITY_SLASH = 10
    ABILITY_STOMP_HIT = 11
    ABILITY_BLOODLUST = 12
    ABILITY_ARCANE_FIRE = 13
    ABILITY_SHIV_STEALTHED = 14
    ABILITY_FIREBALL_HIT = 15
    ABILITY_ENTANGLING_ROOTS_HIT = 16
    ABILITY_CHARGE_HIT = 17
    ABILITY_STOMP = 18
    WARP = 40
    CONSUMABLE_POTION = 50
    CONSUMABLE_BUFF = 51
    EVENT_PLAYER_LEVELED_UP = 100
    EVENT_PICKED_UP = 101
    EVENT_PLAYER_DIED = 102
    EVENT_ENEMY_DIED = 103
    EVENT_PICKED_UP_MONEY = 104
    EVENT_PURCHASED_SOMETHING = 105
    EVENT_PORTAL_ACTIVATED = 106
    EVENT_COMPLETED_QUEST = 107
    EVENT_PICKED_TALENT = 108
    EVENT_SOLD_SOMETHING = 109
    EVENT_SAVED_GAME = 110
    WARNING = 200
    INVALID_ACTION = 201
    PLAYER_PAIN = 300
    ENEMY_ATTACK_GOBLIN_WARLOCK = 400
    ENEMY_ATTACK = 401
    ENEMY_ATTACK_WAS_BLOCKED = 402
    ENEMY_NECROMANCER_SUMMON = 403
    ENEMY_ATTACK_ICE_WITCH = 404
    ENEMY_ATTACK_NECRO = 405
    ENEMY_NECROMANCER_HEAL = 406
    ENEMY_ATTACK_WAS_DODGED = 407
    DEATH_RAT = 500
    DEATH_ZOMBIE = 501
    DEATH_BOSS = 502
    DEATH_GOBLIN = 503
    DEATH_ICE_WITCH = 504
    DEATH_HUMAN = 505
    DEATH_NECRO = 506
    UI_ITEM_WAS_MOVED = 600
    UI_START_DRAGGING_ITEM = 601
    UI_ITEM_WAS_DROPPED_ON_GROUND = 602
    UI_TOGGLE = 603
    DIALOG = 700
    FOOTSTEPS = 800


class PortalId(Enum):
    A_BASE = 1
    A_REMOTE = 2
    B_BASE = 3
    B_REMOTE = 4
    C_BASE = 5
    C_REMOTE = 6
    D_BASE = 7
    D_REMOTE = 8


class HeroId(Enum):
    MAGE = 1
    WARRIOR = 2
    ROGUE = 3
    GOD = 4


class UiIconSprite(Enum):
    POTION_HEALTH_LESSER = 1
    POTION_HEALTH = 2
    POTION_MANA_LESSER = 3
    POTION_MANA = 4
    POTION_SPEED = 11
    POTION_INVISIBILITY = 12
    CONSUMABLE_SCROLL_SUMMON_DRAGON = 13
    POTION_BREW = 14
    CONSUMABLE_WARPSTONE = 15
    ELIXIR_POWER = 16
    ABILITY_FIREBALL = 101
    ABILITY_HEAL = 102
    ABILITY_ARCANE_FIRE = 103
    ABILITY_TELEPORT = 104
    ABILITY_FROST_NOVA = 105
    ABILITY_WHIRLWIND = 106
    ABILITY_ENTANGLING_ROOTS = 107
    ABILITY_SWORD_SLASH = 109
    ABILITY_BLOODLUST = 110
    ABILITY_CHARGE = 111
    ABILITY_STOMP = 112
    ABILITY_SHIV = 113
    ABILITY_STEALTH = 114
    ABILITY_INFUSE_DAGGER = 115
    ABILITY_DASH = 116
    ABILITY_KILL_EVERYTHING = 117
    ITEM_MESSENGERS_HAT = 201
    ITEM_AMULET_OF_MANA = 202
    ITEM_SKULL_STAFF = 203
    ITEM_ROD_OF_LIGHTNING = 204
    ITEM_SOLDIERS_HELMET = 205
    ITEM_BLESSED_SHIELD = 206
    ITEM_STAFF_OF_FIRE = 207
    ITEM_BLUE_ROBE = 208
    ITEM_ORB_OF_THE_MAGI = 209
    ITEM_WIZARDS_COWL = 210
    ITEM_ZULS_AEGIS = 211
    ITEM_KNIGHTS_ARMOR = 212
    ITEM_GOATS_RING = 213
    ITEM_BLOOD_AMULET = 214
    ITEM_WOODEN_SHIELD = 215
    ITEM_ELVEN_ARMOR = 216
    ITEM_GOLD_NUGGET = 217
    ITEM_SAPHIRE = 218
    ITEM_LEATHER_COWL = 219
    ITEM_WINGED_HELMET = 220
    ITEM_ELITE_ARMOR = 221
    ITEM_RING_OF_POWER = 222
    ITEM_LEATHER_ARMOR = 223
    ITEM_FREEZING_GAUNTLET = 224
    ITEM_ROYAL_DAGGER = 225
    ITEM_ROYAL_SWORD = 226
    ITEM_MOLTEN_AXE = 227
    ITEM_ORB_OF_WISDOM = 228
    ITEM_ORB_OF_LIFE = 229
    ITEM_WAND = 230
    ITEM_GLADIATOR_ARMOR = 231
    ITEM_NOBLE_DEFENDER = 232
    ITEM_FROG = 233
    ITEM_HATCHET = 234
    ITEM_ELITE_HELMET = 235
    ITEM_STONE_AMULET = 236
    ITEM_TORN_DOCUMENT = 237
    ITEM_KEY = 238
    ITEM_WOODEN_SWORD = 239
    ITEM_DRUIDS_RING = 240
    ITEM_WARLOCKS_COWL = 241
    ITEM_LICH_ARMOR = 242
    ITEM_WARLORDS_ARMOR = 243
    ITEM_HEALING_WAND = 244
    ITEM_SKULL_SHIELD = 245
    ITEM_THIEFS_MASK = 246
    ITEM_SERPENT_SWORD = 247
    ITEM_WHIP = 248
    ITEM_CLEAVER = 249
    ITEM_DESERT_BLADE = 250
    ITEM_PRACTICE_SWORD = 251
    ITEM_NOVICE_WAND = 252
    ITEM_SORCERESS_ROBE = 253
    ITEM_BLESSED_CHALICE = 254
    ITEM_NECKLACE_OF_SUFFERING = 255
    ITEM_FIRE_WAND = 256
    MAP_EDITOR_TRASHCAN = 301
    MAP_EDITOR_RECYCLING = 302
    INVENTORY_TEMPLATE_HELMET = 400
    INVENTORY_TEMPLATE_CHEST = 401
    INVENTORY_TEMPLATE_MAINHAND = 402
    INVENTORY_TEMPLATE_OFFHAND = 403
    INVENTORY_TEMPLATE_NECK = 404
    INVENTORY_TEMPLATE_RING = 405
    TALENT_LIGHT_FOOTED = 500


# Portraits that are shown in UI (player portrait and dialog portraits)
class PortraitIconSprite(Enum):
    VIKING = 2
    NOMAD = 3
    NINJA = 4
    SORCERER = 5
    YOUNG_SORCERESS = 6
    WARPSTONE_MERCHANT = 7
    CHALLENGE_STARTER = 9
    HERO_MAGE = 100
    HERO_WARRIOR = 101
    HERO_ROGUE = 102
    HERO_GOD = 103


class HeroStat(Enum):
    MAX_HEALTH = 1
    HEALTH_REGEN = 2
    MAX_MANA = 3
    MANA_REGEN = 4
    ARMOR = 5
    MOVEMENT_SPEED = 6
    LIFE_STEAL = 7
    BLOCK_AMOUNT = 8
    DODGE_CHANCE = 9
    DAMAGE = 10
    PHYSICAL_DAMAGE = 11
    MAGIC_DAMAGE = 12
    BLOCK_CHANCE = 13


# Use to handle timing-related boilerplate for buffs, items, enemy behaviours, etc
class PeriodicTimer:
    def __init__(self, cooldown: Millis):
        self.cooldown = cooldown
        self.time_until_next_run = cooldown

    # notify the timer of how much time has passed since the last call
    # the timer checks if enough time has passed. If it has, it resets
    # and returns True.
    def update_and_check_if_ready(self, time_passed: Millis) -> bool:
        self.time_until_next_run -= time_passed
        if self.time_until_next_run <= 0:
            self.time_until_next_run += self.cooldown
            return True
        return False


def get_random_hint():
    hints = [
        "Hold Shift to see more info about lootable items",
        "Press Space to interact with NPCs and objects",
        "Reaching certain levels unlocks new abilities",
        "Use the number keys for potions and other consumables",
        "Gold coins are looted by simply walking over them",
        "If you die, you'll respawn but lose exp points",
        "Use magic statues and warpstones to teleport long distances",
        "Hover over things with the mouse cursor to get more info",
        "Drag inventory items and consumables with the mouse cursor",
        "Equip items by dragging them to the appropriate inventory slot",
        "Choose talents to improve your stats and abilities"
    ]
    return random.choice(hints)


class SceneTransition:
    def __init__(self, scene):
        self.scene = scene


class AbstractScene:

    def on_enter(self):
        pass

    def handle_user_input(self, events: List[Any]) -> Optional[SceneTransition]:
        pass

    def run_one_frame(self, _time_passed: Millis) -> Optional[SceneTransition]:
        pass

    def render(self):
        pass


# These are sent as messages to player. They let buffs and items react to events. One buff might have its
# duration prolonged if an enemy dies for example, and an item might give mana on enemy kills.
class Event:
    pass


class HeroUpgrade:

    def __init__(self, hero_upgrade_id: HeroUpgradeId):
        self._hero_upgrade_id = hero_upgrade_id

    # Override this method for upgrades that need to actively handle events
    def handle_event(self, event: Event, game_state: Any):
        pass

    def get_upgrade_id(self):
        if self._hero_upgrade_id is None:
            raise Exception("hero_upgrade_id is not initialized: " + str(HeroUpgrade))
        return self._hero_upgrade_id


class DialogOptionData:
    def __init__(self, summary: str, action_text: str, action: Optional[Any],
                 ui_icon_sprite: Optional[UiIconSprite] = None, detail_header: Optional[str] = None,
                 detail_body: Optional[str] = None):
        self.summary = summary
        self.action_text = action_text
        self.action = action
        self.ui_icon_sprite = ui_icon_sprite
        self.detail_header = detail_header
        self.detail_body = detail_body


class DialogData:
    def __init__(self, portrait_icon_sprite: PortraitIconSprite, text_body: str, options: List[DialogOptionData]):
        self.portrait_icon_sprite = portrait_icon_sprite
        self.text_body = text_body
        self.options = options
