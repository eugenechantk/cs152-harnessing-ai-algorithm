import pyswip
from pyswip.easy import *
from Tkinter import *


KB = """
% Enter your KB below this line:
pick_restaurant(anandam) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [vegetarian,indian]), payment(Pay), memberOfPay(Pay , [card]), price(Price), smallerThan(150, Price), rating(Rating), smallerThan(Rating,3.6), distance(Distance), smallerThan(2.5, Distance).
pick_restaurant(mainland_china) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [chinese, seafood]), payment(Pay), memberOfPay(Pay , [card,cash]), price(Price), smallerThan(400, Price), rating(Rating), smallerThan(Rating,3.7), distance(Distance), smallerThan(1.6, Distance).
pick_restaurant(burger_king) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [fast_food, burger]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(200, Price), rating(Rating), smallerThan(Rating,3.6), distance(Distance), smallerThan(4.7, Distance).
pick_restaurant(kfc) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [fast_food, burger]), payment(Pay), memberOfPay(Pay , [cash]), price(Price), smallerThan(200, Price), rating(Rating), smallerThan(Rating,3.7), distance(Distance), smallerThan(3.1, Distance).

pick_restaurant(dominos_pizza) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [fast_food, pizza]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(300, Price), rating(Rating), smallerThan(Rating,3.7), distance(Distance), smallerThan(1.9, Distance).
pick_restaurant(karachi_cafe) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [cafe]), payment(Pay), memberOfPay(Pay , [card]), price(Price), smallerThan(250, Price), rating(Rating), smallerThan(Rating,4.0), distance(Distance), smallerThan(3.3, Distance).
pick_restaurant(whiteboard_cafe) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [vegetarian,cafe]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(250, Price), rating(Rating), smallerThan(Rating,3.9), distance(Distance), smallerThan(2.5, Distance). 
pick_restaurant(firangi_bake) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [italian,mexican]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(250, Price), rating(Rating), smallerThan(Rating,3.6), distance(Distance), smallerThan(2.9, Distance).
pick_restaurant(little_italy) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [vegetarian,italian,continental]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(750, Price), rating(Rating), smallerThan(Rating,3.6), distance(Distance), smallerThan(2.2, Distance).
pick_restaurant(mamagoto) :- cuisine(Cuisine),  memberOfCuisine(Cuisine , [asian]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(600, Price), rating(Rating), smallerThan(Rating,4.3), distance(Distance), smallerThan(1.0, Distance).
pick_restaurant(urban_asia) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [asian]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(450, Price), rating(Rating), smallerThan(Rating,4.2), distance(Distance), smallerThan(9.0, Distance).
pick_restaurant(hitec_nanking) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [chinese]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(350, Price), rating(Rating), smallerThan(Rating,3.7), distance(Distance), smallerThan(3.7, Distance).
pick_restaurant(grill_box) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [mediterranean]), price(Price), memberOfPay(Pay , [cash,card]), payment(Pay), smallerThan(200, Price), rating(Rating), smallerThan(Rating,2.7), distance(Distance), smallerThan(4.2, Distance).

pick_restaurant(freshies_gourmet_salad) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [healthy_food, salad]), payment(Pay), memberOfPay(Pay , [cash]), price(Price), smallerThan(250, Price), rating(Rating), smallerThan(Rating,3.4), distance(Distance), smallerThan(2.8, Distance).
pick_restaurant(mustang_terrace_lodge) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [mexican,italian,salad,indian]), payment(Pay), memberOfPay(Pay , [cash]), price(Price), smallerThan(550, Price), rating(Rating), smallerThan(Rating,3.9), distance(Distance), smallerThan(3.9, Distance).
pick_restaurant(india_bistro) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [indian]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(500, Price), rating(Rating), smallerThan(Rating,4.5), distance(Distance), smallerThan(1.4, Distance).
pick_restaurant(drunken_monkey) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [healthy_food]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(200, Price), rating(Rating), smallerThan(Rating,4.0), distance(Distance), smallerThan(3.0, Distance).
pick_restaurant(wich_please) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [fast_food]), payment(Pay), memberOfPay(Pay , [card]), price(Price), smallerThan(100, Price), rating(Rating), smallerThan(Rating,3.6), distance(Distance), smallerThan(2.9, Distance).

pick_restaurant(punjabi_bytes) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [indian]), payment(Pay), memberOfPay(Pay , [cash]), price(Price), smallerThan(100, Price), rating(Rating), smallerThan(Rating,3.7), distance(Distance), smallerThan(2.7, Distance).
pick_restaurant(holi_restaurant) :-  cuisine(Cuisine), memberOfCuisine(Cuisine , [indian,chinese]), payment(Pay), memberOfPay(Pay , [cash,card]), price(Price), smallerThan(400, Price), rating(Rating), smallerThan(Rating,2.5), distance(Distance), smallerThan(0.8, Distance).
memberOfCuisine([Xh|Xt], Y) :- member(Xh,Y), (length(Xt,0) -> !; memberOfCuisine(Xt, Y)).
memberOfPay([H|T], P) :- member(H,P); memberOfPay(T,P).
smallerThan(X,Y) :- X =< Y.
"""

