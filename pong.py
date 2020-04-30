from tkinter import *
import math
import threading

def draw_paddle( x, y, p_width, p_height):
  print("create paddle!")
  item_paddle = canvas.create_rectangle(x - p_width / 2,
                                       y - p_height / 2,
                                       x + p_width/ 2,
                                       y +  p_height/ 2,
                                       fill = "blue")

def draw_ball(x, y, b_radius):
    print("create ball")
    item_ball = canvas.create_oval(x - b_radius, y - b_radius,
                                  x + b_radius, y + b_radius,
                                  fill="white")

def motion(event):
    xM, yM = event.x, event.y
    #print('{}, {}'.format(x, y))
    #canvas.getBoundingClientRect()
    #let rect = canvas.getBoundingClientRect();
    #user.y = evt.clientY - rect.top - user.height/2;
    t = canvas.bbox(ALL)
    #print('{}, {}, {}, {}'.format(t[0], t[1], t[2], t[3]))
    m_player["y"] = int(yM) - int(t[0]) - int(m_player["height"]) / 2
    print('{}' .format(m_player["y"]))

def reset():
    ball["x"] = m_cwidth / 2
    ball["y"] = m_cheight / 2
    ball["velocityX"] = -ball["velocityX"] 
    ball["speed"] = 7
 
def draw_net():
    for nx in range(0, int(m_cheight )):
        draw_paddle(m_net["x"], m_net["y"] + nx, m_net["width"] , m_net["height"]  )

def draw_text(text, x, y):
    font = ('Helvetica', 40)
    return canvas.create_text(x, y, text=text, font=font)

def collision(c_ball, c_player):
    c_player["top"]    = c_player["y"]
    c_player["bottom"] = c_player["y"] + c_player["height"]
    c_player["left"]   = c_player["x"]
    c_player["right"]  = c_player["x"] + c_player["width"]
    
    c_ball["top"]      = c_ball["y"] - c_ball["radius"]
    c_ball["bottom"]   = c_ball["y"] + c_ball["radius"]
    c_ball["left"]     = c_ball["x"] - c_ball["radius"]
    c_ball["right"]    = c_ball["x"] + c_ball["radius"]
    return c_player["left"] < c_ball["right"] and c_player["top"] < c_ball["bottom"] and  c_player["right"] >  c_ball["left"] and c_player["bottom"] >    c_ball["top"] 

def update():
    if ball["x"] - ball["radius"] < 0:
        m_ai["score"] += 1
        reset()
    elif ((ball["x"] + ball["radius"]) > m_cwidth): 
        m_player["score"] += 1 
        reset()
    else:
        ball["x"]  += ball["velocityX"]
        ball["y"]  += ball["velocityY"]
    
    
    m_ai["y"] += ((ball["y"] - (m_ai["y"] + m_ai["height"] / 2))) * 0.1
    
    if(ball["y"] - ball["radius"] < 0 or ball["y"]  + ball["radius"] > m_cheight):
        ball["velocityY"] = -ball["velocityY"]
    # we check if the paddle hit the user or the com paddle
  
    if ((ball["x"] + ball["radius"]) < m_cwidth / 2):
        player_context = m_player
    else: 
        player_context = m_ai
    
    if (collision(ball, player_context)):
        # // we check where the ball hits the paddle
        collide_point = ( ball["y"] - (player_context["y"] + player_context["height"] / 2 ) )
        collide_point = collide_point / (player_context["height"] / 2 )
        angle_rad = ( math.pi / 4) * collide_point
        #change the X and Y velocity direction
        if ((ball["x"] + ball["radius"]) < m_cwidth / 2):
            direction_xy = 1
        else:
            direction_xy = -1
     #speed up the ball everytime a paddle hits it.
        ball["speed"] += 0.1

def render():
    canvas.create_rectangle(0, 0, m_cwidth, m_cheight, fill="red")
    draw_text(m_player["score"], m_cwidth /4 , m_cheight / 5)
    draw_text(m_ai["score"], 3 * m_cwidth /4 , m_cheight / 5)
    draw_net()
    draw_paddle(m_player["x"], m_player["y"], m_player["width"], m_player["height"])
    draw_paddle(m_ai["x"], m_ai["y"], m_ai["width"], m_ai["height"])
    draw_ball(ball["x"], ball["y"], ball["radius"])

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

#window.bind('<Motion>', motion)#

def game():
    #update()
    render()

####

if __name__ == '__main__': 
    #root = tk.Tk()
    #root.title('Hello, Pong!') 
    #game = Game(root) 
    #game.mainloop()
    window = Tk()
    window.title('Pong')
    canvas = Canvas(window, bg = '#aaaaff', height = 400, width = 600)
    m_cwidth = int(canvas.cget("width")) 
    m_cheight = int(canvas.cget("height"))
    
    ball = {
        "x" : m_cwidth / 2,
        "y" : m_cheight / 2,
        "radius" : 10,
        "velocityX" : 5,
        "velocityY" : 5,
        "speed" : 7,
        "color" : "WHITE"
    }

    m_player = {
        "x" : 0,                #left side of canvas
        "y" : (m_cheight - 100)/2, #-100 the height of paddle
        "width" : 10,
        "height" : 100,
        "score" : 0,
        "color" : "WHITE"
    }

    m_ai = {
        "x" : m_cwidth- 10, # - width of paddle
        "y" : (m_cheight - 100)/ 2, # -100 the height of paddle
        "width" : 10,
        "height" : 100,
        "score" : 0,
        "color" : "WHITE"
    }

    m_net = {
        "x" : (m_cwidth - 2)/2,
        "y" : 0,
        "height" : 10,
        "width" : 2,
        "color" : "WHITE"
    }

    canvas.update()
    game()
    canvas.pack()
    window.bind('<Motion>', motion)
    window.mainloop()

