from engine.optimizer import QueryOptimizer

def run_optimizer(facts):
    optimizer = QueryOptimizer()
    return optimizer.analyze(facts)
