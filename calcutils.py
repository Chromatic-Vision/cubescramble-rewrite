import crf


def get_average_of(times_: list[crf.Result], length) -> int:

    # if times_.__len__() < length:
    #     return -1
    # elif times_.__len__() < 3:
    #     raise NotImplementedError(f"Tried to calculate average of {times_.__len__()} which is impossible")

    if times_.__len__() < length:
        return -1
    elif times_.__len__() < 3:
        return -1

    times = times_[:]
    times = times[-length:]

    dnf_count = 0

    for time in times:
        if time.penalty == "DNF":
            dnf_count += 1

    if dnf_count >= 2:
        return -2

    if dnf_count == 1: # always True but if something happens that makes possible smh
        times = [time for time in times if time.penalty != "DNF"]
    else:
        times.remove(max(times, key=lambda result: result.get_time_including_penalty()))

    times.remove(min(times, key=lambda result: result.get_time_including_penalty()))

    total_sum = sum(result.get_time_including_penalty() for result in times)
    return round(total_sum / times.__len__())