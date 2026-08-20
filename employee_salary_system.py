"""
Employee Salary Management System

A menu-driven payroll application for a mid-sized UK company.
All figures are ANNUAL amounts in pounds sterling.

Data structure choice: a list of dictionaries.
Each employee is one dictionary with seven named keys, and all ten-plus
employees live in a single list that every function receives as a parameter.
A dictionary keeps each field labelled and readable (emp["basic"] rather
than emp[3]), and a list keeps the records ordered and easy to loop over,
append to and remove from. No external libraries are needed for either.
"""


# ---------------------------------------------------------------------------
# SEED DATA
# Ten starter records, so the program has something to work with the moment
# it launches. Add Employee
# still works on top of these.
# ---------------------------------------------------------------------------

def build_seed_data():
    """Return the ten starter employee records as a list of dictionaries."""
    return [
        {"id": "E101", "name": "James Whitfield", "department": "Sales",
         "basic": 35000, "allowance": 5000, "bonus": 3000, "deduction": 2000},
        {"id": "E102", "name": "Charlotte Bennett", "department": "HR",
         "basic": 40000, "allowance": 4000, "bonus": 3500, "deduction": 1500},
        {"id": "E103", "name": "Daniel Okonkwo", "department": "IT",
         "basic": 50000, "allowance": 6000, "bonus": 4000, "deduction": 3000},
        {"id": "E104", "name": "Sophie Hargreaves", "department": "IT",
         "basic": 62000, "allowance": 7000, "bonus": 5000, "deduction": 4000},
        {"id": "E105", "name": "Callum Fraser", "department": "Finance",
         "basic": 28000, "allowance": 3000, "bonus": 1500, "deduction": 1200},
        {"id": "E106", "name": "Amelia Clarke", "department": "Sales",
         "basic": 24000, "allowance": 2500, "bonus": 1000, "deduction": 800},
        {"id": "E107", "name": "Omar Rahman", "department": "IT",
         "basic": 45000, "allowance": 5000, "bonus": 2500, "deduction": 2500},
        {"id": "E108", "name": "Grace Adeyemi", "department": "HR",
         "basic": 30000, "allowance": 3500, "bonus": 2000, "deduction": 1500},
        {"id": "E109", "name": "Thomas Barlow", "department": "Operations",
         "basic": 55000, "allowance": 6000, "bonus": 4500, "deduction": 3500},
        {"id": "E110", "name": "Niamh O'Sullivan", "department": "Finance",
         "basic": 38000, "allowance": 4000, "bonus": 2000, "deduction": 1800},
    ]


# ---------------------------------------------------------------------------
# SALARY FORMULAS
# Written once here and called from everywhere else. Gross and net are never
# stored on the record - they are recalculated from the four components each
# time they are needed, so updating a bonus can never leave a stale figure.
# ---------------------------------------------------------------------------

def calculate_gross(employee):
    """Gross Salary = Basic Salary + Allowance + Bonus."""
    return employee["basic"] + employee["allowance"] + employee["bonus"]


def calculate_net(employee):
    """Net Salary = Gross Salary - Deduction."""
    return calculate_gross(employee) - employee["deduction"]


def format_money(amount):
    """Format a number as pounds sterling with thousands separators."""
    return "£{:,.0f}".format(amount)


# ---------------------------------------------------------------------------
# INPUT VALIDATION HELPERS
# Every prompt in the program goes through one of these, so bad input is
# rejected in one place rather than being re-checked in eight modules.
# ---------------------------------------------------------------------------

def read_text(prompt):
    """Ask for text and keep asking until something non-blank is typed."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("   Invalid entry. This field cannot be left blank. Please try again.")


def read_money(prompt, field_name):
    """Ask for a salary figure. Rejects text and negative numbers, then retries."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("   Invalid entry. {} must be a number. Please try again."
                  .format(field_name))
            continue
        if value < 0:
            print("   Invalid entry. Salary cannot be negative. Please try again.")
            continue
        return value


