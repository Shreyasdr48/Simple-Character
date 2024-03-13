from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)

# Calculates Compound Interest
def calculate_compound_interest(principal, rate, time, compounding_frequency):
    if compounding_frequency == 0:
        return principal * (1 + (rate / 100)) ** time
    else:
        amount = principal * (1 + (rate / 100) / compounding_frequency) ** (compounding_frequency * time)
        return amount

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_choice = request.form.get('user_choice', '')
        if user_choice == 'customer':
            return render_template('customer.html')
        elif user_choice == 'banker':
            return render_template('banker.html')

    return render_template('index.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = int(request.form['time'])
        compounding_frequency = float(request.form['compounding_frequency'])

        return render_template('customer.html', principal=principal, rate=rate, time=time, compounding_frequency=compounding_frequency)

    return redirect(url_for('index'))

@app.route('/banker', methods=['GET', 'POST'])
def banker():
    if request.method == 'POST':
        # Retrieve form data using request.form
        age = int(request.form.get('age', 0))
        check_haz = request.form.get('check_haz', '').lower()
        salary = int(request.form.get('salary', 0))
        type_j = int(request.form.get('type_j', 0))
        pension = request.form.get('pension', '').lower()

        flag = 0

        if age > 40:
            flag += 1
        if check_haz == "yes":
            flag += 1
        if salary < 70000:
            flag += 1
        if type_j == 2:
            flag += 1
        if pension == "yes":
            flag += 1

        # Determine loan status based on the conditions
        if flag == 0:
            loan_status = "Loan is safe to be taken"
        elif flag == 1:
            loan_status = "Loan may have some risks"
        elif flag == 2:
            loan_status = "Proceed with caution, significant risks present"
        elif flag == 3:
            loan_status = "Not advisable to take a loan"
        elif flag == 4:
            loan_status = "Strongly discourage taking a loan"
        elif flag == 5:
            loan_status = "Loan is not viable based on your profile"

        return render_template('banker.html', loan_status=loan_status)

    return redirect(url_for('index'))
@app.route('/loan_calculator', methods=['GET', 'POST'])
def loan_calculator():
    if request.method == 'POST':
        principal = float(request.form.get('principal', 0))
        rate = float(request.form.get('rate', 0))
        time = int(request.form.get('time', 0))
        compounding_frequency = float(request.form.get('compounding_frequency', 0))

        # Calculate compound interest
        amount = principal * (1 + (rate / 100) / compounding_frequency) ** (compounding_frequency * time)
        compound_interest = amount - principal

        # Check if the "Show Graph" button is clicked
        show_graph = request.form.get('show_graph') == 'true'

        # Generate chart data if the button is clicked
        chart_data = generate_chart_data(principal, rate, time, compounding_frequency) if show_graph else None

        return render_template('loan_calculator.html', principal=principal, rate=rate, time=time,
                               compounding_frequency=compounding_frequency, compound_interest=compound_interest,
                               show_graph=show_graph, chart_data=chart_data)

    return render_template('loan_calculator.html')

def generate_chart_data(principal, rate, time, compounding_frequency):
    # Generate data points for the chart
    time_points = np.arange(0, time + 1)
    compound_interest_points = [
        principal * (1 + (rate / 100) / compounding_frequency) ** (compounding_frequency * t) - principal
        for t in time_points
    ]

    chart_data = {
        'labels': time_points.tolist(),
        'data': compound_interest_points
    }

    return chart_data

@app.route('/salary_advisor')
def salary_advisor_page():
    AgeLeft = int(request.args.get('age_left', 0))
    AnnumSalary = int(request.args.get('annual_salary', 0))
    time = int(request.args.get('time', 0))  # Assuming this is the same variable used in loan_calculator

    final_amount = AnnumSalary + calculate_compound_interest(AnnumSalary, AnnumSalary, time, AnnumSalary)
    depreciation = 0.6 * AgeLeft * AnnumSalary

    if final_amount > depreciation:
        loan_status = "Loan is safe to be taken"
    else:
        asset_choice = request.args.get('asset_choice', '').lower()

        if asset_choice == "yes":
            asset_cost = int(request.args.get('asset_cost', 0))
            assage = depreciation * asset_cost * 0.6

            if final_amount > assage:
                loan_status = "Sorry, the loan is not viable from your finances either"
            else:
                loan_status = "It is possible to obtain a loan if assets are considered"
        else:
            loan_status = "Loan is not possible"

    return render_template('salary_advisor.html', loan_status=loan_status)

@app.route('/common_loan_calculator')
def common_loan_calculator():
    # Retrieve values from the request or another source
    principal = float(request.args.get('principal', 0))  # Replace with actual default value
    compounding_frequency = float(request.args.get('compounding_frequency', 0))  # Replace with actual default value

    loan_type = int(request.args.get('loan_type', 0))
    time = int(request.args.get('time', 0))

    interest = 0  # Default value

    if loan_type == 1:
        time += 5
        rate = 12
        interest = round(calculate_compound_interest(principal, rate, time, compounding_frequency), 2)
    elif loan_type == 3:
        rate = 12
        interest = round(calculate_compound_interest(principal, rate, time, compounding_frequency), 2)
    elif loan_type == 2:
        prop_type = request.args.get('prop_type', '').lower()

        if prop_type == "land":
            rate = 12
            interest = round(calculate_compound_interest(principal, rate, time, compounding_frequency), 2)
        elif prop_type == "building":
            rate = 10
            interest = round(calculate_compound_interest(principal, rate, time, compounding_frequency), 2)
        else:
            return "Invalid entry"

    return render_template('common_loan_calculator.html', interest=interest)


if __name__ == '__main__':
    app.run(debug=True)