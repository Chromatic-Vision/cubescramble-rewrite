import pygame
import time
from assets.stackmat import stackmat

DEVICE_NUM = 30 # TODO: be able to choose device number in GUI

class Timer:

    def __init__(self):
        self.started_timestamp = time.time_ns()
        self.running = False
        self.ms = 0
        self.timing_method = 0  # 0 = spacebar, 1 = stackmat

        self.ready = 0
        self.started_timestamp_spacebar = time.time_ns()

        self.stackmat = None
        self.error = None

        self.time_history = []

        self.reset(False)

    def reset(self, run):

        self.started_timestamp = time.time_ns()
        self.running = run
        self.error = None

        if self.stackmat is not None:
            self.stackmat.close()

        if self.timing_method == 0:
            self.stackmat = None

        elif self.timing_method == 1:
            try:
                self.stackmat = stackmat.Stackmat(DEVICE_NUM)
            except Exception as e:
                self.error = f'Error initialising stackmat: {repr(e)}'

        else:
            assert False, f"Unknown timing method {self.timing_method}"

    def update(self, events: list[pygame.event.Event]):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    if self.running:
                        self.stop()

                    else:
                        self.started_timestamp_spacebar = time.time_ns()
                        self.ready = 1
                        self.ms = 0

                if event.key == pygame.K_s:

                    self.timing_method = 0 if self.timing_method == 1 else 1
                    self.reset(False)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.ready == 1:
                        self.ready = 0
                    elif self.ready == 2:
                        self.ready = 3
                        self.running = True

        if self.timing_method == 0:

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if round(time.time_ns() - self.started_timestamp_spacebar) / 1e6 > 550 and self.started_timestamp_spacebar != 0:
                    self.ready = 2
                    self.started_timestamp = time.time_ns()

            if self.running:
                self.ms = round((time.time_ns() - self.started_timestamp) / 1e6)

        elif self.timing_method == 1:

            if self.stackmat is not None and self.stackmat.state is not None:

                # print(self.stackmat.state.state)

                self.ms = self.stackmat.state.time
                self.error = None

                if not self.running:

                    if self.stackmat.state.state == "S":
                        self.ready = -1
                    elif self.stackmat.state.state == "L" or self.stackmat.state.state == "R" or self.stackmat.state.state == "I":

                        if self.ready < 2:
                            self.ready = 0
                        else:
                            self.ready = 3
                            self.running = True

                    elif self.stackmat.state.state == "C":
                        self.ready = 1
                    elif self.stackmat.state.state == "A":
                        self.ready = 2
                    elif self.stackmat.state.state == " ":
                        self.ready = 3
                        self.running = True
                else:

                    if self.stackmat.state.frozen or self.stackmat.state.state == "S": # otherwise without frozen statement, it won't detect if timer is stopped because the timer doesn't override S (if left sensor is being pressed, it sends L even if the timer has stopped)
                        print("freeze detected!")
                        self.ready = -1
                        self.running = False

                        self.time_history.append(self.stackmat.state.time)

            else:
                self.ms = -1
                if self.error is None:
                    self.error = 'No data from stackmat!'

        else:
            assert False, f"Unknown timing method {self.timing_method}"

    def stop(self):
        self.running = False
        self.ready = 0
        self.started_timestamp_spacebar = 0
        self.time_history.append(self.ms)