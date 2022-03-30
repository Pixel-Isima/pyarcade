import pygame
import enum

class Axis(enum.Enum):
    X_POSITIVE = 0
    X_NEGATIVE = 2

    Y_POSITIVE = 1
    Y_NEGATIVE = 3

class Controllers:
    _controllers: list[pygame.joystick.Joystick]
    _controllers_with_joystick: list[int]

    _axis_trigger: float = .9

    def __init__(self):
        pygame.joystick.init()

        self._controllers = [pygame.joystick.Joystick(x) for x in range(min(pygame.joystick.get_count(), 2))]
        self._controllers_with_joystick = [x for x in range(min(pygame.joystick.get_count(), 2))]

        if len(self._controllers) > 0:
            print("There is {} devices:".format(len(self._controllers)))
        else:
            print("There is no device")

        ctrl_i = 0
        for i in range(len(self._controllers)):
            print("\t- {}", self._controllers[i].get_name())

            if self._controllers[i].get_numaxes() < 2:
                self._controllers_with_joystick.remove(ctrl_i)
            else:
                ctrl_i += 1

    def __del__(self):
        for i in self._controllers:
            i.quit()

        pygame.joystick.quit()

    def _get_joystick_position_by_controller(self, controller, axis: Axis) -> bool:
        match axis:
            case Axis.X_POSITIVE:
                return self._controllers[controller].get_axis(0) > self._axis_trigger
            case Axis.X_NEGATIVE:
                return self._controllers[controller].get_axis(0) < -self._axis_trigger
            case Axis.Y_POSITIVE:
                return self._controllers[controller].get_axis(1) > self._axis_trigger
            case Axis.Y_NEGATIVE:
                return self._controllers[controller].get_axis(1) < -self._axis_trigger

    def get_joystick_position(self, axis: Axis) -> bool:
        for controller in self._controllers_with_joystick:
            if self._get_joystick_position_by_controller(controller, axis):
                return True
        return False

    def get_validation_action(self) -> bool:
        for controller in self._controllers:
            if controller.get_button(5):
                return True
        return False

    def get_insert_coin_action(self) -> bool:
        return self._controllers[0].get_button(9)

    def print_all(self):
        for controller in self._controllers:
            for button in range(controller.get_numbuttons()):
                if controller.get_button(button):
                    print("Controller: {}, button {}".format(controller.get_id(), button))
