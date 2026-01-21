import math

def inches_to_meters(input:float) -> float:
    """ Input in inches returns meters """
    return input*0.0254

def remap(value: float, threshold: float) -> float:
    if abs(value) > threshold:
        value = value / abs(value) * threshold
    return value

def deadband(value: float, threshold: float) -> float:
    if abs(value) < threshold:
        value = 0
    return value

def max_min_check(value, goal, tolerance) -> bool:
    if abs(goal - value) < tolerance:
        return True
    else:
        return False

