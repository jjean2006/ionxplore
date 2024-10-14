import mysql.connector
import random
import math

db_conn = mysql.connector.connect(user="root", password="password", host="localhost", database="ionxdb")
cur = db_conn.cursor()

def linebreak(n):
    print("\n"*(n-1))


def get_max_sl():
    cur.execute("select * from history")
    max_sl = len(cur.fetchall())
    return max_sl


def histread():
    linebreak(2)
    cur.execute("select * from history")
    hist = cur.fetchall()
    for i in hist:
        print(f"{i[0]}. {i[1]} - {i[2]}")
    linebreak(2)


def histwrite(ion, result):
    sl = get_max_sl() + 1
    cur.execute(f"insert into history values({sl}, '{ion}', '{result}')")


# Generate salt
def gensalt():
    cur.execute("select anion from anion_db")
    anion = random.choice(cur.fetchall())[0]

    cur.execute("select cation from cation_db")
    cation = random.choice(cur.fetchall())[0]

    cur.execute(f"select valency from anion_db where anion = '{anion}'")
    an_val = int(cur.fetchall()[0][0])
    cur.execute(f"select valency from cation_db where cation = '{cation}'")
    cat_val = int(cur.fetchall()[0][0])

    lcm = math.lcm(an_val, cat_val)
    cat_count = int(lcm/cat_val)
    an_count = int(lcm/an_val)

    if cat_count != 1 and an_count != 1:
        salt = f"({cation}){str(cat_count)}({anion}){str(an_count)}"
    elif cat_count != 1:
        salt = f"({cation}){str(cat_count)}{anion}"
    elif an_count != 1:
        salt = f"{cation}({anion}){str(an_count)}"
    else:
        salt = f"{cation}{anion}"

    return salt, anion, cation


def get_observ_chktests(reagent, ion, type):
    prel_cond = False
    conf_cond = False
    
    if type == "cat":
        cur.execute(f"select preliminary_reagent from cation_db where cation = '{ion}'")
        prelim_reagent = cur.fetchall()[0][0]
        cur.execute(f"select confirmatory_reagent from cation_db where cation = '{ion}'")
        confirm_reagent = cur.fetchall()[0][0]
    elif type == "an":
        cur.execute(f"select preliminary_reagent from anion_db where anion = '{ion}'")
        prelim_reagent = cur.fetchall()[0][0]
        cur.execute(f"select confirmatory_reagent from anion_db where anion = '{ion}'")
        confirm_reagent = cur.fetchall()[0][0]

    if reagent == prelim_reagent:
        prel_cond = True
        if type == "cat":
            cur.execute(f"select preliminary_observation from cation_db where cation = '{ion}'")
            obs = cur.fetchall()[0][0]
        elif type == "an":
            cur.execute(f"select preliminary_observation from anion_db where anion = '{ion}'")
            obs = cur.fetchall()[0][0]
    elif reagent == confirm_reagent:
        conf_cond = True
        if type == "cat":
            cur.execute(f"select confirmatory_observation from cation_db where cation = '{ion}'")
            obs = cur.fetchall()[0][0]
        elif type == "an":
            cur.execute(f"select confirmatory_observation from anion_db where anion = '{ion}'")
            obs = cur.fetchall()[0][0]
    else:
        obs = "Unknown result"

    return  obs, prel_cond, conf_cond


def test(ion, type):
    prel_conducted = False
    conf_conducted = False

    print("Enter the reagent or what you think the ion is.")
    print("Enter NNN if unsure.")
    print("Answer will not be accepted if preliminary and confirmatory have not been conducted yet.")

    linebreak(2)

    guess = input("Enter reagent/ion:")
    
    if guess == "NNN":
        print(f"Ion is {ion}")
        return False

    results = get_observ_chktests(guess, ion, type)

    if results[1]:
        prel_conducted = results[1]
    if results[2]:
        conf_conducted = results[2]

    print("Observation:", results[0])
    print("Preliminary conducted:", prel_conducted)
    print("Confirmatory conducted:", conf_conducted)
    linebreak(2)

    while guess != ion or (not prel_conducted or not conf_conducted):
        guess = input("Enter reagent/ion:")

        if guess == "NNN":
            print(f"Ion is {ion}")
            return False
           
        results = get_observ_chktests(guess, ion, type)

        if results[1]:
            prel_conducted = results[1]
        if results[2]:
            conf_conducted = results[2]

        print("Observation:", results[0])
        print("Preliminary conducted:", prel_conducted)
        print("Confirmatory conducted:", conf_conducted)
        linebreak(2)

    else:
        print("Correct!")
        return True
        

def analysis():
    salt, anion, cation = gensalt()
    print(salt, anion, cation)

    print("Starting anion test:")
    an_test = test(anion, "an")
    if an_test:
        histwrite(anion, "correct")
    else:
        histwrite(anion, "wrong")

    linebreak(2)

    print("Starting cation test:")
    cat_test = test(cation, "cat")
    if cat_test:
        histwrite(cation, "correct")
    else:
        histwrite(cation, "wrong")
    
    linebreak(2)


def calc_prof(n=10):
    sl = get_max_sl() - (n + 1)
    
    cur.execute(f"select * from history where result = 'correct' and sl_no > {sl}")
    cors = cur.fetchall()
    ccount = len(cors)
    if ccount != 0:
        cions = list(set([x[1] for x in cors]))
    else:
        cions = None

    cur.execute(f"select * from history where result = 'wrong' and sl_no > {sl}")
    wros = cur.fetchall()
    wcount = len(wros)
    if wcount != 0:
        wions = list(set([x[1] for x in wros]))
    else:
        wions = None

    prof = len(cors)/(ccount + wcount)
    linebreak(2)
    print(f"Out of the last {n} attempts:")
    print(f"Proficiency = {prof}")
    linebreak(1)
    print(f"Number of correct attempts: {ccount}")
    print(f"Number of incorrect attempts: {wcount}")
    linebreak(1)
    print(f"Ions to revise: {wions}")
    print(f"Correct ions: {cions}")
    linebreak(2)


def main():
    valid = ["1", "2", "3"]
    c = "1"
    while c in valid:
        print("Enter 1 to run a new salt analysis")
        print("Enter 2 to view proficiency report")
        print("Enter 3 to view history")
        print("Enter anything else to exit")
        c = input("Enter choice: ")

        if c == "1": 
            analysis()

        elif c == "2":
            n = input("Enter number of  previous attempts to include in report (leave blank for default = 10): ")
            if n:
                calc_prof(int(n))
            else:
                calc_prof()

        elif c == "3":
            histread()

    else:
        print("Exiting...")

main()
db_conn.commit()