with open("KB.pl", "w") as text_file: text_file.write(KB)

cuisine_options = ['vegetarian', 'indian', 'chinese', 'seafood', 'fast_food',
                   'burger', 'pizza', 'cafe', 'italian', 'mexican', 'continental', 'asian',
                   'mediterranean', 'healthy_food', 'salad']

payment_options = ['cash', 'card']

def get_restaurant():
    chosen_cuisines = []
    chosen_cuisines = [key for key, ans in zip(cuisine.keys(),
                                               [cuisine[key].get() for key in cuisine.keys()]) if ans]
    chosen_payment = []
    chosen_payment = [key for key, ans in zip(payment.keys(),
                                               [payment[key].get() for key in payment.keys()]) if ans]

    prolog = pyswip.Prolog() # Global handle to interpreter
    prolog.consult("KB.pl") # open the KB
    pick_restaurant = Functor("pick_restaurant",1)

    # declaring dynamic procedures to allow multiple executions
    # to allow asserta and retractall as inputs change
    prolog.dynamic('cuisine/1')
    prolog.dynamic('payment/1')
    prolog.dynamic('price/1')
    prolog.dynamic('rating/1')
    prolog.dynamic('distance/1')

    # assert user input (list object) into the respective predicates
    prolog.asserta("cuisine(" + str(chosen_cuisines) + ")")
    prolog.asserta("payment("+ str(chosen_payment) + ")")
    prolog.asserta("price("+ str(price.get()) + ")")
    prolog.asserta("rating(" + str(rating.get()) + ")")
    prolog.asserta("distance(" + str(distance.get()) + ")")

    q = prolog.query('pick_restaurant(X)')
    sols = [] # used to find length of solution
    ans = '' # placeholder for answers for printing
    for value in list(q):
        if value not in sols:
            # iterate over solutions and remove repetitions
            sols.append(value)

    ans = ', '.join(d['X'] for d in sols) # convert list of dicts to string

    if not len(sols): ans = "Sorry, couldn't found any restaurant."

    ans_label.config(text = "You can get food from: " + ans )

    # retract all assertions after obtaining results
    prolog.retractall("cuisine(" + str(chosen_cuisines) + ")")
    prolog.retractall("payment("+ str(chosen_payment) + ")")
    prolog.retractall("price("+ str(price.get()) + ")")
    prolog.retractall("rating(" + str(rating.get()) + ")")
    prolog.retractall("distance(" + str(distance.get()) + ")")

# using TkInter for Graphical User Interface
master = Tk()
master.title("Minerva Hyderabad Restaurant Selector")

##Make some spacing on the left
for row in range(13):
    Label(master, text="").grid(row= row, column = 1, sticky=W)

Label(master, text=" Minerva Hyderabad Restaurant Selector").grid(row=0, sticky=W, column = 2)

Label(master, text="\t\t").grid(row=1, sticky=W)
price = DoubleVar()
Scale(master, label = "Avg Price (Rupees per person)", from_= 100, to = 1000,
      variable = price, orient = HORIZONTAL, length = 300).grid(row = 2,  column = 2)

Label(master, text="\t\t").grid(row=2, sticky=W)
distance = DoubleVar()
Scale(master, label = "Distance from Res Hall (km)", from_= 0.5, to = 5,
      variable = distance, resolution =   0.1, orient = HORIZONTAL, length = 300).grid(row = 3, column = 2)

Label(master, text="\t\t").grid(row=4, sticky=W)
rating = DoubleVar()
Scale(master, label = "Minimum restaurant rating (0 to 5)", from_= 0.0, to = 5.0,
      variable = rating, resolution =   0.1, orient = HORIZONTAL, length = 300).grid(row = 5, column = 2)

#Make checklist for cuisines
Label(master, text="\t\t").grid(row=6, sticky=W)
Label(master, text="Select Cuisines: ").grid(row=7, sticky=W, column = 2)
cuisine = {}
row = 8
for key in cuisine_options:
    cuisine[key] = IntVar()
    Checkbutton(master, text= key, variable= cuisine[key]).grid(row = row, sticky=W, column = 2)
    row += 1

#Add payment methods
Label(master, text="Payment Method:").grid(row=7, column = 3, sticky=W)
payment = {}
row = 8
for key in payment_options:
    payment[key] = IntVar()
    Checkbutton(master, text= key, variable= payment[key]).grid(row= row, column = 3, sticky=W)
    row += 1

Button(master, text='GIVE ME FOOD', command=get_restaurant).grid(row= 15, pady=4, column = 3)
ans_label = Label(master, text= "")
ans_label.grid(row=17, column = 3)
mainloop()
