import random

class Enemy:
    def __init__(self, name, hp, damage_range, image_path):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage_range = damage_range
        self.image_path = image_path

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def is_alive(self):
        return self.hp > 0

    def attack(self, players):
        alive_players = [p for p in players if p.is_alive()]
        if alive_players:
            target = random.choice(alive_players)
            dmg = random.randint(*self.damage_range)
            target.take_damage(dmg)
            return f"{self.name} attacks {target.name} for {dmg} hit points!"
        return ""


ENEMY_POOL = [
    Enemy("Goblin", 60, (5, 15), "assets/enemies/goblin.png"),
    Enemy("Skeleton", 50,  (10, 15), "assets/enemies/skeleton.png"),
    Enemy("Ghost", 40, (15, 20), "assets/enemies/ghost.png"),
    Enemy("Beholder", 60, (15, 30), "assets/enemies/beholder.png"),
    Enemy("Troll", 140, (15, 20), "assets/enemies/troll.png"),
    Enemy("Vampire", 80, (25, 35), "assets/enemies/vampire.png"),
    Enemy("Demon", 160, (20, 30), "assets/enemies/demon.png"),
    Enemy("Dragon", 180, (25, 40), "assets/enemies/dragon.png")
]
