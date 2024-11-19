import random
import copy

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

    if pos in articualted_objects:
        actions.append((Actions.PUSH, affordance))

    return actions

def place_object(state, pos):
    actions = []
    actions.append((Actions.PLACE, pos))

    return actions

def use_object(state, obj):
    if obj == Affordances.FAUCET_HANDLE:
        actions = [(Actions.TURN_ON, obj), (Actions.TURN_OFF, obj)]
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


# ===================================== traj ================================
# [['state':[State], 'actions': ['', '', '']], ]

def get_state_traj():
    state = State()
    state.random_initial()
    traj = [{'s': state, 'a': []}]

    # 1. Pick out chicken 
    action1 = pick_out_object(state, MoveObjects.CHICKEN_LEG)

    # 2. place chicken in sink
    actions2 = place_object(state, Positions.IN_SINK)
    state2 = copy.deepcopy(state)
    state2.set_state(MoveObjects.CHICKEN_LEG, Positions.IN_SINK)

    traj.append({'s': state2, 'a': action1 + actions2})

    # 3. chicken in pot
    action3_1 = use_object(state2, Affordances.FAUCET_HANDLE)
    action3_2 = pick_out_object(state2, MoveObjects.CHICKEN_LEG)
    action3_3 = place_object(state2, Positions.IN_POT)

    state3 = copy.deepcopy(state2)
    state3.set_state(MoveObjects.CHICKEN_LEG, Positions.IN_POT)

    traj.append({'s': state3, 'a': action3_1 + action3_2 + action3_3})

    # 4. Salt 
    action4_1 = pick_out_object(state3, MoveObjects.SALT_SHAKER)
    action4_2 = use_object(state3, MoveObjects.SALT_SHAKER)
    action4_3 = place_object(state3, Positions.ON_COUNTER_RIGHT)

    state4 = copy.deepcopy(state3)
    state4.set_state(MoveObjects.SALT_SHAKER, Positions.ON_COUNTER_RIGHT)

    traj.append({'s': state4, 'a': action4_1 + action4_2 + action4_3})


    # 5. Pepper
    action5_1 = pick_out_object(state4, MoveObjects.PEPPER_SHAKER)
    action5_2 = use_object(state4, MoveObjects.PEPPER_SHAKER)
    action5_3 = place_object(state4, Positions.ON_COUNTER_RIGHT)

    state5 = copy.deepcopy(state4)
    state5.set_state(MoveObjects.PEPPER_SHAKER, Positions.ON_COUNTER_RIGHT)

    traj.append({'s': state5, 'a': action5_1 + action5_2 + action5_3})


    # 6. pot in sink
    action6_1 = pick_out_object(state5, MoveObjects.POT)
    action6_2 = place_object(state5, Positions.IN_SINK)
    action6_3 = use_object(state5, Affordances.FAUCET_HANDLE)

    state6 = copy.deepcopy(state5)
    state6.set_state(MoveObjects.POT, Positions.IN_SINK)

    traj.append({'s': state6, 'a': action6_1 + action6_2 + action6_3})

    # 7. pot in stove
    action7_1 = pick_out_object(state6, MoveObjects.POT)
    action7_2 = place_object(state6, Positions.ON_STOVE_LEFT)
    action7_3 = use_object(state6, Affordances.STOVE_LEFT_KNOB)

    state7 = copy.deepcopy(state6)

    traj.append({'s': state7, 'a': action7_1 + action7_2 + action7_3})

    # 8. bowl on counter
    action8_1 = pick_out_object(state7, MoveObjects.BOWL)
    action8_2 = place_object(state7, Positions.ON_COUNTER_RIGHT)


    # 9. chicken in bowl
    action9_1 = pick_out_object(state7, MoveObjects.SPOON)
    action9_2 = use_object(state7, MoveObjects.SPOON)
    action9_3 = place_object(state7, Positions.IN_BOWL)

    state9 = copy.deepcopy(state7)
    state9.set_state(MoveObjects.SPOON, Positions.IN_BOWL)
    state9.set_state(MoveObjects.CHICKEN_LEG, Positions.IN_BOWL)

    traj.append({'s': state9, 'a': action9_1 + action9_2 + action9_3})

    # ================================ convert to any format ========================

    # 1. (action, obj) 

    text = ""

    for key, value in traj[0]['s'].state_list.items():
        text += key + " " + value + " | "
    text += "\n"

    length_actions = 0
    for traj_i in traj:
        actions = traj_i['a']
        length_actions += len(actions)

        action_text = ' '.join(' '.join(pair) for pair in actions)
        text += action_text 


    return text, length_actions