import random
import sys
import shlex
import os
from functools import partial
from subprocess import run, DEVNULL, PIPE, CalledProcessError

print_error = partial(print, file=sys.stderr)
dokku_env = {}


def fn_get_remote():
    result = run(shlex.split('git config dokku.remote'),
                 stdout=PIPE, stderr=DEVNULL)
    return result.stdout.decode('utf-8') or 'dokku'


def is_git_repository():
    try:
        run(["git", "rev-parse", "--git-dir"],
            stdout=DEVNULL, stderr=PIPE, check=True)
        return True
    except CalledProcessError:
        return False


def get_dokku_app_name(dokku_git_remote, dokku_remote_host):
    try:
        result = run(
            ["git", "remote", "-v"],
            stdout=PIPE,
            stderr=DEVNULL,
            check=True,
            text=True
        )
        remotes = result.stdout.splitlines()
        for remote in remotes:
            if (remote.startswith(dokku_git_remote)
                    and f"dokku@{dokku_remote_host}" in remote):
                app_name = remote.split('@')[1].split(':')[1].split()[0]
                return app_name
    except CalledProcessError:
        return None
    return None


def fn_dokku_host(dokku_git_remote, dokku_host):
    if not dokku_host:
        if os.path.isdir(".git") or is_git_repository():
            try:
                result = run(
                    ["git", "remote", "-v"],
                    stdout=PIPE,
                    check=True,
                    text=True
                )
                remotes = result.stdout.splitlines()
                for remote in remotes:
                    if remote.startswith(dokku_git_remote):
                        dokku_host = remote.split()[1].split('@')[1].split(':')[0]
                        break
            except CalledProcessError:
                pass

    return dokku_host


def fn_client_help_msg():
    print("=====> Configure the DOKKU_HOST environment variable or run dokku from a repository with a git remote named dokku")
    print("       i.e. git remote add dokku dokku@<dokku-host>:<app-name>")
    sys.exit(20)  # exit with specific status. only used in units tests for now


