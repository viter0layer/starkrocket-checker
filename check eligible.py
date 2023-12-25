import requests
from loguru import logger


def check_eligibility_and_calculate_points(addresses):
    total_points = 0
    eligible_addresses = []

    with requests.Session() as session:
        for address in addresses:
            try:
                response = session.get(f'https://starkrocket.xyz/api/check_wallet?address={address}').json()
                if response.get("result", {}).get("eligible", False):
                    points = response["result"]["points"]
                    total_points += points
                    eligible_addresses.append(f'{address};{points}\n')
                    logger.success(f'Address: {address[:7]}...{address[-4:]} | Points: {points}')
                else:
                    logger.error(f'Address: {address[:7]}...{address[-4:]} | Not eligible')
            except requests.RequestException as e:
                logger.error(f"Error fetching data for address {address}: {e}")

    return total_points, eligible_addresses


def main():
    with open('addresses.txt') as file:
        addresses = [line.strip() for line in file.readlines()]

    total_points, eligible_addresses = check_eligibility_and_calculate_points(addresses)

    with open('eligible.txt', 'a') as file_w:
        file_w.writelines(eligible_addresses)

    logger.success(f'Total points count: {total_points}')


if __name__ == "__main__":
    main()