def print_payslip(employee):
    """Print one employee's full record as an aligned multi-line block."""
    label = "{:<18}: {}"
    money = "{:<18}: {}"
    print("-" * 40)
    print(label.format("Employee ID", employee["id"]))
    print(label.format("Name", employee["name"]))
    print(label.format("Department", employee["department"]))
    print(money.format("Basic Salary", format_money(employee["basic"])))
    print(money.format("Allowance", format_money(employee["allowance"])))
    print(money.format("Bonus", format_money(employee["bonus"])))
    print(money.format("Gross Salary", format_money(calculate_gross(employee))))
    print(money.format("Deduction", format_money(employee["deduction"])))
    print(money.format("Net Salary", format_money(calculate_net(employee))))
    print("-" * 40)


def find_by_id(employees, emp_id):
    """Return the employee dictionary with this ID, or None if there is no match.

    The comparison ignores capitalisation so 'e101' finds E101.
    """
    for employee in employees:
        if employee["id"].upper() == emp_id.strip().upper():
            return employee
    return None


# ---------------------------------------------------------------------------
# MODULE 1 - ADD EMPLOYEE
# ---------------------------------------------------------------------------

def add_employee(employees):
    """Prompt for all seven fields and append a new employee to the list."""
    print("\n--- ADD NEW EMPLOYEE ---")

    # The ID must be unique, so keep asking until an unused one is given.
    while True:
        emp_id = read_text("Employee ID      : ")
        if find_by_id(employees, emp_id) is None:
            break
        print("   Employee ID {} already exists. Please enter a different ID."
              .format(emp_id.upper()))

    new_employee = {
        "id": emp_id.upper(),
        "name": read_text("Employee Name    : "),
        "department": read_text("Department       : "),
        "basic": read_money("Basic Salary     : ", "Basic Salary"),
        "allowance": read_money("Allowance        : ", "Allowance"),
        "bonus": read_money("Bonus            : ", "Bonus"),
        "deduction": read_money("Deduction        : ", "Deduction"),
    }
    employees.append(new_employee)

    print("\nEmployee {} added successfully.".format(new_employee["id"]))
    print("Gross Salary: {} | Net Salary: {}".format(
        format_money(calculate_gross(new_employee)),
        format_money(calculate_net(new_employee))))


# ---------------------------------------------------------------------------
# MODULE 2 - VIEW ALL EMPLOYEES
# ---------------------------------------------------------------------------

def view_all_employees(employees):
    """Print every stored employee in one aligned table."""
    print("\n--- ALL EMPLOYEES ---")

    if not employees:
        print("No employees have been added yet.")
        return

    # Column widths are set once in the format string, so the header and the
    # rows can never drift apart.
    row_format = "{:<6} {:<20} {:<12} {:>10} {:>10} {:>10}"
    print(row_format.format("ID", "NAME", "DEPARTMENT", "BASIC", "GROSS", "NET"))
    print("-" * 72)

    for employee in employees:
        print(row_format.format(
            employee["id"],
            employee["name"],
            employee["department"],
            format_money(employee["basic"]),
            format_money(calculate_gross(employee)),
            format_money(calculate_net(employee))))

    print("-" * 72)
    print("Total employees: {}".format(len(employees)))


# ---------------------------------------------------------------------------
# MODULES 3 TO 8 - SEARCH, CALCULATE, ANALYSE, UPDATE AND DELETE
# Each of these takes the same employees list and reuses the shared helpers
# above, so the salary formulas and the validation rules are written once.
# ---------------------------------------------------------------------------

