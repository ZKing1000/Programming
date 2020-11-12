import pyglet
import data

class Player(pyglet.media.Player):
    def __init__(self):
        if not pyglet.media.have_avbin: return
        super(Player, self).__init__()
        self.eos_action = 'loop'
        self.track = None
    def switch(self, track):
        if not pyglet.media.have_avbin: return
        if track == self.track: return
        self.track = track
        if not track:
            self.next()
        else:
            try:
                song = data.load_song(track)
                self.next()
                self.queue(song)
                self.play()
            except pyglet.media.avbin.AVbinException:
                print "You don't seem to have", track
        
        
if __name__ == '__main__':
    import random
    win = pyglet.window.Window()
    player = Player()
    
    @win.event
    def on_key_press(sym, mods):
        player.switch(random.choice(['Pinball Spring.mp3', 'Blipotron.mp3', None]))
    
    pyglet.app.run()