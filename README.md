# Scripts

Run `/game.py` for an interactive execution of chess where the user is asked to input the moves for both sides.

Run `/main.py` for a non-interactive execution of chess where an engine calculates the moves for both sides. Requires an implementation of an [engine](#engines) and of an [evaluator](#evaluators).

Run `/test.py` to run logic in specific positions. Best used for debugging purposes. Requires an implementation of an [engine](#engines) and of an [evaluator](#evaluators).

# Engines

They use an evaluator to calculate the best move in a position. They should extend the classes `Evaluator` or `MemoryEvaluator` in `/domain/engine/engine.py` and implement the abstract method.

# Evaluators

They evaluate a position and assign a numeric score to it. They should Extend the class `Evaluator` in `/domain/evaluator/evaluator.py` and implement the abstract method.

