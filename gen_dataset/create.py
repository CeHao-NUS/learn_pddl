import random
import copy
random.seed(None) 

# 0. categories of object, poses and actions

class MoveObjects(enumerate):
    SALT_SHAKER = 'SaltShaker'
    PEPPER_SHAKER = 'PepperShaker'
    SPOON =  'Spoon'
    POT_LID = 'PotLid'
    CHICKEN_LEG = 'ChickenLeg'
    POT = 'Pot'
    BOWL = 'Bowl'

class StaticObjects(enumerate):
    FRIDGE = 'Fridge'
    FRIDGE_SHELF = 'FridgeShelf'
    COUNTER_LEFT = 'CounterLeft'
    COUNTER_RIGHT = 'CounterRight'
    STOVE_LEFT = 'StoveLeft'
    STOVE_RIGHT = 'StoveRight'
    DRAWER_PLACE = 'DrawerPlace'
    KITCHEN_SINK = 'KitchenSink'
    CABINET_LEFT = 'CabinetLeft'
    CABINET_RIGHT = 'CabinetRight'


class Positions(enumerate):
    IN_FRIDGE = 'InFridge'
    IN_FRIDGE_SHELF = 'InFridgeShelf'
    ON_COUNTER_LEFT = 'OnCounterLeft'
    ON_COUNTER_RIGHT = 'OnCounterRight'
    ON_STOVE_LEFT = 'OnStoveLeft'
    ON_STOVE_RIGHT = 'OnStoveRight'
    IN_DRAWER_PLACE = 'InDrawerPlace'
    IN_KITCHEN_SINK = 'InKitchenSink'
    IN_CABINET_LEFT = 'InCabinetLeft'
    IN_CABINET_RIGHT = 'InCabinetRight'
    ON_POT = 'OnPot'
    IN_POT = 'InPot'
    IN_BOWL = 'InBowl'
    IN_SINK = 'InSink'


class Actions(enumerate):
    MOVE = 'Move'
    PICK = 'Pick'
    PLACE = 'Place'
    GRASP = 'Grasp'
    PULL = 'Pull'
    PUSH = 'Push'
    TURN_ON = 'TurnOn'
    TURN_OFF = 'TurnOff'
    SPRINKLE = 'Sprinkle'
    SCOOP = 'Scoop'

class Affordances(enumerate):
    FRIDGE_DOOR_HANDLE = 'FridgeDoorHandle'
    CABINET_LEFT_DOOR_HANDLE = 'CabinetLeftDoorHandle'
    CABINET_RIGHT_DOOR_HANDLE = 'CabinetRightDoorHandle'
    FAUCET_HANDLE = 'FaucetHandle'
    STOVE_LEFT_KNOB = 'StoveLeftKnob'
    STOVE_RIGHT_KNOB = 'StoveRightKnob'
    DRAWER_HANDLE = 'DrawerHandle'

move_objects_list = [MoveObjects.SALT_SHAKER, MoveObjects.PEPPER_SHAKER, MoveObjects.SPOON, MoveObjects.POT_LID, MoveObjects.CHICKEN_LEG, MoveObjects.POT, MoveObjects.BOWL]
static_objects_list = [StaticObjects.FRIDGE, StaticObjects.FRIDGE_SHELF, StaticObjects.COUNTER_LEFT, StaticObjects.COUNTER_RIGHT, StaticObjects.STOVE_LEFT, StaticObjects.STOVE_RIGHT, StaticObjects.DRAWER_PLACE, StaticObjects.KITCHEN_SINK, StaticObjects.CABINET_LEFT, StaticObjects.CABINET_RIGHT]
positions_list = [Positions.IN_FRIDGE, Positions.IN_FRIDGE_SHELF, Positions.ON_COUNTER_LEFT, Positions.ON_COUNTER_RIGHT, Positions.ON_STOVE_LEFT, Positions.ON_STOVE_RIGHT, Positions.IN_DRAWER_PLACE, Positions.IN_KITCHEN_SINK, Positions.IN_CABINET_LEFT, Positions.IN_CABINET_RIGHT, Positions.ON_POT, Positions.IN_POT, Positions.IN_BOWL, Positions.IN_SINK]
actions_list = [Actions.MOVE, Actions.PICK, Actions.PLACE, Actions.GRASP, Actions.PULL, Actions.PUSH, Actions.TURN_ON, Actions.TURN_OFF, Actions.SPRINKLE, Actions.SCOOP]
affordances_list = [Affordances.FRIDGE_DOOR_HANDLE, Affordances.CABINET_LEFT_DOOR_HANDLE, Affordances.CABINET_RIGHT_DOOR_HANDLE, Affordances.FAUCET_HANDLE, Affordances.STOVE_LEFT_KNOB, Affordances.STOVE_RIGHT_KNOB, Affordances.DRAWER_HANDLE]

