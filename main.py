import concurrent.futures
import requests
banner = f"""

 ██████╗██╗  ██╗███████╗███████╗███████╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
██║     ███████║█████╗  ███████╗███████╗
██║     ██╔══██║██╔══╝  ╚════██║╚════██║
╚██████╗██║  ██║███████╗███████║███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
                                        
                 mq#0222
"""
print(banner)
def check_username(username):
    response = requests.get(f'https://www.chess.com/member/{username}')
    if response.status_code == 404:
        return username

def check_chess_usernames():
    with open('usernames.txt', 'r') as file:
        usernames = [line.strip() for line in file if line.strip()]

    with open('available.txt', 'w') as output_file:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_username = {executor.submit(check_username, username): username for username in usernames}
            for future in concurrent.futures.as_completed(future_to_username):
                username = future_to_username[future]
                available_username = future.result()
                if available_username:
                    output_file.write(f'{available_username}\n')
                    print(f'Username {available_username} is available!')
                else:
                    print(f'Username {username} is taken.')

if __name__ == '__main__':
    check_chess_usernames()
