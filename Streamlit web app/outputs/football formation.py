import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from matplotlib.widgets import Button

# Formations dictionary
formations = {
    '4-3-3': [(10, 15), (10, 35), (10, 65), (10, 85),  # Defenders
              (35, 20), (35, 50), (35, 80),             # Midfielders
              (45, 20), (48, 50), (45, 80)],            # Attackers
    '4-4-2': [(10, 15), (10, 35), (10, 65), (10, 85),
              (35, 15), (35, 35), (35, 65), (35, 85),
              (45, 30), (45, 70)],
    '3-4-3': [(10, 25), (10, 50), (10, 75),
              (35, 15), (35, 35), (35, 65), (35, 85),
              (45, 20), (48, 50), (45, 80)]
}

class DraggablePlayer:
    def __init__(self, circle, text):
        self.circle = circle
        self.text = text
        self.press = None
        self.connect()

    def connect(self):
        self.cid_press = self.circle.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.circle.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.circle.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.circle.axes:
            return
        contains, _ = self.circle.contains(event)
        if not contains:
            return
        self.press = (self.circle.center), (event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.circle.axes or event.xdata is None or event.ydata is None:
            return
        (x0, y0), (xpress, ypress) = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        new_center = (x0 + dx, y0 + dy)
        self.circle.center = new_center
        self.text.set_position(new_center)
        self.circle.figure.canvas.draw_idle()

    def on_release(self, event):
        self.press = None
        self.circle.figure.canvas.draw_idle()

def createPitch(ax):
    ax.plot([0,0],[0,90], color="black")
    ax.plot([0,130],[90,90], color="black")
    ax.plot([130,130],[90,0], color="black")
    ax.plot([130,0],[0,0], color="black")
    ax.plot([65,65],[0,90], color="black")
    
    ax.plot([16.5,16.5],[65,25],color="black")
    ax.plot([0,16.5],[65,65],color="black")
    ax.plot([16.5,0],[25,25],color="black")
    
    ax.plot([130,113.5],[65,65],color="black")
    ax.plot([113.5,113.5],[65,25],color="black")
    ax.plot([113.5,130],[25,25],color="black")
    
    ax.plot([0,5.5],[54,54],color="black")
    ax.plot([5.5,5.5],[54,36],color="black")
    ax.plot([5.5,0.5],[36,36],color="black")
    
    ax.plot([130,124.5],[54,54],color="black")
    ax.plot([124.5,124.5],[54,36],color="black")
    ax.plot([124.5,130],[36,36],color="black")
    
    centreCircle = plt.Circle((65,45),9.15,color="black",fill=False)
    centreSpot = plt.Circle((65,45),0.8,color="black")
    leftPenSpot = plt.Circle((11,45),0.8,color="black")
    rightPenSpot = plt.Circle((119,45),0.8,color="black")
    
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)
    
    leftArc = Arc((11,45),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((119,45),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)
    
    ax.set_xlim(-5, 135)
    ax.set_ylim(-5, 95)
    ax.axis('off')

def create_team(ax, formation, side='left', color='blue', start_number=1):
    players = []

    # Goalkeeper
    if side == 'left':
        gk_pos = (8, 45)
    else:
        gk_pos = (122, 45)

    gk_circle = Circle(gk_pos, 2.8, color='yellow', ec='black', zorder=4)
    ax.add_patch(gk_circle)
    gk_text = ax.text(gk_pos[0], gk_pos[1], 'GK', color='black', ha='center', va='center', weight='bold', fontsize=8, zorder=5)
    players.append(DraggablePlayer(gk_circle, gk_text))

    # Field players
    for idx, (x, y) in enumerate(formations[formation]):
        x = x * 1.3
        y = y * 0.9
        if side == 'right':
            x = 130 - x

        circle = Circle((x, y), 2.5, color=color, zorder=3)
        ax.add_patch(circle)
        text = ax.text(x, y, str(start_number), ha='center', va='center', color='white', fontsize=8, weight='bold', zorder=4)
        players.append(DraggablePlayer(circle, text))
        start_number += 1
    return players

# Global variables
team1_formation = None
team2_formation = None
players = []

def start_board(event):
    global players
    players = []

    if team1_formation and team2_formation:
        fig.clf()
        ax = fig.add_subplot(1,1,1)
        createPitch(ax)
        
        players += create_team(ax, team1_formation, side='left', color='blue', start_number=1)
        players += create_team(ax, team2_formation, side='right', color='red', start_number=1)

        # Ball
        ball_circle = Circle((65, 45), 2, color='white', ec='black', zorder=5)
        ax.add_patch(ball_circle)
        ball_text = ax.text(65, 45, "Ball", color="black", ha="center", va="center", fontsize=8, weight="bold", zorder=6)
        players.append(DraggablePlayer(ball_circle, ball_text))

        plt.title(f"Tactics Board  |  {team1_formation} vs {team2_formation}", fontsize=18, weight="bold")
        plt.draw()

def set_team1_formation(event, form):
    global team1_formation
    team1_formation = form
    print(f"Team 1: {form}")

def set_team2_formation(event, form):
    global team2_formation
    team2_formation = form
    print(f"Team 2: {form}")

# Interface
fig = plt.figure(figsize=(14, 10))

ax_btn1_433 = plt.axes([0.05, 0.85, 0.1, 0.05])
ax_btn1_442 = plt.axes([0.05, 0.78, 0.1, 0.05])
ax_btn1_343 = plt.axes([0.05, 0.71, 0.1, 0.05])

btn1_433 = Button(ax_btn1_433, 'T1 4-3-3')
btn1_442 = Button(ax_btn1_442, 'T1 4-4-2')
btn1_343 = Button(ax_btn1_343, 'T1 3-4-3')

btn1_433.on_clicked(lambda event: set_team1_formation(event, '4-3-3'))
btn1_442.on_clicked(lambda event: set_team1_formation(event, '4-4-2'))
btn1_343.on_clicked(lambda event: set_team1_formation(event, '3-4-3'))

ax_btn2_433 = plt.axes([0.85, 0.85, 0.1, 0.05])
ax_btn2_442 = plt.axes([0.85, 0.78, 0.1, 0.05])
ax_btn2_343 = plt.axes([0.85, 0.71, 0.1, 0.05])

btn2_433 = Button(ax_btn2_433, 'T2 4-3-3')
btn2_442 = Button(ax_btn2_442, 'T2 4-4-2')
btn2_343 = Button(ax_btn2_343, 'T2 3-4-3')

btn2_433.on_clicked(lambda event: set_team2_formation(event, '4-3-3'))
btn2_442.on_clicked(lambda event: set_team2_formation(event, '4-4-2'))
btn2_343.on_clicked(lambda event: set_team2_formation(event, '3-4-3'))

ax_start = plt.axes([0.4, 0.05, 0.2, 0.1])
btn_start = Button(ax_start, 'Generate Board')
btn_start.on_clicked(start_board)

plt.show()