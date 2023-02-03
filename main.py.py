from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition,NoTransition
from kivy.properties import ListProperty
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
import sqlite3 as sql
import random
from random import choice
from random import shuffle
from kivy.config import Config
import pickle
from datetime import date,timedelta
from kivy_garden.graph import Graph, LinePlot


class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class EndScreen(Screen):
    pass

class OptionsScreen(Screen):
    pass

class GraphScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class ProjectApp(App):
    kor_word_list = ListProperty()
    word_dict = DictProperty()
    usable_words = ListProperty()
    Config.set("kivy", "exit_on_escape", "0")
    def build(self):
        self.counter = 0
        self.kor_word_list, self.word_dict, self.usable_words = create_list() ##function returns list, dict, list
        self.rand_word = get_rand_word(self.usable_words)

        self.update_dict = {}
        self.root = Builder.load_file('mainkv.kv')
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        return self.root
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        if keycode[0] == 27:
            ScreenManager.transition = SlideTransition()
            ScreenManager.transition.direction = "up"
            self.root.current = "main"

        
    def reset_counter(self,end):
        self.counter =0
        self.kor_word_list, self.word_dict, self.usable_words = create_list()
        self.rand_word = get_rand_word(self.usable_words)

    def set_words(self, screen, testing_word, choice_1, choice_2, choice_3, choice_4, choice_5, progress_bar):
        ScreenManager.transition = SlideTransition()
        ScreenManager.transition.direction = "left"
        progress_bar.value = (self.counter/len(self.kor_word_list))
        print("list len is " + str(len(self.kor_word_list)))
        print("counter is " + str(self.counter))
        if self.counter == len(self.kor_word_list):
            self.root.current = "end"
            print("here")
        else:
            testing_word.text = self.kor_word_list[self.counter]
            self.update_dict[testing_word.text] = 0
            #print(testing_word.text)
            correct_translation = self.word_dict[testing_word.text]
            #print(correct_translation)
            correct_and_random = []
            for i in range(4):
                word = choice(self.usable_words)[1]
                correct_and_random.append(word)
            correct_and_random.append(correct_translation)
            choice_1.text = str(choice(correct_and_random))
            correct_and_random.remove(choice_1.text)
            choice_2.text = str(choice(correct_and_random))
            correct_and_random.remove(choice_2.text)
            choice_3.text = str(choice(correct_and_random))
            correct_and_random.remove(choice_3.text)
            choice_4.text = str(choice(correct_and_random))
            correct_and_random.remove(choice_4.text)
            choice_5.text = str(choice(correct_and_random))
            correct_and_random.remove(choice_5.text)
        con = sql.connect("vocab_data.db")
        cur = con.cursor()
        conf5 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 5").fetchall()
        num_conf5 = len(conf5)
        conf4 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 4").fetchall()
        num_conf4 = len(conf4)
        conf3 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 3").fetchall()
        num_conf3 = len(conf3)
        conf2 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 2").fetchall()
        num_conf2 = len(conf2)
        conf1 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 1").fetchall()
        num_conf1 = len(conf1)
        score = ((num_conf5*5)+(num_conf4*4)+(num_conf3*3)+(num_conf2*2)+(num_conf1*1))
        with open('score_dict.pkl','rb') as f:
            score_dict = pickle.load(f)
        today = date.today()
        YYMMDD = today.strftime("%Y%m%d")
        score_dict[YYMMDD]=score
        with open("score_dict.pkl","wb") as f:
            pickle.dump(score_dict,f)


    def inc_counter(self):
        if self.counter < len(self.words_list):
            self.counter +=1
        else:
            self.counter = self.counter

    def get_counter(self,buttonpressed,testing_word):
        print(testing_word.text)
        print(buttonpressed.text)
        if (buttonpressed.background_color == [0,1,0,1]):
            print("same")
            print(self.counter)
            print(buttonpressed.background_color)
            self.counter+=1
        else:
            print(self.counter)
            print("diff")
    
    def check_correct(self, buttonpressed, testing_word):
        con = sql.connect("vocab_data.db")
        cur = con.cursor()
        test_word = testing_word.text
        guessed_word = buttonpressed.text
        print("testword is " + test_word)
        print("guessedword is " + guessed_word)
        print(self.update_dict)
        if self.update_dict[test_word] == 0:
            if self.word_dict[test_word] == guessed_word:
                cur.execute("UPDATE Vocab SET Confidence = Confidence + 1 WHERE Korean = ? AND Confidence < 5",(test_word,))
                con.commit()
            else:
                cur.execute("UPDATE Vocab SET Confidence = Confidence - 1 WHERE Korean = ? AND Confidence > 0",(test_word,))
                con.commit()
        self.update_dict[test_word] = 1

    def get_progress(self,options,conf5button,conf4button,conf3button,conf2button,conf1button,conf0button):
        con = sql.connect("vocab_data.db")
        cur = con.cursor()
        conf5 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 5").fetchall()
        num_conf5 = len(conf5)
        conf4 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 4").fetchall()
        num_conf4 = len(conf4)
        conf3 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 3").fetchall()
        num_conf3 = len(conf3)
        conf2 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 2").fetchall()
        num_conf2 = len(conf2)
        conf1 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 1").fetchall()
        num_conf1 = len(conf1)
        conf0 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 0").fetchall()
        num_conf0 = len(conf0)
        conf5button.text = str(num_conf5) + " words"
        conf4button.text = str(num_conf4) + " words"
        conf3button.text = str(num_conf3) + " words"
        conf2button.text = str(num_conf2) + " words"
        conf1button.text = str(num_conf1) + " words"
        conf0button.text = str(num_conf0) + " words"


    def expand(self,button,confidence_label):
        con = sql.connect("vocab_data.db")
        cur = con.cursor() 
        level = confidence_label.text[0]
        words_list = cur.execute("SELECT * FROM Vocab WHERE Confidence = ?",(level,)).fetchall()
        words_list = words_list[:48]
        if len(words_list) > 50:
            button.text = "50+ words"
            button.size_hint_x = .7
            confidence_label.size_hint_x = .3
        else:
            print("HERE")
            print(words_list)
            string = ""
            for i in words_list:
                string = string + i[0] + ", "
            button.text = string
            button.size_hint_x = .7
            confidence_label.size_hint_x = .3
            button.text_size = button.width,None



    def reset_expand(self,button,confidence_label):
        print("GOT HERE")
        button.size_hint_x =1
        confidence_label.size_hint_x = 1
        con = sql.connect("vocab_data.db")
        cur = con.cursor() 
        level = confidence_label.text[0]
        words_list = cur.execute("SELECT * FROM Vocab WHERE Confidence = ?",(level,)).fetchall()
        num_words_list = len(words_list)
        button.text = str(num_words_list) + " words"

    def do_nothing(self):
        print("GOT TO DO NOTHING")
        
    def open_popup(self,conf5label):
        level = conf5label.text[0]
        con = sql.connect("vocab_data.db")
        cur = con.cursor()
        words_list = cur.execute("SELECT * FROM Vocab WHERE Confidence = ?",(level,)).fetchall()
        print(words_list)
        superBox = BoxLayout(orientation="vertical")
        scrollBox = ScrollView()
        superBox2 = BoxLayout(orientation="vertical",size_hint_y=None,pos_hint={"y":.9})
        superBox2.bind(minimum_height=superBox2.setter("height"))
        for i in words_list:
            hbox = BoxLayout(orientation="horizontal",size_hint_y=None)
            lbl1 = Label(text = i[1],font_name="NanumGothic.ttf")
            lbl2 = Label(text=i[0],font_name="NanumGothic.ttf")
            hbox.add_widget(lbl1)
            hbox.add_widget(lbl2)
            superBox2.add_widget(hbox)
        scrollBox.add_widget(superBox2)
        superBox.add_widget(scrollBox)
        popup = Popup(title="Words",auto_dismiss=True,size_hint=(.7,1),pos_hint={"x":.15},content=superBox)
        popup.open()


    def change_transition(self,text):
        if text == "left":
            ScreenManager.transition = SlideTransition()
            ScreenManager.transition.direction="left"
        if text =="right":
            ScreenManager.transition = SlideTransition()
            ScreenManager.transition.direction = "right"

    def draw_graph(self,testbox):
        testbox.clear_widgets()
        with open("score_dict.pkl","rb") as f:
            score=pickle.load(f)
        print(score)
        x1=[]
        y1=[]

        for i in score:
            x1.append(i)
            y1.append(score[i])
        print(x1)
        print(y1)
        #x1=[1,2,3,4]
        # plt.plot(x,y)
        # plt.ylabel("Score")
        # plt.xlabel("Time")
        # testbox.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        xticks = (int(x1[-1])-int(x1[0]))/len(x1)
        graph_theme = {'label_options': {'color':[0,0,0,1],'bold':True},'background_color':[1,1,1,1],'tick_color':[1,0,0,1],'border_color':[0,0,0,1]}
        graph=Graph(xlabel="Time",ylabel="Score",xmin=x1[0],ymin=y1[0],xmax=x1[-1],ymax=y1[-1],y_ticks_major=50,x_ticks_major=1,
                    x_grid_label=True,y_grid_label=True,x_grid=True,y_grid=True,draw_border=False,**graph_theme)
        plot=LinePlot(color=[0,0,0,1],line_width=1.5)
        plot.points = [(int(y),y1[x]) for x,y in enumerate(x1)]
        graph.add_plot(plot)
        testbox.add_widget(graph)


    def increase_daily(self,label):
        with open("daily_check_in.pkl","rb") as f:
            check_daily = pickle.load(f)
        print(check_daily)
        last_check_in = check_daily["last_check_in"]
        days_in_a_row = check_daily["days_in_a_row"]
        today = date.today()
        yesterday = today - timedelta(days=1)
        try:
            print(check_daily[today])
            print("tried") 
        except KeyError:
            if last_check_in == yesterday:
                check_daily["days_in_a_row"] = days_in_a_row+1
            check_daily["last_check_in"] = today
            check_daily[today] = 1
            print("excepted")
        with open("daily_check_in.pkl","wb") as f:
            pickle.dump(check_daily,f)
        print(check_daily)
        label.text = str(check_daily["days_in_a_row"]) + " days in a row"




