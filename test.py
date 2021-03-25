import argparse

import core

def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    transcript = commands.add_parser('transcript', aliases=['t'],
                                        help = 'Tworzy tranksrypcje 16kHz plików monoaudio o rozszerzeniu .wav')
    transcript.set_defaults(func=core.transcript)
    transcript.add_argument('--name', '-n', help='Uruchomi funkcje tylko w podanym folderze')

    #transcript.add_argument('--reset', '-r', action='store_true', help='Nadpisuje poprzednie transkrypcje')
    #transcript.add_argument('--force', '-f', action='store_true', help='Tworzy transkrypcje nawet dla nie spelniajacych wymagan plikow .wav')
    #transcript.add_argument('--nowarning',  '-nw', action='store_true', help='Nie wyswietli warningow')

    analyze = commands.add_parser('analyze', aliases=['a'],
                                        help = 'Tworzy wyniki (jeżeli nie istnieja) dla każdej grupy plików')
    analyze.set_defaults(func=core.analyze)
    
    #analyze.add_argument('--name', '-n', help='Uruchomi funkcje tylko w podanym folderze')
    #analyze.add_argument('--reset', '-r', action='store_true', help='Nadpisuje poprzednie wyniki')
    #analyze.add_argument('--nowarning',  '-nw', action='store_true', help='Nie wyswietli warningow')


    repair = commands.add_parser('repair', aliases=['r'],
                                        help = 'Przygotowuje folder pod kolejny test case')
    repair.add_argument('--name', '-n', required=True, help='Nazwa nowego folderu')       
    repair.add_argument('--tag', '-t', type=str, help='Podaj liczbe, każda cyfra oznacza numer taga z configu, (dla booli 0|1 = default|~default)')
    
    repair.set_defaults(func=core.repair)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    args.func(args)