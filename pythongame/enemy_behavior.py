from pythongame.common import *
from pythongame.game_data import ENEMY_PROJECTILE_SIZE
from pythongame.game_state import WorldEntity, Projectile, VisualLine, Enemy, GameState
from pythongame.projectiles import create_projectile_controller


def create_enemy_mind(enemy_behavior: EnemyBehavior):
    if enemy_behavior == EnemyBehavior.DUMB:
        return DumbEnemyMind()
    elif enemy_behavior == EnemyBehavior.SMART:
        return SmartEnemyMind()
    elif enemy_behavior == EnemyBehavior.MAGE:
        return MageEnemyMind()
    else:
        raise Exception("Unhandled behavior: " + str(enemy_behavior))


class DumbEnemyMind:
    def __init__(self):
        self._time_since_decision = 0
        self._decision_interval = 750
        self._flight_duration = 3000
        self._state = "INIT"
        self._time_since_started_fleeing = 0

    def control_enemy(self, _game_state: GameState, enemy: Enemy, player_entity: WorldEntity, is_player_invisible: bool,
                      time_passed: Millis):
        self._time_since_decision += time_passed
        if self._state == "FLEEING":
            self._time_since_started_fleeing += time_passed
        if self._time_since_decision > self._decision_interval:
            is_low_health = enemy.health <= enemy.max_health / 2
            if self._state == "INIT" and is_low_health:
                self._state = "FLEEING"
            if self._state == "FLEEING" and self._time_since_started_fleeing > self._flight_duration:
                self._state = "STOPPED_FLEEING"

            self._time_since_decision = 0
            if is_player_invisible:
                direction = random_direction()
            else:
                direction = get_direction_between(enemy.world_entity, player_entity)
                if self._state == "FLEEING":
                    direction = get_opposite_direction(direction)
                if random.random() < 0.2:
                    direction = random.choice(get_perpendicular_directions(direction))
            enemy.world_entity.set_moving_in_dir(direction)


class SmartEnemyMind:
    def __init__(self):
        self._time_since_decision = 0
        self._decision_interval = 350
        self._time_since_firing = 0
        self._update_firing_cooldown()
        self._pause_after_fire_duration = 700

    def control_enemy(self, game_state: GameState, enemy: Enemy, player_entity: WorldEntity, is_player_invisible: bool,
                      time_passed: Millis):
        self._time_since_firing += time_passed
        self._time_since_decision += time_passed
        if self._time_since_decision > self._decision_interval \
                and self._time_since_firing > self._pause_after_fire_duration:
            self._time_since_decision = 0
            if is_player_invisible:
                direction = random_direction()
                enemy.world_entity.set_moving_in_dir(direction)
            else:
                if self._time_since_firing > self._firing_cooldown:
                    self._time_since_firing = 0
                    self._update_firing_cooldown()
                    enemy.world_entity.set_not_moving()
                    center_position = enemy.world_entity.get_center_position()
                    projectile_pos = (center_position[0] - ENEMY_PROJECTILE_SIZE[0] / 2,
                                      center_position[1] - ENEMY_PROJECTILE_SIZE[1] / 2)
                    entity = WorldEntity(projectile_pos, ENEMY_PROJECTILE_SIZE, Sprite.POISONBALL,
                                         enemy.world_entity.direction, 2)
                    projectile = Projectile(entity, create_projectile_controller(ProjectileType.ENEMY_POISON))
                    game_state.projectile_entities.append(projectile)
                else:
                    direction = get_direction_between(enemy.world_entity, player_entity)
                    enemy.world_entity.set_moving_in_dir(direction)

    def _update_firing_cooldown(self):
        self._firing_cooldown = 1500 + random.random() * 5000


class MageEnemyMind:
    def __init__(self):
        self._time_since_decision = 0
        self._decision_interval = 750
        self._time_since_firing = 0
        self._firing_cooldown = 3000
        self._time_since_healing = 0
        self._healing_cooldown = 5000

    def control_enemy(self, game_state: GameState, enemy: Enemy, _player_entity: WorldEntity,
                      _is_player_invisible: bool, time_passed: Millis):
        self._time_since_decision += time_passed
        self._time_since_firing += time_passed
        self._time_since_healing += time_passed
        if self._time_since_firing > self._firing_cooldown:
            self._time_since_firing = 0
            center_position = enemy.world_entity.get_center_position()
            projectile_pos = (center_position[0] - ENEMY_PROJECTILE_SIZE[0] / 2,
                              center_position[1] - ENEMY_PROJECTILE_SIZE[1] / 2)
            entities = [WorldEntity(projectile_pos, ENEMY_PROJECTILE_SIZE, Sprite.POISONBALL, direction, 2)
                        for direction in get_all_directions()]
            projectiles = [Projectile(entity, create_projectile_controller(ProjectileType.ENEMY_POISON))
                           for entity in entities]
            game_state.projectile_entities += projectiles

        if self._time_since_healing > self._healing_cooldown:
            self._time_since_healing = 0
            mage_pos = enemy.world_entity.get_center_position()
            healing_range = 200
            nearby_hurt_enemies = [e for e in game_state.enemies if abs(e.world_entity.x - mage_pos[0]) < healing_range
                                   and abs(e.world_entity.y - mage_pos[1]) < healing_range and e != enemy
                                   and e.health < e.max_health]
            if nearby_hurt_enemies:
                healing_target = nearby_hurt_enemies[0]
                healing_target.gain_health(5)
                healing_target_pos = healing_target.world_entity.get_center_position()
                visual_line = VisualLine((80, 80, 250), mage_pos, healing_target_pos, 350)
                game_state.visual_lines.append(visual_line)

        if self._time_since_decision > self._decision_interval:
            self._time_since_decision = 0
            if random.random() < 0.2:
                direction = random_direction()
                enemy.world_entity.set_moving_in_dir(direction)
            else:
                enemy.world_entity.set_not_moving()