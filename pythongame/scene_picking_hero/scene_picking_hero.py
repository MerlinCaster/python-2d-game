from typing import Optional, Callable, List, Any

import pygame

from pythongame.core.common import HeroId, AbstractScene, SceneTransition, SoundId
from pythongame.core.sound_player import play_sound
from pythongame.scene_creating_world.scene_creating_world import InitFlags
from pythongame.scene_picking_hero.view_picking_hero import PickingHeroView

HEROES = [HeroId.MAGE, HeroId.WARRIOR, HeroId.ROGUE]


class PickingHeroScene(AbstractScene):
    def __init__(self, creating_world_scene: Callable[[InitFlags], AbstractScene], view: PickingHeroView,
                 flags: InitFlags):
        self.creating_world_scene = creating_world_scene
        self.view = view
        self.selected_hero_index = 0
        self.flags: InitFlags = flags

    def handle_user_input(self, events: List[Any]) -> Optional[SceneTransition]:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    self._change_hero(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    self._change_hero(1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.flags.picked_hero = HEROES[self.selected_hero_index]
                    return SceneTransition(self.creating_world_scene(self.flags))

    def _change_hero(self, delta: int):
        self.selected_hero_index = (self.selected_hero_index + delta) % 3
        play_sound(SoundId.DIALOG)

    def render(self):
        self.view.render(HEROES, self.selected_hero_index)