def search_employee(employees):
    """Module 3 - find an employee by Employee ID or by Employee Name.

    Asks which of the two to search by, then prints the full record of every
    match, gross and net salary included. Both searches ignore capitalisation,
    so "charlotte bennett" finds Charlotte Bennett. A search that matches
    nothing says so rather than printing an empty result.
    """
    print("\n--- SEARCH EMPLOYEE ---")

    if not employees:
        print("No employees have been added yet.")
        return

    choice = input("Search by (1) ID or (2) Name: ").strip()

    matches = []
    if choice == "1":
        emp_id = read_text("Enter Employee ID: ")
        found = find_by_id(employees, emp_id)
        if found is not None:
            matches.append(found)
    elif choice == "2":
        term = read_text("Enter Employee Name: ").lower()
        matches = [e for e in employees if e["name"].lower() == term]
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    if not matches:
        print("No matching employee found.")
        return

    for employee in matches:
        print_payslip(employee)



def calculate_salary(employees):
    """Module 4 - show one employee's full salary breakdown as a payslip block.

    Looks the employee up by ID, then hands the record to print_payslip(),
    which lays out the four components followed by gross, deduction and net
    on separate lines with the colons aligned.
    """
    print("\n--- CALCULATE SALARY ---")

    if not employees:
        print("No employees have been added yet.")
        return

    emp_id = read_text("Enter Employee ID: ")
    employee = find_by_id(employees, emp_id)
    if employee is None:
        print("No employee found with ID {}.".format(emp_id.upper()))
        return

    print_payslip(employee)


def salary_analysis(employees):
    """Module 5 - answer six questions about the whole workforce, on NET salary.

    Reports the highest and lowest earner, the company average, how many earn
    strictly more than 50,000 and strictly less than 30,000, and the total
    annual payroll cost. An empty list returns early, so the average is never
    a division by zero.

    Against the seed data:
      highest Sophie Hargreaves E104 70,000 | lowest Amelia Clarke E106 26,700
      average 46,020 | more than 50k = 3 | less than 30k = 1 | total 460,200
    """
    print("\n--- SALARY ANALYSIS ---")

    if not employees:
        print("No employees have been added yet.")
        return

    highest = max(employees, key=calculate_net)
    lowest = min(employees, key=calculate_net)
    total = sum(calculate_net(e) for e in employees)
    average = total / len(employees)
    over_50k = sum(1 for e in employees if calculate_net(e) > 50000)
    under_30k = sum(1 for e in employees if calculate_net(e) < 30000)

    print("Highest net salary : {} {} ({})".format(
        highest["name"], highest["id"], format_money(calculate_net(highest))))
    print("Lowest net salary  : {} {} ({})".format(
        lowest["name"], lowest["id"], format_money(calculate_net(lowest))))
    print("Average net salary : {}".format(format_money(average)))
    print("Earning more than £50,000 : {}".format(over_50k))
    print("Earning less than £30,000 : {}".format(under_30k))
    print("Total annual payroll cost : {}".format(format_money(total)))


def department_analysis(employees):
    """Module 6 - report on one department the user selects.

    Matches the department name ignoring capitalisation, so "it" finds IT,
    then reports the number of employees along with the total, average,
    highest and lowest net salary. A department with no members prints a
    message instead of crashing.

    Against the seed data, on net salary:
      IT         3 / 177,000 / 59,000 / 70,000 / 50,000
      HR         2 /  80,000 / 40,000 / 46,000 / 34,000
      Sales      2 /  67,700 / 33,850 / 41,000 / 26,700
      Finance    2 /  73,500 / 36,750 / 42,200 / 31,300
      Operations 1 /  62,000 / 62,000 / 62,000 / 62,000
    """
    print("\n--- DEPARTMENT ANALYSIS ---")

    if not employees:
        print("No employees have been added yet.")
        return

    dept = read_text("Enter Department: ").lower()
    members = [e for e in employees if e["department"].lower() == dept]

    if not members:
        print("No employees found in that department.")
        return

    nets = [calculate_net(e) for e in members]
    total = sum(nets)
    average = total / len(members)

    print("Department        : {}".format(members[0]["department"]))
    print("Number of employees: {}".format(len(members)))
    print("Total net salary  : {}".format(format_money(total)))
    print("Average net salary: {}".format(format_money(average)))
    print("Highest net salary: {}".format(format_money(max(nets))))
    print("Lowest net salary : {}".format(format_money(min(nets))))


