from typing import List, Any, Dict

from interfaces.Constraint import Constraint

class TimeConstraint(Constraint):
    def __init__(self, variables: List[str], min_time: int, max_time: int):
        super().__init__(variables)
        self.min_time = min_time
        self.max_time = max_time
        if variables[-1] != variables[0]:
            self.expression = f"{min_time} <= {variables[-1]} - {variables[0]} <= {max_time}"
        else:
            self.expression = f"{min_time} <= {variables[0]}[i] - {variables[0]}[0] <= {max_time}"

    def validate(self, event, context) -> bool:
        first_variables = self.variables[0]
        first_event = context.get_events_for_pattern(first_variables)
        try:
            time = event.timestamp
            if len(first_event) > 0:
                time_span = time - first_event[0].timestamp
            else:
                # 可能获取之前的模式有问题，先暴力用starttimestamp代替
                time_span = time - context.computation_state.start_timestamp
            return self.min_time <= time_span <= self.max_time
        except Exception as e:
            print(f"Validation error: {e}")
            return False

    def __eq__(self, other):
        if isinstance(other, TimeConstraint):
            return (self.variables == other.variables and
                    self.min_time == other.min_time and
                    self.max_time == other.max_time)
        return False

    def __hash__(self):
        return hash((tuple(self.variables), self.min_time, self.max_time))

    def __str__(self):
        return (f"TimeConstraint(variables={self.variables}, "
                f"min_time={self.min_time}, max_time={self.max_time}, "
                f"expression='{self.expression}')")