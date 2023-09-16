import time
from Model import *
from Button import *
from Counters import *
from Displays import *
from Lights import *
from Buzzer import *

class StopwatchController:

    def __init__(self):

        self._button1 = Button(17, "start/lap", buttonhandler=None)
        self._button2 = Button(16, "stop/reset", buttonhandler=None)
        self._timekeeper = TimeKeeper()
        self._timeLapKeeper = TimeKeeper()
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)

        self._timerLight = DimLight(8, "Timer Light")
        self._timerLight.off()
        self._lapCount = 0
        self._model = Model(4, self, debug=True)

        self._beep = ActiveBuzzer(15)

        self._model.addButton(self._button1)
        self._model.addButton(self._button2)

        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [BTN2_PRESS], 2)
        self._model.addTransition(2, [BTN2_PRESS], 0)
        self._model.addTransition(1, [BTN1_PRESS], 1)

    def run(self):
        self._model.run()

    def resumeTimer(self):
        if self._model.getState() == 2:
            self._timekeeper.start()

    def stateEntered(self, state, event):
        if state == 0:
            print('State 0 entered')
            self._display.showText('Press button1 tostart the timer!')

        elif state == 1:
            print('State 1 entered')
            self._timekeeper.start()
            self._timerLight.on()
            self._display.showText("TOT:", row=0)
            self._display.showText("L" + f"{self._lapCount:02}" + ":", row=1)
            self._timeLapKeeper.start()

        elif state == 2:
            print('State 2 entered')
            self._timekeeper.stop()
            self._timerLight.off()

    def stateDo(self, state):
        if state == 1:
            self._display.showText("TOT:" + str(self._timekeeper), row=0)
            self._display.showText("L" + f"{self._lapCount:02}" + ":" + str(self._timeLapKeeper), row=1)

    def stateLeft(self, state, event):
        if state == 1 and event == BTN1_PRESS:
            self._timekeeper.stop()
            self._lapCount += 1
            self._display.showText("L" + f"{self._lapCount:02}" + ":" + str(self._timeLapKeeper), row=1)
            self._timeLapKeeper.reset()
            self._beep.beep()
        elif state == 2:
            self._timekeeper.reset()
            self._lapCount = 0


if __name__ == '__main__':
    StopwatchController().run()

