from AtmosProperties import AtmoProperties


def main():
    altitude_range = input('Please input the altitude range (comma-separated): ').split(',')

    for i in range(int(altitude_range[0]), int(altitude_range[1])):
        print(i)
        print(AtmoProperties.calculate_atmospheric_properties(i, 0))


if __name__ == '__main__':
    main()
