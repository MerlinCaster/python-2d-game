from enum import Enum
from typing import Optional, List, Any

from pythongame.core.common import ItemType


class ItemEquipmentCategory(Enum):
    CHEST = 1
    MAIN_HAND = 2
    OFF_HAND = 3
    HEAD = 4
    NECK = 5
    RING = 6


ITEM_EQUIPMENT_CATEGORY_NAMES = {
    ItemEquipmentCategory.CHEST: "Chest",
    ItemEquipmentCategory.MAIN_HAND: "Main-Hand",
    ItemEquipmentCategory.OFF_HAND: "Off-Hand",
    ItemEquipmentCategory.HEAD: "Head",
    ItemEquipmentCategory.NECK: "Neck",
    ItemEquipmentCategory.RING: "Ring",
}


class ItemActivationEvent:
    pass


class ItemWasActivated(ItemActivationEvent):
    def __init__(self, item_type: ItemType):
        self.item_type = item_type


class ItemWasDeactivated(ItemActivationEvent):
    def __init__(self, item_type: ItemType):
        self.item_type = item_type


class ItemActivationStateDidNotChange(ItemActivationEvent):
    def __init__(self, item_type: ItemType):
        self.item_type = item_type


class ItemInSlot:
    def __init__(self, item_effect, item_equipment_category: ItemEquipmentCategory):
        self.item_effect = item_effect
        self.item_equipment_category = item_equipment_category


class ItemInventorySlot:
    def __init__(self, item: Optional[ItemInSlot], enforced_equipment_category: Optional[ItemEquipmentCategory]):
        self.item = item
        self.enforced_equipment_category = enforced_equipment_category

    def is_empty(self) -> bool:
        return self.item is None

    def can_contain_item(self, item: Optional[ItemInSlot]):
        if not self.enforced_equipment_category or not item:
            return True
        return item.item_equipment_category == self.enforced_equipment_category

    # Putting an item in an 'active' inventory slot enables the effect of that item.
    # Moving it to a slot that is not 'active', removes the effect
    # Slots that are not 'active' simply serve as storage
    def is_active(self) -> bool:
        return self.enforced_equipment_category is not None

    def get_item_type(self) -> ItemType:
        return self.item.item_effect.get_item_type()


class ItemInventory:
    def __init__(self, slots: List[ItemInventorySlot]):
        self.slots = slots

    def switch_item_slots(self, slot_1_index: int, slot_2_index: int) -> List[ItemActivationEvent]:
        slot_1 = self.slots[slot_1_index]
        slot_2 = self.slots[slot_2_index]
        content_1 = slot_1.item
        content_2 = slot_2.item
        events = []
        is_switch_allowed = slot_2.can_contain_item(content_1) and slot_1.can_contain_item(content_2)
        if is_switch_allowed:
            if content_1:
                item_type_1 = slot_1.get_item_type()
                if slot_1.is_active() and not slot_2.is_active():
                    event_1 = ItemWasDeactivated(item_type_1)
                elif not slot_1.is_active() and slot_2.is_active():
                    event_1 = ItemWasActivated(item_type_1)
                else:
                    event_1 = ItemActivationStateDidNotChange(item_type_1)
                events.append(event_1)
            if content_2:
                item_type_2 = slot_2.get_item_type()
                if slot_2.is_active() and not slot_1.is_active():
                    event_2 = ItemWasDeactivated(item_type_2)
                elif not slot_2.is_active() and slot_1.is_active():
                    event_2 = ItemWasActivated(item_type_2)
                else:
                    event_2 = ItemActivationStateDidNotChange(item_type_2)
                events.append(event_2)
            slot_1.item = content_2
            slot_2.item = content_1
        return events

    def has_item_in_inventory(self, item_type: ItemType):
        matches = [slot for slot in self.slots if not slot.is_empty() and slot.get_item_type() == item_type]
        if len(matches) > 0:
            return True

    # Note: this will need to return events, if it's used for items that have effects
    def lose_item_from_inventory(self, item_type: ItemType):
        for slot_number in range(len(self.slots)):
            slot = self.slots[slot_number]
            if not slot.is_empty() and slot.get_item_type() == item_type:
                self.slots[slot_number].item = None
                return
        print("WARN: item not found in inventory: " + item_type.name)

    def is_slot_empty(self, slot_index: int) -> bool:
        return self.slots[slot_index].is_empty()

    def try_add_item(self, item_effect, item_equipment_category: ItemEquipmentCategory) \
            -> Optional[ItemActivationEvent]:
        item_in_slot = ItemInSlot(item_effect, item_equipment_category)
        empty_slot_index = self._find_empty_slot_for_item(item_in_slot)
        if empty_slot_index is not None:
            slot = self.slots[empty_slot_index]
            slot.item = item_in_slot
            if slot.is_active():
                return ItemWasActivated(item_effect.get_item_type())
            else:
                return ItemActivationStateDidNotChange(item_effect.get_item_type())
        return None

    def put_item_in_inventory_slot(self, item_effect, item_equipment_category: ItemEquipmentCategory, slot_number: int):
        item_in_slot = ItemInSlot(item_effect, item_equipment_category)
        slot = self.slots[slot_number]
        if not slot.is_empty():
            raise Exception("Can't put item in non-empty slot!")
        slot.item = item_in_slot
        if slot.is_active():
            return ItemWasActivated(item_effect.get_item_type())
        else:
            return ItemActivationStateDidNotChange(item_effect.get_item_type())

    def _find_empty_slot_for_item(self, item: ItemInSlot) -> Optional[int]:
        empty_slot_indices = [i for i in range(len(self.slots))
                              if self.slots[i].is_empty() and self.slots[i].can_contain_item(item)]
        if empty_slot_indices:
            return empty_slot_indices[0]
        return None

    def get_item_type_in_slot(self, slot_index: int) -> ItemType:
        if self.slots[slot_index].is_empty():
            raise Exception("Can't get item type from empty inventory slot: " + str(slot_index))
        return self.slots[slot_index].get_item_type()

    def remove_item_from_slot(self, slot_index: int) -> ItemActivationEvent:
        slot = self.slots[slot_index]
        if slot.is_empty():
            raise Exception("Can't remove item from empty inventory slot: " + str(slot_index))
        item_type = slot.get_item_type()
        slot.item = None
        if slot.is_active():
            return ItemWasDeactivated(item_type)
        return ItemActivationStateDidNotChange(item_type)

    def get_all_active_item_effects(self) -> List[Any]:
        return [slot.item.item_effect for slot in self.slots if slot.is_active() and not slot.is_empty()]