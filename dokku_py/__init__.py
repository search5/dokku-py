import random
import sys
import shlex
import os
import re
from subprocess import run, DEVNULL, PIPE

dokku_env = {}


def fn_get_remote():
    result = run(shlex.split('git config dokku.remote'),
                 stdout=PIPE, stderr=DEVNULL)
    return result.stdout.decode('utf-8') or 'dokku'


def git_rev_parse_result(dokku_git_remote):
    git_rev_parse = run(["git", "rev-parse", "--git-dir"], stdout=DEVNULL, stderr=DEVNULL)
    if os.path.exists(".git") or git_rev_parse.returncode == 0:
        pattern = re.compile(
            rf"^{re.escape(dokku_git_remote)}\s",
            re.IGNORECASE|re.MULTILINE)
        git_remote_cmd = run(["git", "remote", "-v"],
                             stderr=DEVNULL,
                             stdout=PIPE)
        cmd_stdout = git_remote_cmd.stdout.decode('utf-8')

        return (cmd_stdout if pattern.search(cmd_stdout) else '',
                git_remote_cmd.returncode)
    else:
        return '', ''


def fn_dokku_host(dokku_git_remote, dokku_host):
    if not dokku_host:
        cmd_stdout, ret_code = git_rev_parse_result(dokku_git_remote)
        if cmd_stdout:
            git_dokku_rev = cmd_stdout.splitlines()[0]
            git_dokku_host = git_dokku_rev.split(" ")[0].split("@")[1]
            dokku_host = git_dokku_host.split(":")[0] if ret_code == 0 else ''

    if not dokku_host:
        return ''

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


