from functions import weather,notep,calend,wiki,timeDate,weather_now
from helping import speak,get_audio
import random
import webbrowser

           
def main():
    greetings = ['γειά σου', 'γεια', 'γειά', 'επ', 'που είσα εσύ', 'γεια σου σόνια']
    greetings1 = ['Γειά σου', 'Γειάα', 'Γειά σου και εσένα']
    question = ['τι κάνεις', 'πώς είσαι']
    responses = ['Μια χαρά', "Είμαι καλά"]
    var1 = ['ποιός σε έφτιαξε', 'ποιός είναι ο δημιουργός σου']
    var2 = ['Με δημιούργησε ο Μάκης', 'Μάκης', 'Ένας άνθρωπος που δεν έχω γνωρίσει ποτέ']
    var4 = ['ποιά είσαι', 'πώς σε λένε']
    jokes = ['Η σόφτεξ εξαγοράζει την άμαζον','Τελικά το μέγεθος δεν μετράει.. Κοιτάξτε τι μας έκαναν οι κινεζοι...']
    cmd9 = ['ευχαριστώ']
    repfr9 = ['Παρακαλώ', 'Χαίρομαι που βοήθησα']
    speak("Πώς μπορώ να σε βοηθήσω")
    text = ""
    loop = 0

    while text.count("αναμονή λειτουργίας") < 1 or loop < 5:
        text = get_audio()
        loop +=1
        if text in greetings:
            random_greeting = random.choice(greetings1)
            print(random_greeting)
            speak(random_greeting)
        elif text in question:
            speak('Μια χαρά')
            print('Μια χαρά')
        elif text in var1:
            speak(random.choice(var2))
            reply = random.choice(var2)
            print(reply)
        elif text in cmd9:
            print(random.choice(repfr9))
            speak(random.choice(repfr9))
        elif text.count("μουσική") > 0 or text.count("τραγούδι") > 0 or text.count("music player") > 0:
            webbrowser.open("path of an mp3 file")
        elif text in var4:
            speak('Είμαι η Σόνια')
        elif text.count("youtube") > 0:
            webbrowser.open('www.youtube.com')
        elif text.count("κλείσε") > 0 or text.count("close") > 0 or text.count("έξοδος") > 0 or text.count("exit") > 0:
            print('Τα λέμε μετά')
            speak('Τα λέμε μετά')
            exit()
        elif text.count("ημερολόγιο") > 0 or text.count("ατζέντα") > 0:
            calend()        
        elif text.count("θερμοκρασία") > 0 or text.count("καιρό") > 0:
            speak("Για πότε?")
            for x in range(0, 3):
                d = get_audio()    
                if d.count("σήμερα") > 0 or d.count("τώρα") > 0:
                    weather()
                if d.count("επόμενη") > 0 or d.count("επόμενες") > 0 or d.count("αύριο") > 0:
                    weather_now()
        elif  text.count("πες μου την ώρα") > 0 or text.count("ώρα") > 0 or text.count("ημερομηνία") > 0 or text.count("τί ημερομηνία έχουμε") > 0:
            timeDate()
        elif text.count("browser") > 0 or text.count("google") > 0:
            webbrowser.open('www.google.com')
        elif text.count("ανέκδοτο") > 0 or text.count("αστείο") > 0 or text.count("ανέκδοτα") > 0:
            jokrep = random.choice(jokes)
            speak(jokrep)
        elif text not in "" and (text.count("ψάξε") > 0 or text.count("αναζήτηση")):
            wiki()
        elif text.count("σημείωση") > 0 or text.count("σημειωματάριο" or text.count("καταχώρηση")):
            notep()
        elif text.count("αναμονή λειτουργίας") > 0:   
            speak("Αναμονή Λειτουργίας")
