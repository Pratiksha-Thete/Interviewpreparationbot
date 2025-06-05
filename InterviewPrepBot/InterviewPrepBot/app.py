from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'quiz-secret-key'

# --- Sample Questions (Only TCS shown, repeat for others) ---
questions = {
    "TCS": [
        {"question": "What is 20% of 150?", "options": ["30", "25", "20", "15"], "answer": "30"},
        {"question": "5 workers in 20 days. 10 workers take?", "options": ["10", "15", "25", "5"], "answer": "10"},
        {"question": "Speed of train 120km/h. Time for 240km?", "options": ["2", "1.5", "3", "2.5"], "answer": "2"},
        {"question": "LCM of 8 and 12?", "options": ["24", "16", "48", "12"], "answer": "24"},
        {"question": "50% of 300?", "options": ["150", "100", "200", "75"], "answer": "150"},
        {"question": "Simplify: (3x + 2) + (2x - 5)", "options": ["5x - 3", "5x + 3", "6x - 3", "5x - 7"], "answer": "5x - 3"},
        {"question": "Next in series: 2, 4, 8, 16, ?", "options": ["24", "32", "30", "36"], "answer": "32"},
        {"question": "Area of square with side 6?", "options": ["36", "30", "18", "12"], "answer": "36"},
        {"question": "What is cube of 3?", "options": ["27", "9", "81", "12"], "answer": "27"},
        {"question": "Reverse of 123?", "options": ["321", "231", "312", "213"], "answer": "321"},
        {"question": "Sum of angles in triangle?", "options": ["180", "360", "90", "270"], "answer": "180"},
        {"question": "100 ÷ 25?", "options": ["4", "5", "2", "6"], "answer": "4"},
        {"question": "2x = 10, x = ?", "options": ["5", "10", "2", "8"], "answer": "5"},
        {"question": "Square root of 49?", "options": ["7", "6", "8", "9"], "answer": "7"},
        {"question": "Binary of 5?", "options": ["101", "110", "111", "100"], "answer": "101"},
        {"question": "Factorial of 3?", "options": ["6", "9", "3", "2"], "answer": "6"},
        {"question": "15 is what percent of 60?", "options": ["25%", "20%", "30%", "15%"], "answer": "25%"},
        {"question": "12 ÷ 3 + 2 = ?", "options": ["6", "4", "5", "3"], "answer": "6"},
        {"question": "If x=2, then x² + 3x + 1?", "options": ["11", "12", "13", "14"], "answer": "11"},
        {"question": "Find HCF of 18 and 24?", "options": ["6", "12", "3", "18"], "answer": "6"}
    ],
    "Infosys": [
    {"question": "What comes next: 1, 4, 9, 16, ?", "options": ["20", "25", "36", "30"], "answer": "25"},
    {"question": "Find the odd one: Apple, Banana, Mango, Carrot", "options": ["Apple", "Banana", "Mango", "Carrot"], "answer": "Carrot"},
    
    {"question": "What is the output of: 5 + 3 * 2", "options": ["16", "11", "13", "10"], "answer": "11"},
    {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Array", "Tree"], "answer": "Stack"},
    {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": "O(log n)"},
    {"question": "Which of these is a primary key?", "options": ["Duplicate value", "Unique identifier", "Foreign key", "Composite key"], "answer": "Unique identifier"},
    {"question": "Which language is used for styling web pages?", "options": ["HTML", "JQuery", "CSS", "XML"], "answer": "CSS"},
    {"question": "Which SQL statement is used to extract data?", "options": ["GET", "SELECT", "EXTRACT", "FETCH"], "answer": "SELECT"},
    {"question": "What does RAM stand for?", "options": ["Read Access Memory", "Random Access Memory", "Run Active Memory", "None"], "answer": "Random Access Memory"},
    {"question": "Which of the following is not an OOP concept?", "options": ["Encapsulation", "Polymorphism", "Abstraction", "Compilation"], "answer": "Compilation"},
    
    {"question": "If A = 1, B = 2, ..., Z = 26, what is the value of CAT?", "options": ["24", "27", "48", "41"], "answer": "24"},
    {"question": "Which number replaces the question mark? 2, 6, 12, 20, ?", "options": ["30", "28", "24", "32"], "answer": "30"},
    {"question": "Find the missing number: 3, 6, 18, 72, ?", "options": ["144", "216", "360", "288"], "answer": "360"},
    {"question": "A man walks 5 km north, then turns east and walks 3 km. How far is he from the start?", "options": ["5 km", "6 km", "7 km", "8 km"], "answer": "5.83 km"},  # Distance = √(5² + 3²)
    {"question": "What is the angle between the hour and minute hand at 3:15?", "options": ["0°", "7.5°", "30°", "22.5°"], "answer": "7.5°"},
    
    {"question": "What does HTML stand for?", "options": ["Hyper Text Makeup Language", "Hyper Text Markup Language", "Home Tool Markup Language", "Hyperlink Text Markup Language"], "answer": "Hyper Text Markup Language"},
    {"question": "Which sorting algorithm is best on average?", "options": ["Bubble Sort", "Quick Sort", "Selection Sort", "Linear Sort"], "answer": "Quick Sort"},
    {"question": "Which protocol is used for web communication?", "options": ["FTP", "SMTP", "HTTP", "IP"], "answer": "HTTP"},
    {"question": "Which one is a NoSQL database?", "options": ["MySQL", "MongoDB", "PostgreSQL", "SQLite"], "answer": "MongoDB"},
    {"question": "Which of the following is immutable in Python?", "options": ["List", "Set", "Dictionary", "Tuple"], "answer": "Tuple"}
   ],

    "Wipro": [
    {"question": "Train 100m long takes 20 sec. Speed?", "options": ["5 m/s", "10 m/s", "20 m/s", "15 m/s"], "answer": "5 m/s"},
    {"question": "Simplify: (2x + 3) + (4x - 5)", "options": ["6x - 2", "2x - 8", "6x + 2", "6x - 8"], "answer": "6x - 2"},

    {"question": "Which number is the odd one out: 2, 3, 5, 7, 11, 13, 15", "options": ["3", "5", "11", "15"], "answer": "15"},
    {"question": "What is the output of: int x = 10; x += 5; print(x);", "options": ["10", "15", "5", "20"], "answer": "15"},
    {"question": "What does RAM stand for?", "options": ["Read Access Memory", "Random Access Memory", "Run Access Memory", "Rapid Access Memory"], "answer": "Random Access Memory"},
    {"question": "What is the next term: 2, 6, 12, 20, ?", "options": ["28", "30", "32", "36"], "answer": "30"},
    {"question": "Which sorting algorithm is the fastest in average case?", "options": ["Bubble Sort", "Insertion Sort", "Quick Sort", "Selection Sort"], "answer": "Quick Sort"},
    {"question": "Which is a valid Python variable name?", "options": ["1var", "var_1", "var-1", "var 1"], "answer": "var_1"},
    {"question": "Speed of sound is fastest in?", "options": ["Water", "Air", "Vacuum", "Steel"], "answer": "Steel"},
    {"question": "What is 15% of 200?", "options": ["15", "20", "30", "25"], "answer": "30"},
    {"question": "Which number replaces the question mark? 3, 6, 18, 72, ?", "options": ["144", "216", "288", "360"], "answer": "360"},
    {"question": "A cube has how many faces?", "options": ["4", "6", "8", "12"], "answer": "6"},
    {"question": "Find x: 3x - 5 = 16", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"question": "Choose the word most nearly opposite to: 'Artificial'", "options": ["Natural", "Automatic", "Genuine", "Real"], "answer": "Natural"},
    {"question": "Identify the output: 5 % 2", "options": ["1", "2", "2.5", "0"], "answer": "1"},
    {"question": "Which data structure uses FIFO?", "options": ["Stack", "Queue", "Tree", "Graph"], "answer": "Queue"},
    {"question": "Which keyword is used to define a function in Python?", "options": ["def", "function", "define", "lambda"], "answer": "def"},
    {"question": "In C, which symbol is used to denote a pointer?", "options": ["&", "*", "#", "%"], "answer": "*"},
    {"question": "A man walks 3 km north, 4 km east. Distance from start?", "options": ["5 km", "7 km", "6 km", "3.5 km"], "answer": "5 km"},
    {"question": "What is the binary of decimal 10?", "options": ["1010", "1100", "1001", "1111"], "answer": "1010"}
],

    "Capgemini": [
    {"question": "Selling price = 240, profit = 20%. CP?", "options": ["200", "220", "230", "250"], "answer": "200"},
    {"question": "LCM of 12, 18, 30?", "options": ["180", "90", "60", "120"], "answer": "180"},

    {"question": "Find the missing term: 2, 5, 10, 17, ?", "options": ["24", "26", "30", "28"], "answer": "26"},
    {"question": "What is 25% of 640?", "options": ["120", "150", "160", "180"], "answer": "160"},
    {"question": "If 3x = 81, then x = ?", "options": ["27", "24", "18", "21"], "answer": "27"},
    {"question": "Binary of 15?", "options": ["1100", "1111", "1001", "1010"], "answer": "1111"},
    {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Tree", "Graph"], "answer": "Stack"},
    {"question": "Which sorting algorithm is not stable?", "options": ["Merge Sort", "Insertion Sort", "Quick Sort", "Bubble Sort"], "answer": "Quick Sort"},
    {"question": "If x + y = 10 and x - y = 4, find x.", "options": ["2", "3", "7", "8"], "answer": "7"},
    {"question": "Which is a prime number?", "options": ["9", "15", "17", "21"], "answer": "17"},
    {"question": "Which keyword is used for inheritance in Java?", "options": ["extends", "inherits", "super", "class"], "answer": "extends"},
    {"question": "Speed = 60 km/hr, Time = 2 hr. Distance?", "options": ["100 km", "90 km", "120 km", "80 km"], "answer": "120 km"},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Venus", "Mars", "Jupiter"], "answer": "Mars"},
    {"question": "Odd one out: Cat, Dog, Lion, Car", "options": ["Cat", "Lion", "Car", "Dog"], "answer": "Car"},
    {"question": "Which of these is not a programming language?", "options": ["Python", "HTML", "Java", "C++"], "answer": "HTML"},
    {"question": "Output of 3 ** 2 in Python?", "options": ["6", "9", "8", "12"], "answer": "9"},
    {"question": "Which logic gate gives 1 only when both inputs are 1?", "options": ["OR", "AND", "NOT", "XOR"], "answer": "AND"},
    {"question": "What is the opposite of 'Minimum'?", "options": ["Few", "Tiny", "Maximum", "Low"], "answer": "Maximum"},
    {"question": "What is the next term: A, C, F, J, O, ?", "options": ["S", "U", "V", "T"], "answer": "U"},
    {"question": "Find x: 2x + 3 = 11", "options": ["4", "5", "6", "3"], "answer": "4"}
],

    "Cognizant": [
    {"question": "Boat covers 30km upstream in 6h. Speed?", "options": ["6", "5", "4", "3"], "answer": "5"},
    {"question": "Average of 7, 9, 11, 13, 15", "options": ["11", "10", "12", "13"], "answer": "11"},

    {"question": "What is the next number in the series: 3, 6, 12, 24, ?", "options": ["48", "50", "52", "54"], "answer": "48"},
    {"question": "Simplify: 2x + 3x - 5x + 6", "options": ["x + 6", "3x + 6", "x - 6", "3x - 6"], "answer": "x + 6"},
    {"question": "Which is the largest prime number less than 50?", "options": ["47", "43", "41", "31"], "answer": "47"},
    {"question": "If a train travels 100 km in 2 hours, what is its average speed?", "options": ["50 km/h", "60 km/h", "40 km/h", "55 km/h"], "answer": "50 km/h"},
    {"question": "What is the square root of 144?", "options": ["10", "12", "14", "16"], "answer": "12"},
    {"question": "Which of the following is a valid IP address?", "options": ["192.168.1.256", "192.168.1.1", "256.256.256.256", "255.255.255.0"], "answer": "192.168.1.1"},
    {"question": "Find the odd one out: Cat, Dog, Rabbit, Tree", "options": ["Cat", "Rabbit", "Dog", "Tree"], "answer": "Tree"},
    {"question": "Which is the largest number?", "options": ["1000", "999", "998", "997"], "answer": "1000"},
    {"question": "The next number in the series: 2, 5, 10, 17, ?", "options": ["26", "30", "32", "36"], "answer": "26"},
    {"question": "Which of the following is a loop control statement in C?", "options": ["continue", "break", "return", "exit"], "answer": "continue"},
    {"question": "Find x: 5x - 3 = 22", "options": ["5", "7", "6", "4"], "answer": "5"},
    {"question": "What is the output of print(2 ** 3) in Python?", "options": ["6", "8", "10", "16"], "answer": "8"},
    {"question": "Which is the first prime number?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "If x = 2, y = 3, and z = 4, find x * y + z", "options": ["10", "12", "14", "16"], "answer": "10"},
    {"question": "Which data structure is used in the breadth-first search algorithm?", "options": ["Queue", "Stack", "Tree", "Graph"], "answer": "Queue"},
    {"question": "What is the output of 9 / 3 in Python?", "options": ["3", "2", "6", "1"], "answer": "3"},
    {"question": "Which sorting algorithm is based on the divide-and-conquer approach?", "options": ["Quick Sort", "Merge Sort", "Bubble Sort", "Insertion Sort"], "answer": "Quick Sort"},
    {"question": "Which programming language is known for its use in data science?", "options": ["Java", "C", "Python", "Ruby"], "answer": "Python"}
],

    "Accenture": [
    {"question": "What is 3/4 of 240?", "options": ["180", "160", "200", "120"], "answer": "180"},
    {"question": "Complete: 2, 6, 12, 20, ?", "options": ["30", "28", "32", "36"], "answer": "30"},

    {"question": "What is the next number in the series: 5, 10, 20, 40, ?", "options": ["60", "70", "80", "90"], "answer": "80"},
    {"question": "Simplify: 3x - 5x + 7", "options": ["-2x + 7", "2x + 7", "-2x - 7", "2x - 7"], "answer": "-2x + 7"},
    {"question": "What is the LCM of 5 and 10?", "options": ["15", "10", "50", "20"], "answer": "10"},
    {"question": "Which of the following is a valid HTML tag?", "options": ["<div>", "<container>", "<header>", "<section>"], "answer": "<div>"},
    {"question": "Find the next number in the series: 1, 4, 9, 16, ?", "options": ["18", "25", "30", "36"], "answer": "25"},
    {"question": "Which is the largest prime number less than 20?", "options": ["19", "17", "13", "11"], "answer": "19"},
    {"question": "Which data structure is used in depth-first search?", "options": ["Queue", "Stack", "Linked List", "Array"], "answer": "Stack"},
    {"question": "What is the average of 4, 7, 9, 12, 15?", "options": ["9", "8", "10", "11"], "answer": "9"},
    {"question": "What is the square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"question": "Simplify: 3(2x + 5) - 4x", "options": ["2x + 15", "6x + 15", "2x + 11", "6x + 11"], "answer": "2x + 15"},
    {"question": "What is the next term in the series: 2, 6, 12, 20, 30, ?", "options": ["36", "40", "50", "42"], "answer": "42"},
    {"question": "Which of the following is a loop control statement in Java?", "options": ["continue", "break", "return", "exit"], "answer": "continue"},
    {"question": "What is the output of 4 + 5 * 2 in Python?", "options": ["14", "13", "15", "12"], "answer": "14"},
    {"question": "Which programming language is used for web development?", "options": ["Python", "C++", "JavaScript", "Java"], "answer": "JavaScript"},
    {"question": "Find the value of x: 4x - 7 = 21", "options": ["7", "6", "8", "5"], "answer": "7"},
    {"question": "What is the output of print('Hello, World!'.lower()) in Python?", "options": ["hello, world!", "HELLO, WORLD!", "Hello, World!", "hello, World!"], "answer": "hello, world!"},
    {"question": "Which is the correct syntax to create a dictionary in Python?", "options": ["{}", "[]", "()", "dict{}"], "answer": "{}"}
],

    "IBM": [
    {"question": "If x = 4, x² + 2x + 1?", "options": ["25", "24", "20", "21"], "answer": "25"},
    {"question": "90km in 1.5h. Speed?", "options": ["60", "70", "50", "80"], "answer": "60"},

    {"question": "What comes next in the series: 2, 6, 12, 20, ?", "options": ["30", "25", "35", "40"], "answer": "30"},
    {"question": "Simplify: 5(2x + 3) - 3x", "options": ["7x + 15", "7x - 15", "10x + 15", "7x + 9"], "answer": "7x + 15"},
    {"question": "What is the area of a circle with radius 7?", "options": ["49π", "14π", "22π", "7π"], "answer": "49π"},
    {"question": "Which of the following is a correct HTML tag for a paragraph?", "options": ["<div>", "<p>", "<span>", "<h1>"], "answer": "<p>"},
    {"question": "Find the value of x: 3x + 7 = 22", "options": ["5", "6", "4", "3"], "answer": "5"},
    {"question": "Which data structure is used in breadth-first search?", "options": ["Queue", "Stack", "Linked List", "Array"], "answer": "Queue"},
    {"question": "What is the next number in the series: 1, 4, 9, 16, ?", "options": ["20", "25", "30", "35"], "answer": "25"},
    {"question": "Which of the following is a valid Python dictionary syntax?", "options": ["{key: value}", "[key: value]", "(key: value)", "key: value"], "answer": "{key: value}"},
    {"question": "What is the output of 2 + 3 * 5 in Python?", "options": ["17", "15", "20", "10"], "answer": "17"},
    {"question": "If 2x + 3 = 7, what is the value of x?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "Which of the following is a web development language?", "options": ["Python", "C++", "JavaScript", "Java"], "answer": "JavaScript"},
    {"question": "What is the value of the expression: 6 * (3 + 2)?", "options": ["30", "24", "28", "18"], "answer": "30"},
    {"question": "Which of the following is NOT a type of loop in Python?", "options": ["for", "while", "repeat", "do-while"], "answer": "repeat"},
    {"question": "What is the largest prime number less than 20?", "options": ["19", "17", "13", "11"], "answer": "19"},
    {"question": "What is the time complexity of searching an element in an unsorted array?", "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"], "answer": "O(n)"},
    {"question": "Which of the following is the correct way to define a function in Python?", "options": ["def functionName():", "function functionName():", "def functionName[]:", "functionName[]:"], "answer": "def functionName():"},
    {"question": "Which of the following is NOT a valid Python data type?", "options": ["list", "tuple", "dictionary", "array"], "answer": "array"}
],

    "Tech Mahindra": [
    {"question": "SI for 1000 at 5% for 2 years?", "options": ["100", "110", "120", "150"], "answer": "100"},
    {"question": "2 pens = Rs.30. 5 pens cost?", "options": ["75", "80", "60", "70"], "answer": "75"},

    {"question": "What is the next number in the series: 2, 6, 12, 20, ?", "options": ["30", "25", "35", "40"], "answer": "30"},
    {"question": "Simplify: (x + 4)(x + 2)", "options": ["x² + 6x + 8", "x² + 6x + 4", "x² + 8x + 8", "x² + 6x + 6"], "answer": "x² + 6x + 8"},
    {"question": "The sum of the ages of two brothers is 30. The elder brother is 4 years older than the younger one. What are their ages?", "options": ["14 and 16", "15 and 15", "12 and 18", "13 and 17"], "answer": "13 and 17"},
    {"question": "What is the area of a rectangle with length 8 and breadth 5?", "options": ["40", "50", "60", "70"], "answer": "40"},
    {"question": "If a car travels 60 km in 1 hour, what is its speed?", "options": ["40 km/h", "60 km/h", "50 km/h", "70 km/h"], "answer": "60 km/h"},
    {"question": "What is the next number in the series: 3, 9, 27, 81, ?", "options": ["243", "200", "300", "400"], "answer": "243"},
    {"question": "What is the value of √49?", "options": ["6", "7", "8", "9"], "answer": "7"},
    {"question": "Which of the following is a valid HTML tag for a hyperlink?", "options": ["<link>", "<a>", "<href>", "<hyperlink>"], "answer": "<a>"},
    {"question": "What is the output of 3 + 2 * 5 in Python?", "options": ["13", "15", "10", "25"], "answer": "13"},
    {"question": "If 5x - 3 = 2x + 12, what is the value of x?", "options": ["3", "4", "5", "6"], "answer": "5"},
    {"question": "Which of the following is NOT a programming language?", "options": ["Python", "Java", "HTML", "C++"], "answer": "HTML"},
    {"question": "What is the next term in the sequence: 1, 4, 9, 16, ?", "options": ["20", "24", "25", "30"], "answer": "25"},
    {"question": "What is the output of the expression 10 % 3 in Python?", "options": ["1", "2", "3", "4"], "answer": "1"},
    {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "answer": "O(log n)"},
    {"question": "Which of the following is a CSS property used to change the background color?", "options": ["color", "background-color", "bg-color", "text-color"], "answer": "background-color"},
    {"question": "What is the total surface area of a cube with side length 4?", "options": ["96", "64", "128", "80"], "answer": "96"},
    {"question": "What is the largest prime number less than 30?", "options": ["29", "27", "25", "23"], "answer": "29"}
],

    "HCL": [
    {"question": "Which number is not prime?", "options": ["7", "11", "15", "13"], "answer": "15"},
    {"question": "Next in series: 1,2,4,8,16,?", "options": ["24", "30", "32", "64"], "answer": "32"},
    
    {"question": "What is the square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"question": "Which is the largest prime number less than 50?", "options": ["47", "43", "41", "37"], "answer": "47"},
    {"question": "What is the LCM of 6 and 8?", "options": ["24", "48", "12", "36"], "answer": "24"},
    {"question": "What is the next number in the series: 2, 6, 12, 20, ?", "options": ["28", "30", "36", "40"], "answer": "30"},
    {"question": "Simplify: 5x - 2 + 3x + 4", "options": ["8x + 2", "6x + 2", "8x + 4", "6x + 4"], "answer": "8x + 2"},
    {"question": "If a number is divisible by 4 and 5, it is also divisible by?", "options": ["10", "20", "15", "30"], "answer": "20"},
    {"question": "What is the output of 9 // 4 in Python?", "options": ["2", "2.25", "3", "3.0"], "answer": "2"},
    {"question": "What is the value of x in the equation 2x - 3 = 7?", "options": ["4", "5", "6", "7"], "answer": "5"},
    {"question": "Which of the following is used to define a class in Python?", "options": ["def", "function", "class", "object"], "answer": "class"},
    {"question": "Which of the following is the correct way to import a module in Python?", "options": ["import module", "import module as m", "from module import", "include module"], "answer": "import module as m"},
    {"question": "What is the derivative of 3x²?", "options": ["6x", "6x²", "3x", "x²"], "answer": "6x"},
    {"question": "What is the time complexity of the bubble sort algorithm?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "answer": "O(n²)"},
    {"question": "Which of the following is a valid CSS property to change font size?", "options": ["font-size", "text-size", "font", "text-font"], "answer": "font-size"},
    {"question": "Which of the following data types is used to represent real numbers in Python?", "options": ["int", "str", "float", "list"], "answer": "float"},
    {"question": "What is the sum of angles in a triangle?", "options": ["180°", "90°", "360°", "270°"], "answer": "180°"},
    {"question": "What is the next number in the series: 5, 10, 20, 40, ?", "options": ["50", "60", "80", "100"], "answer": "80"},
    {"question": "Which of the following is used to define a function in Python?", "options": ["def", "function", "method", "class"], "answer": "def"}
],

    "Oracle": [
    {"question": "144 divided by 12?", "options": ["10", "11", "12", "13"], "answer": "12"},
    {"question": "Simplify: (a + b)²", "options": ["a² + b²", "a² + 2ab + b²", "a² - b²", "(a - b)²"], "answer": "a² + 2ab + b²"},
    
    {"question": "What is the square root of 64?", "options": ["6", "7", "8", "9"], "answer": "8"},
    {"question": "Which number is divisible by both 3 and 5?", "options": ["15", "10", "5", "20"], "answer": "15"},
    {"question": "Simplify: 3x + 2x - 4", "options": ["5x - 4", "5x + 4", "3x - 4", "3x + 4"], "answer": "5x - 4"},
    {"question": "What is the next number in the series: 3, 6, 9, 12, ?", "options": ["14", "15", "16", "18"], "answer": "15"},
    {"question": "If a number is divisible by both 6 and 8, it is also divisible by?", "options": ["24", "14", "18", "12"], "answer": "24"},
    {"question": "What is the value of x in the equation 2x + 3 = 11?", "options": ["4", "5", "3", "6"], "answer": "4"},
    {"question": "Which of the following is used to define a function in Python?", "options": ["def", "function", "method", "class"], "answer": "def"},
    {"question": "What is the sum of angles in a triangle?", "options": ["180°", "90°", "360°", "270°"], "answer": "180°"},
    {"question": "Which of the following is the correct way to import a module in Python?", "options": ["import module", "import module as m", "from module import", "include module"], "answer": "import module as m"},
    {"question": "Which of the following is used to define a class in Python?", "options": ["class", "function", "object", "module"], "answer": "class"},
    {"question": "What is the output of 5 // 2 in Python?", "options": ["2", "2.5", "3", "1"], "answer": "2"},
    {"question": "What is the value of x in the equation 3x - 5 = 10?", "options": ["5", "4", "3", "7"], "answer": "5"},
    {"question": "Which of the following data types is used to represent real numbers in Python?", "options": ["int", "str", "float", "list"], "answer": "float"},
    {"question": "Which of the following is a valid CSS property to change font size?", "options": ["font-size", "text-size", "font", "text-font"], "answer": "font-size"},
    {"question": "What is the next number in the series: 2, 5, 10, 17, ?", "options": ["26", "24", "23", "22"], "answer": "26"},
    {"question": "What is the time complexity of the bubble sort algorithm?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "answer": "O(n²)"}
]

}

user_performance = []

@app.route('/')
def home():
    return render_template('home.html', companies=questions.keys())

@app.route('/login')
def login():
    return render_template('login.html', companies=questions.keys())

@app.route('/index')
def index():
    return render_template('index.html', companies=questions.keys())

@app.route('/select_company', methods=['POST'])
def select_company():
    company = request.form.get('company')
    session['company'] = company
    session['score'] = 0
    session['q_index'] = 0
    session['answers'] = []

    # Shuffle the questions and store them in session
    q_list = questions[company][:]
    random.shuffle(q_list)
    session['shuffled_questions'] = q_list

    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'company' not in session or 'shuffled_questions' not in session:
        return redirect(url_for('index'))

    company_questions = session['shuffled_questions']

    if session['q_index'] >= len(company_questions):
        user_performance.append({
            'company': session['company'],
            'score': session['score'],
            'total': len(company_questions),
            'answers': session['answers']
        })
        return redirect(url_for('result'))

    if request.method == 'POST':
        selected = request.form.get('option')
        current_question = company_questions[session['q_index']]
        correct_answer = current_question['answer']

        session['answers'].append({
            'question': current_question['question'],
            'selected': selected,
            'correct': correct_answer,
            'is_correct': selected == correct_answer
        })

        if selected == correct_answer:
            session['score'] += 1

        session['q_index'] += 1
        return redirect(url_for('quiz'))

    question = company_questions[session['q_index']]
    return render_template('quiz.html', question=question, index=session['q_index'] + 1)

@app.route('/result')
def result():
    return render_template('result.html',
                           score=session.get('score'),
                           total=len(session.get('shuffled_questions', [])),
                           answers=session.get('answers'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', performances=user_performance)

if __name__ == '__main__':
    app.run(debug=True)