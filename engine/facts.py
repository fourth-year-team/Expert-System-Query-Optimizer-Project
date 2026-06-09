from experta import Fact

class RecommendationFact(Fact):
    recommendation_id: int
    category: str
    recommendation_text: str
    reasoning: str
    priority: str
    expected_improvement: str
    applies_to: str
