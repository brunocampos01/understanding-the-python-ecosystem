from subprocess import Popen, PIPE, getoutput


def process(args, wait=True, pipe=True, timeout=None, **kwargs):
    ''' Run process 'args' and return the Popen instance after it's
        finished.
    '''
    if pipe:
        kwargs.update(stdout=PIPE, stderr=PIPE)
    proc = Popen(args, **kwargs)
    if wait:
        proc.wait(timeout)
    return proc


def process_output(args):
    ''' runs process 'args' and returns a list containing the
        stdout and stderr lines
    '''
    return getoutput(' '.join(args)).splitlines()
