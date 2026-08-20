# Employee Salary Management System

A menu-driven payroll application for a mid-sized UK company, written in plain
Python with no external libraries. All figures are **annual** amounts in pounds
sterling.

## Running it

```bash
python employee_salary_system.py
```

Requires Python 3.6 or later. Nothing to install — the program uses only
built-in types and functions.

The program starts with ten seed employee records already loaded, so every menu
option can be tried immediately.

## Menu options

| # | Option | What it does |
|---|--------|--------------|
| 1 | Add Employee | Prompts for all seven fields, rejects duplicate IDs, appends the record |
| 2 | View All Employees | Prints every employee in one aligned table with basic, gross and net |
| 3 | Search Employee | Finds an employee by ID or by name, ignoring capitalisation |
| 4 | Calculate Salary | Shows one employee's full salary breakdown as a payslip block |
| 5 | Salary Analysis | Highest, lowest, average, counts above £50k / below £30k, total payroll |
| 6 | Department Analysis | Count, total, average, highest and lowest for one department |
| 7 | Update Employee | Changes a single field and reprints the record before and after |
| 8 | Delete Employee | Removes an employee by ID after showing the record and confirming |
| 9 | Exit | Ends the program |

## Data structure

Employees are stored as a **list of dictionaries**. Each employee is one
dictionary with seven named keys:

```python
{"id": "E101", "name": "James Whitfield", "department": "Sales",
 "basic": 35000, "allowance": 5000, "bonus": 3000, "deduction": 2000}
```

A dictionary keeps every field labelled and readable — `emp["basic"]` rather
than `emp[3]` — and a list keeps the records ordered and easy to loop over,
append to and remove from. Neither needs an external library.

## Salary formulas

```
Gross Salary = Basic Salary + Allowance + Bonus
Net Salary   = Gross Salary - Deduction
```

Gross and net are never stored on the record. They are recalculated from the
four components every time they are needed, so changing a bonus can never leave
a stale figure behind.

## Expected results from the seed data

Salary analysis (option 5), on net salary:

| Measure | Value |
|---------|-------|
| Highest | Sophie Hargreaves (E104) — £70,000 |
| Lowest | Amelia Clarke (E106) — £26,700 |
| Average | £46,020 |
| Earning more than £50,000 | 3 |
| Earning less than £30,000 | 1 |
| Total annual payroll | £460,200 |

Department analysis (option 6), on net salary:

| Department | Count | Total | Average | Highest | Lowest |
|------------|------:|------:|--------:|--------:|-------:|
| IT | 3 | £177,000 | £59,000 | £70,000 | £50,000 |
| HR | 2 | £80,000 | £40,000 | £46,000 | £34,000 |
| Sales | 2 | £67,700 | £33,850 | £41,000 | £26,700 |
| Finance | 2 | £73,500 | £36,750 | £42,200 | £31,300 |
| Operations | 1 | £62,000 | £62,000 | £62,000 | £62,000 |

## Input validation

Every prompt goes through one of two helpers, so bad input is rejected in one
place rather than being re-checked in each module:

- `read_text()` — rejects blank entries and re-prompts.
- `read_money()` — rejects non-numeric text and negative figures, and
  re-prompts.

Menu choices outside 1–9, unknown employee IDs, empty employee lists and
departments with no members are all handled with a message rather than a crash.

## Repository contents

```
employee_salary_system.py   The complete program
project_report.pdf          Written report
screenshot/                 Screenshots of each module running
```
