from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ListProperty
from kivy.properties import DictProperty
import sqlite3 as sql
import random
from random import choice
from random import shuffle

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class ProjectApp(App):
    test_word= StringProperty('')
    kor_word_list = ListProperty()
    word_dict = DictProperty()
    usable_words = ListProperty()
    multiple_choice_1 = StringProperty('')
    multiple_choice_2 = StringProperty('')
    multiple_choice_3 = StringProperty('')
    multiple_choice_4 = StringProperty('')
    multiple_choice_5 = StringProperty('')
    def build(self):
        self.counter = 0
        self.kor_word_list, self.word_dict, self.usable_words = create_list() ##function returns list, dict, list
        self.rand_word = get_rand_word(self.usable_words)
        self.test_word = "Choice1"
        self.multiple_choice_1 = "Choice1"
        self.multiple_choice_2 = choice(self.usable_words)[1]
        self.multiple_choice_3 = choice(self.usable_words)[1]
        self.multiple_choice_4 = choice(self.usable_words)[1]
        self.multiple_choice_5 = choice(self.usable_words)[1]
        self.update_dict = {}
        self.root = Builder.load_file('mainkv.kv')
        return self.root
    
    def on_button_press(self,screen,testing_word):
        pass

    def set_words(self, screen, testing_word, choice_1, choice_2, choice_3, choice_4, choice_5):
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
    return kor_word_list, word_dict, usable_words


if __name__ == '__main__':
    ProjectApp().run()