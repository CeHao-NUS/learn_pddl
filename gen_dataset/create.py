import random
import copy
random.seed(None) 

# 0. categories of object, poses and actions


class MoveObjects:
    SALT_SHAKER = 'SaltShaker'
    PEPPER_SHAKER = 'PepperShaker'
    SPOON =  'Spoon'
    POT_LID = 'PotLid'
    CHICKEN_LEG = 'ChickenLeg'
    POT = 'Pot'
    BOWL = 'Bowl'

class StaticObjects:
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


class Positions:
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


class Actions:
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

class Affordances:
    FRIDGE_DOOR_HANDLE = 'FridgeDoorHandle'
    CABINET_LEFT_DOOR_HANDLE = 'CabinetLeftDoorHandle'
    CABINET_RIGHT_DOOR_HANDLE = 'CabinetRightDoorHandle'
    FAUCET_HANDLE = 'FaucetHandle'
    STOVE_LEFT_KNOB = 'StoveLeftKnob'
    STOVE_RIGHT_KNOB = 'StoveRightKnob'
    DRAWER_HANDLE = 'DrawerHandle'

move_objects_list = [MoveObjects.SALT_SHAKER, MoveObjects.PEPPER_SHAKER, MoveObjects.SPOON, MoveObjects.POT_LID, MoveObjects.CHICKEN_LEG, MoveObjects.POT, MoveObjects.BOWL]
static_objects_list = [StaticObjects.FRIDGE, StaticObjects.FRIDGE_SHELF, StaticObjects.COUNTER_LEFT, StaticObjects.COUNTER_RIGHT, StaticObjects.STOVE_LEFT, StaticObjects.STOVE_RIGHT, StaticObjects.DRAWER_PLACE, StaticObjects.KITCHEN_SINK, StaticObjects.CABINET_LEFT, StaticObjects.CABINET_RIGHT]

positions_storage_list = [Positions.IN_FRIDGE, Positions.IN_FRIDGE_SHELF, Positions.ON_COUNTER_LEFT, Positions.ON_COUNTER_RIGHT, Positions.ON_STOVE_LEFT, Positions.ON_STOVE_RIGHT, Positions.IN_DRAWER_PLACE, Positions.IN_KITCHEN_SINK, Positions.IN_CABINET_LEFT, Positions.IN_CABINET_RIGHT]
positions_object_list = [Positions.ON_POT, Positions.IN_POT, Positions.IN_BOWL, Positions.IN_SINK]
positions_list = positions_storage_list + positions_object_list

actions_list = [Actions.MOVE, Actions.PICK, Actions.PLACE, Actions.GRASP, Actions.PULL, Actions.PUSH, Actions.TURN_ON, Actions.TURN_OFF, Actions.SPRINKLE, Actions.SCOOP]
affordances_list = [Affordances.FRIDGE_DOOR_HANDLE, Affordances.CABINET_LEFT_DOOR_HANDLE, Affordances.CABINET_RIGHT_DOOR_HANDLE, Affordances.FAUCET_HANDLE, Affordances.STOVE_LEFT_KNOB, Affordances.STOVE_RIGHT_KNOB, Affordances.DRAWER_HANDLE]

initial_positions_list = [Positions.IN_FRIDGE, Positions.IN_FRIDGE_SHELF, Positions.ON_COUNTER_LEFT, Positions.ON_COUNTER_RIGHT, \
                          Positions.IN_DRAWER_PLACE, Positions.IN_KITCHEN_SINK, Positions.IN_CABINET_LEFT, Positions.IN_CABINET_RIGHT]

position_2_object= {
    Positions.IN_FRIDGE: StaticObjects.FRIDGE,
    Positions.IN_FRIDGE_SHELF: StaticObjects.FRIDGE_SHELF,
    Positions.ON_COUNTER_LEFT: StaticObjects.COUNTER_LEFT,
    Positions.ON_COUNTER_RIGHT: StaticObjects.COUNTER_RIGHT,
    Positions.ON_STOVE_LEFT: StaticObjects.STOVE_LEFT,
    Positions.ON_STOVE_RIGHT: StaticObjects.STOVE_RIGHT,
    Positions.IN_DRAWER_PLACE: StaticObjects.DRAWER_PLACE,
    Positions.IN_KITCHEN_SINK: StaticObjects.KITCHEN_SINK,
    Positions.IN_CABINET_LEFT: StaticObjects.CABINET_LEFT,
    Positions.IN_CABINET_RIGHT: StaticObjects.CABINET_RIGHT,
    Positions.ON_POT: MoveObjects.POT,
    Positions.IN_POT: MoveObjects.POT,
    Positions.IN_BOWL: MoveObjects.BOWL,
    Positions.IN_SINK: StaticObjects.KITCHEN_SINK,
}

object_2_position = {value: key for key, value in position_2_object.items()}

affordance_mapping = {
    Positions.IN_FRIDGE: Affordances.FRIDGE_DOOR_HANDLE,
    Positions.IN_CABINET_LEFT: Affordances.CABINET_LEFT_DOOR_HANDLE,
    Positions.IN_CABINET_RIGHT: Affordances.CABINET_RIGHT_DOOR_HANDLE,
    Positions.IN_DRAWER_PLACE: Affordances.DRAWER_HANDLE,
    Positions.IN_SINK: Affordances.FAUCET_HANDLE,
}

