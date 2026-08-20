# Employee Salary Management System

A menu-driven payroll application for a mid-sized UK company, written in plain
Python with no external dependencies.

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Interface](https://img.shields.io/badge/interface-CLI-lightgrey)

Manage employee records and analyse payroll across the workforce: add, search,
update and remove employees, produce individual payslips, and report on
salaries company-wide or by department. All figures are **annual** amounts in
pounds sterling.

---

## Contents

- [Quick start](#quick-start)
- [Features](#features)
- [Example output](#example-output)
- [Design notes](#design-notes)
- [Verified results](#verified-results)
- [Input validation](#input-validation)
- [Project structure](#project-structure)
- [Possible extensions](#possible-extensions)

---

## Quick start

```bash
git clone https://github.com/jumma786/employee-salary-system.git
cd employee-salary-system
python employee_salary_system.py
```

Requires **Python 3.6 or later**. Nothing to install — the program uses only
built-in types and functions.

Ten employee records are seeded at launch, so every menu option can be
exercised immediately without entering data first.

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Add Employee** | Captures all seven fields, rejects duplicate IDs, validates every entry |
| 2 | **View All Employees** | Aligned table of every record with basic, gross and net salary |
| 3 | **Search Employee** | Lookup by ID or by name, case-insensitive, reports no-match clearly |
| 4 | **Calculate Salary** | Full payslip breakdown for a single employee |
| 5 | **Salary Analysis** | Highest, lowest, average, threshold counts and total payroll cost |
| 6 | **Department Analysis** | Headcount, total, average, highest and lowest for any department |
| 7 | **Update Employee** | Edits a single field in place and reprints the record before and after |
| 8 | **Delete Employee** | Removes a record after showing it and requiring confirmation |
| 9 | **Exit** | Closes the application |

---

## Example output

Viewing all employees (option 2):

```
--- ALL EMPLOYEES ---
ID     NAME                 DEPARTMENT        BASIC      GROSS        NET
------------------------------------------------------------------------
E101   James Whitfield      Sales           £35,000    £43,000    £41,000
E102   Charlotte Bennett    HR              £40,000    £47,500    £46,000
E103   Daniel Okonkwo       IT              £50,000    £60,000    £57,000
E104   Sophie Hargreaves    IT              £62,000    £74,000    £70,000
E105   Callum Fraser        Finance         £28,000    £32,500    £31,300
E106   Amelia Clarke        Sales           £24,000    £27,500    £26,700
E107   Omar Rahman          IT              £45,000    £52,500    £50,000
E108   Grace Adeyemi        HR              £30,000    £35,500    £34,000
E109   Thomas Barlow        Operations      £55,000    £65,500    £62,000
E110   Niamh O'Sullivan     Finance         £38,000    £44,000    £42,200
------------------------------------------------------------------------
Total employees: 10
```

Workforce analysis (option 5):

```
--- SALARY ANALYSIS ---
Highest net salary : Sophie Hargreaves E104 (£70,000)
Lowest net salary  : Amelia Clarke E106 (£26,700)
Average net salary : £46,020
Earning more than £50,000 : 3
Earning less than £30,000 : 1
Total annual payroll cost : £460,200
```

Further screenshots of each module are in [`screenshot/`](screenshot/).

---

## Design notes

### Data model

Employees are held as a **list of dictionaries** — one dictionary per employee,
seven named keys each:

```python
{"id": "E101", "name": "James Whitfield", "department": "Sales",
 "basic": 35000, "allowance": 5000, "bonus": 3000, "deduction": 2000}
```

A dictionary keeps every field labelled and self-documenting at the point of
use — `employee["basic"]` rather than `employee[3]` — while the enclosing list
keeps records ordered and cheap to iterate, append to and remove from. Neither
requires a third-party library.

### Derived values are never stored

```
Gross Salary = Basic Salary + Allowance + Bonus
Net Salary   = Gross Salary − Deduction
```

Gross and net are computed on demand by `calculate_gross()` and
`calculate_net()` and are deliberately **not** persisted on the record.
Updating an employee's bonus therefore cannot leave a stale total behind
anywhere in the system — there is exactly one source of truth for every figure.

### Menu dispatch

The main loop maps each menu choice to its handler through a dictionary rather
than a chain of `elif` branches:

```python
actions = {"1": add_employee, "2": view_all_employees, ...}
actions[choice](employees)
```

Adding a tenth option is a single new entry, not another branch in a growing
conditional.

### Single-responsibility helpers

`find_by_id()`, `print_payslip()`, `format_money()`, `read_text()` and
`read_money()` are each defined once and shared by every module that needs
them, so lookup semantics, payslip layout, currency formatting and validation
rules stay consistent across all eight features.

---

## Verified results

Workforce analysis (option 5), computed on **net** salary:

| Measure | Value |
|---------|-------|
| Highest earner | Sophie Hargreaves (E104) — £70,000 |
| Lowest earner | Amelia Clarke (E106) — £26,700 |
| Average net salary | £46,020 |
| Earning more than £50,000 | 3 |
| Earning less than £30,000 | 1 |
| Total annual payroll | £460,200 |

Department analysis (option 6), computed on **net** salary:

| Department | Headcount | Total | Average | Highest | Lowest |
|------------|----------:|------:|--------:|--------:|-------:|
| IT | 3 | £177,000 | £59,000 | £70,000 | £50,000 |
| HR | 2 | £80,000 | £40,000 | £46,000 | £34,000 |
| Sales | 2 | £67,700 | £33,850 | £41,000 | £26,700 |
| Finance | 2 | £73,500 | £36,750 | £42,200 | £31,300 |
| Operations | 1 | £62,000 | £62,000 | £62,000 | £62,000 |

---

## Input validation

Every prompt in the program is routed through one of two helpers, so invalid
input is rejected in a single place rather than being re-checked in eight
separate modules:

| Helper | Rejects | Behaviour |
|--------|---------|-----------|
| `read_text()` | Blank or whitespace-only entries | Re-prompts until valid |
| `read_money()` | Non-numeric text, negative figures | Re-prompts until valid |

Handled without crashing: menu choices outside 1–9, unknown employee IDs,
duplicate IDs on creation, operations attempted on an empty employee list,
departments with no members, and deletions the user declines to confirm.

---

## Project structure

```
employee_salary_system.py   Complete application — helpers, eight modules, menu loop
README.md                   This file
screenshot/                 Screenshots of each module in use
```

The application is a single self-contained module of roughly 470 lines,
organised as: seed data → salary formulas → shared helpers → the eight
feature modules → menu and main loop.

---

## Possible extensions

- Persist records to CSV or JSON so data survives between sessions
- Add UK income tax and National Insurance bands to the deduction calculation
- Support monthly as well as annual figures
- Export individual payslips to file
- Add a unit test suite covering the salary formulas and edge cases
