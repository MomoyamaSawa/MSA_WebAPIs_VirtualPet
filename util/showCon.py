from PyQt6.QtWidgets import QWidget

class StateBase:
    _q = None

    def __init__(self,q:QWidget):
        self._q = q

    def forward(self,main):
        pass

    def backward(self,main):
        pass

class DialogState(StateBase):

    def __init__(self,q:QWidget):
        super().__init__(q)

    def forward(self,main):
        self._q.show()

    def backward(self,main):
        self._q.hide()

class FromBoxState(StateBase):

    def __init__(self,q:QWidget):
        super().__init__(q)

    def forward(self,main):
        main.viewLayAddShowW(self._q)

    def backward(self,main):
        self._q.hide()
        self._q.deleteLater()



class ShowWinStateMachine:
    _state = None
    _main = None

    def __init__(self,main):
        self._main = main

    def setState(self,state:StateBase):
        if self._state != None:
            self._state.backward(self._main)
        self._state = state
        if self._state != None:
            self._state.forward(self._main)