affordance_2_object = {
    Affordances.FRIDGE_DOOR_HANDLE: StaticObjects.FRIDGE,
    Affordances.CABINET_LEFT_DOOR_HANDLE: StaticObjects.CABINET_LEFT,
    Affordances.CABINET_RIGHT_DOOR_HANDLE: StaticObjects.CABINET_RIGHT,
    Affordances.DRAWER_HANDLE: StaticObjects.DRAWER_PLACE,
    Affordances.FAUCET_HANDLE: StaticObjects.KITCHEN_SINK,
    Affordances.STOVE_LEFT_KNOB: StaticObjects.STOVE_LEFT,
    Affordances.STOVE_RIGHT_KNOB: StaticObjects.STOVE_RIGHT,
}


articulated_objects = [StaticObjects.FRIDGE, StaticObjects.CABINET_LEFT, StaticObjects.CABINET_RIGHT, StaticObjects.DRAWER_PLACE]
in_articulated_objects = [Positions.IN_FRIDGE, Positions.IN_CABINET_LEFT, Positions.IN_CABINET_RIGHT, Positions.IN_DRAWER_PLACE]

objects_with_states = move_objects_list +  articulated_objects + [StaticObjects.KITCHEN_SINK, StaticObjects.STOVE_LEFT, StaticObjects.STOVE_RIGHT]

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

    if pos in in_articulated_objects:
        affordance = affordance_mapping[pos]
        actions.append((Actions.GRASP, affordance))
        actions.append((Actions.PULL, affordance))

    actions.append((Actions.PLACE, pos))

    if pos in in_articulated_objects:
        actions.append((Actions.PUSH, affordance))


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

def check_in_list(obj, obj_list):
    # obj is an element or also a list, obj is not in not_object, obj_list is a list
    if isinstance(obj, list):
        return all([item in obj_list for item in obj])
    else:
        return obj in obj_list

class Stages:
    # 1. Pick out chicken & place chicken in sink ---------------------------
    # 2. chicken in pot ---------------------------
    # 3. Salt  ---------------------------
    # 4. Pepper ---------------------------
    # 5. pot in sink ---------------------------
    # 6. pot on stove ---------------------------
    # 7 lid on pot ---------------------------
    # 8. bowl on counter ---------------------------
    # 9. take off pot lid ---------------------------
    # 10. chicken in bowl ---------------------------

    stage_finish_text = {
        1: "Pick out chicken & place chicken in sink",
        2: "chicken in pot",
        3: "Salt",
        4: "Pepper",
        5: "pot in sink",
        6: "pot on stove",
        7: "lid on pot",
        8: "bowl on counter",
        9: "take off pot lid",
        10: "chicken in bowl",
    }

    def __init__(self):
        self.stage = [0]
        
    @property
    def finished_tasks(self):
        return len(self.stage)

    def check_stage(self, state):
        if check_in_list(0, self.stage) and not check_in_list(1, self.stage) and state.state_list[MoveObjects.CHICKEN_LEG] == Positions.IN_SINK:
            new_stage = 1
        elif check_in_list(1, self.stage) and not check_in_list(2, self.stage) and state.state_list[MoveObjects.CHICKEN_LEG] == Positions.IN_POT:
            new_stage = 2
        elif check_in_list(2, self.stage) and not check_in_list(3, self.stage) and state.state_list[MoveObjects.SALT_SHAKER] == Positions.ON_COUNTER_RIGHT:
            new_stage = 3
        elif check_in_list(2, self.stage) and not check_in_list(4, self.stage) and state.state_list[MoveObjects.PEPPER_SHAKER] == Positions.ON_COUNTER_RIGHT:
            new_stage = 4
        elif check_in_list([3,4], self.stage) and not check_in_list(5, self.stage) and state.state_list[MoveObjects.POT] == Positions.IN_SINK:
            new_stage = 5
        elif check_in_list(5, self.stage) and not check_in_list(6, self.stage) and state.state_list[MoveObjects.POT] == Positions.ON_STOVE_LEFT:
            new_stage = 6
        elif check_in_list(5, self.stage) and not check_in_list(7, self.stage) and state.state_list[MoveObjects.POT_LID] == Positions.ON_POT:
            new_stage = 7
        elif check_in_list(0, self.stage) and not check_in_list(8, self.stage) and state.state_list[MoveObjects.BOWL] == Positions.ON_COUNTER_RIGHT:
            new_stage = 8
        elif check_in_list([7, 8], self.stage) and not check_in_list(9, self.stage) and state.state_list[MoveObjects.POT_LID] != Positions.ON_POT:
            new_stage = 9
        elif check_in_list(9, self.stage) and not check_in_list(10, self.stage) and state.state_list[MoveObjects.SPOON] == Positions.IN_BOWL:
            new_stage = 10
        else:
            new_stage = 0


        if not check_in_list(new_stage, self.stage):
            print("$$$$ finish task ", new_stage, ":", self.stage_finish_text[new_stage])
            self.stage.append(new_stage)

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
    new_state = copy.deepcopy(state)

    # find one in move_objects_list, pick, place / execpt chicken_leg
    obj = random.choice(move_objects_list)

    while obj == MoveObjects.CHICKEN_LEG:
        obj = random.choice(move_objects_list)

    action_x1 = pick_out_object(new_state, obj)


    place_target = random.choice(positions_list)
    action_x2 = place_object(new_state, place_target)

    new_state.set_state(obj, place_target)

    return new_state, action_x1 + action_x2 

# def dummy_openclose(state):
#     return state, []

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