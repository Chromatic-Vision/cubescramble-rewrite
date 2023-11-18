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

    for result in times:
        if result.penalty == "DNF":
            dnf_count += 1

    if dnf_count > 2:
        return -2

    times.remove(min(times, key=lambda result: result.get_real_time()))
    times.remove(max(times, key=lambda result: result.get_real_time()))

    total_sum = sum(result.get_real_time() for result in times)
    return round(total_sum / times.__len__())