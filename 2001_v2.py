import random, re
from flask import Flask, request, render_template


def random_dice():
    dice = [3, 4, 6, 8, 10, 12, 20, 100]
    random.shuffle(dice)
    return dice[4]



def user_dice(code: str) -> int:
    patern = r"^[D](3|4|6|8|10|12|20|100){1}$"
    if re.fullmatch(patern, code) is not None:
        return int(re.split("[D]", code)[1])
    else:
        return 6


def sum_of_roll_of_dices(choice: int = random_dice(), move: int = 2) -> int:
    sum_of_all_meshes = 0
    for i in range(move):
        sum_of_all_meshes += random.randint(1, choice)
    return sum_of_all_meshes


def sum_of_points(sum_of_points: int, sum_of_roll_of_dices: int) -> int:
    sum_of_move = sum_of_roll_of_dices
    if sum_of_points == 0:
        sum_of_points += sum_of_move
    else:
        if sum_of_move == 7:
            sum_of_points /= 7
        elif sum_of_move == 11:
            sum_of_points *= 11
        else:
            sum_of_points += sum_of_move
    return int(sum_of_points)


app = Flask(__name__)


history = []
@app.route("/", methods=["POST", "GET"])
def game():
    if request.method == "GET":
        method = "GET"

        return render_template('2001.html', method=method)

    if request.method == "POST":
        method = "POST"
        user_points = int(request.form["user_points"])
        comp_points = int(request.form["comp_points"])
        counter = int(request.form["counter"])
        stage = "again"
        if request.form["stage"] == "game":
            choice_one = user_dice(request.form["choice_one"])
            choice_two = user_dice(request.form["choice_two"])


            comp_roll_meshes = sum_of_roll_of_dices(random_dice(),2)
            comp_points = sum_of_points(comp_points, comp_roll_meshes)
            counter +=1
            user_roll_meshes = sum_of_roll_of_dices(choice_one,1) + sum_of_roll_of_dices(choice_two,1)
            user_points = sum_of_points(user_points, user_roll_meshes)
            result = (user_roll_meshes, comp_roll_meshes)
            history.insert(0,  f"""\n{counter}: Your roll meshes {user_roll_meshes} | Your point {user_points}  - vs. - """ \
                        f""" Comp roll meshes {comp_roll_meshes} | Comp point {comp_points}""" )

            if user_points >= 2001 or comp_points >= 2001:
                result = "User Win!" if user_points > comp_points else "Computer Win!"
                stage = "end"

            else:
                pass
        else:
            result = ""
            history.clear()

    return  render_template('2001.html', method=method, \
                               user_points=user_points, comp_points=comp_points, \
                               result=result, stage=stage, history=history, counter=counter)

if __name__ == "__main__":
    app.run(debug=True, port=5040)
