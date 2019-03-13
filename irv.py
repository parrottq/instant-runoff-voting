from csv import reader as csvreader


def colume_seperator(colume_select, colume_names, contents):
    for content in contents:
        data = {}
        for name, value in zip(colume_names, content):
            if name in colume_select:
                data[name] = value
        yield data


def format_ballot(ballot):
    # Remove empty values and none numbers
    ballot_cleaned = {key:int(value) for key, value in ballot.items() if value.isdigit()}

    # Sort candidates
    ballot_sorted = sorted(ballot_cleaned.items(), key=lambda e: e[1])

    # Return just the candidates names in order
    return [name for name, rank in ballot_sorted]


def round_tally(votes):
    results = {}

    total_votes = 0

    for vote in votes:

        if len(vote) > 1:
            for sub_vote in vote:
                if not sub_vote in results:
                    results[sub_vote] = 0

        if len(vote):
            active_vote = vote[0]
            if active_vote in results:
                results[active_vote] += 1
            else:
                results[active_vote] = 1

            total_votes += 1

    return results


def majority_present(results, total_votes):
    for candidate, votes in results.items():
        if votes/total_votes > 0.5:
            return candidate

    return False


def lowest_candidate(results):
    worst_candidates = sorted(results.items(), key=lambda k: k[1])

    last_places = []
    smallest_vote = 0
    for candidate, vote_count in worst_candidates:
        if not len(last_places):
            last_places.append(candidate)
            smallest_vote = vote_count
        else:
            if smallest_vote == vote_count:
                last_places.append(candidate)
            else:
                return last_places

    return last_places


def remove_candidate(candidate, votes):
    return [[inner for inner in outer if inner != candidate] for outer in votes]


def election(votes):
    history = []
    total_votes = len([e for e in votes if e])
    majority_leader = None

    while True:
        results = round_tally(votes)

        # Detect unlimited looping
        if len(history) and history[-1] == results:
            raise Exception("Rounds are not changing")

        history.append(results.copy())

        # The election is over if a candidate gets a majority
        candidate = majority_present(results, total_votes)
        if candidate and not majority_leader:
            # This will enable a special history recorder to see if
            # the majority leader would have gotten any votes if the
            # election continued
            majority_leader = candidate

            # Remove all votes for other candidates as they are all
            # eliminated
            stripped_votes = []
            for vote in votes:
                stripped_votes.append([vote[0], *[e for e in vote if e == majority_leader]])
            votes = stripped_votes

        # Only one candidate is left, finish
        # Note: Only one candidate can be eliminated
        #   in each history entry. This is so we know
        #   where votes come from in print_history
        #   and print_sankey
        if len(results) == 1:
            return (list(results)[0], history)

        # If there is a majority this will record
        # individual candidates being removed
        if majority_leader:
            # This picks the first candidate that is
            # not a majority and removes them so it
            # can be recoreded
            for candidate in results:
                if candidate == majority_leader:
                    continue
                votes = remove_candidate(candidate, votes)
                break

            # Skip the other elimination code below
            continue

        # Determine who is eliminated if no majority
        last_place = lowest_candidate(results)
        if len(last_place) == 1:
            votes = remove_candidate(last_place[0], votes)
        else:
            # This indicates that single last place could
            # be found, most likely because of a draw
            # We stop the election so user can resolve it
            return (None, history)


def print_history(history):
    for num, event in enumerate(history):
        message = f"Round: {num}; "
        for candidate, vote in event.items():
            message += f"Candidate {candidate}: {vote}"
            if num > 0:
                point_change = vote - history[num-1][candidate]

                sign = "+" if point_change > 0 else ""
                message += f"({sign}{point_change})"
            message += ", "
        print(message)


def generate_sankey(history):
    winner, vote_history = history
    output = ""

    last_round = 0
    for round_num, event in enumerate(zip(vote_history, vote_history[1:])):
        last_round = round_num + 1
        current_event, next_event = event

        # Check for missing key
        missing_candidate = None
        for search_candidate in current_event:
            if not (search_candidate in next_event):
                missing_candidate = search_candidate
                break

        # Add transfered votes
        for candidate, votes in next_event.items():
            # Add Candiadate current votes
            output += f"{candidate} ({round_num +1}) [{current_event[candidate]}] {candidate} ({round_num + 2})\n"

            # Difference in votes between current and next round
            votes_gained = votes - current_event[candidate]

            # Did they actually get any
            if votes_gained < 1:
                continue

            # If so note the difference
            output += f"{missing_candidate} ({round_num + 1}) [{votes_gained}] {candidate} ({round_num + 2})\n"

    return output.strip('\n')


if __name__ == "__main__":
    with open("vote_results.csv", 'r') as f:
        reader = csvreader(f)

        colume_titles = [title.strip(' ') for title in next(reader)]

        # Candidate names
        candidate_names = [name.strip('[]') for name in colume_titles if len(name) and name[0] == '[' and name[-1] == ']']
        print(candidate_names)

        ballots = []
        for column in colume_seperator(candidate_names, [e.strip('[]') for e in colume_titles], reader):
            vote = format_ballot(column)
            if vote:
                print(f"Vote: {vote}")
                ballots.append(vote)

        history = election(ballots)

        print_history(history[1])

        print()
        print("'Sankey Graph")
        print("'sankeymatic.com/build")
        print(generate_sankey(history))
        print()
