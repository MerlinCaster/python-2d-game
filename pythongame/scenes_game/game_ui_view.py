from typing import List, Tuple, Optional, Dict

import pygame
from pygame.rect import Rect

from pythongame.core.common import ConsumableType, ItemType, HeroId, UiIconSprite, AbilityType
from pythongame.core.game_data import ABILITIES, BUFF_TEXTS, \
    KEYS_BY_ABILITY_TYPE, CONSUMABLES, ITEMS, HEROES
from pythongame.core.game_state import PlayerState
from pythongame.core.item_inventory import ItemInventorySlot, ItemEquipmentCategory, ITEM_EQUIPMENT_CATEGORY_NAMES
from pythongame.core.math import is_point_in_rect
from pythongame.core.npc_behaviors import DialogGraphics
from pythongame.core.talents import TalentsGraphics
from pythongame.core.view.render_util import DrawableArea, split_text_into_lines
from pythongame.scenes_game.game_ui_state import GameUiState, UiToggle
from pythongame.scenes_game.ui_components import AbilityIcon, ConsumableIcon, ItemIcon, TooltipGraphics, StatBar, \
    ToggleButton, ControlsWindow, StatsWindow, TalentIcon, TalentsWindow

COLOR_WHITE = (250, 250, 250)
COLOR_BLACK = (0, 0, 0)
COLOR_HIGHLIGHTED_ICON = (250, 250, 150)
COLOR_HOVERED_ICON_HIGHLIGHT = (200, 200, 250)
COLOR_HIGHLIGHT_HAS_UNSEEN = (150, 250, 200)
COLOR_BORDER = (139, 69, 19)
COLOR_ITEM_TOOLTIP_HEADER = (250, 250, 150)
UI_ICON_SIZE = (32, 32)
PORTRAIT_ICON_SIZE = (100, 70)

DIR_FONTS = './resources/fonts/'


class MouseHoverEvent:
    def __init__(self, item_slot_number: Optional[int], consumable_slot_number: Optional[int],
                 is_over_ui: bool, ui_toggle: Optional[UiToggle],
                 talent_choice_option: Optional[Tuple[int, int]]):
        self.item_slot_number = item_slot_number
        self.consumable_slot_number = consumable_slot_number
        self.is_over_ui: bool = is_over_ui
        self.ui_toggle = ui_toggle
        self.talent_choice_option = talent_choice_option  # (choice_index, option_index)


