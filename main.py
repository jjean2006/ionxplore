import mysql.connector
import random
import math

db_conn = mysql.connector.connect(user="root", password="password", host="localhost", database="ionxdb")
cur = db_conn.cursor()

def linebreak(n):
    print("\n"*(n-1))

# Generate salt
def gensalt():
    cur.execute("select anion from anion_db")
    anion = random.choice(cur.fetchall())[0]
    print(anion)

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


def observ(reagent, ion, type):

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
    print("Answer will not be accepted if preliminary and confirmatory have not been conducted yet.")
    guess = input("Enter reagent/ion:")
    results = observ(guess, ion, type)

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
        results = observ(guess, ion, type)

        if results[1]:
            prel_conducted = results[1]
        if results[2]:
            conf_conducted = results[2]

        print("Observation:", results[0])
        print("Preliminary conducted:", prel_conducted)
        print("Confirmatory conducted:", conf_conducted)
        linebreak(2)

    print("Correct!")

    

def main():
    salt, anion, cation = gensalt()
    print(salt, anion, cation)
    print("Starting anion test:")
    test(anion, "an")

    linebreak(2)

    print("Starting cation test:")
    test(cation, "cat")

main()