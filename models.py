class User:
    def __init__(self, id, username, karma=0):
        self.id = id
        self.username = username
        self.karma = karma

    def update_karma(self, points):
        self.karma = max(0, self.karma + points)

    def get_tree_level(self):
        if self.karma < 100:
            return "🌱 Росток"
        elif self.karma < 300:
            return "🌿 Куст"
        elif self.karma < 500:
            return "🌳 Дерево"
        return "🌲 Могучее древо"