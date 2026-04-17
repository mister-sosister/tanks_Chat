class game_lobby():
    def __init__(self, fplayer, splayer):
        self.fplayer = fplayer
        self.splayer = splayer
        
        
    def check_status(self):
        if self.fplayer != None and self.splayer != None:
            print("лобби полное", f"первый игрок - {self.fplayer}",f'второй игрок - {self.splayer}')
        else: 
            print("лобби неполное", f"первый игрок - {self.fplayer}",f'второй игрок - {self.splayer}')
        #обратная связь, появление и завершение лоббм
        
        #ssh -i ssh-key-1775571418998 artemiy@158.160.7.136