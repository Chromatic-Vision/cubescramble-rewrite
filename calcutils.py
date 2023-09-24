

def get_average_of(times_: list[int], length) -> int:

    if times_.__len__() < length:
        return -1
    elif times_.__len__() < 3:
        raise NotImplementedError(f"Tried to calculate average of {times_.__len__()} which is impossible")

    times = times_[:]
    times = times[-length:]

    times.pop(times.index(min(times)))
    times.pop(times.index(max(times)))

    total_sum = sum(times)
    return round(total_sum / times.__len__())