
from enum import Enum

Allignment = Enum('Allignment', 'Townsfolk Outsider Minion Demon') #Could add traveler later

class BotcCharacter:
    def __init__(self, name, priority=0, allignment=Allignment.Townsfolk):
        self.name = name
        self.night_priority = priority
        self.allignment = allignment

        self.is_evil = allignment in (Allignment.Minion, Allignment.Demon)

    def __str__(self):
        return self.name
    
class TestCharacter1(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 1", priority=1, allignment=Allignment.Townsfolk)

class TestCharacter2(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 2", priority=2, allignment=Allignment.Townsfolk)

class TestCharacter3(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 3", priority=3, allignment=Allignment.Townsfolk)

class TestCharacter4(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 4", priority=4, allignment=Allignment.Townsfolk)

class TestCharacter5(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 5", priority=5, allignment=Allignment.Townsfolk)

class TestCharacter6(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 6", priority=6, allignment=Allignment.Townsfolk)

class TestCharacter7(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 7", priority=7, allignment=Allignment.Minion)

class TestCharacter8(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 8", priority=8, allignment=Allignment.Demon)

class TestCharacter9(BotcCharacter):
    def __init__(self):
        super().__init__("Test Character 9", priority=9, allignment=Allignment.Townsfolk)

test_script = [TestCharacter1(), TestCharacter2(), TestCharacter3(), TestCharacter4(), TestCharacter5(), TestCharacter6(), TestCharacter7(), TestCharacter8(), TestCharacter9()]