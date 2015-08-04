from tkinter import *
import random
import time

def point_collision(a, b):
    cx = (b[2] - b[0]) / 2
    cy = (b[3] - b[1]) / 2
    r = cx
    #left-top
    dx = cx - a[0]
    dy = cy - a[1]
    p1 = dx**2 + dy**2 < r**2
    #right-top
    dx = cx - a[2]
    dy = cy - a[1]
    p2 = dx**2 + dy**2 < r**2
    #right-bottom
    dx = cx - a[2]
    dy = cy - a[3]
    p3 = dx**2 + dy**2 <r**2
    #left-bottom
    dx = cx - a[0]
    dy = cy - a[3]
    p4 = dx**2 + dy**2 < r**2

    return p1 or p2 or p3 or p4

class Ball:
    def __init__(self, canvas, paddle, score, blocks, speed, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.speed = speed
        self.blocks = blocks
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 300)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start)

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                return True
            return False

    def hit_block(self, pos):
        collision_type = 0
        for block in self.blocks:
            block_pos = self.canvas.coords(block.id)
            c = [(pos[2] - pos[0]) / 2 + pos[0], (pos[3] - pos[1]) / 2 + pos[1]]

            if block_pos[0] <= c[0] <= block_pos[2]:
                if block_pos[1] <= pos[3] < block_pos[3] or block_pos[1] < pos[1] <= block_pos[3]:
                    collision_type |= 1
                    
            if block_pos[1] <= c[1] <= block_pos[3]:
                if block_pos[0] <= pos[2] < block_pos[2] or block_pos[0] < pos[0] <= block_pos[2]:
                    collision_type |= 2
                    
            if collision_type !=0:
                self.score.hit()
                return (block, collision_type)
        return(None, collision_type)

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y *= -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = self.y * -1
        if pos[0] <= 0:
            self.x *= -1
        if pos[2] >= self.canvas_width:
            self.x *= -1
        (target, collision_type) = self.hit_block(pos)
        if target != None:
            target.delete()
            del self.blocks[self.blocks.index(target)]
            if (collision_type & 1) != 0:
                self.y *= -1
            if (collision_type & 2) != 0:
                self.x *= -1
            print(len(self.blocks))

   
    def start(self, evt):
        self.x = -self.speed
        self.y = self.speed            

class Paddle:
    def __init__(self, canvas, speed, color):
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 550)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        #self.x = 0
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x =0
            
    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed

class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle(0, 0, 30, 30, fill=color)
        self.canvas.move(self.id,130 + self.pos_x * 30,
                         30 + self.pos_y * 30)

    def delete(self):
        self.canvas.delete(self.id)

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(550, 7, text=self.score, fill=color)

    def hit(self):
        self.score += 1000
        self.canvas.itemconfig(self.id, text=self.score)

#config
WIDTH = 600
HEIGHT = 600
FPS = 100
BALL_SPEED = 4
PADDLE_SPEED = 7
COLORS = {0:'black',1:'purple'}
Block_x = 11
Block_y = 9
Block_List = [0,0,1,0,0,0,0,0,1,0,0,
              0,0,0,1,0,0,0,1,0,0,0,
              0,0,0,1,1,1,1,1,0,0,0,
              0,0,1,1,1,1,1,1,1,0,0,
              0,1,1,0,1,1,1,0,1,1,0,
              1,0,1,1,1,1,1,1,1,0,1,
              1,0,1,1,1,1,1,1,1,0,1,
              1,0,1,0,0,0,0,0,1,0,1,
              0,0,0,1,1,0,1,1,0,0,0,]
#initialaize
tk = Tk()
tk.title("Breakout")
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=WIDTH, height=HEIGHT,
                bd=0, highlightthickness=0)
canvas.pack()
tk.update()

#background image
#bgimage = PhotoImage(file='6.png')
#canvas.create_image(50, 10, anchor=NW, image=bgimage)

blocks = []
for y in range(Block_y):
    for x in range(Block_x):
        blocks.append(Block(canvas, x, y, COLORS[Block_List[x + y * Block_x]]))

score = Score(canvas, 'green')
paddle = Paddle(canvas, PADDLE_SPEED, 'blue')
ball = Ball(canvas, paddle, score, blocks, BALL_SPEED, 'red')
game_over = canvas.create_text(300, 300, text='Game Over!', state='hidden',
                               fill='red', font=('serif',25))
while True:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    else:
        canvas.itemconfig(game_over, state='normal')
        break

    tk.update_idletasks()
    tk.update()
    time.sleep(1/FPS)
