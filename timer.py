import pygame
import time

import calcutils
import crf
from assets.scrambler import clock, pyraminx
from assets.stackmat import stackmat

DEVICE_NUM = 30


class Timer:

    def __init__(self, game):

        self.started_timestamp = time.time_ns()
        self.running = False
        self.ms = 0
        self.timing_method = 0  # 0 = spacebar, 1 = stackmat

        self.ready = 0
        self.started_timestamp_spacebar = time.time_ns()

        self.stackmat = None
        self.error = None

        self.game = game

        self.current_scramble = ""
        self.event = self.game.config.current_event

        self.clock = clock.Clock()
        self.pyraminx = pyraminx.Pyraminx()

        self.rescramble()

        self.crf_handler = crf.CrfHandler()

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

                if event.key == pygame.K_s and not event.mod & pygame.KMOD_CTRL:
                    self.timing_method = 0 if self.timing_method == 1 else 1
                    self.reset(False)

                if event.key == pygame.K_r:
                    self.rescramble()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.ready == 1:
                        self.ready = 0
                    elif self.ready == 2:
                        self.ready = 3
                        self.on_start()

        if self.timing_method == 0:

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if round(time.time_ns() - self.started_timestamp_spacebar) / 1e6 > 550 and self.started_timestamp_spacebar != 0:
                    self.ready = 2
                    self.started_timestamp = time.time_ns()

            if self.running:
                self.ms = round((time.time_ns() - self.started_timestamp) / 1e6)

        elif self.timing_method == 1:

            if self.stackmat is not None and self.stackmat.state is not None:

                self.ms = self.stackmat.state.time
                self.error = None

                if not self.running:

                    if self.stackmat.state.state == "S":
                        self.ready = -1
                    elif self.stackmat.state.state == "L" or self.stackmat.state.state == "R" or self.stackmat.state.state == "I":

                        if self.stackmat.state.time <= 0:
                            if self.ready < 2:
                                self.ready = 0
                            else:
                                self.ready = 3
                                self.on_start()

                    elif self.stackmat.state.state == "C":

                        if self.stackmat.state.time <= 0:
                            self.ready = 1

                    elif self.stackmat.state.state == "A":

                        if self.stackmat.state.time <= 0:
                            self.ready = 2

                    elif self.stackmat.state.state == " ":
                        self.ready = 3
                        self.on_start()
                else:

                    if self.stackmat.state.frozen or self.stackmat.state.state == "S":  # otherwise without frozen statement, it won't detect if timer is stopped because the timer doesn't override S (if left sensor is being pressed, it sends L even if the timer has stopped)
                        # print("freeze detected!")
                        self.stop()

            else:
                self.ms = -1
                if self.error is None:
                    self.error = 'No data from stackmat!'

        else:
            assert False, f"Unknown timing method {self.timing_method}"

    def on_start(self):

        self.running = True
        self.game.on_timer_start()

    def stop(self):

        self.running = False
        self.ready = -1
        self.started_timestamp_spacebar = 0

        self.crf_handler.write(crf.Result([self.crf_handler.get_index(), self.ms, self.current_scramble, "none"]))

        self.rescramble()
        self.refresh_stats()

        self.game.on_timer_stop()

    def refresh_stats(self):
        for stat in self.game.time_stats.stats:
            stat.refresh(self.crf_handler.get_all())


    def get_color(self): # ???
        pass

    def rescramble(self):

        if self.event == "clock":
            self.current_scramble = clock.get_scramble()
            self.clock.reset()
            self.clock.convert_scramble(self.current_scramble)

        elif self.event == "pyraminx":
            self.current_scramble = pyraminx.get_scramble()
            self.pyraminx.reset_puzzle()
            self.pyraminx.convert_scramble(self.current_scramble)


class TimeStats:

    def __init__(self):
        self.stats = [TimeStats.Stat("ao", 5),
                      TimeStats.Stat("ao", 12)]

    class Stat:

        def __init__(self, type, amount):
            self.type = type
            self.amount = amount
            self.ms = 0

        def refresh(self, times: list[crf.Result]):
            if self.type == "ao":
                self.ms = calcutils.get_average_of(times, self.amount)