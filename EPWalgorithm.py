def extreme_points(data):
    H = 300
    extreme_points = []

    # Identify all the extreme points
    for i, point in enumerate(data):
        if 0 < i < len(data) - 1:
            prev_y = int(data[i - 1]['y-coordinate'])
            current_y = int(point['y-coordinate'])
            next_y = int(data[i + 1]['y-coordinate'])

 

            if prev_y < current_y > next_y or prev_y > current_y < next_y:
                extreme_points.append(point)
        else:
            extreme_points.append(point)

    # Filter out ripples out of extreme points
    result = []
    for i in range(1, len(extreme_points) - 1):
        prev_y = int(extreme_points[i - 1]['y-coordinate'])
        current_y = int(extreme_points[i]['y-coordinate'])
        next_y = int(extreme_points[i + 1]['y-coordinate'])

 
        if (abs(prev_y - current_y) > H and abs(next_y - current_y) > H):
            result.append(extreme_points[i])

    return [extreme_points[0]] + result + [extreme_points[-1]]
 