def main():
    dokku_env['DOKKU_TRACE'] = os.getenv('DOKKU_TRACE', 0)
    dokku_env['DOKKU_PORT'] = os.getenv('DOKKU_PORT', 22)
    dokku_env['DOKKU_HOST'] = os.getenv('DOKKU_HOST', '')

    app = ''
    dokku_git_remote = fn_get_remote()
    dokku_remote_host = ''

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
        is_flag = False

        if arg.startswith('--'):
            is_flag = True

        if arg == "--app":
            app = args[next_index]
            skip = True
            args = args[2:]
        elif arg == "--remote":
            dokku_git_remote = args[next_index]
            skip = True
            args = args[2:]
        elif arg.startswith("--"):
            if cmd_set and (not is_flag):
                app_arg = arg
                break
            if arg == "--trace":
                dokku_env['DOKKU_TRACE'] = 1
        else:
            if cmd_set and (not is_flag):
                app_arg = arg
            else:
                cmd = arg
                cmd_set = True

        next_index += 1

    dokku_remote_host = fn_dokku_host(dokku_git_remote, dokku_env['DOKKU_HOST'])

    if (not dokku_remote_host) and (not cmd.startswith("remote")):
        fn_client_help_msg()

    if not app:
        escape_host = f"dokku@{dokku_remote_host}"
        pattern = re.compile(
            rf"{escape_host}",
            re.IGNORECASE | re.MULTILINE)
        cmd_stdout, ret_code = git_rev_parse_result(dokku_git_remote)
        if ret_code == 0:
            if cmd_stdout and pattern.search(cmd_stdout):
                git_dokku_rev = cmd_stdout.splitlines()[0]
                app = git_dokku_rev.split(" ")[0].split("@")[1].split(":")[1]
        else:
            print(" !     This is not a git repository")

    match cmd:
        case "apps:create":
            if not app and not app_arg:
                app = fn_random_name()
                counter = 0
                ssh_command = f"ssh -p {dokku_env['DOKKU_PORT']} dokku@{dokku_remote_host} apps"
                # while ssh -p "$DOKKU_PORT" "dokku@$DOKKU_REMOTE_HOST" apps 2>/dev/null | grep -q "$APP"; do
                while True:
                    if counter >= 100:
                        print(" !     Could not reasonably generate a new app name. Try cleaning up some apps...")
                        # ssh -p "$DOKKU_PORT" "dokku@$DOKKU_REMOTE_HOST" apps
                        sys.exit(1)
                    else:
                        app = 'random_name'
                        counter += 1
            elif not app:
                app = app_arg
            """
            # if git remote add "$DOKKU_GIT_REMOTE" "dokku@$DOKKU_REMOTE_HOST:$APP"; then
            #   echo "-----> Dokku remote added at ${DOKKU_REMOTE_HOST} called ${DOKKU_GIT_REMOTE}"
            #   echo "-----> Application name is ${APP}"
            # else
            #   echo " !     Dokku remote not added! Do you already have a dokku remote?" 1>&2
            #   return
            # fi
            # ;;
        """
        case "apps:destroy":
            pass
        case "remote":
            pass
        case "remote:add":
            pass
        case "remote:list":
            pass
        case "remote:set":
            pass
        case "remote:remove":
            pass
        case "remote:unset":
            pass

    #   case "$CMD" in
    #     apps:create)

    #     apps:destroy)
    #       fn-is-git-repo && fn-has-dokku-remote && git remote remove "$DOKKU_GIT_REMOTE"
    #       ;;
    #     remote)
    #       echo "$DOKKU_GIT_REMOTE"
    #       exit 0
    #       ;;
    #     remote:add)
    #       shift 1
    #       git remote add "$@"
    #       exit "$?"
    #       ;;
    #     remote:list)
    #       git remote
    #       exit "$?"
    #       ;;
    #     remote:set)
    #       shift 1
    #       git config dokku.remote "$@"
    #       exit "$?"
    #       ;;
    #     remote:remove)
    #       shift 1
    #       git remote remove "$@"
    #       local exit_code="$?"
    #       if [[ "$(git config dokku.remote)" == "$1" ]]; then
    #         git config --unset dokku.remote
    #       fi
    #       exit "$exit_code"
    #       ;;
    #     remote:unset)
    #       if [[ -n "$(git config dokku.remote)" ]]; then
    #         git config --unset dokku.remote
    #         exit "$?"
    #       fi
    #       exit 0
    #       ;;
    #   esac
    #
    #   [[ " apps certs help ls nginx shell storage trace version " == *" $CMD "* ]] && unset APP
    #   [[ " certs:chain domains:add-global domains:remove-global domains:set-global ps:restore " == *" $CMD "* ]] && unset APP
    #   [[ " storage:ensure-directory " == *" $CMD "* ]] && unset APP
    #   [[ "$CMD" =~ events*|plugin*|ssh-keys* ]] && unset APP
    #   [[ -n "$APP_ARG" ]] && [[ "$APP_ARG" == "--global" ]] && unset APP
    #   if [[ -n "$@" ]] && [[ -n "$APP" ]]; then
    #     set -- "$APP" "$@"
    #     set -- "--app" "$@"
    #   fi
    #   # echo "ssh -o LogLevel=QUIET -p $DOKKU_PORT -t dokku@$DOKKU_REMOTE_HOST -- $app_arg $@"
    #   local ssh_args=("-o" "LogLevel=QUIET" "-p" "$DOKKU_PORT" "-t" "dokku@$DOKKU_REMOTE_HOST" "--")
    #   ssh_args+=("$@")
    #   ssh "${ssh_args[@]}" || {
    #     ssh_exit_code="$?"
    #     echo " !     Failed to execute dokku command over ssh: exit code $?" 1>&2
    #     echo " !     If there was no output from Dokku, ensure your configured SSH Key can connect to the remote server" 1>&2
    #     return $ssh_exit_code
    #   }
#
# fn-is-git-repo() {
#   git rev-parse &>/dev/null
# }
#
# fn-has-dokku-remote() {
#   git remote show | grep -E "^${DOKKU_GIT_REMOTE}\s"
# }
#
# if [[ "$0" == "dokku" ]] || [[ "$0" == *dokku_client.sh ]] || [[ "$0" == $(command -v dokku) ]]; then
#   main "$@"
#   exit $?
# fi
