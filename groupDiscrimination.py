from itertools import chain, combinations, product
from utils import build, defineDict

fields = defineDict('./file/inputHeading.txt')


def _all_other_fields(self, i_fields):
    try:
        return [f for f in self.fields if f not in i_fields]
    except:
        print("Issue in _all_other_fields")


def field_filter(field, dict):
    list(filter(lambda a: a.race != 'white', dict))

    '''
    i_fields: list of `Input.name`
        The inputs of interest, i.e. compute the casual discrimination wrt
        these fields.
    conf: float in [0, 1]
        The z * confidence level(percentage of normal distribution.
    margin: float in [0, 1]
        The margin of error for the confidence.

    Returns
    - ------
    tuple
        * list of dict
            The test suite used to compute group discrimination.
        * float
            The percentage of group discrimination
    '''
    assert i_fields != None
    try:
        data_suite = build()
        print("Start execution on " + data_suite + "samples\n")
        print("Field setted:" + race)
        print(i_fields)
        print(data_suite)
        min_group = float("inf")
        min_group = 0
        max_group = 0
        p = 0
        rand_fields = self._all_other_fields(i_fields)
        print(rand_fields)
        '''for fixed_sub_assign in self._gen_all_sub_inputs(args=i_fields): '''
        for fixed_sub_assign in data_suite:
            count = 0
            '''for num_sampled in range(1, self.max_samples):'''
            for num_sampled in range(1, 10):
                assign = self._new_random_sub_input(args=rand_fields)
                assign.update(fixed_sub_assign)
                self._add_assignment(data_suite, assign)
                count += self._get_test_result(assign=assign)

                p, end = self._end_condition(count, num_sampled, conf, margin)
                if end:
                    break
            min_group = min(min_group, p)
            max_group = max(max_group, p)

        return data_suite, (max_group - min_group)
    except:
        print("Issue in group_discrimination")


def discrimination_search(self, threshold=0.2, conf=0.99, margin=0.01,
                          group=False, causal=False):
    """
    Find all minimall subsets of characteristics that discriminate.

    Choose to search by group or causally and set a threshold for
    discrimination.

    Parameters
    - ---------
    threshold: float in [0, 1]
        At least this level of discrimination to be considered.
    conf: float in [0, 1]
        The z * confidence level(percentage of normal distribution.
    margin: float in [0, 1]
        The margin of error for the confidence.
    group: bool
        Search for group discrimination if `True`.
    causal: bool
        Search for causal discrimination if `True`.

    Returns
    - ------
    tuple of dict
        The lists of subsets of the input characteristics that discriminate.
    """
    try:
        assert group or causal
        group_d_scores, causal_d_scores = {}, {}
        for sub in self._all_relevant_subs(self.input_order):
            if self._supset(list(set(group_d_scores.keys()) |
                                 set(causal_d_scores.keys())), sub):
                continue
            if group:
                _, p = self.group_discrimination(i_fields=sub, conf=conf,
                                                 margin=margin)
                if p > threshold:
                    group_d_scores[sub] = p
            if causal:
                _, p = self.causal_discrimination(i_fields=sub, conf=conf,
                                                  margin=margin)
                if p > threshold:
                    causal_d_scores[sub] = p

        return group_d_scores, causal_d_scores
    except:
        print("Issue in trying to search for discrimination")


def _all_relevant_subs(self, xs):
    try:
        return chain.from_iterable(combinations(xs, n)
                                   for n in range(1, len(xs)))
    except:
        print("Issue in returning reltive ssubsets. Possible a divide by zer error")


def discrimination_search(self, threshold=0.2, conf=0.99, margin=0.01,
                          group=False, causal=False):
    """
    Find all minimall subsets of characteristics that discriminate.

    Choose to search by group or causally and set a threshold for
    discrimination.

    Parameters
    - ---------
    threshold: float in [0, 1]
        At least this level of discrimination to be considered.
    conf: float in [0, 1]
        The z * confidence level(percentage of normal distribution.
    margin: float in [0, 1]
        The margin of error for the confidence.
    group: bool
        Search for group discrimination if `True`.
    causal: bool
        Search for causal discrimination if `True`.

    Returns
    - ------
    tuple of dict
        The lists of subsets of the input characteristics that discriminate.
    """
    try:
        assert group or causal
        group_d_scores, causal_d_scores = {}, {}
        for sub in self._all_relevant_subs(self.input_order):
            if self._supset(list(set(group_d_scores.keys()) |
                                 set(causal_d_scores.keys())), sub):
                continue
            if group:
                _, p = self.group_discrimination(i_fields=sub, conf=conf,
                                                 margin=margin)
                if p > threshold:
                    group_d_scores[sub] = p
            if causal:
                _, p = self.causal_discrimination(i_fields=sub, conf=conf,
                                                  margin=margin)
                if p > threshold:
                    causal_d_scores[sub] = p

        return group_d_scores, causal_d_scores
    except:
        print("Issue in trying to search for discrimination")
