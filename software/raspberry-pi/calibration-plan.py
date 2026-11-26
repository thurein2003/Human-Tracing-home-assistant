"""Calculate and record a one-axis dry-run sweep without accessing GPIO."""
import argparse
from decimal import Decimal


def plan(low, neutral, high, step):
    if not all(value.is_finite() for value in (low, neutral, high, step)):
        raise ValueError("Use finite angles")
    if not 0 <= low <= neutral <= high <= 180 or not 0 < step <= 5:
        raise ValueError("Require 0 <= low <= neutral <= high <= 180 and 0 < step <= 5")
    if (high - low) / step > 100:
        raise ValueError("Limit the plan to 100 increments per traversal")
    positions = [neutral]
    for target, direction in ((low, -1), (neutral, 1), (high, 1), (neutral, -1)):
        while positions[-1] != target:
            distance = min(step, abs(target - positions[-1]))
            positions.append(positions[-1] + direction * distance)
    return positions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("axis", choices=("pan", "tilt"))
    for name in ("low", "neutral", "high", "step"):
        parser.add_argument(name, type=Decimal)
    args = parser.parse_args()
    try:
        positions = plan(args.low, args.neutral, args.high, args.step)
    except ValueError as error:
        parser.error(str(error))
    print(args.axis, "planned commanded angles:", ", ".join(map(str, positions)))


if __name__ == "__main__":
    main()