initial_positions_list = [Positions.IN_FRIDGE, Positions.IN_FRIDGE_SHELF, Positions.ON_COUNTER_LEFT, Positions.ON_COUNTER_RIGHT, \
                          Positions.IN_DRAWER_PLACE, Positions.IN_KITCHEN_SINK, Positions.IN_CABINET_LEFT, Positions.IN_CABINET_RIGHT]


affordance_mapping = {
    Positions.IN_FRIDGE: Affordances.FRIDGE_DOOR_HANDLE,
    Positions.IN_CABINET_LEFT: Affordances.CABINET_LEFT_DOOR_HANDLE,
    Positions.IN_CABINET_RIGHT: Affordances.CABINET_RIGHT_DOOR_HANDLE,
    Positions.IN_DRAWER_PLACE: Affordances.DRAWER_HANDLE,
}

articualted_objects = [StaticObjects.FRIDGE, StaticObjects.CABINET_LEFT, StaticObjects.CABINET_RIGHT, StaticObjects.DRAWER_PLACE]
in_articulated_objects = [Positions.IN_FRIDGE, Positions.IN_CABINET_LEFT, Positions.IN_CABINET_RIGHT, Positions.IN_DRAWER_PLACE]


# 1. generate initial pos of every object
class State:
    def __init__(self):
        self.state_list = {}
        for obj in move_objects_list:
            self.state_list[obj] = None

    def random_initial(self):
        for obj in move_objects_list:
            self.state_list[obj] = random.choice(initial_positions_list)

    def set_state(self, obj, pos):
        self.state_list[obj] = pos

    def __repr__(self):
        return str(self.state_list)


# 2. for every step, generate the sub-actions

def pick_out_object(state, obj):
    actions = []

    # 1. search the pose of object
    pos = state.state_list[obj]
    
    # if in articualted objects, FRIDGE, CABINET_LEFT, CABINET_RIGHT, DRAWER_PLACE
    if pos in in_articulated_objects:
        affordance = affordance_mapping[pos]
        actions.append((Actions.GRASP, affordance))
        actions.append((Actions.PULL, affordance))

    actions.append((Actions.PICK, obj))

    if pos in in_articulated_objects:
        actions.append((Actions.PUSH, affordance))

    return actions

def place_object(state, pos):
    actions = []
    actions.append((Actions.PLACE, pos))

    return actions

def use_object(state, obj):
    if obj == Affordances.FAUCET_HANDLE:
        actions = [(Actions.GRASP, obj), (Actions.TURN_ON, obj), (Actions.TURN_OFF, obj)]
    elif obj == MoveObjects.SALT_SHAKER:
        actions = [(Actions.SPRINKLE, obj)]
    elif obj == MoveObjects.PEPPER_SHAKER:
        actions = [(Actions.SPRINKLE, obj)]
    elif obj == Affordances.STOVE_LEFT_KNOB:
        actions = [(Actions.TURN_ON, obj), (Actions.TURN_OFF, obj)]
    elif obj == Affordances.STOVE_RIGHT_KNOB:
        actions = [(Actions.TURN_ON, obj), (Actions.TURN_OFF, obj)]
    elif obj == MoveObjects.SPOON:
        actions = [(Actions.SCOOP, obj)]

    return actions


# ======================== sub tasks ========================

def task1(state):
    # 1. Pick out chicken & place chicken in sink ---------------------------
    action1_1 = pick_out_object(state, MoveObjects.CHICKEN_LEG)
    action1_2 = place_object(state, Positions.IN_SINK)
    state2 = copy.deepcopy(state)
    state2.set_state(MoveObjects.CHICKEN_LEG, Positions.IN_SINK)

    return state2, action1_1 + action1_2

def task2(state):
    # 2. chicken in pot ---------------------------
    action2_1 = use_object(state, Affordances.FAUCET_HANDLE)
    action2_2 = pick_out_object(state, MoveObjects.CHICKEN_LEG)
    action2_3 = place_object(state, Positions.IN_POT)

    state3 = copy.deepcopy(state)
    state3.set_state(MoveObjects.CHICKEN_LEG, Positions.IN_POT)

    return state3, action2_1 + action2_2 + action2_3

def task3(state):
    # 3. Salt  ---------------------------
    action3_1 = pick_out_object(state, MoveObjects.SALT_SHAKER)
    action3_2 = use_object(state, MoveObjects.SALT_SHAKER)
    action3_3 = place_object(state, Positions.ON_COUNTER_RIGHT)

    state4 = copy.deepcopy(state)
    state4.set_state(MoveObjects.SALT_SHAKER, Positions.ON_COUNTER_RIGHT)

    return state4, action3_1 + action3_2 + action3_3

