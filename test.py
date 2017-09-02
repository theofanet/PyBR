from opensimplex import OpenSimplex
gen = OpenSimplex()


def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def generate_map(width, height):
    value = [[0 for x in range(width)] for y in range(height)]

    for y in range(height):
        for x in range(width):
            nx = x/width - 0.5
            ny = y/height - 0.5
            value[y][x] = int(noise(nx, ny) * 100)

    return value


if __name__ == '__main__':
    print(generate_map(10, 10))
