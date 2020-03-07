#!/home/zsiegel/anaconda3/bin/python

import zauxpy


def main():
    # print(...)

    if False:
        # print(zauxpy.__dict__)
        for key, value in zauxpy.__dict__.items():
            print(key)
            print(value, '\n')
        print(zauxpy)
        print(zauxpy.intan.RHSData)
        # print(zauxpy.RHSData)
        print(zauxpy.formatting.sinum(12435234523))


if __name__ == "__main__":
    main()