def task4(state):
    # 4. Pepper ---------------------------
    action4_1 = pick_out_object(state, MoveObjects.PEPPER_SHAKER)
    action4_2 = use_object(state, MoveObjects.PEPPER_SHAKER)
    action4_3 = place_object(state, Positions.ON_COUNTER_RIGHT)

    state5 = copy.deepcopy(state)
    state5.set_state(MoveObjects.PEPPER_SHAKER, Positions.ON_COUNTER_RIGHT)

    return state5, action4_1 + action4_2 + action4_3


def task5(state):
    # 5. pot in sink ---------------------------
    action5_1 = pick_out_object(state, MoveObjects.POT)
    action5_2 = place_object(state, Positions.IN_SINK)
    action5_3 = use_object(state, Affordances.FAUCET_HANDLE)

    state6 = copy.deepcopy(state)
    state6.set_state(MoveObjects.POT, Positions.IN_SINK)

    return state6, action5_1 + action5_2 + action5_3


def task6(state):
    # 6. pot on stove ---------------------------
    action6_1 = pick_out_object(state, MoveObjects.POT)
    action6_2 = place_object(state, Positions.ON_STOVE_LEFT)

    state7 = copy.deepcopy(state)
    state7.set_state(MoveObjects.POT, Positions.ON_STOVE_LEFT)

    return state7, action6_1 + action6_2

def task7(state):
    # 7 lid on pot ---------------------------
    action7_1 = pick_out_object(state, MoveObjects.POT_LID)
    action7_2 = place_object(state, Positions.ON_POT)
    action7_3 = use_object(state, Affordances.STOVE_LEFT_KNOB)

    state7 = copy.deepcopy(state)
    state7.set_state(MoveObjects.POT_LID, Positions.ON_POT)

    return state7, action7_1 + action7_2 + action7_3

def task8(state):
    # 8. bowl on counter ---------------------------
    action8_1 = pick_out_object(state, MoveObjects.BOWL)
    action8_2 = place_object(state, Positions.ON_COUNTER_RIGHT)

    state8 = copy.deepcopy(state)
    state8.set_state(MoveObjects.BOWL, Positions.ON_COUNTER_RIGHT)

    return state8, action8_1 + action8_2

def task9(state):
    # 9. take off pot lid ---------------------------
    action9_1 = pick_out_object(state, MoveObjects.POT_LID)
    action9_2 = place_object(state, Positions.ON_COUNTER_RIGHT)

    state9 = copy.deepcopy(state)
    state9.set_state(MoveObjects.POT_LID, Positions.ON_COUNTER_RIGHT)

    return state9, action9_1 + action9_2


def task10(state):
    # 10. chicken in bowl ---------------------------
    action10_1 = pick_out_object(state, MoveObjects.SPOON)
    action10_2 = use_object(state, MoveObjects.SPOON)
    action10_3 = place_object(state, Positions.IN_BOWL)

    state10 = copy.deepcopy(state)
    state10.set_state(MoveObjects.SPOON, Positions.IN_BOWL)
    state10.set_state(MoveObjects.CHICKEN_LEG, Positions.IN_BOWL)

    return state10, action10_1 + action10_2 + action10_3

def dummy_openclose(state):
    # find one in affordances_list, grasp open, close
    actions = []
    affordance = random.choice(affordances_list)
    actions.append((Actions.GRASP, affordance))
    actions.append((Actions.PULL, affordance))
    actions.append((Actions.PUSH, affordance))

    return state, actions

def dummy_pickplace(state):
    # find one in move_objects_list, pick, place
    obj = random.choice(move_objects_list)
    action_x1 = pick_out_object(state, obj)

    if len(action_x1) > 1:
        last_push = [action_x1.pop()]
    else:
        last_push = []

    action_x2 = place_object(state, random.choice(positions_list))

    return state, action_x1 + action_x2 + last_push

def add_state_action(traj, state, actions):
    traj.append({'s': state, 'a': actions})

task_mapping = {
    1: task1,
    2: task2,
    3: task3,
    4: task4,
    5: task5,
    6: task6,
    7: task7,
    8: task8,
    9: task9,
    10: task10,
    11: dummy_openclose,
    12: dummy_pickplace,
}

# ===================================== traj ================================
# [['state':[State], 'actions': ['', '', '']], ]

from task_seq import generate_sequence_with_11_12

def get_state_traj():
    state = State()
    state.random_initial()
    traj = [{'s': state, 'a': []}]


    task_sequence = generate_sequence_with_11_12(prob=0.3)

    for idx in task_sequence:
        state, actions = task_mapping[idx](state)
        add_state_action(traj, state, actions)


    return traj