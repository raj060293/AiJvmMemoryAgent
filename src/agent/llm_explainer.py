
class LLMExplainer:
    def explain(self, issues):
        explanations = []
        for issue in issues:
            explanations.append(
                f"{issue.name}: Heap usage is critically high"
            )
        return explanations