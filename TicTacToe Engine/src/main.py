'''
Created on May 16, 2016

@author: Mian Mubasher

The code base has been taken from following URL
https://www.leaseweb.com/labs/2013/12/python-tictactoe-tk-minimax-ai/
'''
    
from Tkinter import Tk, Button
from copy import deepcopy
import os
from subprocess import Popen, PIPE
import sys
import time
from tkFont import Font
import tkMessageBox

#===============================================================================
# provide names of agent files
#===============================================================================

AGENT_ONE = 'SampleAgent.class'
AGENT_TWO = 'SampleAgent.class'

#------------------------------------------------------------------------------ 

class AgentInteractionManager:
    
    @staticmethod
    def load_agent():
        script_dir = os.path.dirname(os.path.realpath(__file__))
        script_path = os.path.join(script_dir,AGENT_ONE)
        if AGENT_ONE.split('.')[1] == 'py':
            a1 = Popen([sys.executable, '-u', script_path],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        elif AGENT_ONE.split('.')[1] == 'exe':
            a1 = Popen([script_path],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        elif AGENT_ONE.split('.')[1] == 'class':
            a1 = Popen(['java','-cp',script_dir,AGENT_ONE.split('.')[0]],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        else:
            tkMessageBox.showerror("Invalid agent 1", "The agent must be a exe file or python file")
            exit()
        
        script_path = os.path.join(script_dir,AGENT_TWO)
        if AGENT_TWO.split('.')[1] == 'py':
            a2 = Popen([sys.executable, '-u', script_path],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        elif AGENT_TWO.split('.')[1] == 'exe':
            a2 = Popen([script_path],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        elif AGENT_TWO.split('.')[1] == 'class':
            a2 = Popen(['java','-cp',script_dir,AGENT_TWO.split('.')[0]],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        else:
            tkMessageBox.showerror("Invalid agent 2", "The agent must be a exe file or python file")
            exit()
            
        return a1,a2
    
    @classmethod
    def init(cls, gui):
        cls.gui = gui
        cls.PLAYER_ONE = 0
        cls.PLAYER_TWO = 1
        cls.init_pipes()
    
    @classmethod
    def init_pipes(cls):
        cls.a1, cls.a2 = cls.load_agent()
        cls.a1.stdin.write(str(1)+os.linesep)
        cls.a2.stdin.write(str(2)+os.linesep)
        cls.agents = [cls.a1, cls.a2]
    
    @classmethod
    def reset(cls):
        cls.a1.kill()
        cls.a2.kill()
        cls.init_pipes()
    
    @staticmethod
    def row_major_board(board):
        retval = []
        d = {}
        d[board.empty] = 0
        d[board.player] = 1
        d[board.opponent] = -1
        
        for i in range(board.size):
            for j in range(board.size):
                retval.append(d[board.fields[(j,i)]])
        return retval
    
    @classmethod
    def player_move(cls, board, player):
        time.sleep(1)
        for i in cls.row_major_board(board):
            cls.agents[player].stdin.write(str(i)+os.linesep)
        try:
            n = cls.agents[player].stdout.readline()
            n = int(n)
            x = n/3
            y = n%3
            if n<0 or n>8:
                tkMessageBox.showerror("Invalid move", "board configuration: "+str(board)+", player: "+str(player+1)+" move selected: "+str(n))
                cls.gui.reset()
            if not board.fields[(y,x)] == board.empty:
                tkMessageBox.showerror("Invalid move", "board configuration: "+str(board)+", player: "+str(player+1)+" move selected: "+str(n))
                cls.gui.reset()
            return y, x
        except Exception as e:
            print e

class Board:
 
    def __init__(self,other=None):
        self.player = 'X'
        self.opponent = 'O'
        self.empty = '.'
        self.size = 3
        self.fields = {}
        for y in range(self.size):
            for x in range(self.size):
                self.fields[x, y] = self.empty
        # copy constructor
        if other:
            self.__dict__ = deepcopy(other.__dict__)
 
    def move(self, x, y):
        board = Board(self)
        board.fields[x, y] = board.player
        (board.player, board.opponent) = (board.opponent, board.player)
        return board

    def __sp(self, player):
        if self.won() or self.tied():
            return (None, None)
        else:
            best = (None, None)
            x, y = AgentInteractionManager.player_move(self, AgentInteractionManager.PLAYER_TWO)
            best = (None, (x, y))
            return best
 
    def __minimax(self, player):
        if self.won():
            if player:
                return (-1, None)
            else:
                return (+1, None)
        elif self.tied():
            return (0, None)
        elif player:
            best = (-2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.move(x, y).__minimax(not player)[0]
                    if value > best[0]:
                        best = (value, (x, y))
            return best
        else:
            best = (+2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.move(x, y).__minimax(not player)[0]
                    if value < best[0]:
                        best = (value, (x, y))
            return best
 
    def best(self):
#         return self.__minimax(True)[1]
        return self.__sp(True)[1]
 
    def tied(self):
        for (x, y) in self.fields:
            if self.fields[x, y] == self.empty:
                return False
        return True
 
    def won(self):
        # horizontal
        for y in range(self.size):
            winning = []
            for x in range(self.size):
                if self.fields[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return winning
        # vertical
        for x in range(self.size):
            winning = []
            for y in range(self.size):
                if self.fields[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return winning
        # diagonal
        winning = []
        for y in range(self.size):
            x = y
            if self.fields[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return winning
        # other diagonal
        winning = []
        for y in range(self.size):
            x = self.size - 1 - y
            if self.fields[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return winning
        # default
        return None
 
    def __str__(self):
        string = ''
        for y in range(self.size):
            for x in range(self.size):
                string += self.fields[x, y]
            string += "\n"
        return string

class GUI:
 
    def __init__(self):
        self.app = Tk()
        self.app.title('TicTacToe')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}
        for x, y in self.board.fields:
            handler = None
#             handler = lambda x = x, y = y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=2, height=1)
            button.grid(row=y, column=x)
            self.buttons[x, y] = button
        handler = lambda: self.reset()
        button = Button(self.app, text='reset', command=handler)
        button.grid(row=self.board.size + 1, column=0, columnspan=self.board.size, sticky="WE")
        handler = lambda: self.start()
        button = Button(self.app, text='start', command=handler)
        button.grid(row=self.board.size + 2, column=0, columnspan=self.board.size, sticky="WE")
        self.start_button = button
        self.update()

    def reset(self):
        AgentInteractionManager.reset()
        self.board = Board()
        self.start_button['state'] = 'normal'
        self.start_button.update()
        self.update()
        
    def start(self):
        x,y = AgentInteractionManager.player_move(self.board, AgentInteractionManager.PLAYER_ONE)
        self.move(x,y)
        if self.board.won() or self.board.tied():
            self.start_button['state'] = 'disabled'
            self.start_button.update()
        else:    
            self.start()
            
    def move(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        self.update()
        move = self.board.best()
        if move:
            self.board = self.board.move(*move)
            self.update()
        self.app.config(cursor="")
 
    def update(self):
        for (x, y) in self.board.fields:
            text = self.board.fields[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'black'
            if text == self.board.empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'
        winning = self.board.won()
        if winning:
            for x, y in winning:
                self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
            for (x, y) in self.board.fields:
                self.buttons[x, y].update()
                
    def mainloop(self):
        self.app.mainloop()
    
def main():
    gui = GUI()
    AgentInteractionManager.init(gui=gui)
    gui.mainloop()

if __name__ == '__main__':
    main()
