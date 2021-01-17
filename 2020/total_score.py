import os
import re

files = os.listdir(os.path.join('old_solvers/results', 'solver1')) + os.listdir(os.path.join('old_solvers/results', 'solver2')) + \
        os.listdir(os.path.join('old_solvers/results', 'solverd'))

problems = [f[0] for f in files]
scores = [int(re.sub(r'^.*_(.*)\.txt$', '\\1', f)) for f in files]

result = {k: [] for k in set(problems)}
[result[k].append(v) for k, v in zip(problems, scores)]
result = {k: max(result[k]) for k in result.keys() if k != 'a'}

print('#### Results #####')
print(result)
print(f'Total Result = {sum(result.values())}')