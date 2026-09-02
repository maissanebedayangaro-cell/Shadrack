from flask import Flask, render_template, request

app = Flask(__name__)

#page d'accueil
@app.route ("/")
def accueil():
    return render_template("accueil.html")

#page matieres
@app.route ("/matiere")
def matiere():
    return render_template("matiere.html")

#page devoirs
@app.route("/devoir", methods=["POST"])
def page_devoir():
    matieres= request.form.getlist("matiere")
    return render_template ("devoir.html", matieres=matieres)

#page tableau
@app.route ("/tableau",methods=["POST"])
def tableau():
     matieres= request.form.getlist('matiere')
     devoirs= request.form.getlist('devoir')
     return render_template("tableau.html", matieres=matieres, devoirs=devoirs)
     
#page resultat
@app.route ("/resultat", methods=["POST"])
def resultat():
    matieres= request.form.getlist("matiere")
    devoirs= ["Devoir1", "Devoir2", "Devoir3"]
    total= 0
    coef_total= 0 
     
    for matiere in  matieres:
        #notes envoyées par  users
        m= matiere.lower().replace("-","-")
        note_devoirs = []
        for  devoir in  devoirs:
             note= request.form.get(f"note_{m}_{devoir}")
             if note and note.strip() != "":
                  note_devoirs.append(float(note))
            
        composition = float(request.form.get(f"composition_{m}", 0))
        coef =int(request.form.get(f"coef_{m}", 1))
            #calcule 
        moyenne_devoir=sum(note_devoirs)/len(note_devoirs) if note_devoirs else 0
        moyenne_matiere= (moyenne_devoir + composition)/2
        note_matiere= moyenne_matiere * coef
        total += note_matiere
        coef_total += coef
        

    moyenne_generale= total/coef_total if coef_total > 0 else 0
    if moyenne_generale <=10:
        print('moyenne faible fais de ton mieux la prochaine fois')
    else:
        print('admis(e), félicitation')
     
    return render_template("resultat.html", moyenne= round(moyenne_generale, 2))


if __name__ == "__main__":
    app.run(debug=True)