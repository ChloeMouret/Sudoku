from flask import Flask, render_template, request
import numpy as np
import sudoku
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def process_sudoku():
    if request.method == 'GET':
        return render_template('grille.html.jinja2')
    else:
        result = request.form
        t = np.zeros((9, 9), dtype=int)
        if "fetch" in request.form:
            (t, logs) = sudoku.get_sudoku(3)
            for log in logs:
                app.logger.info(log)
            return render_template('grille.html.jinja2', old=t)
        else:
            for key, value in result.items():
                if key != "type" and value != "":
                    i = int(key[0])
                    j = int(key[1])
                    t[i, j] = int(value)
            (res, logs) = sudoku.launch(t)
            for log in logs:
                app.logger.info(log)
            return render_template('grille.html.jinja2', old=t, new=res)


if __name__ == '__main__':
    app.run()