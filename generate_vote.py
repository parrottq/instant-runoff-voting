from random import sample, randint

candidates = ["Liz", "Carl", "Jim", "Steve", "Bob", "Stacy"]
voter_count = 10000

with open("out.csv", 'w') as f:
    # Write Column titles
    f.write(",".join([f"[{e}]" for e in candidates]))
    f.write('\n')

    for e in range(voter_count):
        reorder = sample(candidates, randint(1, len(candidates)))
        for c in candidates:
            if c in reorder:
                f.write(str(reorder.index(c) + 1))
            f.write(',')
        f.write('\n')
