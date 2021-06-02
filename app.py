from flask import Flask, render_template, request, flash, redirect, url_for
from collections import defaultdict

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        source = request.files["source"].read()
        try:
            content = source.decode("utf-8")
        except UnicodeDecodeError:
            flash("CHYBA: Soubor není v kódování UTF-8")
            return redirect(url_for("index"))

        result = []
        errors = defaultdict(str)
        deleted = []
        lines = content.splitlines()
        for index, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            # RC;jmeno;prijmeni;adresa;mesto;psc,zp,odbery
            parts = line.strip().split(";")
            if any([p == "" for p in parts[:-1]]):
                errors[index+1] = "Chybí některá část"
            parts[1] = parts[1].capitalize()
            parts[2] = parts[2].capitalize()
            if parts[-1] == "":
                deleted.append(index+1)
            else:
                result.append(";".join(parts))
                if ";;" in result[-1]:
                    result[-1] = result[-1].replace(";;", ";")

        return render_template("index.html", original=lines, result=result,
                               errors=errors, deleted=deleted)


if __name__ == '__main__':
    app.run(debug=True)