def update_employee(employees):
    """Module 7 - locate an employee by ID and change their details.

    Prints the current record, then offers Department, Basic Salary,
    Allowance, Bonus and Deduction as the editable fields and changes only the
    one chosen, leaving the rest untouched. The record is printed again
    afterwards with the recalculated net salary. Employee ID is deliberately
    not editable, because it is what identifies the record.
    """
    print("\n--- UPDATE EMPLOYEE ---")

    if not employees:
        print("No employees have been added yet.")
        return

    emp_id = read_text("Enter Employee ID: ")
    employee = find_by_id(employees, emp_id)
    if employee is None:
        print("No employee found with ID {}.".format(emp_id.upper()))
        return

    print("\nCurrent record:")
    print_payslip(employee)

    print("\nWhich field would you like to update?")
    print("   1. Department")
    print("   2. Basic Salary")
    print("   3. Allowance")
    print("   4. Bonus")
    print("   5. Deduction")
    field_choice = input("Enter your choice (1-5): ").strip()

    if field_choice == "1":
        employee["department"] = read_text("New Department   : ")
    elif field_choice == "2":
        employee["basic"] = read_money("New Basic Salary : ", "Basic Salary")
    elif field_choice == "3":
        employee["allowance"] = read_money("New Allowance    : ", "Allowance")
    elif field_choice == "4":
        employee["bonus"] = read_money("New Bonus        : ", "Bonus")
    elif field_choice == "5":
        employee["deduction"] = read_money("New Deduction    : ", "Deduction")
    else:
        print("Invalid choice. No changes made.")
        return

    print("\nUpdated record:")
    print_payslip(employee)


def delete_employee(employees):
    """Module 8 - remove an employee by Employee ID.

    Prints the record and asks for confirmation before removing it, so a
    mistyped ID cannot delete someone silently, and reports the deletion once
    it is done. An ID that does not exist, or an empty employee list, prints a
    message instead of crashing.
    """
    print("\n--- DELETE EMPLOYEE ---")

    if not employees:
        print("No employees have been added yet.")
        return

    emp_id = read_text("Enter Employee ID: ")
    employee = find_by_id(employees, emp_id)
    if employee is None:
        print("No employee found with ID {}.".format(emp_id.upper()))
        return

    print("\nEmployee to be deleted:")
    print_payslip(employee)

    confirm = input("Are you sure you want to delete this employee? (y/n): ").strip().lower()
    if confirm == "y":
        employees.remove(employee)
        print("Employee {} deleted successfully.".format(employee["id"]))
    else:
        print("Deletion cancelled.")


# ---------------------------------------------------------------------------
# MENU AND MAIN LOOP
# ---------------------------------------------------------------------------

def display_menu():
    """Print the main menu."""
    print("\n=========================================")
    print("   EMPLOYEE SALARY MANAGEMENT SYSTEM")
    print("=========================================")
    print("   1. Add Employee")
    print("   2. View All Employees")
    print("   3. Search Employee")
    print("   4. Calculate Salary")
    print("   5. Salary Analysis")
    print("   6. Department Analysis")
    print("   7. Update Employee")
    print("   8. Delete Employee")
    print("   9. Exit")
    print("=========================================")


def main():
    """Run the menu loop until the user chooses option 9."""
    employees = build_seed_data()

    # Each menu number is mapped to the function that handles it, so adding
    # an option later means adding one line rather than another elif branch.
    actions = {
        "1": add_employee,
        "2": view_all_employees,
        "3": search_employee,
        "4": calculate_salary,
        "5": salary_analysis,
        "6": department_analysis,
        "7": update_employee,
        "8": delete_employee,
    }

    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == "9":
            print("\nThank you for using the Employee Salary Management System.")
            break
        elif choice in actions:
            actions[choice](employees)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()