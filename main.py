import requests
import random
import json
from flask import Flask, request
app = Flask(__name__)

INF = 1000000007
color_to_diff = {
    "gray" : (0, 400),
    "brown" : (400, 800),
    "green" : (800, 1200),
    "cyan" : (1200, 1600),
    "blue" : (1600, 2000),
    "yellow" : (2000, 2400),
    "orange" : (2400, 2800),
    "red" : (3200, 3600),
    "silver" : (3600, 4000),
    "gold" : (4000, INF)
}

def get_problems(lower, upper) :
    res = requests.get("https://kenkoooo.com/atcoder/resources/problem-models.json")
    if res.status_code != 200 : return []

    problem_models = res.json()
    for problem in problem_models.items():
        try:    
            if problem[1]["difficulty"] < 0:
                problem[1]["difficulty"] = 0
        except KeyError:
            problem[1]["difficulty"] = 100000000007
    return [problem[0] for problem in problem_models.items() if lower <= int(problem[1]["difficulty"]) < upper]

def color_req(message):
    color = message
    if color in color_to_diff.keys() :
        diffculties = color_to_diff[color]
        return diffculties[0], diffculties[1]

    return INF, INF

def fix_code_fes_link(contest):
    return "cf" + contest[15:17] + contest[17:len(contest)]

@app.route('/')
def atcoder():  

    try:    
        lower = int(request.args.get('lower', 0))
        upper = int(request.args.get('upper', 0))
        problems = get_problems(lower, upper)            
    except KeyError:
        res = "Could not find problem"
        return json.dumps({"problem" : res})
        
    if(len(problems) == 0) :
        res = "Could not find problem"
        return json.dumps({"problem" : res})

    rnd = random.randrange(len(problems) - 1)
    problem = str(problems[rnd])

    contest = str(problem[0:len(problem) - 2]).replace('_', '-')
    if contest[len(contest) - 1] == "-" : contest = contest[0 : len(contest) - 1]
    if contest[0:4] == "code" : contest = fix_code_fes_link(contest)

    link = "https://atcoder.jp/contests/" + contest + "/tasks/" + problem
    return json.dumps({"problem" : link})

if __name__ == '__main__':
    app.run(port=8080)