def get_rand_word(usable_words):
    word= choice(usable_words)
    print(usable_words)
    return word


def create_list():
    kor_word_list = []
    word_dict = {} 
    carry_counter = 0
    con = sql.connect("vocab_data.db")
    cur = con.cursor()
    conf5 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 5").fetchall()
    num_conf5 = len(conf5)
    conf4 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 4").fetchall()
    num_conf4 = len(conf4)
    conf3 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 3").fetchall()
    num_conf3 = len(conf3)
    conf2 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 2").fetchall()
    num_conf2 = len(conf2)
    conf1 = cur.execute("SELECT * FROM Vocab WHERE Confidence = 1").fetchall()
    num_conf1 = len(conf1)
    new_words = cur.execute("SELECT * FROM Vocab WHERE Confidence = 0").fetchall()
    usable_words = cur.execute("SELECT * FROM Vocab WHERE Confidence > 0").fetchall()
    if num_conf5 < 1:
        carry_counter +=1
    else:
        randword = conf5[random.randint(0,len(conf5)-1)]
        kor_word_list.append(randword[0])
        word_dict[randword[0]]=randword[1]
    if num_conf4 < (2+carry_counter):
        carry_counter = ((2+carry_counter)-num_conf4)
        for i in range(num_conf4):
            randword = conf4[random.randint(0,len(conf4)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf4.remove(randword)
    else:
        for i in range(2+carry_counter):
            randword = conf4[random.randint(0,len(conf4)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf4.remove(randword)
    if num_conf3 < (3+carry_counter):
        carry_counter = ((3+carry_counter)-num_conf3)
        for i in range(num_conf3):
            randword=conf3[random.randint(0,len(conf3)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf3.remove(randword)
    else:
        for i in range(3+carry_counter):
            randword = conf3[random.randint(0,len(conf3)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf3.remove(randword)
    if num_conf2 < (4+carry_counter):
        carry_counter = ((4+carry_counter)-num_conf2)
        for i in range(num_conf2):
            randword = conf2[random.randint(0,len(conf2)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf2.remove(randword)
    else:
        for i in range(4+carry_counter):
            randword = conf2[random.randint(0,len(conf2)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf2.remove(randword)
    if num_conf1 < (3+carry_counter):
        carry_counter = ((3+carry_counter)-num_conf1)
        for i in range(num_conf1):
            randword=conf1[random.randint(0,len(conf1)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf1.remove(randword)
    else:
        for i in range(3+carry_counter):
            randword = conf1[random.randint(0,len(conf1)-1)]
            kor_word_list.append(randword[0])
            word_dict[randword[0]]=randword[1]
            conf1.remove(randword)
    for i in range(carry_counter+2):
        randword = new_words[0]
        new_words.remove(randword)
        kor_word_list.append(randword[0])
        word_dict[randword[0]]=randword[1]
    print(word_dict)
    shuffle(kor_word_list)
    ##kor_word_list = kor_word_list[:2]
    return kor_word_list, word_dict, usable_words


if __name__ == '__main__':
    ProjectApp().run()