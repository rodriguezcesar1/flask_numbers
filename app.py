import sqlite3
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.exceptions import abort
import sympy.ntheory as nt


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_data', methods=('GET','POST'))
def handle_data():
    if request.method == "POST":
        number = request.form['num']
        option = request.form['options']

        if option == "all":
            return redirect(url_for("show_numbers", number=number))
        elif option == "even":
            return redirect(url_for("show_even", number=number))
        elif option == "odd":
            return redirect(url_for("show_odd", number=number))
        elif option == "prime":
            return redirect(url_for("show_prime", number=number))
        else:
            return redirect(url_for("index"))
    return render_template('index.html')
    


@app.route('/<int:number>')
def show_numbers(number):
    arr = [i for i in range(number+1)]
    return render_template('show_numbers.html', number=number, arr=arr)

@app.route('/<int:number>/odd')
def show_odd(number):
    arr = [i for i in range(1, number+1, 2)]
    return render_template('show_odd.html', number=number, arr=arr)

@app.route('/<int:number>/even')
def show_even(number):
    arr = [i for i in range(0, number+1, 2)]
    return render_template('show_even.html', number=number, arr=arr)

@app.route('/<int:number>/prime', methods=('GET', 'POST'))
def show_prime(number):
    #check if number has next prime in database
    conn = get_db_connection()
    max_num = conn.execute('SELECT MAX(num) FROM primes').fetchone()[0]
    max_prime = conn.execute('SELECT prime FROM primes WHERE num= ? ', (max_num,)).fetchone()[0]
    print(max_prime)
    
    if max_prime <= number:
        #generate primes from max_num to number and store them in primes
        next_prime = max_prime
        for num in range(max_num+1, number+1):
            if next_prime >= num:
                next_prime = nt.nextprime(num)
            conn.execute('INSERT into primes (num, prime) VALUES (?,?)', (num, next_prime))
    
    arr, i = [], 1
    #list all primes up to number
    while i <= number:
        i = conn.execute('SELECT prime from primes WHERE num = ?', (i,)).fetchone()[0]
        arr.append(i)
    if arr[-1] > number:
        del arr[-1]

    conn.close()
    return render_template('show_prime.html', number=number, arr=arr)

if  __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)