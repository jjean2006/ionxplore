import mysql.connector
import random
import math

db_conn = mysql.connector.connect(user="root", password="password", host="localhost", database="ionxdb")
cur = db_conn.cur()

# Generate salt
def gensalt():
    cur.execute("select anion from anion_tb")
    anion = random.choice(cur.fetchall()[0])

    cur.execute("select cation from cation_tb")
    cation = random.choice(cur.fetchall()[0])

    cur.execute("select valency from anion_tb where anion = " + anion)
    an_val = int(cur.fetchall()[0][0])
    cur.execute("select valency from cation_tb where cation = " + cation)
    cat_val = int(cur.fetchall()[0][0])

    lcm = math.lcm(an_val, cat_val)

    salt = cation + str(lcm/an_val) + anion + str(lcm/cat_val)

    return salt, anion, cation


def observ(reagent, ion, type):
    
    if type == "cat":
        cur.execute("select preliminary_reagent from cation_tb where cation = " + ion)
        prelim_reagent = cur.fetchall()[0][0]
        cur.execute("select confirmatory_reagent from cation_tb where cation = " + ion)
        confirm_reagent = cur.fetchall()[0][0]
    elif type == "an":
        cur.execute("select preliminary_reagent from anion_tb where anion = " + ion)
        prelim_reagent = cur.fetchall()[0][0]
        cur.execute("select confirmatory_reagent from anion_tb where anion = " + ion)
        confirm_reagent = cur.fetchall()[0][0]

    if reagent == prelim_reagent:
        if type == "cat":
            cur.execute("select preliminary_observation from cation_tb where cation = " + ion)
            obs = cur.fetchall()[0][0]
        elif type == "an":
            cur.execute("select preliminary_observation from anion_tb where anion = " + ion)
            obs = cur.fetchall()[0][0]
    elif reagent == confirm_reagent:
        if type == "cat":
            cur.execute("select confirmatory_observation from cation_tb where cation = " + ion)
            obs = cur.fetchall()[0][0]
        elif type == "an":
            cur.execute("select confirmatory_observation from anion_tb where anion = " + ion)
            obs = cur.fetchall()[0][0]
    else:
        obs = "Unknown"
    return  obs

    
def anion_test(ion):
    # Group 1
    reagent = input("Enter reagent:")
    observ(reagent)