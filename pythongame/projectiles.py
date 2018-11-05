from pythongame.common import *
from pythongame.game_state import Projectile, Enemy, GameState
from pythongame.visual_effects import VisualCircle, create_visual_damage_text


def create_projectile_controller(projectile_type: ProjectileType):
    return projectile_controllers[projectile_type]()


class AbstractProjectileController:
    def __init__(self, max_age):
        self._age = 0
        self._max_age = max_age

    def notify_time_passed(self, _game_state: GameState, projectile: Projectile, time_passed: Millis):
        self._age += time_passed
        if self._age > self._max_age:
            projectile.has_expired = True

    def apply_enemy_collision(self, _enemy: Enemy, _game_state: GameState):
        return False

    def apply_player_collision(self, _game_state: GameState):
        return False


class PlayerAoeProjectileController(AbstractProjectileController):
    def __init__(self):
        super().__init__(3000)
        self._dmg_cooldown = 350
        self._time_since_dmg = self._dmg_cooldown

    def notify_time_passed(self, game_state: GameState, projectile: Projectile, time_passed: Millis):
        super().notify_time_passed(game_state, projectile, time_passed)
        self._time_since_dmg += time_passed
        if self._time_since_dmg > self._dmg_cooldown:
            self._time_since_dmg = False
            projectile_entity = projectile.world_entity
            for enemy in game_state.get_enemies_intersecting_with(projectile_entity):
                damage_amount = 1
                enemy.lose_health(damage_amount)
                game_state.visual_effects.append(create_visual_damage_text(enemy.world_entity, damage_amount))
            if random.random() < 0.07:
                projectile_entity.direction = random.choice(get_perpendicular_directions(projectile_entity.direction))


class PlayerMagicMissileProjectileController(AbstractProjectileController):
    def __init__(self):
        super().__init__(400)
        self._enemies_hit = []

    def apply_enemy_collision(self, enemy: Enemy, game_state: GameState):
        if enemy not in self._enemies_hit:
            damage_amount = 1
            enemy.lose_health(damage_amount)
            game_state.visual_effects.append(create_visual_damage_text(enemy.world_entity, damage_amount))
            game_state.visual_effects.append(VisualCircle((250, 100, 250), enemy.world_entity.get_center_position(), 25,
                                                          Millis(100), 0))
            self._enemies_hit.append(enemy)
        return False


class EnemyPoisonProjectileController(AbstractProjectileController):
    def __init__(self):
        super().__init__(2000)

    def apply_player_collision(self, game_state: GameState):
        damage_amount = 1
        game_state.player_state.lose_health(damage_amount)
        game_state.visual_effects.append(create_visual_damage_text(game_state.player_entity, damage_amount))
        game_state.player_state.gain_buff(BuffType.DAMAGE_OVER_TIME, Millis(2000))
        game_state.visual_effects.append(VisualCircle((50, 180, 50), game_state.player_entity.get_center_position(),
                                                      50, Millis(100), 0))
        return True


projectile_controllers = {
    ProjectileType.PLAYER_AOE: PlayerAoeProjectileController,
    ProjectileType.ENEMY_POISON: EnemyPoisonProjectileController,
    ProjectileType.PLAYER_MAGIC_MISSILE: PlayerMagicMissileProjectileController
}


def register_projectile_controller(projectile_type: ProjectileType, controller: AbstractProjectileController):
    projectile_controllers[projectile_type] = controller
