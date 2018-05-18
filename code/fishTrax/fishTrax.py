import ArenaControllerMainWindow

if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', '--rig', dest='rig', default=None, 
                        help="Shortcut to auto-configure camera and ardiuno left or right rig (pass l or r)")
    args = parser.parse_args()

    ardPortName = None
    cameraId = None
    if args.rig == 'l' or args.rig == 'left':
       ardPortName = '/dev/ttyACM0'
       cameraId = 1
 
    if args.rig == 'r' or args.rig == 'right':
       ardPortName = '/dev/ttyACM1'        
       cameraId = 0

    ArenaControllerMainWindow.main(ardPortName=ardPortName, cameraId=cameraId)
