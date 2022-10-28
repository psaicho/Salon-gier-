import random, re

def random_dice():
    """
    return max number of meshes from list o dice [D3, D4, D6, D8, D10, D12, D20, D100]
    :return:
    """
    dice = [3, 4, 6, 8, 10, 12, 20, 100]
    random.shuffle(dice)
    return dice[0]

def user_dice() -> int:
    print("dice available : D3, D4, D6, D8, D10, D12, D20, D100")
    code = input("select a dice ")
    patern = r"^[D](3|4|6|8|10|12|20|100){1}$"
    if re.fullmatch(patern, code) is not None:
        return int(re.split("[D]", code)[1])
    else:
        print("The specified string is not code for roll of dice")
        user_dice()


def sum_of_roll_of_dices(choice:str = "random", move: int = 2) -> int:
    sum_of_all_meshes = 0
    for i in range(move):
        if choice == 'user':
            sum_of_all_meshes += random.randint(1, user_dice())
        else:
            sum_of_all_meshes += random.randint(1, random_dice())
    return sum_of_all_meshes

def pause():
    input("click enter to roll of dice")


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

def game():
    user_points = 0
    comp_points = 0

    while True:
        if user_points >= 2001 or comp_points >= 2001:
            break
        else:
            pause()
            comp_roll_meshes = sum_of_roll_of_dices()
            print("Computer's number of meshes: ", comp_roll_meshes)
            comp_points = sum_of_points(comp_points, comp_roll_meshes)
            print(f"Comp points: {comp_points}")

            user_roll_meshes = sum_of_roll_of_dices("user")
            print("User's number of meshes: ",user_roll_meshes)
            user_points = sum_of_points(user_points, user_roll_meshes)
            print(f"Your points: {user_points}")
            print("---------------------------")
    print("User Win!" if user_points > comp_points else "Computer Win!")

if __name__ == "__main__":
    game()
