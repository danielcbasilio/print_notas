"""
Substitute the variables in __main__.py to run this script
"""

def get_count_sem_aprovacao(alist, top_marks):
    count = 0
    for std in alist:
        if std[2] == -1 or (std[1]/top_marks)*20 < 9.5:
            count += 1
    return count

def get_percentage_pos(alist, top_marks):
    positives = 0
    total = 0
    for std in alist:
        if (std[1]/top_marks)*20 >= 9.5:
            positives += 1
            total += 1
        else:
            total += 1
    return round((positives/total)*100, 2)

def media(alist):
    last_elements = [t[1] for t in alist if t[2] != -1]
    average = sum(last_elements) / len(last_elements)
    return round(average, 2)

# must be with top_marks 20
def count_grades(alist):
    res = {
        20:0, 19:0, 18:0, 17:0, 16:0, 15:0, 14:0, 13:0, 12:0, 11:0, 10:0
    }
    for curr in alist:
        if curr[2] in res:
            res[curr[2]] += 1
    return res

def get_top_percenters_list(list1, top_percent):
    grade_limit = list1[int(len(list1)*(top_percent/100))-1][1]
    top_percenters = list(filter(lambda x: x[1]>=grade_limit, list1))
    return top_percenters

# --------------------------------------- Printing Results --------------------------------------- #

BARRA = "-----------------------------------------------------------------------"

def putString(f, astring, end="\n"):
    print(astring, end=end)
    if end == "":
        f.write(str(astring))
    else:
        f.write(str(astring) + "\n")

def print_notas_txt_and_terminal(filename, alist, test_name, top_percent_tup, arg_sem_aprovacao, arg_media, arg_percent_pos, count_dict, top_marks=20, extra_col = False, save = True):
    if save:
        f = open("results/" + filename + ".txt", "w")
    else:
        class Mock:
            def write(self, text):
                return
            def close(self):
                return
        f = Mock()

    putString(f, "")
    putString(f, BARRA)
    putString(f, "Resultados:" + " " + test_name)
    putString(f, BARRA)
    putString(f, "Número de alunos:" + " " + str(len(alist)))
    putString(f, "Alunos sem aprovação:" + " " + str(arg_sem_aprovacao))
    putString(f, "Positivas:" + " " + str(arg_percent_pos)+"%")
    putString(f, "Média:" + " " + str(arg_media) + " " + "/" + str(top_marks))
    putString(f, BARRA)
    if extra_col: # does the from 10 to 20 count if applicable
        # convert to ordered list
        counts_list = []
        for grade, count in count_dict.items():
            counts_list.append((grade, count))
        counts_list = sorted(counts_list, reverse=True)
        putString(f, "Grade: |", end="")
        for grade, _ in counts_list:
            putString(f, f" {grade:<3}|", end="")
        putString(f, "")
        putString(f, "Count: |", end="")
        for _, count in counts_list:
            putString(f, f" {count:<3}|", end="")
        putString(f, "")
        putString(f, BARRA)
    top_percent, top_percenters = top_percent_tup
    putString(f, "Top " + str(top_percent) + "%\n")
    if top_marks == 20:
        for i, std in enumerate(top_percenters):
            if std[1] == top_percenters[i-1][1]:
                putString(f, f"{chr(ord('-')):<3} |  {std[0]:<55} | {std[1]:.2f}")
            else:
                putString(f, f"{str(i+1):<3} |  {std[0]:<55} | {std[1]:.2f}")
    else:
        for i, std in enumerate(top_percenters):
            if std[1] == top_percenters[i-1][1]:
                putString(f, f"{chr(ord('-')):<3} |  {std[0]:<55} | {round(std[1])}")
            else:
                putString(f, f"{str(i+1):<3} |  {std[0]:<55} | {round(std[1])}")
    putString(f, BARRA)
    putString(f, "")
    f.close()

def print_notas(formatted_data_filepath, test_name, top_percent, save):
    format_list = []
    alist = []
    extra_col = True
    top_marks=20
    with open(formatted_data_filepath, "r") as f:
        format_list = "".join(f.readlines()).split("\n")
        del format_list[-1] # delete last empty string
        for line in format_list:
            std = line.split("\t")
            if len(std) == 3:
                name, grade, final_grade = std
                grade = float(grade)
                final_grade = float(final_grade)
                alist.append((name, grade, final_grade))
            elif len(std) == 2:
                extra_col = False
                name, grade = std
                grade = float(grade)
                alist.append((name, grade))
            else:
                print("Error: wrongly formatted")
                break
            if grade > 20:
                top_marks = 100
        arg_percent_pos = get_percentage_pos(alist, top_marks)
        arg_media = media(alist)
        if extra_col:
            arg_sem_aprovacao = get_count_sem_aprovacao(alist, top_marks)
            count_dict = count_grades(alist)
        else:
            count_dict = {}
        alist = sorted(alist, key=lambda x: x[1], reverse=True)
        filename = formatted_data_filepath[15:-4]
        top_percenters_list = get_top_percenters_list(alist, top_percent)
        print_notas_txt_and_terminal(filename, alist, test_name, (top_percent, top_percenters_list), arg_sem_aprovacao, arg_media, arg_percent_pos, count_dict, top_marks, extra_col, save)

# exemplo
# print_notas("formatted_data/am_23_24.tsv", "AM - Notas finais", 10, True)