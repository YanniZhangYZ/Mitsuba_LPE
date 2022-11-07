from prototype.lexical_analysis import EdgeUtils
from prototype.lexical_analysis import StateUtils


class Verifier(object):

    # verify string using jump table
    def dfa_match(self, input_string, jump_table):
        cur_status = 0
        for i, c in enumerate(input_string):
            jump_dict = jump_table[cur_status]
            if jump_dict:
                js = jump_dict.get(c)
                if js is None:
                    return False
                else:
                    cur_status = js
            if i == len(input_string) - 1 and jump_dict.get(StateUtils.ACCEPT_STATE):
                return True
        return jump_table[cur_status].get(StateUtils.ACCEPT_STATE) is not None

    def verify_all(self, event_idx_list, nfa_start_node):
        passed_node = []
        start_node = nfa_start_node

        curr_node_set = [start_node]
        next_node_set = self.closure(curr_node_set)
        # print("----------- first closure-------------")
        # if next_node_set is not None:
        #     for n in next_node_set:
        #         print(n.node_ID)

        for i, ch in enumerate(event_idx_list):
            curr_node_set = self.move(next_node_set, ch)
            next_node_set = self.closure(curr_node_set)
            # print("----------- " + str(ch) + " finish-------------")
            # if next_node_set is not None:
            #     for n in next_node_set:
            #         print(n.node_ID)
            if next_node_set is not None:
                if self.has_accepted_state(next_node_set) and i == len(event_idx_list) - 1:
                    passed_node.append("ACCEPT")
                    return True, passed_node
                passed_node.append(next_node_set[0].node_ID)

            if next_node_set is None:
                # print("early stop at " + ch)
                passed_node.append("KILL")
                return False, passed_node

        # print("string ends, doesn't match regex")
        return False, passed_node

    def verify_batch(self, events, nfa_start_node):
        passed_node = []
        curr_start_node = nfa_start_node
        for i, e in enumerate(events):
            next_node_set = self.verify_one(e, curr_start_node)
            # print("----------- " + e + " finish-------------")
            # if next_node_set is not None:
            #     for n in next_node_set:
            #         print(n.node_ID)
            if next_node_set is not None:
                if self.has_accepted_state(next_node_set) and i == len(events) - 1:
                    passed_node.append("ACCEPT")
                    return True, passed_node
                passed_node.append(next_node_set[0].node_ID)

            if next_node_set is None:
                # print("early stop at " + e)
                passed_node.append("KILL")
                return False, passed_node

            curr_start_node = next_node_set[0]
        # print("string ends, doesn't match regex")
        return False, passed_node

    def verify_one(self, input_event, cur_start_node):
        curr_node_set = [cur_start_node]
        next_node_set = self.closure(curr_node_set)

        curr_node_set = self.move(next_node_set, input_event)
        next_node_set = self.closure(curr_node_set)

        # next_start_node = next_node_set[0]
        return next_node_set

    def closure(self, curr_node_set):
        if len(curr_node_set) <= 0:
            return None

        node_stack = []
        for i in curr_node_set:
            node_stack.append(i)
            # print("push " + str(i.node_ID))

        while len(node_stack) > 0:
            node = node_stack.pop()
            # print("pop "+str(node.node_ID))
            next1 = node.next_1
            next2 = node.next_2
            if next1 is not None and node.edge == EdgeUtils.EPSILON:
                if next1 not in curr_node_set:
                    curr_node_set.append(next1)
                    node_stack.append(next1)
                    # print("push " + str(next1.node_ID))

            if next2 is not None and node.edge == EdgeUtils.EPSILON:
                if next2 not in curr_node_set:
                    curr_node_set.append(next2)
                    node_stack.append(next2)
                    # print("push " + str(next2.node_ID))
        return curr_node_set

    def move(self, curr_node_set, ch):
        out_set = []
        for node in curr_node_set:
            # print(ch, node.edge)
            if node.edge == ch or (node.edge == EdgeUtils.CCL and ch in node.valid_input_set):
                out_set.append(node.next_1)

        return out_set

    def has_accepted_state(self, node_set):
        for node in node_set:
            if node.next_1 is None and node.next_2 is None:
                return True
