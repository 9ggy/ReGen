from requests import get
from random import choice
import pystyle
from concurrent.futures import ThreadPoolExecutor


config = {
  "thread_count": 50, # threads to run on
  "uname_length": 5, # length of usernames that the program generates/checks
  "charset": "abcdefghijklmnopqrstuvwxyz1234567890_" # that character pool the generated usernames pull from
}


class ReGen(object):
  def __init__(self, charset: str):
    self.charset = charset

    return

  
  def generate_username(self, length: int) -> str:
    return "".join([choice(self.charset) for _ in range(length)])

  
  def exist_username(self, username):
    status = get('https://www.roblox.com/users/profile?username=' + username).status_code

    if status == 404:
      return False

    return True

  
  def _start(self) -> None:
    while True:
      
      username = self.generate_username(config["uname_length"])

      if not self.exist_username(username):
        validity = get(
          f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2022-09-04T19%3A10%3A05.906Z&request.context=Signup"
        ).json()["code"]

        if validity == 0:
        
          print(
            pystyle.Colorate.Horizontal(pystyle.Colors.blue_to_green,
            f"[VALID USERNAME]  {username}",
            1
            )
          )
  
          with open("usernames.txt", "a") as outfile:
            outfile.write(username + "\n")

          continue
        
      print(
          pystyle.Colorate.Horizontal(pystyle.Colors.red_to_purple,
          f"[INVALID USERNAME]  {username}",
          1
        )
      )

    return


  def start(self) -> None:
    with ThreadPoolExecutor() as exe:
      for _ in range(config["thread_count"]):
        exe.submit(self._start) 
    
    return



# Driver code
if __name__ == "__main__":
  print(pystyle.Colorate.Horizontal(pystyle.Colors.blue_to_purple, """

██████╗  █████╗ ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝ ██╔════╝████╗  ██║
██║  ██║███████║███████╗███████║██║  ███╗█████╗  ██╔██╗ ██║
██║  ██║██╔══██║╚════██║██╔══██║██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝██║  ██║███████║██║  ██║╚██████╔╝███████╗██║ ╚████║
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                ~ Mass Username Checker ~
              ~ Made with <3 by 3sp & 9ggy ~
            
""", 2))
  input("Enter To Start > ")
  rg = ReGen(config["charset"])
  rg.start()
