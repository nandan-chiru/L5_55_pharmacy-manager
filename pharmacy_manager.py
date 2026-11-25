"""Simple pharmacy stock and prescription management program."""

import ast
import hashlib
import json
import os
import secrets
from datetime import date, datetime

# Global pharmacy state.
medicines = {}


def add_medicine(
    name, qty=0, price=0.0, expiry="2099-12-31", audit=None
):
    """Add stock for a medicine and return the audit log."""
    if not isinstance(name, str) or not name:
        return [] if audit is None else audit

    if qty < 0:
        raise ValueError("Medicine quantity cannot be negative.")

    if price < 0:
        raise ValueError("Medicine price cannot be negative.")

    if audit is None:
        audit = []

    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }

    medicines[name]["qty"] += qty
    audit.append(
        f"{datetime.now()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name, qty):
    """Dispense a quantity of medicine if sufficient stock exists."""
    if name not in medicines or qty <= 0:
        return False

    if medicines[name]["qty"] < qty:
        return False

    medicines[name]["qty"] -= qty
    return True


def get_quantity(name):
    """Return the current quantity of a medicine."""
    return medicines[name]["qty"]


def is_expired(name):
    """Return True when the medicine has passed its expiry date."""
    expiry_date = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry_date < date.today()


def bill_amount(prescription):
    """Calculate the total price for a prescription."""
    total = 0.0

    for item in prescription:
        medicine_name, quantity = item
        total += medicines[medicine_name]["price"] * quantity

    return total


def _evaluate_arithmetic(node):
    """Safely evaluate a basic arithmetic expression."""
    operators = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a**b,
    }

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp) and type(node.op) in operators:
        left = _evaluate_arithmetic(node.left)
        right = _evaluate_arithmetic(node.right)
        return operators[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, (ast.UAdd, ast.USub)):
            value = _evaluate_arithmetic(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

    raise ValueError("Only basic arithmetic expressions are allowed.")


def calculate_dosage(formula):
    """Safely calculate a dosage from basic arithmetic."""
    tree = ast.parse(formula, mode="eval")
    return _evaluate_arithmetic(tree.body)


def patient_id(name, phone):
    """Generate a deterministic patient identifier using SHA-256."""
    data = (name + phone).encode()
    return hashlib.sha256(data).hexdigest()


def generate_rx_number():
    """Generate a six-digit prescription number."""
    number = secrets.randbelow(900000) + 100000
    return f"RX-{number}"


def save_stock(file="pharmacy.json"):
    """Save pharmacy stock as JSON."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=2)


def load_stock(file="pharmacy.json"):
    """Load pharmacy stock from a JSON file."""
    with open(file, "r", encoding="utf-8") as stock_file:
        loaded_stock = json.load(stock_file)

    medicines.clear()
    medicines.update(loaded_stock)


def print_label(name):
    """Print a dispensing label."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    result = []

    for medicine in medicines:
        expiry_date = datetime.strptime(
            medicines[medicine]["expiry"], "%Y-%m-%d"
        ).date()

        if (expiry_date - date.today()).days < days:
            result.append(medicine)

    return result


def pharmacist_login(password):
    """Validate a pharmacist password from an environment variable."""
    expected_password = os.getenv("PHARMA_DB_PASSWORD")

    if expected_password is None:
        return False

    return password == expected_password


def print_stock():
    """Print the current pharmacy stock."""
    print("===== Pharmacy Stock Report =====")

    for medicine, details in medicines.items():
        print(
            f"{medicine} -> {details['qty']} units, "
            f"Rs. {details['price']} exp {details['expiry']}"
        )


def main():
    """Run the pharmacy manager demonstration."""
    add_medicine(
        "Paracetamol 500mg",
        200,
        1.5,
        "2027-06-30",
    )

    add_medicine(
        "Amoxicillin 250mg",
        40,
        6.0,
        "2026-01-15",
    )

    add_medicine(
        "Cetirizine 10mg",
        10,
        2.0,
        "2027-03-31",
    )

    add_medicine("404", 25)

    dispense_medicine("Paracetamol 500mg", 30)
    dispense_medicine("Insulin", 2)

    print(
        "Paracetamol stock:",
        get_quantity("Paracetamol 500mg"),
    )

    print(
        "Amoxicillin expired?",
        is_expired("Amoxicillin 250mg"),
    )

    print(
        "Bill:",
        bill_amount(
            [
                ("Paracetamol 500mg", 10),
                ("Amoxicillin 250mg", 5),
            ]
        ),
    )

    print(
        "Dosage (mg/day):",
        calculate_dosage("250 * 2"),
    )

    print(
        "Patient ID:",
        patient_id("Asha", "9876543210"),
    )

    print(
        "Rx number:",
        generate_rx_number(),
    )

    configured_password = os.getenv(
        "PHARMA_DB_PASSWORD",
        "",
    )

    print(
        "Login:",
        pharmacist_login(configured_password),
    )

    print_label("Paracetamol 500mg")

    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
