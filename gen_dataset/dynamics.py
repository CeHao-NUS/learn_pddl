from create import *
from utils import *

Positions.OPEN = 'Open'
Positions.CLOSE = 'Close'
Positions.IN_HAND = 'InHand'

class State:
    def __init__(self):
        self.state_list = {}

        # move and static
        for obj in move_objects_list:
            self.state_list[obj] = None

        for obj in objects_with_states:
            self.state_list[obj] = Positions.CLOSE

    def set_state(self, obj, pos):
        self.state_list[obj] = pos

    def get_state(self, obj):
        return self.state_list[obj]

    def __repr__(self):
        return str(self.state_list)
    
    def diff_with(self, state):
        # compare self and state, 
        # print as (self) -> (state)

        for obj in self.state_list:
            if self.state_list[obj] != state.state_list[obj]:
                print(f"{obj}: {self.state_list[obj]} -> {state.state_list[obj]}")

        


def parse_state_text(state_text):
    state = State()

    for i in range(0, len(state_text), 2):
        obj = state_text[i]
        pos = state_text[i + 1]

        state.set_state(obj, pos)

    return state

def parse_action_text(text):
    actions = []

    for i in range(0, len(text), 2):
        act = text[i]
        target = text[i + 1]

        actions.append((act, target))

    return actions
    


    

class Dynamic:

    def __init__(self, state, actions):
        self.state = state
        self.actions = actions
        self.stage = Stages()

        self.in_hand = ''
        self.in_dual_hand = ''
        self.traj = []

    def forward(self):
        self.traj.append({'s': self.state, 'a': []})

        for act in self.actions:
            print('====================')
            print(act)
            state_new = self.apply_action(self.state, act)
            if state_new:
                self.state.diff_with(state_new)
                self.state = state_new
                self.stage.check_stage(self.state)
            else:
                print('Failed !!!')
                break
            self.traj.append({'s': state_new, 'a': act})
            a = 1

    def apply_action(self, state, action):
        state_new = copy.deepcopy(state)

        act, target = action  #(act, target)

        # 1. pick, place -> in hand
        if act in [Actions.PICK, Actions.PLACE]:
            # check if target is articulated and open, or just open space
            # the target should be a place or container

            if act == Actions.PICK:
                if self.in_hand:
                    print('Error: Already have object in hand')
                    a = b
                    return None
                
                target_position = state_new.get_state(target)
                target_name = position_2_object[target_position]

            elif act == Actions.PLACE:
                if not self.in_hand:
                    print('Error: No object in hand')
                    a = b
                    return None

                target_name = position_2_object[target]

            case1 = target_name in static_objects_list or target_name in [MoveObjects.POT, MoveObjects.BOWL]
            case2 = True if target_name not in articulated_objects or state_new.state_list[target_name] == Positions.OPEN else False

            if case1 and case2:
                if act == Actions.PICK:
                    self.in_hand = target
                    state_new.set_state(target, Positions.IN_HAND)
                elif act == Actions.PLACE:
                    state_new.set_state(self.in_hand, target)
                    self.in_hand = ''
            else:
                print('Error: Cannot pick or place the target')
                a = b
                return None

            return state_new

        # 2. grasp handle -> pre-check / pull, push, turnon, turnoff -> articulated changed
        elif act in [Actions.GRASP]:
            # check if target is affordance, then make the affordance in-hand
            case1 = target in affordances_list
            case2 = not self.in_dual_hand
            if case1 and case2:
                self.in_dual_hand = target
            else:
                print('Error: Cannot grasp the target')
                a = b
                return None

            return state_new


        elif act in [Actions.PULL, Actions.PUSH, Actions.TURN_ON, Actions.TURN_OFF]:
            # check the target is affordance, and state is in hand. then open or close it.
            case1 = target in affordances_list
            case2 = self.in_dual_hand == target

            if case1 and case2:
                # affordance -> object 
                target_name = affordance_2_object[target]

                if act in [Actions.PULL, Actions.TURN_ON]:
                    state_new.set_state(target_name, Positions.OPEN)

                elif act in [Actions.PUSH, Actions.TURN_OFF]:
                    state_new.set_state(target_name, Positions.CLOSE)
                    self.in_dual_hand = ''


        # 3. Sprinkle, scoop -> pre-check
        elif act in [Actions.SPRINKLE]:
            # special
            a = 1

        elif act in [Actions.SCOOP]:
            # special
            case1 = self.in_hand == MoveObjects.SPOON

            if case1:
                state_new.set_state(MoveObjects.SPOON, Positions.IN_BOWL)
            else:
                print('Error: Cannot scoop')
                a = b
                return None

        return state_new


def check_generated_actions(task):
    state_dim = 7
    state_text = task[:state_dim * 2]
    action_text = task[state_dim * 2:]

    # ============ 1. parse state and actions
    state = parse_state_text(state_text)
    action = parse_action_text(action_text)


    # ============ 2. create dynamics

    dynamic = Dynamic(state, action)

    # ============ 3. forward

    dynamic.forward()

    return dynamic.stage.finished_tasks - 1

# ============ 0. read state and actions from txt


# seperate by individual '\n' 
texts = load_custom_texts('dataset.txt', remove_newline=True)
state_traj = convert_state_trajectory(texts)

all_length = []

for task_name in state_traj.keys():
    print('+++++++++++++++++++++++++++'*3)
    print(task_name)
    print('+++++++++++++++++++++++++++'*3)
    task = state_traj[task_name][0]

    now_stage = check_generated_actions(task)
    if now_stage < 10:
        a = 1

    
    all_length.append(now_stage)


from collections import Counter
frequency = Counter(all_length)

print('Frequency: ', frequency)

print('Average: ', sum(all_length) / len(all_length))
a = 1



