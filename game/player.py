class Player:
    def __init__(self, name, avatar="warrior"):
        self.name = name
        self.avatar = avatar
        self.hp = 100
        self.max_hp = 100

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        return self.hp > 0