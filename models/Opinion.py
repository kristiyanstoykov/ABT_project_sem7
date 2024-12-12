class Opinion:
    """
    Represents a client's opinion about a specific shop.
    """
    def __init__(self, shop_id, initial_score=0.0):
        self.shop_id = shop_id
        self.score = initial_score
        self.history = [] 

    def adjust_score(self, change, reason=""):
        previous_score = self.score
        self.score += change
        # Ensure the score remains within a range
        self.score = max(-10.0, min(10.0, self.score))  # score between -10 and 10

        # Log the change in the history
        self.history.append({
            "previous_score": previous_score,
            "new_score": self.score,
            "change": change,
            "reason": reason
        })

    def get_score(self):
        return self.score

    def get_history(self):
        return self.history

    def __str__(self):
        return f"Opinion for Shop {self.shop_id}: {self.score}"
