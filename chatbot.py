from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia
import requests
from googletrans import Translator
import webbrowser
import random
import re
import json
import pint

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x200+400+200")
        self.root.configure(bg='#2c3e50')

        self.email_label = Label(self.root, text="Email:", font=('arial', 14, 'bold'), fg='#2ecc71', bg='#34495e')
        self.email_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.email_entry = ttk.Entry(self.root, width=30, font=('times new roman', 16, 'bold'))
        self.email_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.password_label = Label(self.root, text="Password:", font=('arial', 14, 'bold'), fg='#2ecc71', bg='#34495e')
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.password_entry = ttk.Entry(self.root, show='*', width=30, font=('times new roman', 16, 'bold'))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        self.login_button = Button(self.root, text='Login', font=('arial', 15, 'bold'), width=15, bg='#3498db', fg='white', command=self.login)
        self.login_button.grid(row=2, column=1, padx=5, pady=10, sticky=W)

    def login(self):
        # Replace the hardcoded values with your actual login credentials
        valid_email = 'sunny18@gmail.com'
        valid_password = '12341234'

        # Check the entered email and password
        entered_email = self.email_entry.get()
        entered_password = self.password_entry.get()

        # Replace the condition below with your actual login logic
        if entered_email == valid_email and entered_password == valid_password:
            # If login successful, close the login window
            self.root.destroy()
            
            # Open the Chatbot window
            chatbot_root = Tk()
            chatbot_obj = Chatbot(chatbot_root)
            chatbot_root.mainloop()
        else:
            # If login fails, show an error message
            messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("720x620+0+0")
        self.root.configure(bg='#2c3e50')

        self.main_frame = Frame(self.root, bd=4, bg='#34495e', width=610)
        self.main_frame.pack()

        img_chat = Image.open('chatbot.jpg')
        img_chat = img_chat.resize((200, 70), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img_chat)

        Title_label = Label(self.main_frame, bd=3, relief=RAISED, anchor='nw', width=500, image=self.photoimg,
                            text='CHAT ME', font=('arial', 30, 'bold'), fg='#2ecc71', bg='#34495e')
        Title_label.pack(side=TOP)

        self.scroll_y = ttk.Scrollbar(self.main_frame, orient=VERTICAL)
        self.text = Text(self.main_frame, width=65, height=20, bd=3, relief=RAISED, font=('arial', 14),
                         yscrollcommand=self.scroll_y.set, bg='#2c3e50', fg='white', insertbackground='white')
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.text.pack()

        btn_frame = Frame(self.root, bd=4, bg='#34495e', width=610)
        btn_frame.pack()

        self.datetime_label = Label(btn_frame, text="", font=('arial', 14, 'bold'), fg='#2ecc71',
                                    bg='#34495e')
        self.datetime_label.grid(row=0, column=1, columnspan=3, pady=10)
        self.update_datetime()

        Label_1 = Label(btn_frame, text="Type Something", font=('arial', 14, 'bold'), fg='#2ecc71',
                        bg='#34495e')
        Label_1.grid(row=1, column=0, padx=5, sticky=W)

        self.entry = StringVar()
        self.entry1 = ttk.Entry(btn_frame, textvariable=self.entry, width=40, font=('times new roman', 16, 'bold'))
        self.entry1.grid(row=1, column=1, padx=5, sticky=W)
        self.entry1.bind('<KeyRelease>', self.autosuggest)

        self.send_button = Button(btn_frame, text='send>>', font=('arial', 15, 'bold'), width=8, bg='#2ecc71',
                                   fg='white', command=self.send)
        self.send_button.grid(row=1, column=2, padx=5, sticky=W)

        self.clear = Button(btn_frame, text='clear data>', font=('arial', 15, 'bold'), width=8, bg='#e74c3c',
                            fg='white', command=self.clear)
        self.clear.grid(row=2, column=0, padx=5, sticky=W)

        self.msg = ''
        self.label_1 = Label(btn_frame, text=self.msg, font=('arial', 14, 'bold'), fg='#2ecc71',
                             bg='#34495e')
        self.label_1.grid(row=2, column=1, padx=5, sticky=W)

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Button for speech-to-text
        self.speech_button = Button(btn_frame, text='Speech to Text', font=('arial', 15, 'bold'), width=12, bg='#2ecc71', fg='white', command=self.speech_to_text)
        self.speech_button.grid(row=2, column=2, padx=5, sticky=W)

        self.suggested_questions_frame = Frame(self.root, bd=4, bg='#34495e', width=610)
        self.suggested_questions_frame.pack()

        self.suggested_questions_label = Label(self.suggested_questions_frame, text="Suggested Questions:", font=('arial', 16, 'bold'), fg='#2ecc71', bg='#34495e')
        self.suggested_questions_label.pack(anchor='w', padx=10, pady=5)

        self.suggested_questions()

    def update_datetime(self):
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.datetime_label.config(text="Current Date and Time: " + date_time_str)
        self.root.after(1000, self.update_datetime)

    def autosuggest(self, event):
        user_input = self.entry.get().lower()
        if user_input:
            suggestions = self.generate_suggestions(user_input)
            self.update_suggestions(suggestions)
        else:
            self.update_suggestions([])

    def generate_suggestions(self, user_input):
        suggestions = [
            "Wikipedia of kolkata?",
            "play music?",
            f"weather in {user_input}?",
            "current news?",
            "translate to bengali.",
            "translate to Spanish.",
            "give python programming for loop",
            "give java programming for method.",
            "how are you",
            "convert 10 meters to feet",
            "convert 100 kilograms to pounds",
            "convert 20 miles to kilometers",
            "convert 30 liters to gallons",
            "convert 50 celsius to fahrenheit",
            "convert 60 acres to square meters"
        ]
        # Filter suggestions based on user input
        filtered_suggestions = [suggestion for suggestion in suggestions if re.search(user_input, suggestion.lower())]
        return filtered_suggestions

    def update_suggestions(self, suggestions):
        for widget in self.suggested_questions_frame.winfo_children():
            widget.destroy()
        
        self.suggested_questions_label = Label(self.suggested_questions_frame, text="Suggested Questions:", font=('arial', 16, 'bold'), fg='#2ecc71', bg='#34495e')
        self.suggested_questions_label.pack(anchor='w', padx=10, pady=5)

        for index, suggestion in enumerate(suggestions[:5]):
            suggested_question_label = Label(self.suggested_questions_frame, text=f"{index + 1}. {suggestion}", font=('arial', 12), fg='#2ecc71', bg='#34495e', cursor="hand2")
            suggested_question_label.bind("<Button-1>", lambda event, suggestion=suggestion: self.populate_entry(suggestion))
            suggested_question_label.pack(anchor='w', padx=10, pady=5)

    def populate_entry(self, suggestion):
        self.entry.set(suggestion)

    def clear(self):
        self.text.delete('1.0', END)
        self.entry.set('')

    def send(self):
        user_input = self.entry.get()
        send_message = '\t\t\t' + "YOU: " + user_input
        self.text.insert(END, '\n' + send_message)

        if user_input == '':
            self.msg = 'Please enter some input'
            self.label_1.config(text=self.msg, fg='#e74c3c')
        else:
            self.msg = ''
            self.label_1.config(text=self.msg, fg='#e74c3c')

            bot_response = self.generate_bot_response(user_input)
            self.text.insert(END, '\n\n' + 'BOT: ' + bot_response)
            self.text.yview(END)
            self.speak(bot_response)

            # Ask for feedback
            self.ask_for_feedback()

        self.entry1.delete(0, 'end')

    def generate_bot_response(self, user_input):
        translator = Translator()
        if user_input.lower().startswith('translate to bengali'):
            text_to_translate = user_input[20:]
            translated_text = translator.translate(text_to_translate, dest='bn').text
            return translated_text
        elif user_input.lower().startswith('translate to hindi'):
            text_to_translate = user_input[18:]
            translated_text = translator.translate(text_to_translate, dest='hi').text
            return translated_text
        elif user_input.lower().startswith('translate to spanish'):
            text_to_translate = user_input[20:]
            translated_text = translator.translate(text_to_translate, dest='es').text
            return translated_text
        elif user_input.lower().startswith('translate to french'):
            text_to_translate = user_input[19:]
            translated_text = translator.translate(text_to_translate, dest='fr').text
            return translated_text
        elif user_input.lower() == 'hello':
            return 'Hi, what can I help you with?'
        elif user_input.lower() == 'how are you':
            return 'I am just a bot, but thanks for asking!'
        elif user_input.lower() == 'bye':
            return 'Thanks for chatting with me.'
        elif user_input.lower() == 'what is machine learning':
            return 'Machine learning is a subfield of artificial intelligence (AI) that focuses on the development of algorithms and statistical models that enable computers to perform tasks without explicit programming.'
        elif user_input.lower().startswith('weather in'):
            location = user_input[11:]
            weather_info = self.get_weather_info(location)
            return f"The weather in {location} is: {weather_info}"
        elif user_input.lower() == 'time':
            current_time = datetime.now().strftime("%H:%M:%S")
            return f"The current time is {current_time}"
        elif user_input.lower() == 'date':
            current_date = datetime.now().strftime("%Y-%m-%d")
            return f"Today's date is {current_date}"
        elif user_input.lower() == 'date and time':
            current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"The current date and time are {current_date_time}"
        elif user_input.lower().startswith('wikipedia'):
            query = user_input[10:].strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                return result
            except wikipedia.DisambiguationError as e:
                return f"Multiple results found. Please be more specific."
            except wikipedia.PageError as e:
                return f"Sorry, I couldn't find information on that topic."
        elif user_input.lower().startswith('give python programming for'):
            text_format = user_input[28:].strip()
            if text_format == 'example':
                code_snippet = '''
                # Example Python code
                def greet(name):
                    return f"Hello, {name}!"

                print(greet("World"))
                '''
                return code_snippet
            elif text_format == 'loop':
                code_snippet = '''
                # Python loop example
                for i in range(5):
                    print(i)
                '''
                return code_snippet
            elif text_format == 'function':
                code_snippet = '''
                # Python function example
                def add(x, y):
                    return x + y
                
                result = add(3, 5)
                print("Result:", result)
                '''
                return code_snippet
            elif text_format == 'class':
                code_snippet = '''
                # Python class example
                class MyClass:
                    def __init__(self, name):
                        self.name = name
                    
                    def greet(self):
                        return f"Hello, {self.name}!"
                
                obj = MyClass("World")
                print(obj.greet())
                '''
                return code_snippet
            elif text_format == 'exception':
                code_snippet = '''
                # Python exception handling example
                try:
                    result = 10 / 0
                except ZeroDivisionError as e:
                    print("Error:", e)
                '''
                return code_snippet
            elif text_format == 'file':
                code_snippet = '''
                # Python file handling example
                with open('example.txt', 'w') as file:
                    file.write("Hello, World!")
                '''
                return code_snippet
            elif text_format == 'dictionary':
                code_snippet = '''
                # Python dictionary example
                my_dict = {'name': 'John', 'age': 30}
                print(my_dict)
                '''
                return code_snippet
            elif text_format == 'list':
                code_snippet = '''
                # Python list example
                my_list = [1, 2, 3, 4, 5]
                print(my_list)
                '''
                return code_snippet
            elif text_format == 'tuple':
                code_snippet = '''
                # Python tuple example
                my_tuple = (1, 2, 3, 4, 5)
                print(my_tuple)
                '''
                return code_snippet
            elif text_format == 'set':
                code_snippet = '''
                # Python set example
                my_set = {1, 2, 3, 4, 5}
                print(my_set)
                '''
                return code_snippet
            elif text_format == 'lambda':
                code_snippet = '''
                # Python lambda function example
                add = lambda x, y: x + y
                print(add(3, 5))
                '''
                return code_snippet
            elif text_format == 'generator':
                code_snippet = '''
                # Python generator example
                def my_generator(n):
                    for i in range(n):
                        yield i

                gen = my_generator(5)
                print(list(gen))
                '''
                return code_snippet
            else:
                return "Invalid format. Available formats: example, loop, function, class, exception, file, dictionary, list, tuple, set, lambda, generator."
        elif user_input.lower().startswith('play music'):
            query = user_input[11:].strip()
            self.play_music(query)
            return "Playing music..."
        elif user_input.lower() == 'current news':
            news = self.get_current_news()
            return news
        elif user_input.lower().startswith('give java programming for'):
            text_format = user_input[26:].strip()
            if text_format == 'example':
                code_snippet = '''
                // Example Java code
                public class Main {
                    public static void main(String[] args) {
                        System.out.println("Hello, World!");
                    }
                }
                '''
                return code_snippet
            elif text_format == 'loop':
                code_snippet = '''
                // Java loop example
                public class Main {
                    public static void main(String[] args) {
                        for (int i = 0; i < 5; i++) {
                            System.out.println(i);
                        }
                    }
                }
                '''
                return code_snippet
            elif text_format == 'method':
                code_snippet = '''
                // Java method example
                public class Main {
                    static int add(int x, int y) {
                        return x + y;
                    }

                    public static void main(String[] args) {
                        int result = add(3, 5);
                        System.out.println("Result: " + result);
                    }
                }
                '''
                return code_snippet
            elif text_format == 'class':
                code_snippet = '''
                // Java class example
                public class MyClass {
                    private String name;

                    public MyClass(String name) {
                        this.name = name;
                    }

                    public void greet() {
                        System.out.println("Hello, " + name + "!");
                    }

                    public static void main(String[] args) {
                        MyClass obj = new MyClass("World");
                        obj.greet();
                    }
                }
                '''
                return code_snippet
            elif text_format == 'exception':
                code_snippet = '''
                // Java exception handling example
                public class Main {
                    public static void main(String[] args) {
                        try {
                            int result = 10 / 0;
                        } catch (ArithmeticException e) {
                            System.out.println("Error: " + e.getMessage());
                        }
                    }
                }
                '''
                return code_snippet
            elif text_format == 'file':
                code_snippet = '''
                // Java file handling example
                import java.io.FileWriter;
                import java.io.IOException;

                public class Main {
                    public static void main(String[] args) {
                        try {
                            FileWriter myWriter = new FileWriter("example.txt");
                            myWriter.write("Hello, World!");
                            myWriter.close();
                            System.out.println("Successfully wrote to the file.");
                        } catch (IOException e) {
                            System.out.println("An error occurred.");
                            e.printStackTrace();
                        }
                    }
                }
                '''
                return code_snippet
            elif text_format == 'array':
                code_snippet = '''
                // Java array example
                public class Main {
                    public static void main(String[] args) {
                        int[] myArray = {1, 2, 3, 4, 5};
                        for (int i = 0; i < myArray.length; i++) {
                            System.out.println(myArray[i]);
                        }
                    }
                }
                '''
                return code_snippet
            elif text_format == 'list':
                code_snippet = '''
                // Java List example
                import java.util.ArrayList;
                import java.util.List;

                public class Main {
                    public static void main(String[] args) {
                        List<Integer> myList = new ArrayList<>();
                        myList.add(1);
                        myList.add(2);
                        myList.add(3);
                        System.out.println(myList);
                    }
                }
                '''
                return code_snippet
            elif text_format == 'map':
                code_snippet = '''
                // Java Map example
                import java.util.HashMap;
                import java.util.Map;

                public class Main {
                    public static void main(String[] args) {
                        Map<String, Integer> myMap = new HashMap<>();
                        myMap.put("One", 1);
                        myMap.put("Two", 2);
                        myMap.put("Three", 3);
                        System.out.println(myMap);
                    }
                }
                '''
                return code_snippet
            elif text_format == 'lambda':
                code_snippet = '''
                // Java lambda expression example
                public class Main {
                    public static void main(String[] args) {
                        MyInterface myInterface = (int x, int y) -> x + y;
                        System.out.println(myInterface.add(3, 5));
                    }
                }

                interface MyInterface {
                    int add(int x, int y);
                }
                '''
                return code_snippet
            elif text_format == 'stream':
                code_snippet = '''
                // Java Stream example
                import java.util.Arrays;

                public class Main {
                    public static void main(String[] args) {
                        int[] arr = {1, 2, 3, 4, 5};
                        Arrays.stream(arr).forEach(System.out::println);
                    }
                }
                '''
                return code_snippet
            else:
                return "Invalid format. Available formats: example, loop, method, class, exception, file, array, list, map, lambda, stream."
        elif re.match(r'convert \d+ meters to feet', user_input.lower()):
            meters = int(re.match(r'convert (\d+) meters to feet', user_input.lower()).group(1))
            feet = meters * 3.28084
            return f"{meters} meters is equal to {feet:.2f} feet."
        elif re.match(r'convert \d+ kilograms to pounds', user_input.lower()):
            kilograms = int(re.match(r'convert (\d+) kilograms to pounds', user_input.lower()).group(1))
            pounds = kilograms * 2.20462
            return f"{kilograms} kilograms is equal to {pounds:.2f} pounds."
        elif re.match(r'convert \d+ miles to kilometers', user_input.lower()):
            miles = int(re.match(r'convert (\d+) miles to kilometers', user_input.lower()).group(1))
            kilometers = miles * 1.60934
            return f"{miles} miles is equal to {kilometers:.2f} kilometers."
        elif re.match(r'convert \d+ liters to gallons', user_input.lower()):
            liters = int(re.match(r'convert (\d+) liters to gallons', user_input.lower()).group(1))
            gallons = liters * 0.264172
            return f"{liters} liters is equal to {gallons:.2f} gallons."
        elif re.match(r'convert \d+ celsius to fahrenheit', user_input.lower()):
            celsius = int(re.match(r'convert (\d+) celsius to fahrenheit', user_input.lower()).group(1))
            fahrenheit = (celsius * 9/5) + 32
            return f"{celsius} Celsius is equal to {fahrenheit:.2f} Fahrenheit."
        elif re.match(r'convert \d+ acres to square meters', user_input.lower()):
            acres = int(re.match(r'convert (\d+) acres to square meters', user_input.lower()).group(1))
            square_meters = acres * 4046.86
            return f"{acres} acres is equal to {square_meters:.2f} square meters."
        else:
            return "I'm sorry, I didn't understand that."

    def ask_for_feedback(self):
        feedback = messagebox.askquestion("Feedback", "Was this helpful?")
        if feedback == 'yes':
            messagebox.showinfo("Feedback", "Thank you!")
        else:
            messagebox.showinfo("Feedback", "Sorry to hear that. We'll try to improve.")

    def get_weather_info(self, location):
        api_key = "cfbd4121db3a5b017413e909d5734250"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "q=" + location + "&appid=" + api_key + "&units=metric"
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            main_info = data["main"]
            temperature = main_info["temp"]
            description = data["weather"][0]["description"]
            return f"{temperature}°C, {description}"
        else:
            return "City not found."

    def get_current_news(self):
        api_key = "fde1fde39a844649917c3e5c2ed0248f"
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        news = response.json()
        articles = news['articles']
        headlines = []
        for article in articles[:5]:
            headlines.append(article['title'])
        return "\n".join(headlines)

    def play_music(self, query):
        search_url = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(search_url)
    def speech_to_text(self):
        with sr.Microphone() as source:
            self.engine.say("Please speak now")
            self.engine.runAndWait()
            audio = self.recognizer.listen(source)

        try:
            user_input = self.recognizer.recognize_google(audio)
            self.entry.set(user_input)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I could not understand your audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Sorry, I could not request results due to network error.")

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

if __name__ == '__main__':
    root = Tk()
    obj = Login(root)
    root.mainloop()