def fn_random_name():
    MOVES = "ABLE ABNORMA AGAIN AIREXPL ANG ANGER ASAIL ATTACK AURORA AWL BAN BAND BARE BEAT BEATED BELLY BIND BITE BLOC BLOOD BODY BOOK BREATH BUMP CAST CHAM CLAMP CLAP CLAW CLEAR CLI CLIP CLOUD CONTRO CONVY COOLHIT CRASH CRY CUT DESCRI D-FIGHT DIG DITCH DIV DOZ DRE DUL DU-PIN DYE EARTH EDU EG-BOMB EGG ELEGY ELE-HIT EMBODY EMPLI ENGL ERUPT EVENS EXPLOR EYES FALL FAST F-CAR F-DANCE FEARS F-FIGHT FIGHT FIR FIRE FIREHIT FLAME FLAP FLASH FLEW FORCE FRA FREEZE FROG G-BIRD GENKISS GIFT G-KISS G-MOUSE GRADE GROW HAMMER HARD HAT HATE H-BOMB HELL-R HEMP HINT HIT HU HUNT HYPNOSI INHA IRO IRONBAR IR-WING J-GUN KEE KICK KNIF KNIFE KNOCK LEVEL LIGH LIGHHIT LIGHT LIVE L-WALL MAD MAJUS MEL MELO MESS MILK MIMI MISS MIXING MOVE MUD NI-BED NOISY NOONLI NULL N-WAVE PAT PEACE PIN PLAN PLANE POIS POL POWDE POWE POWER PRIZE PROTECT PROUD RAGE RECOR REFLAC REFREC REGR RELIV RENEW R-FIGHT RING RKICK ROCK ROUND RUS RUSH SAND SAW SCISSOR SCRA SCRIPT SEEN SERVER SHADOW SHELL SHINE SHO SIGHT SIN SMALL SMELT SMOK SNAKE SNO SNOW SOU SO-WAVE SPAR SPEC SPID S-PIN SPRA STAM STARE STEA STONE STORM STRU STRUG STUDEN SUBS SUCID SUN-LIG SUNRIS SUPLY S-WAVE TAILS TANGL TASTE TELLI THANK TONKICK TOOTH TORL TRAIN TRIKICK TUNGE VOLT WA-GUN WATCH WAVE W-BOMB WFALL WFING WHIP WHIRL WIND WOLF WOOD WOR YUJA".split(" ")
    NAMES = "SEED GRASS FLOWE SHAD CABR SNAKE GOLD COW GUIKI PEDAL DELAN B-FLY BIDE KEYU FORK LAP PIGE PIJIA CAML LAT BIRD BABOO VIV ABOKE PIKAQ RYE SAN BREAD LIDEL LIDE PIP PIKEX ROK JUGEN PUD BUDE ZHIB GELU GRAS FLOW LAFUL ATH BALA CORN MOLUF DESP DAKED MIMI BOLUX KODA GELUD MONK SUMOY GEDI WENDI NILEM NILE NILEC KEZI YONGL HUDE WANLI GELI GUAIL MADAQ WUCI WUCI MUJEF JELLY SICIB GELU NELUO BOLI JIALE YED YEDE CLO SCARE AOCO DEDE DEDEI BAWU JIUG BADEB BADEB HOLE BALUX GES FANT QUAR YIHE SWAB SLIPP CLU DEPOS BILIY YUANO SOME NO YELA EMPT ZECUN XIAHE BOLEL DEJI MACID XIHON XITO LUCK MENJI GELU DECI XIDE DASAJ DONGN RICUL MINXI BALIY ZENDA LUZEL HELE5 0FENB KAIL JIAND CARP JINDE LAPU MUDE YIFU LINLI SANDI HUSI JINC OUMU OUMUX CAP KUIZA PUD TIAO FRMAN CLAU SPARK DRAGO BOLIU GUAIL MIYOU MIY QIAOK BEIL MUKEI RIDED MADAM BAGEP CROC ALIGE OUDAL OUD DADA HEHE YEDEA NUXI NUXIN ROUY ALIAD STICK QIANG LAAND PIQI PI PUPI DEKE DEKEJ NADI NADIO MALI PEA ELECT FLOWE MAL MALI HUSHU NILEE YUZI POPOZ DUZI HEBA XIAN SHAN YEYEA WUY LUO KEFE HULA CROW YADEH MOW ANNAN SUONI KYLI HULU HUDEL YEHE GULAE YEHE BLU GELAN BOAT NIP POIT HELAK XINL BEAR LINB MAGEH MAGEJ WULI YIDE RIVE FISH AOGU DELIE MANTE KONMU DELU HELU HUAN HUMA DONGF JINCA HEDE DEFU LIBY JIAPA MEJI HELE BUHU MILK HABI THUN GARD DON YANGQ SANAQ BANQ LUJ PHIX SIEI EGG".split(" ")

    WORD1 = MOVES[random.randint(0, len(MOVES) - 1)]
    WORD2 = MOVES[random.randint(0, len(MOVES) - 1)]
    WORD3 = MOVES[random.randint(0, len(NAMES) - 1)]

    return f"{WORD1}-{WORD2}-{WORD3}".lower()


def ssh_command(command):
    """Execute an SSH command and return the output."""
    try:
        result = run(shlex.split(command), check=True, stdout=PIPE, stderr=PIPE)
        return result.stdout.decode('utf-8')
    except CalledProcessError as e:
        return e.stderr.decode('utf-8')


def fn_is_git_repo():
    try:
        run(
            ["git", "rev-parse"],
            stdout=DEVNULL,
            check=True
        )
        return True
    except CalledProcessError:
        return False


def fn_has_dokku_remote(dokku_git_remote):
    try:
        result = run(
            ["git", "remote", "show"],
            stdout=PIPE,
            check=True,
            text=True
        )
        remotes = result.stdout.splitlines()
        for remote in remotes:
            if remote.startswith(dokku_git_remote):
                return True
        return False
    except CalledProcessError:
        return False