class GameUiView:

    def __init__(self, pygame_screen, camera_size: Tuple[int, int], screen_size: Tuple[int, int],
                 images_by_ui_sprite, images_by_portrait_sprite, abilities: List[AbilityType]):
        pygame.font.init()
        self.screen_render = DrawableArea(pygame_screen)
        self.ui_render = DrawableArea(pygame_screen, self._translate_ui_position_to_screen)

        self.ui_screen_area = Rect(0, camera_size[1], screen_size[0], screen_size[1] - camera_size[1])
        self.camera_size = camera_size
        self.screen_size = screen_size

        self.font_splash_screen = pygame.font.Font(DIR_FONTS + 'Arial Rounded Bold.ttf', 64)

        self.font_ui_stat_bar_numbers = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 12)
        self.font_ui_money = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 12)
        self.font_npc_action = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 12)
        self.font_ui_headers = pygame.font.Font(DIR_FONTS + 'Herculanum.ttf', 18)
        self.font_tooltip_header = pygame.font.Font(DIR_FONTS + 'Herculanum.ttf', 16)
        self.font_tooltip_details = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 12)
        self.font_stats = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 9)
        self.font_buff_texts = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 12)
        self.font_message = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 14)
        self.font_debug_info = pygame.font.Font(None, 19)
        self.font_game_world_text = pygame.font.Font(DIR_FONTS + 'Arial Rounded Bold.ttf', 12)
        self.font_game_world_text = pygame.font.Font(None, 19)
        self.font_ui_icon_keys = pygame.font.Font(DIR_FONTS + 'Courier New Bold.ttf', 12)
        self.font_level = pygame.font.Font(DIR_FONTS + 'Courier New Bold.ttf', 11)
        self.font_dialog = pygame.font.Font(DIR_FONTS + 'Merchant Copy.ttf', 24)
        self.font_dialog_option_detail_body = pygame.font.Font(DIR_FONTS + 'Monaco.dfont', 12)

        self.images_by_ui_sprite = images_by_ui_sprite
        self.images_by_portrait_sprite = images_by_portrait_sprite

        # This is updated every time the view is called
        self.camera_world_area = None

        self.ability_icons_row: Rect = Rect(0, 0, 0, 0)
        self.ability_icons: List[AbilityIcon] = []
        self._setup_ability_icons(abilities)

        self.consumable_icons_row: Rect = Rect(0, 0, 0, 0)
        self.consumable_icons: List[ConsumableIcon] = []
        self._setup_consumable_icons({})

        self.inventory_icons_row: Rect = Rect(0, 0, 0, 0)
        self.inventory_icons: List[ItemIcon] = []
        self._setup_inventory_icons([])

        self._setup_health_and_mana_bars(0, 0)

        self._setup_toggle_buttons(False)

        self._setup_stats_window(None, 0)
        self._setup_talents_window(TalentsGraphics([]))
        self._setup_controls_window()

    def _setup_ability_icons(self, abilities):
        x_0 = 140
        y = 112
        icon_space = 2
        icon_rect_padding = 2
        abilities_rect_pos = (x_0 - icon_rect_padding, y - icon_rect_padding)
        max_num_abilities = 5
        self.ability_icons_row = Rect(
            abilities_rect_pos[0], abilities_rect_pos[1],
            (UI_ICON_SIZE[0] + icon_space) * max_num_abilities - icon_space + icon_rect_padding * 2,
            UI_ICON_SIZE[1] + icon_rect_padding * 2)

        self.ability_icons = []
        for i, ability_type in enumerate(abilities):
            x = x_0 + i * (UI_ICON_SIZE[0] + icon_space)
            ability = ABILITIES[ability_type]
            rect = Rect(x, y, UI_ICON_SIZE[0], UI_ICON_SIZE[1])
            image = self.images_by_ui_sprite[ability.icon_sprite]
            label = KEYS_BY_ABILITY_TYPE[ability_type].key_string
            tooltip_details = ["Cooldown: " + str(ability.cooldown / 1000.0) + " s",
                               "Mana: " + str(ability.mana_cost),
                               ability.description]
            tooltip = TooltipGraphics(COLOR_WHITE, ability.name, tooltip_details, bottom_left=(x, y))

            icon = AbilityIcon(self.ui_render, rect, image, label, self.font_ui_icon_keys, tooltip, ability_type)
            self.ability_icons.append(icon)

    def _setup_consumable_icons(self, consumable_slots: Dict[int, List[ConsumableType]]):
        x_0 = 140
        y = 52
        icon_space = 2
        icon_rect_padding = 2
        consumables_rect_pos = (x_0 - icon_rect_padding, y - icon_rect_padding)
        max_num_consumables = 5
        self.consumable_icons_row = Rect(
            consumables_rect_pos[0], consumables_rect_pos[1],
            (UI_ICON_SIZE[0] + icon_space) * max_num_consumables - icon_space + icon_rect_padding * 2,
            UI_ICON_SIZE[1] + icon_rect_padding * 2)

        self.consumable_icons = []
        for i, slot_number in enumerate(consumable_slots):
            x = x_0 + i * (UI_ICON_SIZE[0] + icon_space)
            consumable_types = consumable_slots[slot_number]
            tooltip = None
            image = None
            if consumable_types:
                consumable = CONSUMABLES[consumable_types[0]]
                tooltip = TooltipGraphics(COLOR_WHITE, consumable.name, [consumable.description], bottom_left=(x, y))
                image = self.images_by_ui_sprite[consumable.icon_sprite]
            rect = Rect(x, y, UI_ICON_SIZE[0], UI_ICON_SIZE[1])
            icon = ConsumableIcon(self.ui_render, rect, image, str(slot_number), self.font_ui_icon_keys,
                                  tooltip, consumable_types, slot_number)
            self.consumable_icons.append(icon)

    def _setup_inventory_icons(self, item_slots: List[ItemInventorySlot]):
        x_0 = 325
        y_0 = 52
        icon_space = 2
        icon_rect_padding = 2
        items_rect_pos = (x_0 - icon_rect_padding, y_0 - icon_rect_padding)
        num_item_slot_rows = 3
        num_slots_per_row = 3
        self.inventory_icons_row = Rect(
            items_rect_pos[0], items_rect_pos[1],
            (UI_ICON_SIZE[0] + icon_space) * num_slots_per_row - icon_space + icon_rect_padding * 2,
            num_item_slot_rows * UI_ICON_SIZE[1] + (num_item_slot_rows - 1) * icon_space + icon_rect_padding * 2)

        self.inventory_icons = []
        for i in range(len(item_slots)):
            x = x_0 + (i % num_slots_per_row) * (UI_ICON_SIZE[0] + icon_space)
            y = y_0 + (i // num_slots_per_row) * (UI_ICON_SIZE[1] + icon_space)
            slot = item_slots[i]
            item_type = slot.get_item_type() if not slot.is_empty() else None
            slot_equipment_category = slot.enforced_equipment_category

            image = None
            tooltip = None
            if item_type:
                item = ITEMS[item_type]
                image = self.images_by_ui_sprite[item.icon_sprite]
                tooltip_details = []
                if item.item_equipment_category:
                    category_name = ITEM_EQUIPMENT_CATEGORY_NAMES[item.item_equipment_category]
                    tooltip_details.append("[" + category_name + "]")
                tooltip_details += item.description_lines
                tooltip = TooltipGraphics(COLOR_ITEM_TOOLTIP_HEADER, item.name, tooltip_details,
                                          bottom_left=(x, y))
            elif slot_equipment_category:
                image = self._get_image_for_item_category(slot_equipment_category)
                category_name = ITEM_EQUIPMENT_CATEGORY_NAMES[slot_equipment_category]
                tooltip_details = ["[" + category_name + "]",
                                   "You have nothing equipped. Drag an item here to equip it!"]
                tooltip = TooltipGraphics(COLOR_WHITE, "...", tooltip_details, bottom_left=(x, y))

            rect = Rect(x, y, UI_ICON_SIZE[0], UI_ICON_SIZE[1])
            icon = ItemIcon(self.ui_render, rect, image, tooltip, slot_equipment_category, item_type, i)
            self.inventory_icons.append(icon)

    def _setup_health_and_mana_bars(self, health_regen: float, mana_regen: float):

        rect_healthbar = Rect(20, 111, 100, 14)
        tooltip_details = [
            "regeneration: " + "{:.1f}".format(health_regen) + "/s"]
        health_tooltip = TooltipGraphics(COLOR_WHITE, "Health", tooltip_details,
                                         bottom_left=rect_healthbar.topleft)
        self.healthbar = StatBar(self.ui_render, rect_healthbar, (200, 0, 50), health_tooltip, border=True,
                                 show_numbers=True, font=self.font_ui_stat_bar_numbers)

        rect_manabar = Rect(20, 132, 100, 14)
        tooltip_details = [
            "regeneration: " + "{:.1f}".format(mana_regen) + "/s"]
        mana_tooltip = TooltipGraphics(COLOR_WHITE, "Mana", tooltip_details, bottom_left=rect_manabar.topleft)
        self.manabar = StatBar(self.ui_render, rect_manabar, (50, 0, 200), mana_tooltip, border=True,
                               show_numbers=True, font=self.font_ui_stat_bar_numbers)

    def _setup_toggle_buttons(self, has_unseen_talents: bool):
        x = 555
        y_0 = 30
        w = 120
        h = 20
        font = self.font_tooltip_details
        self.toggle_buttons = [
            ToggleButton(self.ui_render, Rect(x, y_0, w, h), font, "STATS    [A]", UiToggle.STATS, False),
            ToggleButton(self.ui_render, Rect(x, y_0 + 30, w, h), font, "TALENTS  [T]", UiToggle.TALENTS,
                         has_unseen_talents),
            ToggleButton(self.ui_render, Rect(x, y_0 + 60, w, h), font, "CONTROLS [C]", UiToggle.CONTROLS, False)
        ]

    def _setup_stats_window(self, player_state: Optional[PlayerState], player_speed_multiplier: float):
        rect = Rect(545, -300, 140, 250)
        self.stats_window = StatsWindow(self.ui_render, rect, self.font_tooltip_details, self.font_stats, player_state,
                                        player_speed_multiplier)

    def _setup_talents_window(self, talents: TalentsGraphics):
        rect = Rect(545, -300, 140, 260)
        icon_rows = []
        x_0 = rect[0] + 22
        y_0 = rect[1] + 35
        for i, choice_graphics in enumerate(talents.choice_graphics_items):
            y = y_0 + i * (UI_ICON_SIZE[1] + 30)
            y_icon = y + 3
            choice = choice_graphics.choice

            image_1 = self.images_by_ui_sprite[choice.first.ui_icon_sprite]
            tooltip_1 = TooltipGraphics(
                COLOR_WHITE, choice.first.name, [choice.first.description],
                bottom_right=(x_0 + UI_ICON_SIZE[0], y_icon))
            icon_1 = TalentIcon(self.ui_render, Rect(x_0, y_icon, UI_ICON_SIZE[0], UI_ICON_SIZE[1]), image_1,
                                tooltip_1, choice_graphics.chosen_index == 0, choice.first.name, self.font_stats,
                                i, 0)

            image_2 = self.images_by_ui_sprite[choice.second.ui_icon_sprite]
            tooltip_2 = TooltipGraphics(COLOR_WHITE, choice.second.name, [choice.second.description],
                                        bottom_right=(x_0 + UI_ICON_SIZE[0] + 60, y_icon))
            icon_2 = TalentIcon(self.ui_render, Rect(x_0 + 60, y_icon, UI_ICON_SIZE[0], UI_ICON_SIZE[1]), image_2,
                                tooltip_2, choice_graphics.chosen_index == 1, choice.second.name, self.font_stats,
                                i, 1)

            icon_rows.append((icon_1, icon_2))
        self.talents_window = TalentsWindow(self.ui_render, rect, self.font_tooltip_details, self.font_stats, talents,
                                            icon_rows)

    def _setup_controls_window(self):
        rect = Rect(545, -300, 140, 170)
        self.controls_window = ControlsWindow(self.ui_render, rect, self.font_tooltip_details, self.font_stats)

    def update_abilities(self, abilities: List[AbilityType]):
        self._setup_ability_icons(abilities)

    def update_consumables(self, consumable_slots: Dict[int, List[ConsumableType]]):
        self._setup_consumable_icons(consumable_slots)

    def update_inventory(self, item_slots: List[ItemInventorySlot]):
        self._setup_inventory_icons(item_slots)

    def update_regen(self, health_regen: float, mana_regen: float):
        self._setup_health_and_mana_bars(health_regen, mana_regen)

    def update_has_unseen_talents(self, has_unseen_talents: bool):
        self._setup_toggle_buttons(has_unseen_talents)

    def update_talents(self, talents: TalentsGraphics):
        self._setup_talents_window(talents)

    def update_player_stats(self, player_state: PlayerState, player_speed_multiplier: float):
        self._setup_stats_window(player_state, player_speed_multiplier)

    def _translate_ui_position_to_screen(self, position):
        return position[0] + self.ui_screen_area.x, position[1] + self.ui_screen_area.y

    def _translate_screen_position_to_ui(self, position: Tuple[int, int]):
        return position[0] - self.ui_screen_area.x, position[1] - self.ui_screen_area.y

    def _get_image_for_item_category(self, slot_equipment_category: ItemEquipmentCategory):
        if slot_equipment_category == ItemEquipmentCategory.HEAD:
            ui_icon_sprite = UiIconSprite.INVENTORY_TEMPLATE_HELMET
        elif slot_equipment_category == ItemEquipmentCategory.CHEST:
            ui_icon_sprite = UiIconSprite.INVENTORY_TEMPLATE_CHEST
        elif slot_equipment_category == ItemEquipmentCategory.MAIN_HAND:
            ui_icon_sprite = UiIconSprite.INVENTORY_TEMPLATE_MAINHAND
        elif slot_equipment_category == ItemEquipmentCategory.OFF_HAND:
            ui_icon_sprite = UiIconSprite.INVENTORY_TEMPLATE_OFFHAND
        elif slot_equipment_category == ItemEquipmentCategory.NECK:
            ui_icon_sprite = UiIconSprite.INVENTORY_TEMPLATE_NECK
        elif slot_equipment_category == ItemEquipmentCategory.RING:
            ui_icon_sprite = UiIconSprite.INVENTORY_TEMPLATE_RING
        else:
            raise Exception("Unhandled equipment category: " + str(slot_equipment_category))
        return self.images_by_ui_sprite[ui_icon_sprite]

    def _minimap_in_ui(self, position_in_ui, size, player_relative_position):
        rect = Rect(position_in_ui[0], position_in_ui[1], size[0], size[1])
        self.ui_render.rect_filled((40, 40, 50), rect)
        self.ui_render.rect((150, 150, 190), rect, 1)
        dot_x = rect[0] + player_relative_position[0] * size[0]
        dot_y = rect[1] + player_relative_position[1] * size[1]
        dot_w = 4
        self.ui_render.rect_filled((100, 160, 100), Rect(dot_x - dot_w / 2, dot_y - dot_w / 2, dot_w, dot_w))

    def _message(self, message):
        w_rect = len(message) * 9 + 10
        x_message = self.ui_screen_area.w / 2 - w_rect / 2
        y_message = self.ui_screen_area.y - 30
        self.screen_render.rect_transparent(Rect(x_message - 10, y_message - 5, w_rect, 28), 135, (0, 0, 0))
        self.screen_render.text(self.font_message, message, (x_message, y_message))

    def _tooltip(self, tooltip: TooltipGraphics):

        detail_lines = []
        detail_max_line_length = 32
        for detail in tooltip.details:
            detail_lines += split_text_into_lines(detail, detail_max_line_length)

        w_tooltip = 260
        h_tooltip = 60 + 17 * len(detail_lines)
        if tooltip.bottom_left_corner is not None:
            bottom_left_corner = tooltip.bottom_left_corner
        else:
            bottom_left_corner = (tooltip.bottom_right_corner[0] - w_tooltip, tooltip.bottom_right_corner[1])
        x_tooltip = bottom_left_corner[0]
        y_tooltip = bottom_left_corner[1] - h_tooltip - 3
        rect_tooltip = Rect(x_tooltip, y_tooltip, w_tooltip, h_tooltip)
        self.ui_render.rect_transparent(Rect(x_tooltip, y_tooltip, w_tooltip, h_tooltip), 200, (0, 0, 30))
        self.ui_render.rect(COLOR_WHITE, rect_tooltip, 1)
        self.ui_render.text(self.font_tooltip_header, tooltip.title, (x_tooltip + 20, y_tooltip + 15),
                            tooltip.title_color)
        y_separator = y_tooltip + 40
        self.ui_render.line(COLOR_WHITE, (x_tooltip + 10, y_separator), (x_tooltip + w_tooltip - 10, y_separator),
                            1)

        for i, line in enumerate(detail_lines):
            self.ui_render.text(self.font_tooltip_details, line, (x_tooltip + 20, y_tooltip + 50 + i * 18),
                                COLOR_WHITE)

    def _player_portrait(self, hero_id: HeroId, ui_position: Tuple[int, int]):
        portrait_sprite = HEROES[hero_id].portrait_icon_sprite
        player_portrait_image = self.images_by_portrait_sprite[portrait_sprite]
        self.ui_render.image(player_portrait_image, ui_position)
        rect = Rect(ui_position[0], ui_position[1], PORTRAIT_ICON_SIZE[0], PORTRAIT_ICON_SIZE[1])
        self.ui_render.rect((160, 160, 180), rect, 2)

    def _dialog(self, dialog_graphics: DialogGraphics):

        tall_detail_section = any(
            [o.detail_body is not None or o.detail_header is not None or o.detail_ui_icon_sprite is not None
             for o in dialog_graphics.options])

        h_detail_section_expansion = 82

        options_margin = 10
        option_padding = 4
        h_option_line = 20
        if tall_detail_section:
            h_dialog_container = 310 + len(dialog_graphics.options) * (h_option_line + 2 * option_padding)
        else:
            h_dialog_container = 310 + len(dialog_graphics.options) * (h_option_line + 2 * option_padding) \
                                 - h_detail_section_expansion
        rect_dialog_container = Rect(100, 35, 500, h_dialog_container)

        x_left = rect_dialog_container[0]
        x_right = rect_dialog_container[0] + rect_dialog_container[2]
        self.screen_render.rect((210, 180, 60), rect_dialog_container, 5)
        self.screen_render.rect_transparent(rect_dialog_container, 200, COLOR_BLACK)
        color_separator = (170, 140, 20)
        dialog_container_portrait_padding = 10
        rect_portrait_pos = (x_left + dialog_container_portrait_padding,
                             rect_dialog_container[1] + dialog_container_portrait_padding)
        dialog_image = self.images_by_portrait_sprite[dialog_graphics.portrait_icon_sprite]
        self.screen_render.image(dialog_image, rect_portrait_pos)
        rect_portrait = Rect(rect_portrait_pos[0], rect_portrait_pos[1], PORTRAIT_ICON_SIZE[0], PORTRAIT_ICON_SIZE[1])
        self.screen_render.rect((160, 160, 180), rect_portrait, 2)

        dialog_pos = (x_left + 120, rect_dialog_container[1] + 15)
        dialog_lines = split_text_into_lines(dialog_graphics.text_body, 35)
        for i, dialog_text_line in enumerate(dialog_lines):
            if i == 6:
                print("WARN: too long dialog for NPC!")
                break
            self.screen_render.text(self.font_dialog, dialog_text_line, (dialog_pos[0] + 5, dialog_pos[1] + 32 * i),
                                    COLOR_WHITE)

        y_above_options = dialog_pos[1] + 150
        self.screen_render.line(color_separator, (x_left, y_above_options), (x_right, y_above_options), 2)

        for i, option in enumerate(dialog_graphics.options):
            x_option = x_left + 8
            y_option = y_above_options + options_margin + i * (h_option_line + 2 * option_padding)
            x_option_text = x_option + option_padding + 5
            y_option_text = y_option + option_padding + 2
            color_highlight = COLOR_WHITE

            is_option_active = dialog_graphics.active_option_index == i
            color_option_text = COLOR_WHITE if is_option_active else (160, 160, 160)
            if is_option_active:
                rect_highlight_active_option = Rect(
                    x_option, y_option, rect_dialog_container[2] - 16, h_option_line + 2 * option_padding)
                self.screen_render.rect_transparent(rect_highlight_active_option, 120, COLOR_WHITE)
                self.screen_render.rect(color_highlight, rect_highlight_active_option, 1)
            self.screen_render.text(self.font_dialog, option.summary, (x_option_text, y_option_text), color_option_text)

        active_option = dialog_graphics.options[dialog_graphics.active_option_index]
        y_under_options = y_above_options + 2 * options_margin \
                          + len(dialog_graphics.options) * (h_option_line + 2 * option_padding)
        self.screen_render.line(color_separator, (x_left, y_under_options), (x_right, y_under_options), 2)

        if tall_detail_section:
            y_action_text = y_under_options + 15 + h_detail_section_expansion
        else:
            y_action_text = y_under_options + 15

        if tall_detail_section:
            if active_option.detail_ui_icon_sprite is not None:
                active_option_image = self.images_by_ui_sprite[active_option.detail_ui_icon_sprite]
                pos_option_image = x_left + 6, y_under_options + 7
                self.screen_render.image(active_option_image, pos_option_image)
                rect_option_image = Rect(pos_option_image[0], pos_option_image[1], UI_ICON_SIZE[0], UI_ICON_SIZE[1])
                self.screen_render.rect((150, 150, 150), rect_option_image, 1)
            if active_option.detail_header is not None:
                self.screen_render.text(self.font_dialog, active_option.detail_header,
                                        (x_left + 14 + UI_ICON_SIZE[0] + 4, y_action_text - h_detail_section_expansion))
            if active_option.detail_body is not None:
                detail_body_lines = split_text_into_lines(active_option.detail_body, 70)
                for i, line in enumerate(detail_body_lines):
                    line_pos = (x_left + 10, y_action_text - h_detail_section_expansion + 35 + 20 * i)
                    self.screen_render.text(self.font_dialog_option_detail_body, line, line_pos)
        action_text = active_option.detail_action_text
        self.screen_render.text(self.font_dialog, "[Space] : " + action_text, (x_left + 10, y_action_text))

    def render_item_being_dragged(self, item_type: ItemType, mouse_screen_position: Tuple[int, int]):
        ui_icon_sprite = ITEMS[item_type].icon_sprite
        position = (mouse_screen_position[0] - UI_ICON_SIZE[0] // 2, mouse_screen_position[1] - UI_ICON_SIZE[1] // 2)
        self.screen_render.image(self.images_by_ui_sprite[ui_icon_sprite], position)

    def render_consumable_being_dragged(self, consumable_type: ConsumableType, mouse_screen_position: Tuple[int, int]):
        ui_icon_sprite = CONSUMABLES[consumable_type].icon_sprite
        position = (mouse_screen_position[0] - UI_ICON_SIZE[0] // 2, mouse_screen_position[1] - UI_ICON_SIZE[1] // 2)
        self.screen_render.image(self.images_by_ui_sprite[ui_icon_sprite], position)

    def _splash_screen_text(self, text, x, y):
        self.screen_render.text(self.font_splash_screen, text, (x, y), COLOR_WHITE)
        self.screen_render.text(self.font_splash_screen, text, (x + 2, y + 2), COLOR_BLACK)

    def render_ui(
            self,
            player_state: PlayerState,
            ui_state: GameUiState,
            text_in_topleft_corner: str,
            is_paused: bool,
            mouse_screen_position: Tuple[int, int],
            dialog: Optional[DialogGraphics]) -> MouseHoverEvent:

        player_health = player_state.health_resource.value
        player_max_health = player_state.health_resource.max_value
        player_max_mana = player_state.mana_resource.max_value
        player_mana = player_state.mana_resource.value
        player_active_buffs = player_state.active_buffs
        ability_cooldowns_remaining = player_state.ability_cooldowns_remaining
        player_exp = player_state.exp
        player_max_exp_in_this_level = player_state.max_exp_in_this_level
        player_level = player_state.level
        player_money = player_state.money
        hero_id = player_state.hero_id

        player_minimap_relative_position = ui_state.player_minimap_relative_position
        message = ui_state.message
        highlighted_consumable_action = ui_state.highlighted_consumable_action
        highlighted_ability_action = ui_state.highlighted_ability_action

        hovered_item_slot_number = None
        hovered_consumable_slot_number = None
        hovered_ui_toggle = None
        hovered_talent_option: Optional[Tuple[int, int]] = None
        is_mouse_hovering_ui = is_point_in_rect(mouse_screen_position, self.ui_screen_area)

        mouse_ui_position = self._translate_screen_position_to_ui(mouse_screen_position)
        tooltip: Optional[TooltipGraphics] = None
        self.screen_render.rect(COLOR_BORDER, Rect(0, 0, self.camera_size[0], self.camera_size[1]), 1)
        self.screen_render.rect_filled((20, 10, 0), Rect(0, self.camera_size[1], self.screen_size[0],
                                                         self.screen_size[1] - self.camera_size[1]))

        y_0 = 5

        y_1 = 30
        y_2 = y_1 + 22
        y_3 = 90
        y_4 = y_3 + 22

        x_1 = 140

        x_exp_bar = x_1
        self.ui_render.text(self.font_level, "Level " + str(player_level), (x_exp_bar, y_0))
        self.ui_render.stat_bar(x_exp_bar, y_0 + 18, 380, 2, player_exp / player_max_exp_in_this_level,
                                (200, 200, 200),
                                True)

        x_0 = 20

        self._player_portrait(hero_id, (x_0, y_0 + 13))

        # HEALTHBAR
        self.healthbar.render(player_health, player_max_health)
        if self.healthbar.contains(mouse_ui_position):
            tooltip = self.healthbar.tooltip

        # MANABAR
        self.manabar.render(player_mana, player_max_mana)
        if self.manabar.contains(mouse_ui_position):
            tooltip = self.manabar.tooltip

        # MONEY
        self.ui_render.text(self.font_ui_money, "Money: " + str(player_money), (x_0 + 4, y_4 + 38))

        # CONSUMABLES
        self.ui_render.rect_filled((60, 60, 80), self.consumable_icons_row)
        for icon in self.consumable_icons:
            hovered = icon.contains(mouse_ui_position)
            if hovered:
                hovered_consumable_slot_number = icon.slot_number
                if icon.tooltip:
                    tooltip = icon.tooltip
            strong_highlight = icon.slot_number == highlighted_consumable_action
            icon.render(hovered, strong_highlight)

        # ABILITIES
        self.ui_render.rect_filled((60, 60, 80), self.ability_icons_row)
        for icon in self.ability_icons:
            hovered = icon.contains(mouse_ui_position)
            if hovered:
                tooltip = icon.tooltip
            ability_type = icon.ability_type
            ability = ABILITIES[ability_type]
            cooldown_remaining_ratio = ability_cooldowns_remaining[ability_type] / ability.cooldown
            recently_clicked = ability_type == highlighted_ability_action
            icon.render(hovered, recently_clicked, cooldown_remaining_ratio)

        # ITEMS
        self.ui_render.rect_filled((60, 60, 80), self.inventory_icons_row)
        for icon in self.inventory_icons:
            hovered = icon.contains(mouse_ui_position)
            if hovered:
                hovered_item_slot_number = icon.inventory_slot_index
                tooltip = icon.tooltip
            icon.render(hovered)

        # MINIMAP
        x_3 = 440
        minimap_padding_rect_pos = (x_3 - 2, y_2 - 2)
        minimap_padding_rect = Rect(minimap_padding_rect_pos[0], minimap_padding_rect_pos[1], 80 + 4, 80 + 4)
        self.ui_render.rect_filled((60, 60, 80), minimap_padding_rect)
        self._minimap_in_ui((x_3, y_2), (80, 80), player_minimap_relative_position)

        if dialog:
            self._dialog(dialog)

        # BUFFS
        x_buffs = 10
        buff_texts = []
        buff_duration_ratios_remaining = []
        for active_buff in player_active_buffs:
            buff_type = active_buff.buff_effect.get_buff_type()
            # Buffs that don't have description texts shouldn't be displayed. (They are typically irrelevant to the
            # player)
            if buff_type in BUFF_TEXTS:
                buff_texts.append(BUFF_TEXTS[buff_type])
                buff_duration_ratios_remaining.append(active_buff.get_ratio_duration_remaining())
        num_buffs_to_render = len(buff_texts)
        y_buffs = -35 - (num_buffs_to_render - 1) * 25
        buffs_ui_position = (x_buffs, y_buffs)
        if num_buffs_to_render:
            rect_padding = 5
            # Note: The width of this rect is hard-coded so long buff descriptions aren't well supported
            buffs_background_rect = Rect(
                buffs_ui_position[0] - rect_padding,
                buffs_ui_position[1] - rect_padding,
                140 + rect_padding * 2,
                num_buffs_to_render * 25 + rect_padding * 2)
            self.ui_render.rect_transparent(buffs_background_rect, 125, COLOR_BLACK)
        for i, text in enumerate(buff_texts):
            y_offset_buff = i * 25
            y = y_buffs + y_offset_buff
            self.ui_render.text(self.font_buff_texts, text, (x_buffs, y))
            self.ui_render.stat_bar(x_buffs, y + 20, 60, 2, buff_duration_ratios_remaining[i],
                                    (250, 250, 0), False)

        # TOGGLES
        if ui_state.toggle_enabled == UiToggle.STATS:
            self.stats_window.render()
        elif ui_state.toggle_enabled == UiToggle.TALENTS:
            hovered_talent_icon = self.talents_window.get_icon_containing(mouse_ui_position)
            if hovered_talent_icon:
                tooltip = hovered_talent_icon.tooltip
                hovered_talent_option = (hovered_talent_icon.choice_index, hovered_talent_icon.option_index)
            self.talents_window.render(hovered_talent_icon)
        elif ui_state.toggle_enabled == UiToggle.CONTROLS:
            self.controls_window.render()

        for toggle_button in self.toggle_buttons:
            hovered = toggle_button.contains(mouse_ui_position)
            enabled = ui_state.toggle_enabled == toggle_button.toggle_id
            toggle_button.render(enabled, hovered)
            if hovered:
                hovered_ui_toggle = toggle_button.toggle_id

        self.screen_render.rect(COLOR_BORDER, self.ui_screen_area, 1)

        self.screen_render.rect_transparent(Rect(0, 0, 70, 20), 100, COLOR_BLACK)
        self.screen_render.text(self.font_debug_info, text_in_topleft_corner, (5, 3))

        if message:
            self._message(message)

        if tooltip:
            self._tooltip(tooltip)

        if is_paused:
            self.screen_render.rect_transparent(Rect(0, 0, self.screen_size[0], self.screen_size[1]), 140, COLOR_BLACK)
            self._splash_screen_text("PAUSED", self.screen_size[0] / 2 - 110, self.screen_size[1] / 2 - 50)

        return MouseHoverEvent(hovered_item_slot_number, hovered_consumable_slot_number, is_mouse_hovering_ui,
                               hovered_ui_toggle, hovered_talent_option)
