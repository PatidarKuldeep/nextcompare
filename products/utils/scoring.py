def mobile_processor_score(processor):

    if not processor or not processor.antutu_score:
        return 0

    max_antutu = 2200000

    score = (processor.antutu_score / max_antutu) * 40

    return score

def ram_score(ram):

    if ram >= 16:
        return 15
    elif ram >= 12:
        return 12
    elif ram >= 8:
        return 10
    else:
        return 5

def battery_score(battery):

    if battery >= 6000:
        return 20
    elif battery >= 5000:
        return 17
    elif battery >= 4500:
        return 14
    else:
        return 10

def camera_score(camera):

    if camera >= 200:
        return 15
    elif camera >= 108:
        return 13
    elif camera >= 64:
        return 10
    else:
        return 7

def calculate_mobile_score(spec):

    p = mobile_processor_score(spec.processor)

    r = ram_score(spec.ram)

    b = battery_score(spec.battery)

    c = camera_score(spec.camera)

    total = p + r + b + c

    return round(total,2)

def laptop_processor_score(processor):

    if not processor or not processor.geekbench_multi:
        return 0

    max_score = 20000

    score = (processor.geekbench_multi / max_score) * 40

    return score

def laptop_ram_score(ram):

    if ram >= 32:
        return 20
    elif ram >= 16:
        return 15
    elif ram >= 8:
        return 10
    else:
        return 5

def storage_score(storage):

    if storage >= 1024:
        return 15
    elif storage >= 512:
        return 12
    else:
        return 8

def gpu_score(has_gpu):

    if has_gpu:
        return 15
    else:
        return 5

def calculate_laptop_score(spec):

    p = laptop_processor_score(spec.processor)

    r = laptop_ram_score(spec.ram)

    s = storage_score(spec.storage)

    g = gpu_score(spec.gpu)

    total = p + r + s + g

    return round(total,2)

def calculate_mobile_scores(specs):

    processor_score = specs.processor.benchmark_score if specs.processor else 0

    ram_score = min((specs.ram / 16) * 100, 100)
    storage_score = min((specs.storage / 512) * 100, 100)

    battery_score = min((specs.battery / 6000) * 100, 100)

    camera_score = 0

    performance_score = (processor_score * 0.7) + (ram_score * 0.3)

    overall = (
        performance_score * 0.35 +
        camera_score * 0.25 +
        battery_score * 0.2 +
        storage_score * 0.1 +
        ram_score * 0.1
    )

    return {
        "performance": round(performance_score,2),
        "camera": 0,
        "battery": round(battery_score,2),
        "storage": round(storage_score,2),
        "overall": round(overall,2)
    }