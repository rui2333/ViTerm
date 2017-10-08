import os, sys, inspect, thread, time, json

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# arch_dir = './lib/x64' if sys.maxsize > 2**32 else './lib/x86'
arch_dir = './lib'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        frame = controller.frame()
        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

def main():
    print 'connecting'
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # counter
    countDict = {}
    for i in range(26):
        countDict[chr(ord("a")+i)] = 0

    count = 0
    # when hitting space, output a json
    print "Press Enter to output"
    while True:
        time.sleep(0.02)
        # the output file
        if count == 0:
            letter = sys.stdin.readline()[0]

        filename = 'trainings/'+ letter + str(count)+".json"
        count = count+1
        if count == 500:
            count = 0
            print letter + ' done'

        file  = open(filename, "w")

        frame = controller.frame()
        frameDict = {
            'id': frame.id,
            'timestamp': frame.timestamp,
            'hand': {
                'is_left': frame.hands[0].is_left,
                'is_right': frame.hands[0].is_right,
                'palm_normal': [frame.hands[0].palm_normal.x, frame.hands[0].palm_normal.y, frame.hands[0].palm_normal.z],
                'palm_position': [frame.hands[0].palm_position.x, frame.hands[0].palm_position.y, frame.hands[0].palm_position.z],
                'palm_velocity': [frame.hands[0].palm_velocity.x, frame.hands[0].palm_velocity.y, frame.hands[0].palm_velocity.z],
                'palm_width': frame.hands[0].palm_width,
                'grab_strength': frame.hands[0].grab_strength,
                'pinch_strength': frame.hands[0].pinch_strength,
                'wrist_position': [frame.hands[0].wrist_position.x, frame.hands[0].wrist_position.y, frame.hands[0].wrist_position.z]
            },
            'fingers': []
        }

        for finger in frame.fingers:
            frameDict['fingers'].append({
                'type': finger.type,
                'bone': [
                {
                    'center': [finger.bone(0).center.x, finger.bone(0).center.y, finger.bone(0).center.z],
                    'direction': [finger.bone(0).direction.x, finger.bone(0).direction.y, finger.bone(0).direction.z],
                    'length': finger.bone(0).length
                },
                {
                    'center': [finger.bone(1).center.x, finger.bone(1).center.y, finger.bone(1).center.z],
                    'direction': [finger.bone(1).direction.x, finger.bone(1).direction.y, finger.bone(1).direction.z],
                    'length': finger.bone(1).length
                },
                {
                    'center': [finger.bone(2).center.x, finger.bone(2).center.y, finger.bone(2).center.z],
                    'direction': [finger.bone(2).direction.x, finger.bone(2).direction.y, finger.bone(2).direction.z],
                    'length': finger.bone(2).length
                },
                {
                    'center': [finger.bone(3).center.x, finger.bone(3).center.y, finger.bone(3).center.z],
                    'direction': [finger.bone(3).direction.x, finger.bone(3).direction.y, finger.bone(3).direction.z],
                    'length': finger.bone(3).length
                }
                ]
            })

        jsonStr = json.dumps(frameDict, indent = 4)
        file.write(jsonStr)
        file.close()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

if __name__ == "__main__":
    main()
