#!/home/zsiegel/anaconda3/bin/python

import zauxpy


def main():
    # print(...)

    if False:
        # print(zauxpy.__dict__)
        for key, value in zauxpy.__dict__.items():
            if key not in ['__builtins__']:
                print(key)
                print(value, '\n')
        print(zauxpy)
        print(zauxpy.intan.RHSData)
        # print(zauxpy.RHSData)
        print(zauxpy.formatting.sinum(12435234523))
        zauxpy.formatting.msg('hi')

    if True:
        import pathlib
        trial_rhs = pathlib.Path('/home/zsiegel/projects/stim/zarek_20200302/1_200302_163336.rhs')
        trial = zauxpy.intan.RHSData(trial_rhs, do_load=True)
        print(trial)



if __name__ == "__main__":
    main()
