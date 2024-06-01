# Motors.md

In all cases, if **duration** (seconds) is zero or not specified the motion is as fast as possible.

Also, all commands return True if the command succeeded or False otherwise.

## motors.move(dist,duration)

The motors turn forward for **dist** mm, or reverse if dist is negative. 

## motors.rotate(angle,duration)

The robot will turn right if angle is positive or left if negative. The motion is centred on the point midway between the wheels.

## motors.arc(radius,angle,duration)

The robot motion will describe a righthand arc if radius (mm) is positive and a lefthand arc if negative.

## motors.moveMotors(left,right,duration)

The will move the wheels independently left/right are distances in mm.

## motors.areMoving()

Returns True if the motors are moving, False otherwise

## motors.stop()

Stops any motion.

## motors.setWheelConfig(left,right,spacing)

Left is the diameter of the left wheel in mm, Right is the right wheel. Spacing is the gap between the wheels (mm).

If using the standard robot wheels this is set in Config.py.

## motors.getWheelConfig()

This returns True if the command succeeded otherwise False. It outputs information to the stdout on the pi. Nothing else is returned to your program.

# Example Program
This program just drives the Pixelbot forward 100mm at a time. If it gets withing 50mm of an obstacle the motors are stopped and the Pixelbot turns 90 degrees then resumes moving.

```
while True:
  motors.move(100) # 100mm
  while motors.areMoving():
    if distance()<50:
      motors.stop()
      motors.rotate(90)

```







