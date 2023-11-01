import pygame
import random
import calcutils
import game
from config import Config


class GraphStat:

    def __init__(self, name: str, color, data: list):
        self.name = name
        self.color = color
        self.data = data  # data should be always ms in int


class HistoryRenderer:
    def __init__(self, config: Config, game):
        game: game.Game
        self.config = config
        self.game = game
        self.color_mappings = [
            ("ao5", (122, 35, 177)),
            ("ao12", (34, 155, 64))
        ]

        self.s = pygame.Surface(self.game.screen.get_size())

    def re_render(self):
        self.s.fill((0, 0, 0))
        border = 200

        stats = [GraphStat("single", (112, 255, 255),
                           self.config.times[
                           -self.config.history_draw_length if len(
                               self.config.times) > self.config.history_draw_length else None:
                           ])]

        for stat in self.game.time_stats.stats:

            gs = GraphStat(f"{stat.type}{stat.amount}", (random.randint(0, 255),
                                                         random.randint(0, 255),
                                                         random.randint(0, 255)
                                                         ), [])

            for key, color in self.color_mappings:
                if key == gs.name:
                    gs.color = color
                    break

            times = self.config.times

            # cut_off_lists = [times[i:] for i in range(len(times))]
            #
            # for i in range(len(cut_off_lists)):
            #     if len(cut_off_lists[i]) > stat.amount:
            #         cut_off_lists[i] = cut_off_lists[i][:stat.amount]

            cut_off_lists = []
            for i in range(len(times) - stat.amount):
                cut_off_lists.append(times[i:i+stat.amount])

            # TODO: fix values that are not valid

            for i in range(len(cut_off_lists)):
                res = calcutils.get_average_of(cut_off_lists[i], stat.amount)

                gs.data.append(res)

            for _ in range(stat.amount):
                gs.data.append(None)

            stats.append(gs)



        self.draw_graph(self.s,
                        stats,
                        (border, border, self.s.get_width() - border * 2, self.s.get_height() - border * 2))

    def update(self, events: list[pygame.event.Event]):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.s, (0, 0))

    def draw_graph(self, screen: pygame.Surface, stats: list[GraphStat], rect: tuple[int, int, int, int]):
        ox = rect[0]
        oy = rect[1]
        width = rect[2]
        height = rect[3]

        longest = max(max(time for time in graph_stat.data if time is not None) for graph_stat in stats)
        shortest = min(min(time for time in graph_stat.data if time is not None) for graph_stat in stats)

        pygame.draw.line(screen, (200, 200, 200), (ox, oy), (ox, oy + height), 1)
        pygame.draw.line(screen, (200, 200, 200), (ox, oy), (ox + width, oy), 1)

        s = self.game.font1.render(game.time_str(longest, True), True, (200, 200, 200))
        w = s.get_width()
        screen.blit(s, (ox - w, oy))

        y = round((longest - shortest) / longest * height)
        pygame.draw.line(screen, (200, 200, 200), (ox, oy + y), (ox + width, oy + y), 1)

        s = self.game.font1.render(game.time_str(shortest, True), True, (200, 200, 200))
        w = s.get_width()
        screen.blit(s, (ox - w, oy + y))

        ty = oy + height + 15
        gw = self.game.font1.get_height()

        for stat in stats:

            best = None
            worst = None

            old_x = None
            old_y = None
            for i, time in enumerate(stat.data):
                if time is None:
                    continue

                if best is None or time < best:
                    best = time

                if worst is None or time > worst:
                    worst = time

                x = round(i / len(stat.data) * width)
                y = round((longest - time) / longest * height)
                if old_y is not None:
                    pygame.draw.aaline(screen, stat.color,
                                       (ox + old_x, oy + old_y),
                                       (ox + x, oy + y))
                # pygame.draw.circle(screen, (255, 255, 255), (ox + x, oy + y), 4)
                game.draw_antialias_circle(screen, stat.color, ox + x, oy + y, 4)
                old_x = x
                old_y = y

            pygame.draw.rect(screen, stat.color,(ox, ty, gw, gw))
            s = self.game.font1.render(f"{stat.name} | best: {game.time_str(int(best), long=True)}, worst: {game.time_str(int(worst), long=True)}", True, (200, 200, 200))
            screen.blit(s, (ox + gw + 5, ty))

            ty += gw


