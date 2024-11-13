# Question 1

def norway_pandemic():
    region = input("Hvor er du bosatt? ")
    if region.startswith("V"):
        print("Velkommen til Norge!")
        return
    if yes_or_no("Er du fullvaksinert?") or yes_or_no("Har du gjennomgått koronasykdom de siste seks månedene?"):
        print("Velkommen til Norge!")
    else:
        print("Velkommen til Norge, men du må teste deg og sitte i karantene.")

def yes_or_no(input_question):
    answer = input(input_question).strip().lower()
    return answer == "ja"

# Question 2

def price(drink_order):
    price_dictionary = {"kaffe": 30, "öl": 50, "kola": 25}
    quantity, drink = drink_order.split(" ")

    return price_dictionary.get(drink, 0) * int(quantity)


def get_order():
    total_cost = 0
    while True:
        order = input("Vad vill ni dricka? (Skriv 'Det är bra så' för att avsluta): ")
        if order == "Det är bra så":
            break

        item_price = price(order)
        if item_price == 0:
            print("Finns inte på menyn")
        else:
            total_cost += item_price

    print("Det blir", total_cost, "kronor")

# Question 3

def alter(s):
    if len(s) < 2:
        return s
    else:
        return s[1] + s[0] + alter(s[2:])

def scramble(s):
    if len(s) < 2:
        return s
    return s[0] + alter(s[1:-1]) + s[-1]

def scrambles(s):
    words = s.split()
    scrambled_words = []
    for word in words:
        scrambled_words.append(scramble(word))
    return " ".join(scrambled_words)

# Question 4

edges = [(0,1), (1,2), (2,0), (2,3)]

def edges2adjacency(edges):
    d = {}
    for src, trg in edges:
        d.setdefault(src, []).append(trg)
        d.setdefault(trg, []).append(src)
    return d

print(edges2adjacency(edges))

def adjacency2edges(adj):
    return [(src, trg) for src, trgs in adj.items() for trg in trgs if src < trg]

adj = edges2adjacency(edges)

print(adjacency2edges(adj))