def main():
    dokku_env['DOKKU_TRACE'] = os.getenv('DOKKU_TRACE', 0)
    dokku_env['DOKKU_PORT'] = os.getenv('DOKKU_PORT', 22)
    dokku_env['DOKKU_HOST'] = os.getenv('DOKKU_HOST', '')

    app = ''
    dokku_git_remote = fn_get_remote()

    sys_argv = sys.argv[1:]

    cmd = sys.argv[1] if len(sys_argv) > 0 else ''
    app_arg = sys.argv[2] if len(sys_argv) > 1 else ''

    cmd_set = False
    next_index = 1
    skip = False
    args = sys_argv

    for arg in args:
        if skip:
            next_index += 1
            skip = False
            continue

        is_flag = arg.startswith('--')

        if arg == "--app":
            app = args[next_index]
            skip = True
            args = args[2:]
        elif arg == "--remote":
            dokku_git_remote = args[next_index]
            skip = True
            args = args[2:]
        elif arg.startswith("--"):
            if cmd_set and not is_flag:
                app_arg = arg
                break
            if arg == "--trace":
                dokku_env['DOKKU_TRACE'] = 1
        else:
            if cmd_set and not is_flag:
                app_arg = arg
            else:
                cmd = arg
                cmd_set = True

        next_index += 1

    dokku_remote_host = fn_dokku_host(dokku_git_remote, dokku_env['DOKKU_HOST'])

    if (not dokku_remote_host) and (not cmd.startswith("remote")):
        fn_client_help_msg()

    if not app:
        if os.path.isdir(".git") or is_git_repository():
            app = get_dokku_app_name(dokku_git_remote, dokku_remote_host)
        else:
            print_error("This is not a git repository")

    match cmd:
        case "apps:create":
            if not app and not app_arg:
                app = fn_random_name()
                counter = 0
                while True:
                    command = f"ssh -p {dokku_env['DOKKU_PORT']} dokku@{dokku_remote_host} apps"
                    apps_output = ssh_command(command)
                    if app not in apps_output:
                        break
                    if counter >= 100:
                        print_error(" !     Could not reasonably generate a new app name. Try cleaning up some apps...")
                        print(apps_output)
                        exit(1)
                    else:
                        # TODO fixed callable
                        app = 'random_name'
                        counter += 1
            elif not app:
                app = app_arg
            command = f'git remote add {dokku_git_remote} dokku@{dokku_remote_host}:{app}'
            try:
                run(shlex.split(command), check=True)
                print(f"-----> Dokku remote added at {dokku_remote_host} called {dokku_git_remote}")
                print(f"-----> Application name is {app}")
            except CalledProcessError:
                print_error(" !     Dokku remote not added! Do you already have a dokku remote?")
        case "apps:destroy":
            if fn_is_git_repo() and fn_has_dokku_remote(dokku_git_remote):
                run(["git", "remote", "remove", dokku_git_remote],
                    check=True)
        case "remote":
            print(dokku_git_remote)
            exit(0)
        case "remote:add":
            args.pop(0)
            exit(run(["git", "remote", "add"] + args).returncode)
        case "remote:list":
            exit(run(["git", "remote"]).returncode)
        case "remote:set":
            args.pop(0)
            exit(run(["git", "config", "dokku.remote"] + args).returncode)
        case "remote:remove":
            args.pop(0)
            exit_code = run(["git", "remote", "remove"] + args).returncode
            if run(["git", "config", "dokku.remote"],
                    stdout=PIPE, text=True).stdout.strip() == args[0]:
                run(["git", "config", "--unset", "dokku.remote"])
            exit(exit_code)
        case "remote:unset":
            if run(["git", "config", "dokku.remote"],
                   stdout=PIPE, text=True).stdout.strip():
                exit(run(["git", "config", "--unset", "dokku.remote"]).returncode)
            exit(0)

    commands = ["apps", "certs", "help", "ls", "nginx", "shell", "storage",
                "trace", "version"]
    if any(command in cmd for command in commands):
        app = None

    commands = ["certs:chain", "domains:add-global", "domains:remove-global",
                "domains:set-global", "ps:restore"]
    if any(command in cmd for command in commands):
        app = None

    if "storage:ensure-directory" in cmd:
        app = None

    if cmd.startswith("events") or cmd.startswith("plugin") or cmd.startswith("ssh-keys"):
        app = None

    if app_arg and app_arg == "--global":
        app = None

    if len(args) and app:
        args[0:0] = ("--app", app)

    # print(f"ssh -o LogLevel=QUIET -p {dokku_env['DOKKU_PORT']} -t dokku@{dokku_remote_host} -- {app_arg} {' '.join(args)}")
    ssh_args = ["-o", "LogLevel=QUIET", "-p", str(dokku_env['DOKKU_PORT']), "-t", f"dokku@{dokku_remote_host}", "--"]
    ssh_args.extend(args)
    result = run(["ssh"] + ssh_args, text=True)
    if result.returncode != 0:
        print_error(f"Failed to execute dokku command over ssh: exit code {result.returncode}")
        print_error("If there was no output from Dokku, ensure your configured SSH Key can connect to the remote server")
        exit(result.returncode)
