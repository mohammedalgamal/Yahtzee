"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_sorted_sequences(outcomes, length):
    """
    Function that creates all sorted sequences via gen_all_sequences
    """
    allowed_repeat = []
    all_sequences = gen_all_sequences(outcomes, length)
    sorted_sequences = set([tuple(sorted(sequence)) for sequence in all_sequences])
    for item in outcomes:
         allowed_repeat.append([item, list(outcomes).count(item)])
    #print allowed_repeat        
    for elem in set(sorted_sequences):
        for num in elem:
            for idx in allowed_repeat:
                if elem.count(num) > idx[1] and num == idx[0]:
                    sorted_sequences.discard(elem)          
    return set(sorted_sequences)

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = set([])
    for idx in hand:
        scores.add(hand.count(idx) * idx)
    #print hand    
    #print max(scores)    
    return max(scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = set([])
    scores = []
    exep = 0.0
    for die in range(1, num_die_sides + 1):
        outcomes.add(die)
    pos = gen_all_sequences(outcomes, num_free_dice)
    for seq in pos:
        scores.append(score(seq + held_dice))   
    for elem in scores:
        exep += (float(elem) / len(scores))   
    #print exep       
    return exep


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set([()])
    for elem in hand:
        added = []
        added.append(elem)
        all_holds.add(tuple(added))
        #print hand, list(hand).count(elem)
    for idx in range(len(hand) + 1):
        all_holds.update(gen_sorted_sequences(hand, idx))
    #print all_holds    
    return all_holds



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_ex = 0
    held_dice = 0
    for item in all_holds:
        #print len(list(hand)) - len(list(item))
        temp = expected_value(item, num_die_sides, len(list(hand)) - len(list(item)))
        if temp > max_ex:
            max_ex = temp
            held_dice = item
    return (max_ex, held_dice)


#def run_example():
#    """
#    Compute the dice to hold and expected score for an example hand
#    """
#    num_die_sides = 6
#    hand = (1, 1, 1, 5, 6)
#    hand_score, hold = strategy(hand, num_die_sides)
#    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
#    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
#                                       
#    
#    
    



