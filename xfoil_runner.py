import itertools
import os
import itertools
import numpy as np
import subprocess
from tqdm import tqdm


def run_single(naca='0012', re=1000000, m=0.3, alpha=0):
    result_files = f'{naca}_{re:.2e}_{m:.2}_{alpha}.dat'
    with open('xfoil_commands.txt', 'w') as commands:
        commands.write(f'naca {naca}\n')
        commands.write('oper\n')
        commands.write(f'visc {re}\n')
        commands.write(f'M {m}\n')
        commands.write(f'alfa {alpha}\n')
        commands.write(f'CPWR results/cpwr_{result_files}\n')
        commands.write(f'DUMP results/dump_{result_files}\n')
        commands.write('\nquit\n')
    subprocess.run('xfoil < xfoil_commands.txt', shell=True, stdout=subprocess.DEVNULL)
    return 0


def run_range():
    mach_range = [m for m in np.arange(0.1, 0.4, 0.05)]
    re_range = [1e8]
    alpha_range = [alpha for alpha in np.arange(-4, 12, 2)]
    max_camber = [camber for camber in np.arange(0, 6, 1)]
    max_camber_pos = [camber_pos for camber_pos in np.arange(0, 4, 1)]
    thickness = [thickness for thickness in np.arange(4, 20, 1)]

    all_configurations = itertools.product(mach_range, re_range, alpha_range, max_camber, max_camber_pos, thickness)
    all = [config for config in all_configurations]
    print(f"Number of configurations: {len(all)}")

    pbar = tqdm(total=len(all))
    for no, i in enumerate(all):
        pbar.update(1)
        run_single(f"{i[3]}{i[4]}{str(i[5]).zfill(2)}", i[1], i[0], i[2])

if __name__ == '__main__':
    run_range()

